BEGIN TRANSACTION;

CREATE TABLE banlist_bans (
    name TEXT NOT NULL,
    guild_id INTEGER NOT NULL,
    reason TEXT,
    banned_by TEXT,
    length TEXT,
    PRIMARY KEY (name, guild_id)
);

CREATE INDEX idx_banlist_bans_guild_id ON banlist_bans(guild_id);

COMMIT;
