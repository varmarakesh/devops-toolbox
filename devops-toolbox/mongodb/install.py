__author__ = 'rakesh.varma'
from fabric.api import *
class mongodb_install:

    mirror_site = 'https://fastdl.mongodb.org/linux'
    mongo_install_file = 'mongodb-linux-x86_64-3.0.11'

    def __init__(self, host_ip, host_user, host_key_file):
        env.host_string = host_ip
        env.user = host_user
        env.key_filename = host_key_file

    def install_mongodb(self):
        run('curl -O {0}/{1}.tgz'.format(self.mirror_site, self.mongo_install_file))
        run('tar -zxvf {0}.tgz'.format(self.mongo_install_file))
        run('mv {0}/ mongodb/'.format(self.mongo_install_file))
        cmd = "echo '{0}' >> /home/ubuntu/.bashrc".format("export MONGO_HOME=/home/ubuntu/mongodb")
        run(cmd)
        cmd = "echo '{0}' >> /home/ubuntu/.bashrc".format("export PATH=$PATH:$MONGO_HOME/bin")
        run(cmd)

    def create_directories(self):
        #create data directories
        run('mkdir -p /home/ubuntu/data/db')
        #create log directory
        run('mkdir -p /var/log/mongodb/')

    def create_mongod(self):
        config_file_text = "fork = true \n bind_ip = 0.0.0.0 \n port = 30000 \n quiet = true \n dbpath = /home/ubuntu/data/db \n logpath = /var/log/mongodb/mongod.log \n logappend = true \n journal = true"
        sudo("echo '{0}' > /etc/mongodb.conf".format(config_file_text))
        sudo("/home/ubuntu/mongodb/bin/mongod --config /etc/mongodb.conf")

    def remove_mongo(self):
        #Remove any mongo_home from the bashrc file.
        run('sed {0} ~/.bashrc'.format('/MONGO_HOME/d'))
        #Kill the mongod process
        with settings(warn_only = True):
            sudo('killall mongod')

        run('rm -rf /home/ubuntu/mongodb')
        run('rm -rf /home/data')
        sudo('rm -rf /etc/mongodb.conf')

    def run_remote_command(self, cmd):
        output = sudo(cmd)
        return str(output)





