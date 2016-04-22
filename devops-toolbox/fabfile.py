from mongodb.install import mongodb_install
from fabric.api import *

@task
def mongo_install():
     #Install Salt Master
    m = mongodb_install(
        host_ip  = '52.38.248.53',
        host_user = 'ubuntu',
        host_key_file = '/Users/rakesh.varma/.ssh/ec2.pem'
    )
    m.remove_mongo()
    m.install_mongodb()
    m.create_directories()
    m.create_mongod()
