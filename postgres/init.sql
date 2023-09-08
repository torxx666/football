CREATE SCHEMA IF NOT EXISTS postgres;
CREATE TABLE IF NOT EXISTS postgres.club_hashtags (
    club VARCHAR(255),
    country VARCHAR(255),
    hashtags TEXT,
    lenhash INTEGER
);
CREATE INDEX idx_club ON postgres.club_hashtags (club);
CREATE INDEX idx_country ON postgres.club_hashtags (country);
ALTER TABLE postgres.club_hashtags
ADD CONSTRAINT unique_club UNIQUE (club);