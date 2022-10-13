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