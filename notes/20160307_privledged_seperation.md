Devin Trejo
Notes for Computer Intrusion 20160307

# Privileged Separation (P.S)
General purpose technique for building more secure systems. We will focus 
on Unix systems permission system for implementation. 

We start with an applications running at an unspecified privilege level.
As we saw last class we can have an attacker that makes the application do 
bad things. The attacker's goal is to gain a root shell from your running 
application. For example take a large application like Apache.

```
input ->    |-------------------|
output <-   | Large Application | -> Data
            |-------------------|
```

Apache may be running at high permission levels. 

P.S breaks up the application and data

| Application | Virtual Machine | Data |
|:-----------:|:---------------:|:----:|
| script0     | VM0             | script0 data |
| script1     | VM0             |s cript1 data |
| script2     | script2 data |

- We can break the larger system into a group of virtual machines. 
- SSH implements w/ P.S to protect exposure of data. 

An actual example is Chrome:
- Chrome users P.S to ensure that a singe exploit in one part of the system
does not lead to full system vulnerability. 

## Unix Mechanism
- Principals: Principals are entities that have privileges or rights.
- Subjects: We define these as the Unix processes. So we say that the 
principals describe the rights each subject has. 
- Objects: Things that the processes act on (Note not objects as in OOP)

Example:
Say we are talking about a server. What are the objects we want to protect?
- files
- directories
- sockets/networking
- memory/memory content
- Other processes
- File descriptors

### Unix Permissions
How does the OS kernel decide if an process has access to the objects listed
above. Well in UNIX each running process has a UID, and GID (group ID). When
a process is executed we it runs with a specified UID and GID.  
Files Operations: read, write, change permissions, execute.  
Directory Operations: link/unlink (to an INODE), rename, create  
- *(Note1: In Unix file system objects are represented as inodes data 
structures that represent file system objects. Each inode contains attributes
consisting of permissions and block location of the data.)*  
- *(Note2: A file can have multiple names. Multiple hard links to the inode. 
An inode w/ no links is removed from disk. A files inode number does not
change when that file is moved to another directory on the same device.)*

```
        uids
inode:  gids  
permission bits: r---w---x
```
First three bits are the owner, Second three bits are the group, the third
three bits are the other. The permissions are represented as octal. 
            
|       |   4   |   2   |   1   |

|       |   r   |   w   |   x   |
|:-----:|:-----:|:-----:|:-----:|
| owner |   1   |   1   |   0   |
| group |   1   |   0   |   0   |
| other |   1   |   0   |   0   |

Owner row: 6
Group row: 4
Other row: 4
We thus say this file/directory has 644 permissions. 

For UNIX directories we need the following permissions to perform the
following tasks:
- link & unlink: read permission
- rename: write permission
- execute : required to be able to do a lookup command on the directory. 


### Unix File Descriptors
A file descriptor is a handle used to access a file or other I/O resource
such as a pipe on a socket. Security checks for accessing the file/resource
are checked when the file is opened. After completion the process that opened
the file/resource has access to that resource. The method/function then can
now pass a handle to the resource. By using this approach we can separate 
functionality that has access to resource and that processes that resource.
The idea is to give access without having to give read/write privileged. 

### Unix Process Functionality
Process operations: create, kill, and debug (ptrace)  
Anyone can create a process. The process is created with the same UID that
started the process. The owner/root of the process can kill the process. Again
the owner/root user can debug a process.  
Memory goes along with a process. Only memory created by that process can be
accessed.  
Networking also may go with a process. We can connect, listen, read/write,
data and send/recv raw packets. Anyone can connect to a socket. For listen,
only root can listen to port numbers less than 1024. Read/write operations
can be performed via a file descriptor. Raw packets have no transport layer
protocol and you must be root to perform. 

## Where do UIDs come from?
Idea of bootstraping. The `setuid(uid)` command is used to set the user id 
of a process. Similar process for gid. When you login the command is ran
as root. 
1. The user inputs a user name and password. 
2. The root `login` function looks up `/etc/passwd` to obtain a int number 
for your username.
3. The root `login` function looks up `/etc/shadow` to obtain the hash of 
your password. 
4. After confirming your uid and password the root user starts a shell with
the specified users uid. Example the root would run `setuid(uid)` and then
executes `/bin/sh`

After you login you are running a shell under your uid. To elevate your
privileges:
- You can ask a process running as root for help.
- Call Setuid binary to reset your ID shell. 

We can also trick the shell to redirecting your root directory. `chroot`
changes your root directory to an arbitrary directory. Map `/` to `/foo`.
To get out of chroot:

``` shell
$ open ('/') # Returns a file descriptor for /foor
// Call chroot on /foo/bar
```

