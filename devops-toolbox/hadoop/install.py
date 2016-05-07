from fabric.api import *
class hadoop_install:

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
