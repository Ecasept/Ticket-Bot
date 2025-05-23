-- Migration to add NOT NULL constraints to tickets.user_id,
-- tickets.archived, and tickets.created_at as per schema.sql.

BEGIN TRANSACTION;

-- 1. Create a new 'tickets' table with the updated schema.
--    - user_id is now NOT NULL.
--    - archived is now explicitly NOT NULL.
--    - created_at is now explicitly NOT NULL.
CREATE TABLE tickets_new (
	channel_id TEXT PRIMARY KEY,
	category TEXT CHECK(category IN ('application', 'report', 'support')),
	user_id TEXT NOT NULL,
	assignee_id TEXT,
	archived BOOLEAN DEFAULT FALSE NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	close_at TIMESTAMP
);

-- 2. Copy data from the old 'tickets' table to the new 'tickets_new' table.
--    This step will fail if any existing 'user_id' is NULL.
--    If you have NULL user_ids and want to set a default, you would modify the SELECT statement:
--    e.g., COALESCE(user_id, 'some_default_user_id')
INSERT INTO tickets_new (channel_id, category, user_id, assignee_id, archived, created_at, close_at)
SELECT channel_id, category, user_id, assignee_id, archived, created_at, close_at
FROM tickets;

-- 3. Drop the old 'tickets' table.
DROP TABLE tickets;

-- 4. Rename the new table to 'tickets'.
ALTER TABLE tickets_new RENAME TO tickets;

-- 5. Recreate indexes on the new 'tickets' table (as defined in schema.sql).
CREATE INDEX IF NOT EXISTS idx_tickets_category ON tickets(category);
CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee_id);

COMMIT;
    