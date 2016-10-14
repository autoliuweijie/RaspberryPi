用OSX给树莓派安装系统
===

##0. 下载系统

先去树莓派的[官方网站](https://www.raspberrypi.org/downloads/)下载一个系统镜像，推荐下载Raspbian。

下载到某个PATH目录下, 用ls查看。


```
$ ls -l

total 3788800
-rw-r--r--@ 1 liuweijie  staff  1939865600  2  9  2013 2013-02-09-wheezy-raspbian.img
```
    


##1.插入SD卡

插入sd卡，用如下命令检查是否识别

```
$ df -h

Filesystem      Size   Used  Avail Capacity iused      ifree %iused  Mounted on
/dev/disk1     237Gi   58Gi  179Gi    25% 1072769 4293894510    0%   /
devfs          182Ki  182Ki    0Bi   100%     631          0  100%   /dev
map -hosts       0Bi    0Bi    0Bi   100%       0          0  100%   /net
map auto_home    0Bi    0Bi    0Bi   100%       0          0  100%   /home
/dev/disk2s1    14Gi  2.4Mi   14Gi     1%       0          0  100%   /Volumes/Untitled
```

可以看到，disk2s1就是我们的sd卡

用diskutil卸载sd卡

```
$ diskutil unmount /dev/disk2s1
```
用diskutil list命令确认一下设备号

```
$ diskutil list

/dev/disk0 (internal, physical):
#:                       TYPE NAME                    SIZE       IDENTIFIER
0:      GUID_partition_scheme                        *256.1 GB   disk0
1:                        EFI EFI                     209.7 MB   disk0s1
2:          Apple_CoreStorage Apple SSD               255.2 GB   disk0s2
3:                 Apple_Boot Recovery HD             650.0 MB   disk0s3

/dev/disk1 (internal, virtual):
#:                       TYPE NAME                    SIZE       IDENTIFIER
0:                            Apple SSD              +254.8 GB   disk1
                               
/dev/disk2 (external, physical):
#:                       TYPE NAME                    SIZE       IDENTIFIER
0:     FDisk_partition_scheme                        *15.6 GB    disk2
1:             Windows_FAT_32                         15.6 GB    disk2s1
    
```

确认设备号是disk2


##2. 烧入系统

使用dd命令将系统镜像写入，需要特别特别注意disk后的数字，不能搞错！

（说明：/dev/disk1s1是分区，/dev/disk1是块设备，/dev/rdisk1是原始字符设备）


```
$ sudo dd bs=4m if=2013-02-09-wheezy-raspbian.img of=/dev/rdisk2
```

经过几分钟的等待，出现下面的提示，说明SD卡刷好了：


```
462+1 records in
462+1 records out
1939865600 bytes transferred in 156.680604 secs (12381019 bytes/sec)

```

卸载disk2

```
diskutil unmountDisk /dev/disk2
```

现在就可以拔下SD卡，插到树莓派上启动系统了。


##一些坑：

如果插到显示器上没反应，把系统目录下的config.txt里的hdmi_safe=1前面的注释去掉。

如果分辨率很不理想，参考这篇文章设置：

http://shumeipai.nxez.com/2013/08/31/custom-display-resolution-raspberry-pie.html


##参考

1. Mac OSX下给树莓派安装Raspbian系统： http://shumeipai.nxez.com/2014/05/18/raspberry-pi-under-mac-osx-to-install-raspbian-system.html?variant=zh-cn

2. 官方教程：https://www.raspberrypi.org/documentation/installation/installing-images/README.md



