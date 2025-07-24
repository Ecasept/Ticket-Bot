BEGIN TRANSACTION;

-- Add image_url column to banlist_bans table
ALTER TABLE banlist_bans ADD COLUMN image_url TEXT;

COMMIT;
