from aws_configuration import aws_config
from ec2_operations import ec2_operations
from fabric.api import *

@task
def create_hadoop_cluster():
    c = aws_config()
    instances = ['saltmaster', 'hadoopnamenode', 'hadoopsecondarynamenode', 'hadoopdatanode1', 'hadoopdatanode2']
    ec2 = ec2_operations(region = c.aws_region, access_key_id = c.aws_access_key_id, secret_access_key = c.aws_secret_access_key)
    ec2.create_instances(image_id = c.aws_image_id, key_name = c.aws_key_name, instance_type = c.aws_instance_type, security_group = c.aws_security_group, instances = instances)
    ec2.update_config(config = 'aws.hosts')

