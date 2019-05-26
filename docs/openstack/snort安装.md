# snort



## 安装步骤

[snort官网](https://www.snort.org/)

### 下载源码包

```
wget https://www.snort.org/downloads/snort/daq-2.0.6.tar.gz
                      
wget https://www.snort.org/downloads/snort/snort-2.9.13.tar.gz
```

### 安装daq

```
tar xvzf daq-2.0.6.tar.gz
                      
cd daq-2.0.6
./configure
make && sudo make install
```

### 安装snort

```
tar xvzf snort-2.9.13.tar.gz
                      
cd snort-2.9.13
./configure --enable-sourcefire
make && sudo make install
```

## 问题与解决方案

### 问题0

```
configure: error: no acceptable C compiler found in $PATH
```

### 解决0

```
# yum install gcc gcc-c++
```

### 问题1

```
ERROR! Libpcre header not found.
Get it from http://www.pcre.org
```

### 解决1

```
# yum install pcre-devel
```

### 问题2

```
ERROR! dnet header not found, go get it from
http://code.google.com/p/libdnet/ or use the --with-dnet-*
options, if you have it installed in an unusual place
```

### 解决2

```
# yum install libdnet-devel
```

### 问题3

```
ERROR! daq_static library not found, go get it from 
http://www.snort.org/.
```

### 解决3

https://pradyumnajoshi.wordpress.com/2014/03/25/compiling-snort-daq_static-library-not-found-error/

```
Prior to snort installation, I have compiled DAQ library and I was expecting that I can compile snort in the next few minutes. But, daq_static library gave me lot of headaches. Finally, the solution to this problem was found.
To get rid, check daq-modules-config is in your path.
 
# which daq-modules-config
which: no daq-modules-config in (/sbin:/bin:/usr/sbin:/usr/bin)
 
Then, include daq-modules-config in the path.
# export PATH=$PATH:/usr/local/bin
```

### 问题4

```
ERROR! zlib header not found.
```

### 解决4

```
# yum install zlib-devel
```

### 问题5

```
ERROR! LuaJIT library not found. Go get it from http://www.luajit.org/ (or)
Try compiling without openAppId using ‘–disable-open-appid’
configure: error: “Fatal!”
```

### 解决5

https://blog.csdn.net/rdgfdd/article/details/83420811

```
# ./configure --disable-open-appid
```

### 问题6

```
安装flex和bison
```

