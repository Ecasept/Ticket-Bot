CREATE TABLE IF NOT EXISTS tickets (
	channel_id TEXT PRIMARY KEY,
	category TEXT CHECK(category IN ('application', 'report', 'support')),
	user_id TEXT,
	assignee_id TEXT,
	archived BOOLEAN DEFAULT FALSE,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS constants (
	key TEXT PRIMARY KEY,
	value TEXT
);

-- Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_tickets_category ON tickets(category);
CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee_id);




