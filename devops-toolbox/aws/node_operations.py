__author__ = 'rakesh.varma'
from ConfigParser import SafeConfigParser
import os

class Node:
    name = None
    ip_address = None
    private_ip_address = None
    dns_name = None

    def __init__(self, name, ip_address, private_ip_address, dns_name):
        self.name = name
        self.ip_address = ip_address
        self.private_ip_address  = private_ip_address
        self.dns_name = dns_name

    def __repr__(self):
        return 'name: {0}, ip_address: {1}. private_ip_address: {2}, dns_name : {3}'.format(self.name, self.ip_address, self.private_ip_address, self.dns_name)

class Cluster:
    config = None
    nodes = []

    def __init__(self, config):
        self.config = config
        c = SafeConfigParser()
        c.read(config)

        for item in c.items("main"):
            name = item[0]
            private_ip_address = eval(item[1])['private_ip_address']
            ip_address = eval(item[1])['ip_address']
            dns_name = eval(item[1])['dns_name']
            node = Node(name = name, private_ip_address = private_ip_address, ip_address = ip_address, dns_name = dns_name)
            self.nodes.append(node)

    def getNode(self, name):
        node =  filter(lambda n:n.dns_name == name, self.nodes)
        if node:
            return node[0]
        else:
            return None



