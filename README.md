# library
这是一个开源的网页网盘项目，编程语言是python3，扩展库是flask

使用方法:

windows:

双击运行目录下的install_lib.bat,
双击accounts.json，用记事本打开，
把账号，密码，可以使用的储存空间以以下的方式输入:

账号:["密码","储存空间"]

并且要符合json规范

运行start.py,如果没出错，就可以在浏览器上访问  本机ip:5000了

linux/unix:

cd到根目录下,
使用命令sudo chmod +X install_lib.sh,
使用命令./install_lib.sh
用vim或nano打开accounts.json
把账号，密码，可以使用的储存空间以以下的方式输入:

账号:["密码","储存空间"]

并且要符合json规范

运行start.py,如果没出错，就可以在浏览器上访问  本机ip:5000了


v1.0 最初的版本，加入：下载，上传文件，登录，退出登录，新建文件夹，删除，预览，上一级
