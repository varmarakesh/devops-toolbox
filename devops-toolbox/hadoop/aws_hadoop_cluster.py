#import os
#parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#os.sys.path.insert(0,parentdir)

from aws.node_operations import *

class hadoop_cluster:

    cluster = None

    def __init__(self):
        self.cluster = Cluster('aws/aws.hosts')

    @property
    def namenode(self):
        return self.cluster['hadoopnamenode']

    @property
    def secondarynamenode(self):
        return self.cluster['hadoopsecondarynamenode']

    @property
    def datanodes(self):
        return [node for node in self.cluster.nodes if 'data' in node.name]

    @property
    def saltmaster(self):
        return self.cluster['saltmaster']

    @property
    def all_hadoop_nodes(self):
        nodes = [self.namenode, self.secondarynamenode]
        nodes.extend(self.datanodes)
        return nodes

    def __str__(self):
        return ''.join(str(node)+'\n' for node in self.all_hadoop_nodes)



