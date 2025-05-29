-- Migration to add giveaways table
BEGIN TRANSACTION;

-- Create the giveaways table
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

-- Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_giveaways_ends_at ON giveaways(ends_at);
CREATE INDEX IF NOT EXISTS idx_giveaways_ended ON giveaways(ended);
CREATE INDEX IF NOT EXISTS idx_giveaways_guild ON giveaways(guild_id);

COMMIT;
