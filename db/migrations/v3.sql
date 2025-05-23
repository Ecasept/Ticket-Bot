-- Migration to add close_at column to tickets table
BEGIN TRANSACTION;

-- Add the close_at column to the tickets table
ALTER TABLE tickets ADD COLUMN close_at TIMESTAMP;

COMMIT;
