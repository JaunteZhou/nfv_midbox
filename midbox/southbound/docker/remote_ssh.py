#!/usr/bin/python
# -*- coding: utf-8 -*-
#remote_ssh.py

import pexpect
def remote_ssh(ip,password,cmd,username='root'):
    ssh=pexpect.spawn('ssh '+username+'@'+ip+' '+cmd)
    try:
        i=ssh.expect(['password:','yes/no'],timeout=5)
        if i==0:
            ssh.sendline(password)
        elif i==1:
            ssh.sendline('yes')
            ssh.expect('password:',timeout=5)
            ssh.sendline(password)
    except pexpect.EOF:
        print("EOF")
    except pexpect.TIMEOUT:
        print("TIMEOUT")
    exitcode=ssh.exitstatus
    r=ssh.read().decode()
    ssh.close()
    return exitcode, r