# Kubrik

Kubrik is making [Kopia](https://github.com/kopia/kopia/)  a remote server system so that it can be integrated with Rubrik Ecosystem.

There is a single centralized server which runs and helps running of client and their remote repo management. Client runs and registers itself with server. Once registered, user can use client to register which path they want to use to take backup and its synced with server as well.


User can use server to store all the data and ensure that any restoration can be done easily



## Workflow

Workflow consists of 3 steps
1. Client Registration:
    Client downloads kubrik-client and runs `kubrik-client register` command. Unlike Polaris, we assume only one server here (to simplify the workflow), register knows which server to connect to, so it connects to server and obtains its uuid. 
    
2. Marking a file to be backing up
    client can run the command `kubrik-client snapshot <dir>` command. This two things
    a. makes a call to server to register that snapshot of <dir> needs to be taken. This inturn returns a google_drive_folder id where data should be backedup.
    b. Once client has obtaind google_drive_folder_id then it can do backup with drive directly without server involvement

3. Restoration of file
