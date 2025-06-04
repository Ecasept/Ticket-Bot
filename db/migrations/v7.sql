-- Migration to add application_bans table
BEGIN TRANSACTION;

-- Create the application_bans table
CREATE TABLE IF NOT EXISTS application_bans (
	user_id INTEGER NOT NULL,
	guild_id INTEGER NOT NULL,
	PRIMARY KEY (user_id, guild_id)
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_application_bans_guild ON application_bans(guild_id);

COMMIT;
