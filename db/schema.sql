CREATE TABLE IF NOT EXISTS channels (
	channel_id TEXT PRIMARY KEY,
	category TEXT CHECK(category IN ('application', 'report')),
	assignee_id TEXT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_channels_category ON channels(category);
CREATE INDEX IF NOT EXISTS idx_channels_assignee ON channels(assignee_id);




