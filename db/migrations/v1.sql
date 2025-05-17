BEGIN TRANSACTION;

-- 1. Rename the current 'tickets' table to preserve its data.
ALTER TABLE tickets RENAME TO tickets_old;

-- 2. Create the new 'tickets' table with the updated schema:
--    - 'category' CHECK constraint now includes 'support'.
--    - New 'archived' column with a default value of FALSE.
CREATE TABLE tickets (
    channel_id TEXT PRIMARY KEY,
    category TEXT CHECK(category IN ('application', 'report', 'support')),
    user_id TEXT,
    assignee_id TEXT,
    archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Copy data from 'tickets_old' to the new 'tickets' table.
--    The 'archived' column will automatically get its default value (FALSE)
--    for all existing rows.
INSERT INTO tickets (channel_id, category, user_id, assignee_id, created_at)
SELECT channel_id, category, user_id, assignee_id, created_at
FROM tickets_old;

-- 4. Drop the old 'tickets_old' table as it's no longer needed.
DROP TABLE tickets_old;

-- 5. Recreate indexes on the new 'tickets' table as defined in your target schema.
CREATE INDEX IF NOT EXISTS idx_tickets_category ON tickets(category);
CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee_id);

COMMIT;

-- After this script is successfully executed, your migration tool
-- should update the PRAGMA user_version to 2 (or the version of this script).
