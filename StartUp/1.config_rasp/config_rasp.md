初次配置Raspbian系统
===


说明：在安装好系统后，一般要进行一些配置，这里主要介绍一些常用的配置。

环境: Raspberry-pi 3B + raspbian jessie


##1. 配置分辨率

取出TF卡装入读卡器中，插入PC机中，修改其中的config.txt文件，修改或添加如下内容：

    hdmi_group=****
    hdmi_mode=****
    hdmi_ignore_edid=0xa5000080

hdmi_group=1或者2，1表示用电视规格分辨率CEA, 2表示用计算机规格分辨率DMT。

hdmi_model用来选择分辨率和刷新频率，见[自定义树莓派分辨率](http://shumeipai.nxez.com/2013/08/31/custom-display-resolution-raspberry-pie.html)。

另外一项“hdmi_ignore_edid”，是命令树莓派不检测HDMI设备的任何信息，只按照我们指定的分辨率输出。 如果不加，树莓派可能仍会“自作聪明”的检测HDMI设备的分辨率，结果造成我们设置的分辨率无效。

如果插到显示器上没反应，把系统目录下的config.txt里的hdmi_safe=1前面的注释去掉。


##2. 配置apt-get源

在国内使用系统的apt-get源实在太慢了，幸好国内提供了一些源，推荐使用中科大的源。

编辑/etc/apt/sources.list文件。删除原文件所有内容，用以下内容取代：

    deb http://mirrors.ustc.edu.cn/raspbian/raspbian/ jessie main non-free contrib
    deb-src http://mirrors.ustc.edu.cn/raspbian/raspbian/ jessie main non-free contrib

编辑此文件后，请使用sudo apt-get update命令，更新软件列表.

ref: https://lug.ustc.edu.cn/wiki/mirrors/help/raspbian


##2. 配置键盘

raspbian默认的键盘布局为 gb ，这会导致键盘上的 @ # | \ 变为 " £ ~ # @

解决办法：修改 /etc/default/keyboard ，修改含有 XKBMODEL 这行，改为 XKBMODEL="cn" (默认被设置成了 gb ），重启即可。


##3. 配置时钟

树莓派没有硬件时钟，每次重启都会时间重置，通常需要利用网络时间服务器配置时间。

解决方法：使用openntpd

###第一步：配置时区

首先设置时区，编辑/etc/rc.conf文件（如果不存在，就创建）

    vim /etc/rc.conf

修改成如下内容：

    LOCALE="en_US.UTF-8"
    DAEMON_LOCALE="no"
    HARDWARECLOCK="localtime"
    TIMEZONE="Asia/Shanghai"

    DAEMONS=(syslog-ng network netfs crond openntpd sshd)

做一个软连接（/etc/localtime这个软连接原本不是指向上海的，我们将其改为指向上海）：

    ln -sf /usr/sharte/zoneinfo/Asia/Shanghai /etc/localtime

###第二步：使用NTP来自动对时

NTP是Network Time Protocol, 先安装openntpd:

    sudo apt-get install openntpd

在/etc/rc.conf中添加最后一句话（在第一步时已经添加，表示让openntpd开机启动）：

    DAEMONS=(syslog-ng network netfs crond openntpd sshd)

重启即可。


##4. 开机上报IP

如果没有显示器，想要知道树莓派的IP是很困难的事。

解决办法：写一个脚本，该脚本自动检测ip，并把ip发到指定邮箱，让该脚本开机启动。

脚本send_ip.py如下：

```
import socket
import fcntl
import time
import struct
import smtplib
import urllib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# 发送邮件的基本函数，参数依次如下
# smtp服务器地址、邮箱用户名，邮箱秘密，发件人地址，收件人地址（列表的方式），邮件主题，邮件html内容
def sendEmail(smtpserver,username,password,sender,receiver,subject,msghtml):
    msgRoot = MIMEMultipart('related')
    msgRoot["To"] = ','.join(receiver)
    msgRoot["From"] = sender
    msgRoot['Subject'] =  subject
    msgText = MIMEText(msghtml,'html','utf-8')
    msgRoot.attach(msgText)
    #sendEmail
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()

# 检查网络连同性
def check_network():
    while True:
        try:
            result=urllib.urlopen('http://baidu.com').read()
            print result
            print "Network is Ready!"
            break
        except Exception , e:
           print e
           print "Network is not ready,Sleep 5s...."
           time.sleep(5)
    return True

# 获得本级制定接口的ip地址
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1",80))
    ipaddr=s.getsockname()[0]
    s.close()
    return ipaddr

if __name__ == '__main__':
    check_network()
    ipaddr=get_ip_address()
    sendEmail('smtp.sina.com','your_email@sina.com','your_email_password','your_email@163.com',['targrt_email'],'IP Address Of Raspberry Pi',ipaddr)
```

把该脚本复制到/root/目录下，并chmod 777 /root/send_ip.py

    cp ./send_ip.py /root/send_ip.py
    chmod 777 /root/send_ip.py

修改开机启动文件/etc/rc.local，添加一行命令python /root/send_ip.py

注意：使用的邮箱必须已经开通smtp服务，推荐使用sina邮箱，因为sina邮箱不用授权码。

该脚本的依赖包，如果没有安装，请用pip自行安装。















