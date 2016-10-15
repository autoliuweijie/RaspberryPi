Raspbian搭建python + opencv环境
===

环境：raspberry 3b  + raspbian jessie
参考：http://www.tuicool.com/articles/NZF3q2q
       http://www.pyimagesearch.com/2015/10/26/how-to-install-opencv-3-on-raspbian-jessie/?utm_source=tuicool&utm_medium=referral


##1. 安装依赖项

安装一些开发工具

    sudo apt-get install build-essential git cmake pkg-config

安装一些图片的I/O包

    sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

安装一些vedio的I/O包

    sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
    sudo apt-get install libxvidcore-dev libx264-dev

安装一些图形工具库GTK

    sudo apt-get install libgtk2.0-dev

安装一些opencv的内部库，例如矩阵操作

    sudo apt-get install libatlas-base-dev gfortran

安装python2.7 和 python 3的一些开发工具

    sudo apt-get install python2.7-dev python3-dev


##2. 获取opencv源码

获取opencv源码

    cd ~/
    wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.0.0.zip
    unzip opencv.zip

获取opencv_contrib源码，务必保证与opencv的版本一致（opencv3.0.0 配 opencv_contrib3.0.0)

    wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.0.0.zip
    unzip opencv_contrib.zip


##3. 创造 python 虚拟环境

### 安装和配置virtualenv 和 virtualenvwrapper

安装pip

    wget https://bootstrap.pypa.io/get-pip.py
    sudo python get-pip.py

安装virtualenv 和 virtualenvwrapper

    sudo pip install virtualenv virtualenvwrapper
    sudo rm -rf ~/.cache/pip

设置virtualenv的启动， 修改～/.profile文件：

    sudo vim ~/.profile

在最后加上这两行

    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh

重新加载~/.profile

    source ~/.profile

### 创建env

创建env

    mkvirtualenv cv  # python2.7的环境
    或
    mkvirtualenv cv -p python3  # python3的环境

进入·env环境：

    source ~/.profile
    workon cv

进入以后，命令行前面会多个(cv)

安装numpy

    pip install numpy

##4. 编译和安装opencv

确保在虚拟cv环境中，如果不在请 workon cv

编译opencv, 先build

    cd ~/opencv-3.0.0/
    mkdir build
    cd build
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
     -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.0.0/modules \
    -D BUILD_EXAMPLES=ON ..

开始编译：

    make -j4   # 树莓派2以上有4个核

开始安装

    sudo make install
    sudo ldconfig


##5. 为python配置opencv

至此opencv基本安装好，并且opencv也给系统的python添加了软连接，用如下命令查看

    # for python2.7
    ls -l /usr/local/lib/python2.7/site-packages/
    total 1640
    -rw-r--r-- 1 root staff 1677024 Oct 15 19:11 cv2.so

    # for python3.4
    ls -l /usr/local/lib/python3.4/site-packages/
    total 1636
    -rw-r--r-- 1 root staff 1674656 Oct 15 19:11 cv2.cpython-34m.so


但是我们要为virtualenv中的python引入软连接，需要手动进行：

    # for python2.7
    cd ~/.virtualenvs/cv/lib/python2.7/site-packages/
    ln -s /usr/local/lib/python2.7/site-packages/cv2.so cv2.so

    # for python3.4
    cd ~/.virtualenvs/cv/lib/python3.4/site-packages/
    ln-s/usr/local/lib/python3.4/site-packages/cv2.socv2.so


##6.验证是否安装成功

在shell中

    $ workon cv
    $ python
    >>> import cv2
    >>> cv2.__version__
    '3.0.0'

这就安装成功了！

最后把安装包删了
    
    cd ~/
    rm opencv_contrib.zip opencv.zip get-pip.py
    rm -r opencv_contrib-3.0.0/ opencv-3.0.0/








    






    

