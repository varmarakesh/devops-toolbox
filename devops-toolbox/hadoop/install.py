from fabric.api import *
class hadoop_install:

    mirror_site = 'https://fastdl.mongodb.org/linux'
    mongo_install_file = 'mongodb-linux-x86_64-3.0.11'

    def __init__(self, hadoop_cluster, host_user, host_key_file):
        self.hadoop_cluster = hadoop_cluster
        env.host_user = host_user
        env.key_filename = host_key_file

    def setup_hadoop_nodes_access(self):
        hosts = self.hadoop_cluster.all_hadoop_nodes
        for host in hosts:
            env.host_string = host.ip_address
            #Changing the host name of hadoop nodes to EC2 public dns name.
            cmd_change_hostname = 'hostname {0}'.format(hadoop_cluster.getNode(host).dns_name)
            sudo(cmd_change_hostname)
            #Changing /etc/hosts file to remove localhost and replacing it with the public dns name and 127.0.0.1 with localip.
            sudo('sed -i -e "s/localhost/{0}/" /etc/hosts'.format(hadoop_cluster.getNode(host).dns_name))
            sudo('sed -i -e "s/127.0.0.1/{0}/" /etc/hosts'.format(hadoop_cluster.getNode(host).private_ip_address))


        # Setting up passwordless login from hadoopnamenode to all other hadoop nodes.
        env.host_string = hadoop_cluster.getNode(c.hadoop_namenode).ip_address
        #generating ssh keys in id_rsa, no passphrase.
        run('ssh-keygen -t rsa -f /home/ubuntu/.ssh/id_rsa -q -N ""')
        #adding StrictHostKeyChecking no in the .ssh/config file so that ssh login is not prompted.
        run('echo "{0}" > /home/ubuntu/.ssh/config'.format("Host *"))
        run('echo "{0}" >> /home/ubuntu/.ssh/config'.format("   StrictHostKeyChecking no"))
        #Getting public key from hadoopnamenode
        public_key = sudo('cat /home/ubuntu/.ssh/id_rsa.pub')

        env.host_string = hadoop_cluster.getNode(c.saltmaster).ip_address

        #Issuing a minion blast of public key to all hadoop nodes to enable passwordless login.
        minion_cmd = "echo '{0}' >> /home/ubuntu/.ssh/authorized_keys".format(public_key)
        sudo('salt "*" cmd.run "{0}"'.format(minion_cmd))
        time.sleep(2)


