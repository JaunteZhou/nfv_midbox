# Openstack使用官方ubuntu和Centos镜像无法使用ssh用户名密码登录登录的问题

关于使用官方ubuntu镜像无法使用ssh用户名密码登录登录的问题
在创建instance的时候，选择创建后，然后选择直接输入，输入如下代码

## ubuntu

```
!/bin/sh  
sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/g' /etc/ssh/sshd_config  
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config  
cp -f /home/ubuntu/.ssh/authorized_keys /root/.ssh/  
service ssh restart  
passwd ubuntu<<EOF  
123456
123456
EOF 
```



## Centos7

```
!/bin/sh  
sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/g' /etc/ssh/sshd_config  
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config  
cp -f /home/centos/.ssh/authorized_keys /root/.ssh/  
service sshd restart  
passwd centos<<EOF  
123456
123456
EOF 
```

