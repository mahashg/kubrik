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


INSERT INTO google_drive_ids VALUES ("4a35a5c0-49ff-11ed-b878-0242ac120002", 1);
INSERT INTO google_drive_ids VALUES ("4a35ab74-49ff-11ed-b878-0242ac120002", 1);
INSERT INTO google_drive_ids VALUES ("4a35ad72-49ff-11ed-b878-0242ac120002", 1);
INSERT INTO google_drive_ids VALUES ("4a35a5c1-59ff-11ed-b878-0242ac120002", 1);
INSERT INTO google_drive_ids VALUES ("4a35ab75-49ff-21ed-b878-0242ac120002", 1);
INSERT INTO google_drive_ids VALUES ("4a35ad73-49ff-11ed-c878-0242ac120002", 1);
INSERT INTO google_drive_ids VALUES ("4a35a5c3-49ff-11ed-b878-1242ac120002", 1);
INSERT INTO google_drive_ids VALUES ("4a35a5c0-49ff-11ed-b878-0242ac120003", 1);
INSERT INTO google_drive_ids VALUES ("4a35ab76-49ff-11ed-b878-0242ac120002", 1);
INSERT INTO google_drive_ids VALUES ("4a35a5c1-49ff-11ed-b879-1242ac120002", 1);