from mongodb.install import mongodb_install
from hadoop.aws_hadoop_cluster import *
from salt.salt_operations import *
from aws.aws_configuration import aws_config
from fabric.api import *

@task
def mongo_install():
    m = mongodb_install(
        host_ip  = '*****',
        host_user = 'ubuntu',
        host_key_file = '/Users/rakesh.varma/.ssh/ec2.pem'
    )
    m.remove_mongo()
    m.install_mongodb()
    m.create_directories()
    m.create_mongod()

@task
def salt_install():
    cluster = hadoop_cluster()
    aws = aws_config('aws/config.ini')
    master = salt_master(host_ip = cluster.saltmaster.ip_address, host_key_file = aws.aws_key_location, host_user = aws.aws_user)
    master.install()

    minion = salt_minion(host_ip = cluster.namenode.ip_address, host_key_file = aws.aws_key_location, host_user = aws.aws_user)
    minion.install(master = cluster.saltmaster.ip_address, minion = cluster.namenode.ip_address)

    minion = salt_minion(host_ip = cluster.secondarynamenode.ip_address, host_key_file = aws.aws_key_location, host_user = aws.aws_user)
    minion.install(master = cluster.saltmaster.ip_address, minion = cluster.secondarynamenode.ip_address)

    for datanode in cluster.datanodes:
        minion = salt_minion(host_ip = datanode.ip_address, host_key_file = aws.aws_key_location, host_user = aws.aws_user)
        minion.install(master = cluster.saltmaster.ip_address, minion = datanode.ip_address)

    master = salt_master(host_ip = cluster.saltmaster.ip_address, host_key_file = aws.aws_key_location, host_user = aws.aws_user)
    master.keys_accept()
    master.ping()


