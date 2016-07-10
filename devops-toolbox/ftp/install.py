__author__ = 'rakesh.varma'
from fabric.api import *
import os
import time
class install:

    fuse_git_repo = 'https://github.com/s3fs-fuse/s3fs-fuse.git'

    def __init__(self, host_ip, host_user, host_key_file):
        env.host_string = host_ip
        env.user = host_user
        env.key_filename = host_key_file

    def install_s3fs(self):
        print env.host_string
        print env.user
        print env.key_filename
        sudo('yum install automake fuse-devel gcc-c++ git libcurl-devel libxml2-devel make openssl-devel')
        sudo('git clone {0}'.format(self.fuse_git_repo))
        sudo('./home/ec2-user/s3fs-fuse/autogen.sh; ./home/ec2-user/s3fs-fuse/configure')
        sudo('/bin/make /home/ec2-user')
        sudo('make install')

    def mount(self, access_key, secret_key):
        sudo('touch /etc/passwd-s3fs && chmod 640 /etc/passwd-s3fs && echo "{0}:{1}" > /etc/passwd-s3fs'.format(access_key, secret_key))
        sudo('/opt/bin/s3fs vcs-payment /home/vcsuser -o allow_other -o nonempty')
        sudo('mount|grep s3fs')

    def create_user(self, user, pwd):
        print env.host_string
        print env.user
        print env.key_filename
        sudo('hostname')
        sudo('useradd -d /home/{0} {1}'.format(user, user))
        sudo('echo -e "{0}\n{1}" | passwd {2}'.format(pwd, pwd, user))
        sudo('chown -R {0} /home/{1}'.format(user, user))

    def install_ftp(self, user):
        sudo('yum install -y vsftpd')
        sudo('chkconfig vsftpd on')
        sudo('setsebool -P ftp_home_dir=1')
        sudo('echo "{0}" > /etc/vsftpd/chroot_list'.format(user))
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        f = open(os.path.join(__location__, 'vsftpd.conf'))
        vsftpd_config = f.read()
        sudo('echo "{0}" > /etc/vsftpd/vsftpd.conf'.format(vsftpd_config))
        sudo('service vsftpd restart')