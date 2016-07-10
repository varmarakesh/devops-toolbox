from fabric.api import *
from fabric.api import env, put, run, sudo, task, cd, settings, prefix, shell_env
from fabric.contrib.files import exists
import time
from aws.ec2_operations import *
from aws.s3_operations import *


@task
def keys(access_key, secret_key):
    """
    fab aws_ops.keys:access_key='*****',secret_key='******'
    """
    env.access_key = access_key
    env.secret_key = secret_key

@task
def list():
    """
    Lists the current aws instances.fab aws_ops.list
    """
    ec2 = ec2_operations(access_key_id = env.access_key, secret_access_key = env.secret_key)
    print ec2

@task
def detailed_list():
    ec2 = ec2_operations(access_key_id = env.access_key, secret_access_key = env.secret_key)
    print repr(ec2)

@task
def create_ubuntu_instance(name, security_group):
    ec2 = ec2_operations(access_key_id = env.access_key, secret_access_key = env.secret_key)
    ec2.create_instances(security_group = security_group, instances = [name])

@task
def create_instance(name, imageid, security_group):
    """
    fab aws_ops.create_instance:name='ftpserver',imageid='ami-775e4f16',security_group='HadoopEC2SecurityGroup'
    Create ec2 instance with the specified imageid.
    RHEL 7.2 = ami-775e4f16
    Ubuntu 14.1 = ami-9abea4fb
    """
    ec2 = ec2_operations(access_key_id = env.access_key, secret_access_key = env.secret_key)
    ec2.create_instances(security_group = security_group, image_id = imageid, instances = [name])

@task
def delete_instance(name):
    """
    fab aws_ops.delete_instance:name='ftpserver'
    """
    ec2 = ec2_operations(access_key_id = env.access_key, secret_access_key = env.secret_key)
    ec2.delete_instance(name)

@task
def list_buckets():
    """
    fab aws_ops.list_buckets
    """
    s3 = s3_operations(access_key_id = env.access_key, secret_access_key = env.secret_key)
    print s3