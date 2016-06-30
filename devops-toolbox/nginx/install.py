__author__ = 'rakesh.varma'
from fabric.api import *
class nginx_install:


    def __init__(self, host_ip, host_user, host_key_file):
        env.host_string = host_ip
        env.user = host_user
        env.key_filename = host_key_file

    def install(self):
        sudo('apt-get update')
        sudo('apt-get install nginx')
        sudo('service nginx restart')