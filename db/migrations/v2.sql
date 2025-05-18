-- Migration to create the constants table
CREATE TABLE IF NOT EXISTS constants (
	key TEXT PRIMARY KEY,
	value TEXT
);
