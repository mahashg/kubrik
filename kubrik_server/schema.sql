DROP TABLE IF EXISTS uuids;
DROP TABLE IF EXISTS repository;

CREATE TABLE uuids (
    gmailid varchar(50) PRIMARY KEY,
    google_drive_id varchar(30)
);



CREATE TABLE repository (
    gmailid varchar(50),
    name TEXT NOT NULL,
    policy TEXT,
    local_path TEXT,
    PRIMARY KEY (gmailid, name),
    FOREIGN KEY(gmailid) REFERENCES uuids(gmailid)
);