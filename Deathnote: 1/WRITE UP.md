# Deathnote: 1 Write UP

### Machine INFO

- Date release: *4 Sep 2021*
- Author: *[HWKDS](https://www.vulnhub.com/author/hwkds,816/)*
- Series: *[Deathnote](https://www.vulnhub.com/series/deathnote,499/)*
- Level: *Easy*
- VM Link: *[HERE](https://www.vulnhub.com/entry/deathnote-1,739/)*
- OS suggestion for this WRITE UP: [KALI](https://kali.org/) ^f1ab85

### Little disclaimer

>In the following guide I am going to use the following IP **192.168.1.60** for make things easier **REMEMBER TO CHANGE IT WITH YOUR OWN IP**.

^71cfe1

# Solution

1. [[#Step 1 getting ready | GETTING READY]]
2. [[#Step 2 reconnaissance | RECONNAISSANCE]]
3. [[#Step 3 dig in | DIG IN]]
4. [[#Stage 4 Break In Privilege Escalation | BREAKING IN & PRIVILEGE ESCALATION]]
5. [[#Conclusion | CONCLUSION]]

## Step 1, getting ready

Before scanning the machine to find out possible vulnerabilities we need to know the machine IP which we are going to perform the attacks.

- Start the Virtual Machine [[#Start your virtual machine]].
- Find its IP [[#Net Scan]].
- Result like [[#Result getting ready]]

### Start your virtual machine

Open Virtual Box or VMware, import  **Deathnote.ova** and start it.

### Net Scan

##### Python script

Using this [scapy](https://scapy.net/) python [script](https://github.com/IadRabbit/CTF-S-Write-UPs/blob/main/userful_scripts/arp_ping.py) would scan devices inside your network in just a few seconds.
**It looks even faster than nmap. WTF?**

```bash
sudo python3 arp_ping.py
```

##### Nmap

In alternative you can also use nmap for scan devices inside your network.

```bash
sudo nmap -sn 192.168.1.0/24
```

##### Netdiscover

Netdiscover is another fast tool for discovering devices inside your network

```bash
sudo netdiscover
```

### Result, getting ready

After executing a scan of our network, you should have found something familiar like this, which how you can guess is the IP of our Virtual Machine.

![[found_ip_like.png]] ^64039d

## Step 2, reconnaissance

1. [[#Scanning]]
2. [[#Disclaimer for stealthy Hackers]]
3. [[#Result reconnaissance]]

### Scanning

It think is just a standard, but the first thing to do when you have to find out vulnerabilities on a machine is executing a reconnaissance scan, how do we do that?  **NMAP** Good answer fella :).

```bash
nmap -A -T4 192.168.1.60
```

- **-A** parameter enables OS detection, version detection, script scanning, and traceroute.
- **-T4** parameter enables a parallel, fast scan.
- **192.168.1.60** Is my VM(Virtual Machine) IP address. (**[[#^71cfe1|WRITE UP]]**).
- By default nmap (if you are not in root mode) executes a TCP Scan (**-sT**).

### Disclaimer for stealthy Hackers

If we want to do a stealthy reconnaissance scan, we should run nmap with different parameters.
>We don't need in this case to be stealthy because is just in our own environment and no F.B.I. is gonna knock to your door :).

```bash
sudo nmap -sS -T0 192.168.1.60
```

- **-sS** parameter stands for scan SYN it is a stealthy scan because it never completes the Three-way handshakes. Read more  [here](https://nmap.org/book/synscan.html).
- **-T0** parameter enables a serial, slowest scan. Some IDS(Intrusion detection system) could detects fast scans and evidence them. Slow is better, because the key isn't the traffic, but the speed. Read more [here](https://nmap.org/book/man-performance.html).

### Result, reconnaissance

After performing our scan should result a similar result like this.

![[nmap_scan_like.png]] ^d01fe6

How you can observe by yourself there are two different ports open on the "server" (VM).
- port 22, which means we can connect through **SSH** to this machine.
- port 80, which means the server is hosting a web application.

Now let's focus on the port 80.

## Step 3, dig in

1. [[#Dirb]]
2. [[#Nikto]]
3. [[#Result dig in]]

### Dirb

Let's open the browser and see this website. Let me guess it does a redirect and no page isn't found with the redirected URL? Good, is brute-force time.
At [[#^f1ab85 | startup]] I said that I suggest kali linux distro, because it contains a lot of variety of pentesting tools which are already installed. The tool which we need now is called [dirb](https://gitlab.com/kalilinux/packages/dirb).
DIRB is a Web Content Scanner. It looks for existing (and/or hidden) Web Objects. It basically works by launching a dictionary based attack against a web server and analyzing the response.

```bash
dirb http://192.168.1.60 /usr/share/wordlists/dirb/common.txt
```

- the first argument is the URL
- the second argument is a wordlist which contains the most known directories and files to request if the content is available.


The output should be something similar like this.

![[dirb_scan_like.png]]

>If you are more a GUI guy you can use [dirbuster](https://gitlab.com/kalilinux/packages/dirbuster)

**DON'T LOSE TIME WAITING FOR THE SCAN TO FINISH**, it will take a lot of minutes and we don't have enough time to check all those path to find something useful, what we need is in the first few seconds where you can notice two main __big directories__.
- /manual
- /wordpress

### Nikto

Guess which directory is the most interesting? Exactly ***/wordpress***, but also wordpress have a lot of paths, we need to reduce our research field, maybe [nikto](https://github.com/sullo/nikto) can gives us a little help.

```bash
nikto -h http://192.168.1.60/wordpress/
```

- **-h** is the parameter for specify which host we want to scan

After 40 seconds like it should give us a similar output.

![[nikto_scan_like.png]]

### Result, dig in

Wut Wut? The penultimate row tell us "This may reveal sensitive information?"

Let open it.

>http://192.168.1.60/wordpress/wp-content/uploads/

Mmh there is a folder index "2021", what is inside? there are 3 dirs, last one is empty, second one the same, BINGO the first one contains something. Interesting a file called user.txt and one called notes.txt, maybe some of these combinations enable us access trough [[#^d01fe6 | SSH]]?

## Stage 4, Break In & Privilege Escalation

1. [[#Hydra Brute-force]]
2. [[#SSH LOG IN]]
3. [[#Privilege Escalation or Sherlock Holmes time]]

### Hydra Brute-force

Let download those files.

```bash
wget http://192.168.1.60/wordpress/wp-content/uploads/2021/07/notes.txt
```

```bash
wget http://192.168.1.60/wordpress/wp-content/uploads/2021/07/user.txt
```

And now let use [hydra](https://gitlab.com/kalilinux/packages/hydra) for brute-forcing our access through SSH.

```bash
hydra -L user.txt -P notes.txt ssh://192.168.1.60
```

- **-L** argument specify the users word-list
- **-P** argument specify the passwords word-list

After two minutes approximately it should produce an output like this.

![[hydra_brute_like.png]]

>Why the IP now is **192.168.1.173**? It happens when a machine ask for a new IP and the DHCP server assign a new one. But this doesn't change anything, don't worry.

>If you like GUI **xhydra** is your friend.

BOOM BABY.

- The user is **l**
- The password is **death4me**

### SSH LOG IN

Let login.

```bash
ssh l@192.168.1.173
```

Type the password **death4me** and this is it, ***WE ARE IN***.
Let see if there is something in the current user folder.
Let use **ls** for display to us the files in the current folder, there is a file named **user.txt**, what is inside it? I choose you **cat**.

![[vm_l_user_f.png]]

WTF IS THIS? An encrypted message? I am gonna fuck my brain to understand what the heck is this? WAIT A SECOND... FUCK MY BRAIN. ***BRAINFUCK YOU SON OF B.***

>P.S. It literally took me less than a second to figure it out, when you know [brainfuck](https://en.wikipedia.org/wiki/Brainfuck) and see how it looks like you can't be wrong.

I used this [online compiler](https://www.tutorialspoint.com/execute_brainfk_online.php) to get the message.

```
i think u got the shell , but you wont be able to kill me -kira
```

Kira is such a bad egocentric boy, we still need to complete this machine.
Let see if we are lucky enough to be in **sudo group**  for getting root access, no you are a loser :).
We need to find a user with major permissions than current logged user **l**.

### Privilege Escalation or Sherlock Holmes time

Privilege Escalation is a really big world and there are various possibilities for gaining permissions, if you are more interested read [here](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Linux%20-%20Privilege%20Escalation.md)
How we said before we need to gain root access for have full control on this machine, so let see if there are others users on this machine.
A soft way to do this is going inside the **/home** folder and type **ls**. You found a directory name **kira**, right?. In theory every folder inside should be an **user** folder, but is also true that every folder can be created inside the **/home** directory. So let be sure and check the UNIX file where all users are stored.

```bash
cat /etc/passwd
```

Watch the last line, apparently a user named kira truly exists.
Let see if **kira** in some interesting group by typing

```bash
id kira
```

Nice **kira** is inside **sudo group** but we don't know **kira** password, so how can we access as **kira**?
- Bruteforcing, maybe yes, but most probably you won't find anything and you end in losing time.
- See if we can access to others files where maybe a password is located?
- Look at previous link where were cited various possibilities of Escalation? But they are so much to test everyone.
- Using cited scripts like [LinPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS), sounds good.
- Looking the existence of a ***A GOLDEN TICKET***

The first thing which I do, because happened to me often is looking inside the user **.ssh** folder to see if any available  ***"A GOLDEN TICKET"*** exists.

![[ssh_access.png]]

And we just found a private key, let download it from the server using **sftp** the syntax is very similar to **ssh**

```bash
sftp l@192.168.1.173
```

And type

```bash
get .ssh/id_rsa
```

Now

```bash
ssh -i id_rsa kira@192.168.1.173
```

And **WE ARE LOGGED AS KIRA**.
Wait a second but for access with **sudo** we must know **kira** password and we don't have it, damn.
Let see if inside there is a new message for us.

![[vm_kira_user_f.png]]

It looks like a message encoded in **base64**, for decoding it we could use online tools like [this](https://www.base64decode.org/), but we prefer to do some scripts by our-self, right?
So I created a simple script named [easy_decoder.py](https://github.com/IadRabbit/CTF-S-Write-UPs/blob/main/userful_scripts/arp_ping.py) ^8bcd7b

```bash
./easy_decoder.py base64 cGxlYXNlIHByb3RlY3Qgb25lIG9mIHRoZSBmb2xsb3dpbmcgCjEuIEwgKC9vcHQpCjIuIE1pc2EgKC92YXIp
```

^cf07a9

The decoded message tell us to check two different folders.

- **L** inside **/opt**
- **Misa** inside **/var**

How my mum says always to me is good manners to girl come first, let see what is this **Misa**.

```bash
cat /var/misa
```

Oh no is too late for her, this is I tried :).
Let look inside **L** folder.

```bash
cd /opt/L && ls
```

After searching in these two folders, we notice that the folder **fake-notebook-rules** is the one which need our attention.
Inside there are two file.
- **case.wav**
- **hint**

An audio that is weird, let download that with **sftp** and listen it with any media player. Strange the media player can't play anything, are we sure this is a real wav file?

```bash
file case.wav
```

It looks like an **ASCII text**, so it is a txt. Let read it.

![[case_wav_file.png]]

Here we go again another encoded message? But it is different. If you know how hexadecimal looks like you will realize that this message is encoded in hexadecimal.
So let use again our [[#^8bcd7b | easy_decoder.py]].

```bash
./easy_decoder.py hex "63 47 46 7a 63 33 64 6b 49 44 6f 67 61 32 6c 79 59 57 6c 7a 5a 58 5a 70 62 43 41 3d"
```

>In the previous **hint** file was written a hint about using a program called [cyberchef](https://gchq.github.io/CyberChef/). It a very nice alternative for decoding.

Once decoded here we have still another encoded message, seriously dude, are you having fun? But we saw a similar message [[#^cf07a9 | before]], so still one time let decode this base64 message.

```bash
./easy_decoder.py base64 cGFzc3dkIDoga2lyYWlzZXZpbCA=
```

And then it is.

```
passwd: kiraisevil
```

Let enter in **sudo** mode

```
sudo su
```

Enter the password: ***kiraisevil***
Go inside **/root** directory.

![[root_access.png]]

***AND WE JUST COMPLETED THE MACHINE***

## Conclusion

It took me more writing this write up than solving the machine, this could appear difficult if you don't have any experience, but trust me in compare with others this is just a pre-cocktail.
I just wanted to try to write a full and clear write up for everyone independent by their confidence with the *pen testing world*. And It helped a lot to enforce my knowledge, apparently it help a lot writing what you do for don't forget it.

Maybe next time I won't be so detailed :).

Thanks again to [KDSAMF](https://twitter.com/KDSAMF), the builder of this environment I had fun solving this machine.

