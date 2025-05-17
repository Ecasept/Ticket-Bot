CREATE TABLE IF NOT EXISTS tickets (
	channel_id TEXT PRIMARY KEY,
	category TEXT CHECK(category IN ('application', 'report')),
	user_id TEXT,
	assignee_id TEXT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_tickets_category ON tickets(category);
CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee_id);




