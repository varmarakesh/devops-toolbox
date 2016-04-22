import unittest
from ec2_operations import ec2_operations
from node_operations import *

class test(unittest.TestCase):

    def test_ec2_connection(self):
        ec2 = ec2_operations(region = 'us-west-2', access_key_id = '*****', secret_access_key = '******')
        self.assertIsNotNone(ec2.getInstance("ftpserver2"))

    def test_cluster(self):
        c = Cluster(config = 'aws.hosts')
        print type(c.getNode('testbox'))
        print type(c.nodes[0])
        self.assertEqual(c.getNode('testbox'), c.nodes[0])