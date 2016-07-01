from fabric.api import *
from fabric.api import env, put, run, sudo, task, cd, settings, prefix, shell_env
from fabric.contrib.files import exists
import time
from mongodb.install import mongodb_install
from aws.ec2_operations import *

@task
def aws_keys(access_key, secret_key):
    env.access_key = access_key
    env.secret_key = secret_key

@task
def test():
    ec2 = ec2_operations(access_key_id = env.access_key, secret_access_key = env.secret_key)
    print ec2

@task
def create_instance(name, security_group):
    ec2 = ec2_operations(access_key_id = env.access_key, secret_access_key = env.secret_key)
    ec2.create_instances(security_group = security_group, instances = [name])
