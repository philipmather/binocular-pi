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

### Instal OpenCV
As per https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/
 ~~~https://github.com/amymcgovern/pyparrot/issues/34~~~
```
sudo apt-get remove python3-opencv
sudo apt-get install build-essential cmake git unzip pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev ibavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 python3-dev libtiff-dev libcanberra-gtk* libtbb2 libtbb-dev libdc1394-22-dev v4l-utils libopenblas-dev libatlas-base-dev libblas-dev liblapack-dev gfortran gcc-arm* protobuf-compiler g++-arm-linux-gnueabihf
sudo apt install liblapacke-dev

sudo pip3 install virtualenv virtualenvwrapper

echo "# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source /usr/local/bin/virtualenvwrapper.sh
export VIRTUALENVWRAPPER_ENV_BIN_DIR=bin" >> ~/.bashrc

source ~/.bashrc
mkvirtualenv cv -p python3

pi@raspberrypi:~/Projects/binocular-pi $ cd ~/Projects/
pi@raspberrypi:~/Projects $ wget https://github.com/opencv/opencv/archive/4.3.0.tar.gz
mv 4.3.0.tar.gz opencv-4.3.0.tar.gz 

wget https://github.com/opencv/opencv_contrib/archive/4.3.0.tar.gz
mv 4.3.0.tar.gz opencv_contrib-4.3.0.tar.gz 

tar -xzvf opencv-4.3.0.tar.gz
tar -xzvf opencv_contrib-4.3.0.tar.gz

pi@raspberrypi:~/Projects $ ls -lad opencv*
drwxr-xr-x 11 pi pi     4096 Apr  3 12:45 opencv-4.3.0
-rw-r--r--  1 pi pi 87941482 May 12 21:38 opencv-4.3.0.tar.gz
drwxr-xr-x  6 pi pi     4096 Apr  2 18:01 opencv_contrib-4.3.0
-rw-r--r--  1 pi pi 60881379 May 12 21:30 opencv_contrib-4.3.0.tar.gz

pi@raspberrypi:~/Projects $ sudo sed -ie 's/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=2048/' /etc/dphys-swapfile

pi@raspberrypi:~/Projects $ sudo /etc/init.d/dphys-swapfile stop
[ ok ] Stopping dphys-swapfile (via systemctl): dphys-swapfile.service.
pi@raspberrypi:~/Projects $ sudo /etc/init.d/dphys-swapfile start
[ ok ] Starting dphys-swapfile (via systemctl): dphys-swapfile.service.

workon cv
pip install numpy imutils scikit-lean

(cv) pi@raspberrypi:~/Projects $ cd ~/Projects/opencv-4.3.0/
(cv) pi@raspberrypi:~/Projects/opencv-4.3.0 $ mkdir build
(cv) pi@raspberrypi:~/Projects/opencv-4.3.0 $ cd build
(cv) pi@raspberrypi:~/Projects/opencv-4.3.0/build $ cmake -D CMAKE_BUILD_TYPE=RELEASE \
     -D CMAKE_INSTALL_PREFIX=/usr/local \
     -D OPENCV_EXTRA_MODULES_PATH=~/Projects/opencv_contrib-4.3.0/modules/ \
     -D ENABLE_NEON=ON \
     -D ENABLE_VFPV3=ON \
     -D BUILD_TESTS=OFF \
     -D INSTALL_PYTHON_EXAMPLES=OFF \
     -D OPENCV_ENABLE_NONFREE=ON \
     -D CMAKE_SHARED_LINKER_FLAGS=-latomic \
     -D BUILD_EXAMPLES=OFF ..

(cv) pi@raspberrypi:~/Projects/opencv-4.3.0/build $ make -j4

(cv) pi@raspberrypi:~/Projects/opencv-4.3.0/build $ sudo make install
[  8%] Built target libwebp
[ 15%] Built target IlmImf
...
-- Installing: /usr/local/bin/opencv_interactive-calibration
-- Set runtime path of "/usr/local/bin/opencv_interactive-calibration" to "/usr/local/lib"
-- Installing: /usr/local/bin/opencv_version
-- Set runtime path of "/usr/local/bin/opencv_version" to "/usr/local/lib"

(cv) pi@raspberrypi:~/Projects/opencv-4.3.0/build $ sudo ldconfig
(cv) pi@raspberrypi:~/Projects/opencv-4.3.0/build $ sudo apt-get update

(cv) pi@raspberrypi:~/Projects/opencv-4.3.0/build $ cd /usr/local/lib/python3.7/site-packages/cv2/python-3.7
(cv) pi@raspberrypi:/usr/local/lib/python3.7/site-packages/cv2/python-3.7 $ sudo mv cv2.cpython-37m-arm-linux-gnueabihf.so cv2.so
cv2.cpython-37m-arm-linux-gnueabihf.so
(cv) pi@raspberrypi:/usr/local/lib/python3.7/site-packages/cv2/python-3.7 $ sudo mv cv2.cpython-37m-arm-linux-gnueabihf.so cv2.so
(cv) pi@raspberrypi:/usr/local/lib/python3.7/site-packages/cv2/python-3.7 $ cd ~/.virtualenvs/cv/lib/python3.7/site-packages/
(cv) pi@raspberrypi:~/.virtualenvs/cv/lib/python3.7/site-packages $ n -s /usr/local/lib/python3.7/site-packages/cv2/python-3.7/cv2.so cv2.so^C
(cv) pi@raspberrypi:~/.virtualenvs/cv/lib/python3.7/site-packages $ ln -s /usr/local/lib/python3.7/site-packages/cv2/python-3.7/cv2.so cv2.so
(cv) pi@raspberrypi:~/.virtualenvs/cv/lib/python3.7/site-packages $ python
Python 3.7.3 (default, Dec 20 2019, 18:57:59) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> cv2.__version__
'4.3.0'

pi@raspberrypi:~/Projects/opencv-4.3.0/build $ sudo sed -ie 's/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=100/' /etc/dphys-swapfile
pi@raspberrypi:~/Projects/opencv-4.3.0/build $ sudo /etc/init.d/dphys-swapfile restart
[ ok ] Restarting dphys-swapfile (via systemctl): dphys-swapfile.service.
pi@raspberrypi:~/Projects/opencv-4.3.0/build $ sudo /etc/init.d/dphys-swapfile status
● dphys-swapfile.service - dphys-swapfile - set up, mount/unmount, and delete a swap file
   Loaded: loaded (/lib/systemd/system/dphys-swapfile.service; enabled; vendor preset: enabled)
   Active: active (exited) since Sat 2020-05-16 19:16:34 BST; 6s ago
     Docs: man:dphys-swapfile(8)
  Process: 8012 ExecStart=/sbin/dphys-swapfile setup (code=exited, status=0/SUCCESS)
  Process: 8051 ExecStart=/sbin/dphys-swapfile swapon (code=exited, status=0/SUCCESS)
 Main PID: 8051 (code=exited, status=0/SUCCESS)

May 16 19:16:34 raspberrypi systemd[1]: Starting dphys-swapfile - set up, mount/unmount, and delete a swap file...
May 16 19:16:34 raspberrypi dphys-swapfile[8012]: want /var/swap=100MByte, checking existing: deleting wrong size file (2147483648…100MBytes
May 16 19:16:34 raspberrypi systemd[1]: Started dphys-swapfile - set up, mount/unmount, and delete a swap file.
Hint: Some lines were ellipsized, use -l to show in full.

# VTK bits from https://blog.kitware.com/raspberry-pi-likes-vtk/
sudo apt-get install libvtk6-dev libgl1-mesa-dev libxt-dev libosmesa-dev

# test later, https://qengineering.eu/install-opencv-4.1-on-raspberry-pi-4.html
cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D OPENCV_EXTRA_MODULES_PATH=~/Projects/opencv_contrib-4.3.0/modules/ \
        -D Atlas_INCLUDE_DIR=/usr/include/arm-linux-gnueabihf \
        -D ENABLE_NEON=ON \
        -D ENABLE_VFPV3=ON \
        -D WITH_VTK=ON \
        -D WITH_TENGINE=OFF \
        -D WITH_OPENMP=ON \
        -D BUILD_TIFF=ON \
        -D WITH_FFMPEG=ON \
        -D WITH_GSTREAMER=ON \
        -D WITH_TBB=ON \
        -D BUILD_TBB=ON \
        -D BUILD_TESTS=OFF \
        -D WITH_V4L=ON \
        -D WITH_LIBV4L=ON \
        -D OPENCV_EXTRA_EXE_LINKER_FLAGS=-latomic \
        -D OPENCV_ENABLE_NONFREE=ON \
        -D INSTALL_C_EXAMPLES=OFF \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D BUILD_NEW_PYTHON_SUPPORT=ON \
        -D BUILD_opencv_python3=TRUE \
        -D OPENCV_GENERATE_PKGCONFIG=ON \
        -D BUILD_EXAMPLES=OFF ..

#        -D WITH_EIGEN=OFF \

# also https://github.com/opencv/opencv/wiki/Tengine-based-acceleration
#        -D WITH_TENGINE=ON \
# DO NOT DO THAT, dire performance ensued, went from detecting in 0.3s to 20?!?

$ sudo make install
(cv) pi@raspberrypi:~/Projects/opencv-4.3.0/build $ sudo ldconfig
(cv) pi@raspberrypi:~/Projects/opencv-4.3.0/build $ sudo apt-get update
Get:1 http://raspbian.raspberrypi.org/raspbian buster InRelease [15.0 kB]
Get:2 http://archive.raspberrypi.org/debian buster InRelease [25.1 kB]
Get:3 http://raspbian.raspberrypi.org/raspbian buster/main armhf Packages [13.0 MB]
Get:4 http://archive.raspberrypi.org/debian buster/main armhf Packages [328 kB]
Fetched 13.4 MB in 47s (286 kB/s)                                                                                                          
Reading package lists... Done
(cv) pi@raspberrypi:~/Projects/opencv-4.3.0/build $ sudo sed -ie 's/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=100/' /etc/dphys-swapfile
(cv) pi@raspberrypi:~/Projects/opencv-4.3.0/build $ sudo /etc/init.d/dphys-swapfile restart
[ ok ] Restarting dphys-swapfile (via systemctl): dphys-swapfile.service.

(cv) pi@raspberrypi:~/Projects/opencv-4.3.0/build $ cd ~/.virtualenvs/cv/lib/python3.7/site-packages
(cv) pi@raspberrypi:~/.virtualenvs/cv/lib/python3.7/site-packages $ ln -s /usr/local/lib/python3.7/site-packages/cv2/python-3.7/cv2.cpython-37m-arm-linux-gnueabihf.so

 python extract_embeddings.py --dataset ~/Pictures/individuals/ --embeddings output/embeddings.pickle --detector face_detection_model --embedding-model ./embedding_model/openface_nn4.small2.v1.t7
 python train_model.py --embeddings output/embeddings.pickle --recognizer output/recognizer.pickle --le output/le.pickle

```

## Git config
```
echo "output/**" >> .gitignore
```

## References
https://pypi.org/project/opencv-contrib-python/
https://github.com/scivision/pyimagevideo
https://gist.github.com/tedmiston/6060034
https://docs.opencv.org/4.2.0/d2/de6/tutorial_py_setup_in_ubuntu.html
https://stereopi.com/blog/opencv-comparing-speed-c-and-python-code-raspberry-pi-stereo-vision
https://www.pyimagesearch.com/2018/09/24/opencv-face-recognition
https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/
https://github.com/opencv/opencv/wiki/Tengine-based-acceleration
https://blog.kitware.com/raspberry-pi-likes-vtk/
