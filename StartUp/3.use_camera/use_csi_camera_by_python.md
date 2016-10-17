Raspbian中python使用CSI摄像头
===


概述：csi摄像头是树莓派的官方摄像头，python要调用可以有两种办法，第一种是用官方的picamera包，第二种是使用opencv.


##0. 启用摄像头

无论使用哪种方法，都先确保摄像头启用。在Shell中输入
```
sudo raspi-config
```

移动光标至菜单中的 "Enable Camera（启用摄像头）"，将其设为Enable（启用状态）。完成之后重启树莓派。
![这里写图片描述](http://img.blog.csdn.net/20161016111328068)

##1.使用picamera包

安装picamera
```
pip install picamera
或者
apt-get install picamera
```
具体操作方法见[官方手册](https://www.raspberrypi.org/documentation/usage/camera/python/README.md)


##2.使用opencv

这里要注意一点，树莓派官方摄像头插入后没有/dev/video0节点，这就导致无法直接用opencv调用。

解决办法：树莓派中的camera module是放在/boot/目录下以固件的形式加载的，不是一个标准的v4l2的摄像头ko驱动，所以加载起来之后会找不到/dev/video0的设备节点。这是因为这个驱动是在底层的，v4l2这个驱动框架还没有加载，所以要在/etc/modules里面添加一行bcm2835-v4l2(是4L2，不是412，小写的L)，这句话意思是在系统启动之后会加载bcm2835-v4l2这个模块，这个模块在树莓派系统的/lib/modules/xxx/xxx/xxx下面，添加之后重启系统，就会在/dev/下面发现video0设备节点了。

    # 在/etc/modules里添加这一行
    bcm2835-v4l2

这样之后就可以用opencv调用，可以尝试执行如下代码进行验证：

```
# test_camera.py 

import numpy as np
import cv2 as cv


def take_photo():
    cap = cv.VideoCapture(0)
    ret, photo = cap.read()
    if ret:
        print "take photo successfuly"
        cv.imwrite("./photo.png", photo)
    else:
        print "Error! Photo failed!"


if __name__ == "__main__":
    take_photo()
```

看看是否生成./photo.png照片。

也可以用mplaer播放器播放试试

```
sudo apt-get install mplayer
sudo mplayer tv://
```

