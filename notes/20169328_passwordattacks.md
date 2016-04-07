Devin Trejo
Notes for Computer Intrusion 20160328

# Dictionary Attacks and SSH
SSH attacks which is used for remote management of servers is a typically
under attack. Attack starts a an attempt to find a valid username on a 
remote machine. We guess a large amount of usernames hoping to find an 
actual account. 

## Secure SSH between two locations
For secure ssh access between only two locations we can
secure the connection by using `/etc/hosts.deny` and `/etc/hosts.allow`
For example:

``` shell
$ vi /etc/hosts.deny
---
# file: /etc/hosts.deny

ALL:ALL # Deny all hosts
```

```shell
$ vi /etc/hosts.allow
---
# file: /etc/hosts.allow

sshd:<KNOWN IP ADDR>
```

## Setup SSH Blacklist 
Blacklists disallow future connections from an IP addresses which are known
to be bad. A popular tool before was DenyHosts an application that was found
to have vulnerabilities. DenyHosts works by updating the `/etc/hosts.deny` 
file. 

An alternative recently has been Fail2Ban which
looks at your log files to see if a IP has recently attempted to access
your machine multiple times and failed. Fail2Ban manipulates your
IPTables to enforce its rules.

``` shell
$ sudo iptables -L
INPUT
OUTPUT
FOR VAR
CHAIN f2b-sshd # < Fail2Ban entires
```

Inside of Fail2Ban we can configure certain settings. For example:
- bantime = 3600
- findtime = 3600 # How long is our window
- maxretry = 9 # If you try 9 times in 3600seconds you are banned. 
- mta = sendmail
- destinationmail = root@localhost

# Defeating Password Hashing
## Defeatable Password Hashing
Passwords on Unix machines are stored in `/etc/shadow` where the passwords
are not stored in plain text. Unix will instead store the hash of a password
and authenticate using the hashes of passwords.

Microsoft used a poor implementation of a hash for a while called **LM HASH**.
For LM Hash your password had to be 14 characters. If your password was
not 14 chars then it would pad the tail with all zeros. Also passwords were
converted to all uppercase chars. Next your hash was broken up into
7 char strings so that you have 56 bit substrings. Each substring was then
used as a DES key to encrypt the following string "KGS!@#$%". 

LM Hash was easily defeated by a rainbow table.

## Defeating Password Hash
Create a hash table with all possible passwords and their hashes. These
hash tables are seen in Python in dictionaries. Today, with storage being
really cheap we can store huge databases of passwords and their hashes. 

**Hash Chains**

First seen in 2003, Rainbow tables involves hash chain. Hash chains trade
time for memory space. One fundamental piece of a hash chain is a reduction
function (R). A reduction chain matches a hash to a string which would 
potentially be a password. R is a mapping that should uniformly sample all 
the passwords. 

Let p = plaintext password. c is its hash. 

c=H(p)

- R(c) = p'.
So now given some pair of functions (H, R) and some randomly chosen plaintext
(p1) we can construct a hash table. 

p1 -> c1=H(p1) - > p2 = R(c1) -> c2=H(p2) -> p3 = R(c3).  
The legnth of the chain is a parameter labeled k. Here is what we store
from the chain. 

| Starting Point | End Point or Plain Text after k itter |
|:---:|:---:|
| p_1^1 | p_k^1 |
| p_1^2 | p_k^2 |
| p_1^... | p_k^... |
| p_1^57 | p_k^57 |


The attacker creates a chain "test hash chain". He continues looping through
the chain until one of the endpoints matches one of the qs. He continues
to loop until he has iterated k times. If he has gone through k times he
know that the plaintext password is not in the chain. 

**Rainbow Tables**
Each hash chain is constructed with k different reduction functions. 
({R_1, R_2, R_3}). It is much more improbable that the chain will merge.

# Password Hashing Schemes
Keywords:
- Salts
- Variable Rounds
- A secure hashing function. 

For this example we will say our hashing scheme is sha512_crypt. To begin
we can't just hash a password and store it. Some passwords are too short 
so the complexity of the stored hashes are too simple. You can brute force
the hash algo by hashing a majority of short passwords and storing their 
hashes.
Instead we combine random bits (called the **salt**) with the user chossen 
password. 

Example of `/etc/shadow`

``` shell
$ cat /etc/shadow
devin:$6$yhYzvUl6$Wopirjgao10239ujvaleryj39o4;gnmv9092jtgoiaenwva;sio-qrgjnoi4j0-9khg3oi4ngmo34:16777:0:99999:7:::
```

Here:
- **$6** refers to the password hashing scheme.
    - 1: md5_crypt
    - 2: bcrypt
    - 6: SHA512_crypt
- **$yhYzvUl6$** refers to the salt. 

