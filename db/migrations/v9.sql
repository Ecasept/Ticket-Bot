-- Migration v9: Implement custom ticket categories system
-- This migration creates the custom categories infrastructure and migrates existing hardcoded categories

BEGIN TRANSACTION;

-- 1. First, ensure ticket_categories table exists with correct schema
-- (It should already exist from schema.sql, but we ensure consistency)
CREATE TABLE IF NOT EXISTS ticket_categories (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	emoji TEXT NOT NULL,
	description TEXT NOT NULL,
	guild_id INTEGER NOT NULL
);

-- 2. Ensure ticket_category_roles table exists
CREATE TABLE IF NOT EXISTS ticket_category_roles (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	category_id INTEGER NOT NULL,
	role_id INTEGER NOT NULL,
	FOREIGN KEY (category_id) REFERENCES ticket_categories(id) ON DELETE CASCADE
);

-- 3. Ensure ticket_category_questions table exists
CREATE TABLE IF NOT EXISTS ticket_category_questions (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	category_id INTEGER NOT NULL,
	question TEXT NOT NULL,
	FOREIGN KEY (category_id) REFERENCES ticket_categories(id) ON DELETE CASCADE
);

-- 4. Create a new tickets table that references custom categories instead of using hardcoded strings
CREATE TABLE tickets_new (
	channel_id TEXT PRIMARY KEY NOT NULL,
	category_id INTEGER,
	user_id TEXT NOT NULL,
	assignee_id TEXT,
	archived BOOLEAN DEFAULT FALSE NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	close_at TIMESTAMP,
	FOREIGN KEY (category_id) REFERENCES ticket_categories(id) ON DELETE SET NULL
);

-- 5. For migration, create default categories for each guild that has tickets
-- We need to handle the case where multiple guilds exist

-- First, let's create a temporary table to track guild IDs from constants
CREATE TEMPORARY TABLE guild_list AS
SELECT DISTINCT guild_id FROM constants;

-- Insert default categories for each guild found in constants
-- If no guilds in constants, we'll use a default guild_id of 0
INSERT INTO ticket_categories (name, emoji, description, guild_id)
SELECT 'Bewerbung', '📝', 'Erstelle ein Bewerbungsticket', guild_id
FROM guild_list
UNION ALL
SELECT 'Report', '🚨', 'Melde ein Problem oder Regelverstoß', guild_id
FROM guild_list
UNION ALL
SELECT 'Support', '❓', 'Erhalte Hilfe und Unterstützung', guild_id
FROM guild_list;

-- If no guilds were found in constants, insert for default guild_id 0
INSERT INTO ticket_categories (name, emoji, description, guild_id)
SELECT 'Bewerbung', '📝', 'Erstelle ein Bewerbungsticket', 0
WHERE NOT EXISTS (SELECT 1 FROM guild_list)
UNION ALL
SELECT 'Report', '🚨', 'Melde ein Problem oder Regelverstoß', 0
WHERE NOT EXISTS (SELECT 1 FROM guild_list)
UNION ALL
SELECT 'Support', '❓', 'Erhalte Hilfe und Unterstützung', 0
WHERE NOT EXISTS (SELECT 1 FROM guild_list);

-- 6. Migrate existing ticket data to the new table
-- We need to map the old string categories to the new category IDs
INSERT INTO tickets_new (channel_id, category_id, user_id, assignee_id, archived, created_at, close_at)
SELECT 
    t.channel_id,
    tc.id,
    t.user_id,
    t.assignee_id,
    t.archived,
    t.created_at,
    t.close_at
FROM tickets t
LEFT JOIN ticket_categories tc ON (
    (t.category = 'application' AND tc.name = 'Bewerbung') OR
    (t.category = 'report' AND tc.name = 'Report') OR
    (t.category = 'support' AND tc.name = 'Support')
)
-- We try to match to the guild_id from the ticket context if possible
-- For now, we'll use the first matching category (this could be improved with guild context)
WHERE tc.id IN (
    SELECT MIN(id) FROM ticket_categories tc2 
    WHERE tc2.name = tc.name
);

-- 7. Drop the old tickets table and rename the new one
DROP TABLE tickets;
ALTER TABLE tickets_new RENAME TO tickets;

-- 8. Create indexes for the new table structure
CREATE INDEX IF NOT EXISTS idx_tickets_category_id ON tickets(category_id);
CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee_id);
CREATE INDEX IF NOT EXISTS idx_ticket_categories_guild ON ticket_categories(guild_id);
CREATE INDEX IF NOT EXISTS idx_ticket_category_roles_category ON ticket_category_roles(category_id);
CREATE INDEX IF NOT EXISTS idx_ticket_category_roles_role ON ticket_category_roles(role_id);
CREATE INDEX IF NOT EXISTS idx_ticket_category_questions_category ON ticket_category_questions(category_id);

COMMIT;
