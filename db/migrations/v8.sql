-- Migration to add new column
BEGIN TRANSACTION;

-- Add the new column to the application_bans table
ALTER TABLE application_bans ADD COLUMN ends_at TIMESTAMP;

COMMIT;
