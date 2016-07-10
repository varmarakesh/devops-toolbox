__author__ = 'rakesh.varma'
import boto.ec2
from ConfigParser import SafeConfigParser
from node_operations import Node
import time

class ec2_operations:

    ec2 = None
    nodes = []

    def __init__(self, access_key_id, secret_access_key, region = 'us-west-2'):
        self.ec2 = boto.ec2.connect_to_region(
                        region,
                        aws_access_key_id = access_key_id,
                        aws_secret_access_key = secret_access_key
        )
        self.__loadnodes()

    def __loadnodes(self):
        for instance in self.ec2.get_only_instances():
                if instance.state not in ['terminated', 'stopped']:
                    if 'Name' in instance.tags.keys():
                        name = instance.tags['Name']
                    else:
                        name = 'No Name'
                    self.nodes.append(Node(name = name, private_ip_address = instance.private_ip_address, ip_address = instance.ip_address, dns_name = instance.dns_name))

    def __str__(self):
        result = ""
        if self.ec2:
            for instance in self.ec2.get_only_instances():
                if 'Name' in instance.tags.keys():
                    name = instance.tags['Name']
                else:
                    name = 'No Name'
                result = result + "{0} => {1}\n".format(name, instance.state)
        return result

    def __repr__(self):
        return ''.join(str(node)+'\n' for node in self.nodes)

    def __getitem__(self, item):
        f = lambda node:node.name == item
        return filter(f, self.nodes)

    def get_instance(self, name):
        for instance in self.ec2.get_only_instances():
            if 'Name' in instance.tags.keys():
                if instance.tags['Name'] == name:
                    return instance

    def create_instances(self, security_group, instances, image_id = None, key_name = None, instance_type = None):
        #create ec2 instances.
        image_id = image_id if image_id is not None else 'ami-5189a661'
        key_name = key_name if key_name is not None else 'ec2'
        instance_type = instance_type if instance_type is not None else 't2.micro'
        reservation = self.ec2.run_instances(
                                                image_id = image_id,
                                                key_name = key_name,
                                                instance_type = instance_type,
                                                security_groups =[security_group],
                                                min_count = len(instances),
                                                max_count = len(instances)
        )

        time.sleep(10)
        #add tags to the created instances.
        for index, instance in enumerate(reservation.instances):
            instance.add_tag("Name", instances[index])
        self.__loadnodes()

    def delete_instance(self, name):
        self.ec2.terminate_instances(instance_ids = [self.get_instance(name).id])



    def update_config(self, config):
        c = SafeConfigParser()
        c.add_section("main")
        hadoop_cfgfile = open(config, 'w')

        for instance in self.nodes:
            d = {'private_ip_address':instance.private_ip_address, 'ip_address':instance.ip_address, 'dns_name':instance.dns_name}
            c.set("main",instance.name, str(d))
        c.write(hadoop_cfgfile)
        hadoop_cfgfile.close()
