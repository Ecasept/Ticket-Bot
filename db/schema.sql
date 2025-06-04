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

CREATE TABLE IF NOT EXISTS giveaways (
	message_id INTEGER PRIMARY KEY NOT NULL,
	channel_id INTEGER NOT NULL,
	guild_id INTEGER NOT NULL,
	host_id INTEGER NOT NULL,
	prize TEXT NOT NULL,
	winner_count INTEGER NOT NULL DEFAULT 1,
	role_id INTEGER,
	ends_at TIMESTAMP NOT NULL,
	ended BOOLEAN DEFAULT FALSE NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS application_bans (
	user_id INTEGER NOT NULL,
	guild_id INTEGER NOT NULL,
	PRIMARY KEY (user_id, guild_id)
);

-- Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_tickets_category ON tickets(category);
CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee_id);
CREATE INDEX IF NOT EXISTS idx_constants_guild ON constants(guild_id);
CREATE INDEX IF NOT EXISTS idx_giveaways_ends_at ON giveaways(ends_at);
CREATE INDEX IF NOT EXISTS idx_giveaways_ended ON giveaways(ended);
CREATE INDEX IF NOT EXISTS idx_giveaways_guild ON giveaways(guild_id);
CREATE INDEX IF NOT EXISTS idx_application_bans_guild ON application_bans(guild_id);




