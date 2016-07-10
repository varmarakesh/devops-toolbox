from fabric.api import *
from fabric.api import env, put, run, sudo, task, cd, settings, prefix, shell_env
from fabric.contrib.files import exists
import time
from ftp.install import *

@task
def env(host,user,key_file):
    """
    fab ftp_ops.env:host='*****',user='**',key_file='******'
    """
    env.ftp = install(host_ip = host, host_user = user, host_key_file = key_file)

@task
def test():
    sudo('hostname')

@task
def setup_s3fs(user, pwd):
    #env.ftp.create_user(user = user, pwd = pwd)
    env.ftp.install_s3fs()
    #env.ftp.install_ftp(user = user)