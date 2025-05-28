-- Migration to add NOT NULL constraints to primary keys and add guild_id to constants table

BEGIN TRANSACTION;

-- 1. Create a new 'tickets' table with NOT NULL constraint on primary key
CREATE TABLE tickets_new (
	channel_id TEXT PRIMARY KEY NOT NULL,
	category TEXT CHECK(category IN ('application', 'report', 'support')),
	user_id TEXT NOT NULL,
	assignee_id TEXT,
	archived BOOLEAN DEFAULT FALSE NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	close_at TIMESTAMP
);

-- 2. Copy data from the old 'tickets' table to the new 'tickets_new' table
INSERT INTO tickets_new (channel_id, category, user_id, assignee_id, archived, created_at, close_at)
SELECT channel_id, category, user_id, assignee_id, archived, created_at, close_at
FROM tickets;

-- 3. Drop the old 'tickets' table
DROP TABLE tickets;

-- 4. Rename the new table to 'tickets'
ALTER TABLE tickets_new RENAME TO tickets;

-- 5. Recreate indexes on the new 'tickets' table
CREATE INDEX IF NOT EXISTS idx_tickets_category ON tickets(category);
CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee_id);

-- 6. Create a new 'constants' table with guild_id and NOT NULL constraint on primary key
CREATE TABLE constants_new (
	key TEXT NOT NULL,
	guild_id INTEGER NOT NULL,
	value TEXT,
	PRIMARY KEY (key, guild_id)
);

-- 7. Copy existing constants data into the new table with a default guild_id
INSERT INTO constants_new (key, guild_id, value)
SELECT key, {{DEFAULT_GUILD_ID|0}} as guild_id, value
FROM constants;

-- 8. Drop the old 'constants' table
DROP TABLE constants;

-- 9. Rename the new table to 'constants'
ALTER TABLE constants_new RENAME TO constants;

-- 10. Create index for faster lookups on guild_id
CREATE INDEX IF NOT EXISTS idx_constants_guild ON constants(guild_id);

COMMIT;
