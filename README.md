# Kubrik

Kubrik is making [Kopia](https://github.com/kopia/kopia/)  a remote server system so that it can be integrated with Rubrik Ecosystem.

There is a single centralized server which runs and helps running of client and their remote repo management. Client runs and registers itself with server. Once registered, user can use client to register which path they want to use to take backup and its synced with server as well.


User can use server to store all the data and ensure that any restoration can be done easily



## Workflow

Workflow consists of 3 steps
1. Client Registration:
    Client downloads kubrik-client and runs the registration workflow. This workflow registers the client with server and provides users with information on where and how to backup the data.
    
2. Marking a file to be backing up
    Client can run snapshot command to mark the directory to be taken backup of. There is a background job which takes snapshot of the directory periodically.

3. Seeing all the changes
    Client can run the list command to see all the files under backup and their version, they can also see the file under directory without taking snapshot

4. Taking backup.
    Client can recover either by path or by hash of the file obtained from list command
