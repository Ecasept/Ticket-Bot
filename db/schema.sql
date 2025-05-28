CREATE TABLE IF NOT EXISTS tickets (
	channel_id TEXT PRIMARY KEY NOT NULL,
	category TEXT CHECK(category IN ('application', 'report', 'support')),
	user_id TEXT NOT NULL,
	assignee_id TEXT,
	archived BOOLEAN DEFAULT FALSE NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	close_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS constants (
	key TEXT NOT NULL,
	guild_id INTEGER NOT NULL,
	value TEXT,
	PRIMARY KEY (key, guild_id)
);

-- Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_tickets_category ON tickets(category);
CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee_id);
CREATE INDEX IF NOT EXISTS idx_constants_guild ON constants(guild_id);




