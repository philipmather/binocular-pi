# binocular-pi
## Getting Started

https://www.raspberrypi.org/documentation/installation/installing-images/linux.md

```
pi@raspberrypi:~ $ uname -a
Linux raspberrypi 5.4.44-v8+ #1320 SMP PREEMPT Wed Jun 3 16:20:05 BST 2020 aarch64 GNU/Linux

pi@raspberrypi:~ $ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN group default qlen 1000
    link/ether dc:a6:32:03:7c:10 brd ff:ff:ff:ff:ff:ff
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether dc:a6:32:03:7c:11 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.125/24 brd 192.168.1.255 scope global dynamic noprefixroute wlan0
       valid_lft 86145sec preferred_lft 75345sec
    inet6 fe80::b66a:b3ad:436:3e47/64 scope link 
       valid_lft forever preferred_lft forever

pi@raspberrypi:~ $ sudo systemctl enable ssh
Synchronizing state of ssh.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable ssh
pi@raspberrypi:~ $ sudo systemctl start ssh
pi@raspberrypi:~ $ sudo systemctl status ssh
● ssh.service - OpenBSD Secure Shell server
   Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2020-06-04 00:11:41 BST; 17h ago
     Docs: man:sshd(8)
           man:sshd_config(5)
 Main PID: 521 (sshd)
    Tasks: 1 (limit: 4249)
   CGroup: /system.slice/ssh.service
           └─521 /usr/sbin/sshd -D

Jun 04 00:11:41 raspberrypi systemd[1]: Starting OpenBSD Secure Shell server...
Jun 04 00:11:41 raspberrypi sshd[521]: Server listening on 0.0.0.0 port 22.
Jun 04 00:11:41 raspberrypi sshd[521]: Server listening on :: port 22.
Jun 04 00:11:41 raspberrypi systemd[1]: Started OpenBSD Secure Shell server.
Jun 04 18:03:11 raspberrypi sshd[1011]: Accepted publickey for pi from 192.168.1.97 port 57492 ssh2: RSA SHA256:R+cF8urJOy9Y4Rtc4s4j/c7w9FrU
Jun 04 18:03:11 raspberrypi sshd[1011]: pam_unix(sshd:session): session opened for user pi by (uid=0)


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

pi@raspberrypi:~ $ mkdir Projects
pi@raspberrypi:~ $ cd Projects/
pi@raspberrypi:~ $ git clone git@github.com:philipmather/binocular-pi.git

pi@raspberrypi:~ $ sudo apt-get purge wolfram-engine libreoffice*

pi@raspberrypi:~ $ sudo apt-get update
pi@raspberrypi:~ $ sudo apt-get dist-upgrade
pi@raspberrypi:~ $ sudo rpi-update
pi@raspberrypi:~ $ sudo shutdown -r now
pi@raspberrypi:~ $ sudo su -


   28  echo "set nocompatible" >> ~/.vimrc
   29  sudo vi /boot/config.txt 
   30  sudo apt-get install vim conky

sudo tee "/etc/conky/conky.conf" > /dev/null <<'EOF'
conky.config = {
    alignment = 'middle_middle',
    background = false,
    border_width = 1,
    cpu_avg_samples = 2,
	default_color = 'white',
    default_outline_color = 'white',
    default_shade_color = 'white',
    draw_borders = false,
    draw_graph_borders = true,
    draw_outline = false,
    draw_shades = false,
    use_xft = true,
    font = 'DejaVu Sans Mono:size=24',
    gap_x = 5,
    gap_y = 60,
    minimum_height = 5,
    minimum_width = 5,
    net_avg_samples = 2,
    no_buffers = true,
    out_to_console = false,
    out_to_stderr = false,
    extra_newline = false,
    own_window = true,
    own_window_class = 'Conky',
    own_window_type = 'desktop',
    stippled_borders = 0,
    update_interval = 1.0,
    uppercase = false,
    use_spacer = 'none',
    show_graph_scale = false,
    show_graph_range = false
}

conky.text = [[
${if_existing /proc/net/route wlan0}
${addr wlan0}
${else}${if_existing /proc/net/route eth0}
${addr eth0}
${else}
Network disconnected
${endif}${endif}
]]
EOF

sudo tee "/usr/bin/conky.sh" > /dev/null <<'EOF'
#!/bin/sh
(sleep 4s && conky) &
exit 0
EOF

sudo chmod 744 /usr/bin/conky.sh

sudo tee "/etc/xdg/autostart/conky.desktop" > /dev/null <<'EOF'
[Desktop Entry]
Name=conky
Type=Application
Exec=sh /usr/bin/conky.sh
Terminal=false
Comment=system monitoring tool.Categories=Utility;
EOF

pi@raspberrypi:~ $ DISPLAY=:0 conky &
```

## Make Python 3 default and use a virtual environment
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

### Instal OpenCV
As per https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/
 ~~~https://github.com/amymcgovern/pyparrot/issues/34~~~
```
pi@raspberrypi:~/Projects/binocular-pi $ sudo apt-get remove python3-opencv
Reading package lists... Done
Building dependency tree       
Reading state information... Done
Package 'python3-opencv' is not installed, so not removed
0 upgraded, 0 newly installed, 0 to remove and 4 not upgraded.

pi@raspberrypi:~/Projects/binocular-pi $ sudo apt-get install build-essential cmake git unzip pkg-config libjpeg-dev libtiff5-dev libpng-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 python3-dev libtiff-dev libcanberra-gtk* libtbb2 libtbb-dev libdc1394-22-dev v4l-utils libopenblas-dev libatlas-base-dev libblas-dev liblapack-dev gfortran gcc-arm* protobuf-compiler g++-arm-linux-gnueabihf liblapacke-dev libvtk6-dev libgl1-mesa-dev libxt-dev libosmesa-dev libopenjpip7 libavresample-dev libgstreamer-plugins-base1.0-dev libopenjp2-tools tesseract-ocr tesseract-ocr-eng libtesseract-dev libleptonica-dev libopenjpip-dec-server libgtkglext1-dev libceres-dev libcaffe-cpu-dev libcaffe-cpu1 libgflags2.2 libboost-all-dev libgflags-dev libopenjpip-server libgoogle-glog-dev

pi@raspberrypi:~/Projects/binocular-pi $ sudo pip3 install virtualenv virtualenvwrapper
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Collecting virtualenv
  Downloading https://files.pythonhosted.org/packages/57/6e/a13442adf18bada682f88f55638cd43cc7a39c3e00fdcf898ca4ceaeb682/virtualenv-20.0.21-py2.py3-none-any.whl (4.7MB)
    100% |████████████████████████████████| 4.7MB 102kB/s 
Collecting virtualenvwrapper
  Downloading https://www.piwheels.org/simple/virtualenvwrapper/virtualenvwrapper-5.0.0-py2.py3-none-any.whl
Collecting importlib-metadata<2,>=0.12; python_version < "3.8" (from virtualenv)
  Downloading https://files.pythonhosted.org/packages/98/13/a1d703ec396ade42c1d33df0e1cb691a28b7c08b336a5683912c87e04cd7/importlib_metadata-1.6.1-py2.py3-none-any.whl
Collecting appdirs<2,>=1.4.3 (from virtualenv)
  Downloading https://files.pythonhosted.org/packages/3b/00/2344469e2084fb287c2e0b57b72910309874c3245463acd6cf5e3db69324/appdirs-1.4.4-py2.py3-none-any.whl
Collecting filelock<4,>=3.0.0 (from virtualenv)
  Downloading https://files.pythonhosted.org/packages/93/83/71a2ee6158bb9f39a90c0dea1637f81d5eef866e188e1971a1b1ab01a35a/filelock-3.0.12-py3-none-any.whl
Requirement already satisfied: six<2,>=1.9.0 in /usr/lib/python3/dist-packages (from virtualenv) (1.12.0)
Collecting distlib<1,>=0.3.0 (from virtualenv)
  Downloading https://www.piwheels.org/simple/distlib/distlib-0.3.0-py3-none-any.whl (340kB)
    100% |████████████████████████████████| 348kB 356kB/s 
Collecting virtualenv-clone (from virtualenvwrapper)
  Downloading https://files.pythonhosted.org/packages/83/b8/cd931487d250565392c39409117436d910232c8a3ac09ea2fb62a6c47bff/virtualenv_clone-0.5.4-py2.py3-none-any.whl
Collecting stevedore (from virtualenvwrapper)
  Downloading https://files.pythonhosted.org/packages/11/75/154f7b0bc00a580db2ccac141400dc601f7f2a1bf45bd56515edbda34850/stevedore-2.0.0-py3-none-any.whl (42kB)
    100% |████████████████████████████████| 51kB 472kB/s 
Collecting zipp>=0.5 (from importlib-metadata<2,>=0.12; python_version < "3.8"->virtualenv)
  Downloading https://files.pythonhosted.org/packages/b2/34/bfcb43cc0ba81f527bc4f40ef41ba2ff4080e047acb0586b56b3d017ace4/zipp-3.1.0-py3-none-any.whl
Collecting pbr!=2.1.0,>=2.0.0 (from stevedore->virtualenvwrapper)
  Downloading https://files.pythonhosted.org/packages/96/ba/aa953a11ec014b23df057ecdbc922fdb40ca8463466b1193f3367d2711a6/pbr-5.4.5-py2.py3-none-any.whl (110kB)
    100% |████████████████████████████████| 112kB 422kB/s 
Installing collected packages: zipp, importlib-metadata, appdirs, filelock, distlib, virtualenv, virtualenv-clone, pbr, stevedore, virtualenvwrapper
Successfully installed appdirs-1.4.4 distlib-0.3.0 filelock-3.0.12 importlib-metadata-1.6.1 pbr-5.4.5 stevedore-2.0.0 virtualenv-20.0.21 virtualenv-clone-0.5.4 virtualenvwrapper-5.0.0 zipp-3.1.0

pi@raspberrypi:~/Projects/binocular-pi $ echo "# virtualenv and virtualenvwrapper
> export WORKON_HOME=$HOME/.virtualenvs
> export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
> export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
> source /usr/local/bin/virtualenvwrapper.sh
> export VIRTUALENVWRAPPER_ENV_BIN_DIR=bin" >> ~/.bashrc

pi@raspberrypi:~/Projects/binocular-pi $ source ~/.bashrc
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/premkproject
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/postmkproject
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/initialize
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/premkvirtualenv
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/postmkvirtualenv
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/prermvirtualenv
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/postrmvirtualenv
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/predeactivate
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/postdeactivate
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/preactivate
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/postactivate
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/get_env_details

pi@raspberrypi:~/Projects/binocular-pi $ mkvirtualenv cv -p python3
created virtual environment CPython3.7.3.final.0-64 in 930ms
  creator CPython3Posix(dest=/home/pi/.virtualenvs/cv, clear=False, global=False)
  seeder FromAppData(download=False, pip=latest, setuptools=latest, wheel=latest, via=copy, app_data_dir=/home/pi/.local/share/virtualenv/seed-app-data/v1.0.1)
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator
virtualenvwrapper.user_scripts creating /home/pi/.virtualenvs/cv/usr/local/bin/predeactivate

(cv) pi@raspberrypi:~/Projects/binocular-pi $ cd ~/Projects/

(cv) pi@raspberrypi:~/Projects $ wget https://github.com/opencv/opencv/archive/4.3.0.tar.gz -O opencv-4.3.0.tar.gz 
(cv) pi@raspberrypi:~/Projects $ wget https://github.com/opencv/opencv_contrib/archive/4.3.0.tar.gz -O opencv_contrib-4.3.0.tar.gz

(cv) pi@raspberrypi:~/Projects $ tar -xzvf opencv-4.3.0.tar.gz && tar -xzvf opencv_contrib-4.3.0.tar.gz

(cv) pi@raspberrypi:~/Projects $ ls -lad opencv*
drwxr-xr-x 11 pi pi     4096 Apr  3 12:45 opencv-4.3.0
-rw-r--r--  1 pi pi 87941482 Jun  7 16:20 opencv-4.3.0.tar.gz
drwxr-xr-x  6 pi pi     4096 Apr  2 18:01 opencv_contrib-4.3.0
-rw-r--r--  1 pi pi 60881379 Jun  7 16:23 opencv_contrib-4.3.0.tar.gz

pi@raspberrypi:~/Projects $ sudo sed -ie 's/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=2048/' /etc/dphys-swapfile

(cv) pi@raspberrypi:~/Projects $ sudo sed -ie 's/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=2048/' /etc/dphys-swapfile
(cv) pi@raspberrypi:~/Projects $ sudo /etc/init.d/dphys-swapfile restart
[ ok ] Restarting dphys-swapfile (via systemctl): dphys-swapfile.service.

pi@raspberrypi:~/Projects/opencv-4.3.0/build $ workon cv

(cv) pi@raspberrypi:~/Projects/opencv-4.3.0/build $ pip install numpy
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Collecting numpy
  Downloading numpy-1.18.5.zip (5.4 MB)
     |████████████████████████████████| 5.4 MB 59 kB/s 
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
    Preparing wheel metadata ... done
Building wheels for collected packages: numpy
  Building wheel for numpy (PEP 517) ... /
done
  Created wheel for numpy: filename=numpy-1.18.5-cp37-cp37m-linux_aarch64.whl size=11587825 sha256=cc5107f59bb5a380ecb79d8a062493f1389ce00796f7eb364b662c9027b7004f
  Stored in directory: /home/pi/.cache/pip/wheels/32/f0/3a/ebd0777a9772fd6db59981343ae81b3e025fa572878b2a1bd8
Successfully built numpy
Installing collected packages: numpy
Successfully installed numpy-1.18.5


(cv) pi@raspberrypi:~/Projects $ mkdir ~/Projects/opencv-4.3.0/build
(cv) pi@raspberrypi:~/Projects $ cd ~/Projects/opencv-4.3.0/build

# See https://github.com/opencv/opencv/issues/12957
(cv) pi@raspberrypi:~/Projects/opencv-4.3.0/build $ sed -ie 's#SET(Open_BLAS_INCLUDE_SEARCH_PATHS#SET(Open_BLAS_INCLUDE_SEARCH_PATHS\n  /usr/include/#;s#SET(Open_BLAS_LIB_SEARCH_PATHS#SET(Open_BLAS_LIB_SEARCH_PATHS\n        /usr/lib/aarch64-linux-gnu/#' ../cmake/OpenCVFindOpenBLAS.cmake

(cv) pi@raspberrypi:~/Projects/opencv-4.3.0/build $ cmake -D CMAKE_BUILD_TYPE=RELEASE \
>         -D CMAKE_INSTALL_PREFIX=/usr/local \
>         -D OPENCV_EXTRA_MODULES_PATH=~/Projects/opencv_contrib-4.3.0/modules/ \
>         -D Atlas_INCLUDE_DIR=/usr/include/arm-linux-gnueabihf \
>         -D ENABLE_NEON=ON \
>         -D ENABLE_VFPV3=ON \
>         -D WITH_VTK=ON \
>         -D WITH_OPENGL=ON \
>         -D WITH_TENGINE=OFF \
>         -D WITH_OPENMP=ON \
>         -D BUILD_TIFF=ON \
>         -D WITH_FFMPEG=ON \
>         -D WITH_GSTREAMER=ON \
>         -D WITH_TBB=ON \
>         -D BUILD_TBB=ON \
>         -D BUILD_TESTS=OFF \
>         -D WITH_V4L=ON \
>         -D WITH_LIBV4L=ON \
>         -D OPENCV_EXTRA_EXE_LINKER_FLAGS=-latomic \
>         -D OPENCV_ENABLE_NONFREE=ON \
>         -D INSTALL_C_EXAMPLES=OFF \
>         -D INSTALL_PYTHON_EXAMPLES=OFF \
>         -D BUILD_NEW_PYTHON_SUPPORT=ON \
>         -D BUILD_opencv_python3=TRUE \
>         -D OPENCV_GENERATE_PKGCONFIG=ON \
>         -D BUILD_EXAMPLES=OFF ..



cmake \
  -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D Atlas_INCLUDE_DIR=/usr/include/arm-linux-gnueabihf \
  -D WITH_VTK=ON \
  -D WITH_OPENGL=ON \
  -D WITH_TENGINE=OFF \
  -D WITH_OPENMP=ON \
  -D WITH_FFMPEG=ON \
  -D WITH_GSTREAMER=ON \
  -D WITH_TBB=ON \
  -D WITH_V4L=ON \
  -D WITH_LIBV4L=ON \
  -D OPENCV_EXTRA_MODULES_PATH=~/Projects/opencv_contrib-4.3.0/modules/ \
  -D OPENCV_EXTRA_EXE_LINKER_FLAGS=-latomic \
  -D OPENCV_ENABLE_NONFREE=ON \
  -D OPENCV_GENERATE_PKGCONFIG=ON \
  -D INSTALL_C_EXAMPLES=OFF \
  -D INSTALL_PYTHON_EXAMPLES=OFF \
  -D BUILD_TIFF=ON \
  -D BUILD_NEW_PYTHON_SUPPORT=ON \
  -D BUILD_opencv_python3=TRUE \
  -D BUILD_TBB=ON \
  -D BUILD_TESTS=OFF \
  -D BUILD_EXAMPLES=OFF ..
         
#         -D BUILD_PROTOBUF=ON \
# -D BLAS=open \ ##?
-D UPDATE_PROTO_FILES=ON \
-D ENABLE_VFPV3=ON \
# No longer require these see https://github.com/opencv/opencv/issues/13114
#         -D ENABLE_NEON=ON \
#         -D ENABLE_VFPV3=ON \
# Still results in
#-- Performing Test HAVE_CPU_NEON_SUPPORT (check file: cmake/checks/cpu_neon.cpp)
#-- Performing Test HAVE_CPU_NEON_SUPPORT - Success
#-- Performing Test HAVE_CPU_FP16_SUPPORT (check file: cmake/checks/cpu_fp16.cpp)
#-- Performing Test HAVE_CPU_FP16_SUPPORT - Success
#-- Performing Test HAVE_CPU_BASELINE_FLAGS
#-- Performing Test HAVE_CPU_BASELINE_FLAGS - Success


-- Could not find OpenBLAS include. Turning OpenBLAS_FOUND off
Could NOT find JNI 

      -DCPU_BASELINE="NEON" \
      -DWITH_INF_ENGINE=ON \

#sudo apt install libjasper-dev libpng12-dev ibavcodec-dev mesa-common-dev
