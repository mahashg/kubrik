DROP TABLE IF EXISTS uuids;
DROP TABLE IF EXISTS repository;
DROP TABLE IF EXISTS google_drive_ids;


CREATE TABLE uuids (
    gmailid varchar(50) PRIMARY KEY,
    google_drive_id varchar(30),
    FOREIGN KEY(google_drive_id) REFERENCES google_drive_ids(id)

);

CREATE TABLE google_drive_ids (
    id varchar(30) PRIMARY KEY,
    available INTEGER
);


CREATE TABLE repository (
    gmailid varchar(50),
    name TEXT NOT NULL,
    policy TEXT,
    local_path TEXT,
    PRIMARY KEY (gmailid, name),
    FOREIGN KEY(gmailid) REFERENCES uuids(gmailid)
);


INSERT INTO google_drive_ids VALUES ("1WPP_RpY3v9ZPHM5xGHkyf3xyTAZXBEaH", 1);
INSERT INTO google_drive_ids VALUES ("1ssrdz2EgDRfJ-RHR2S7Q3fB2cd9foX1l", 1);
INSERT INTO google_drive_ids VALUES ("1g9KaIFglDvACO2FIZsUkCCFYWo40wOL2", 1);
INSERT INTO google_drive_ids VALUES ("1tMTzXmaBvniVKeHSd4-dFxGnnmMuoQDp", 1);
INSERT INTO google_drive_ids VALUES ("16vwQ-odNEDMe3n6y34eQXoPbInLSXLSf", 1);
