# binocular-pi
## Getting Started

```
pi@raspberrypi:~ $ ssh-keygen 
Generating public/private rsa key pair.
Enter file in which to save the key (/home/pi/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/pi/.ssh/id_rsa.
Your public key has been saved in /home/pi/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:[[REDACTED SHORT STRING]] pi@raspberrypi
The key's randomart image is:
+---[RSA 2048]----+
|+oB*+oo+++S      |
| REDACTED STRING |
|.X=.oooo.+       |
| o + +  S        |
| REDACTED STRING |
|  * + o  .       |
|      o .+..     |
| REDACTED STRING |
|       o o+      |
+----[SHA256]-----+

# Upload you id_rsa.pub as a SSH key to github as well

pi@raspberrypi:~ $ cat .ssh/id_rsa.pub 
ssh-rsa [[REDACTED MULTILINE STRING]] pi@raspberrypi

pi@raspberrypi:~ $ git config --global user.email "phil@philipmather.me.uk"
pi@raspberrypi:~ $ git config --global user.name "Philip Mather"

pi@raspberrypi:~ $ mkdir Projects/
pi@raspberrypi:~ $ cd Projects

pi@raspberrypi:~/Projects $ git clone git@github.com:philipmather/binocular-pi.git
Cloning into 'binocular-pi'...
Warning: Permanently added the RSA host key for IP address '140.82.118.3' to the list of known hosts.
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 5 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (5/5), 13.45 KiB | 1.34 MiB/s, done.
pi@raspberrypi:~/Projects $ cd binocular-pi/

pi@raspberrypi:~/Projects/binocular-pi $ sudo apt install vim

```

### Make Python 3 default and use a virtual environment
From the "Use Python 3" section of https://learn.sparkfun.com/tutorials/python-programming-tutorial-getting-started-with-the-raspberry-pi/configure-your-pi
```
pi@raspberrypi:~/Projects/binocular-pi $ echo "alias python='/usr/bin/python3'" >> ~/.bashrc
pi@raspberrypi:~/Projects/binocular-pi $ echo "alias pip=pip3" >> ~/.bashrc
pi@raspberrypi:~/Projects/binocular-pi $ python --version
Python 2.7.16
pi@raspberrypi:~/Projects/binocular-pi $ source ~/.bashrc 
pi@raspberrypi:~/Projects/binocular-pi $ python --version
Python 3.7.3
pi@raspberrypi:~/Projects/binocular-pi $ sudo apt-get update
Hit:1 http://archive.raspberrypi.org/debian buster InRelease
Hit:2 http://raspbian.raspberrypi.org/raspbian buster InRelease
Reading package lists... Done
pi@raspberrypi:~/Projects/binocular-pi $ sudo apt-get install python3-pip
Reading package lists... Done
Building dependency tree       
Reading state information... Done
python3-pip is already the newest version (18.1-5+rpt1).
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
```

Then, as per https://docs.python-guide.org/dev/virtualenvs/
```
pi@raspberrypi:~/Projects/binocular-pi $ grep venv .gitignore 
.venv
venv/
venv.bak/
pi@raspberrypi:~/Projects/binocular-pi $ pip install virtualenv
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Collecting virtualenv
  Downloading https://files.pythonhosted.org/packages/9b/67/f28095ba538be54fc48ec7774d5778a7246972cf8c701430ec0c96bf0860/virtualenv-20.0.20-py2.py3-none-any.whl (4.7MB)
    100% |████████████████████████████████| 4.7MB 79kB/s 
Collecting importlib-metadata<2,>=0.12; python_version < "3.8" (from virtualenv)
  Downloading https://files.pythonhosted.org/packages/ad/e4/891bfcaf868ccabc619942f27940c77a8a4b45fd8367098955bb7e152fb1/importlib_metadata-1.6.0-py2.py3-none-any.whl
Requirement already satisfied: six<2,>=1.9.0 in /usr/lib/python3/dist-packages (from virtualenv) (1.12.0)
Collecting distlib<1,>=0.3.0 (from virtualenv)
  Downloading https://www.piwheels.org/simple/distlib/distlib-0.3.0-py3-none-any.whl (340kB)
    100% |████████████████████████████████| 348kB 310kB/s 
Collecting appdirs<2,>=1.4.3 (from virtualenv)
  Downloading https://files.pythonhosted.org/packages/56/eb/810e700ed1349edde4cbdc1b2a21e28cdf115f9faf263f6bbf8447c1abf3/appdirs-1.4.3-py2.py3-none-any.whl
Collecting filelock<4,>=3.0.0 (from virtualenv)
  Downloading https://files.pythonhosted.org/packages/93/83/71a2ee6158bb9f39a90c0dea1637f81d5eef866e188e1971a1b1ab01a35a/filelock-3.0.12-py3-none-any.whl
Collecting zipp>=0.5 (from importlib-metadata<2,>=0.12; python_version < "3.8"->virtualenv)
  Downloading https://files.pythonhosted.org/packages/b2/34/bfcb43cc0ba81f527bc4f40ef41ba2ff4080e047acb0586b56b3d017ace4/zipp-3.1.0-py3-none-any.whl
Installing collected packages: zipp, importlib-metadata, distlib, appdirs, filelock, virtualenv
Successfully installed appdirs-1.4.3 distlib-0.3.0 filelock-3.0.12 importlib-metadata-1.6.0 virtualenv-20.0.20 zipp-3.1.0

pi@raspberrypi:~/Projects/binocular-pi $ virtualenv --version
virtualenv 20.0.20 from /home/pi/.local/lib/python3.7/site-packages/virtualenv/__init__.py

pi@raspberrypi:~/Projects/binocular-pi $ virtualenv venv
created virtual environment CPython3.7.3.final.0-32 in 756ms
  creator CPython3Posix(dest=/home/pi/Projects/binocular-pi/venv, clear=False, global=False)
  seeder FromAppData(download=False, pip=latest, setuptools=latest, wheel=latest, via=copy, app_data_dir=/home/pi/.local/share/virtualenv/seed-app-data/v1.0.1)
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator

pi@raspberrypi:~/Projects/binocular-pi $ source venv/bin/activate
(venv) pi@raspberrypi:~/Projects/binocular-pi $

(venv) pi@raspberrypi:~/Projects/binocular-pi $ tree -d
.
└── venv
    ├── bin
    └── lib
        └── python3.7
            └── site-packages
                ├── pip
                │   ├── _internal
                │   │   ├── cli
                │   │   ├── commands
[[More directories]]

```


