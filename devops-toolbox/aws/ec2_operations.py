__author__ = 'rakesh.varma'
import boto.ec2
from ConfigParser import SafeConfigParser
from node_operations import Node
import time

class ec2_operations:

    ec2 = None
    nodes = []

    def __init__(self, region, access_key_id, secret_access_key):
        self.ec2 = boto.ec2.connect_to_region(
                        region,
                        aws_access_key_id = access_key_id,
                        aws_secret_access_key = secret_access_key
        )
        self.__loadnodes()

    def __loadnodes(self):
        for instance in self.ec2.get_only_instances():
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

    def __getitem__(self, item):
        f = lambda node:node.name == item
        return filter(f, self.nodes)



    def create_instances(self, image_id, key_name, instance_type, security_group, instances):
        #create ec2 instances.
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
        return reservation

    def update_config(self, config, reservation):
        c = SafeConfigParser()
        c.add_section("main")
        hadoop_cfgfile = open(config, 'w')

        for instance in reservation.instances:
            d = {'private_ip_address':instance.private_ip_address, 'ip_address':instance.ip_address, 'dns_name':instance.dns_name}
            c.set("main",instance, str(d))
        c.write(hadoop_cfgfile)
        hadoop_cfgfile.close()
