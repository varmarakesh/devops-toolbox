import unittest
from ec2_operations import ec2_operations
from node_operations import *
from ConfigParser import SafeConfigParser

class test(unittest.TestCase):

    def setUp(self):
        self.config = SafeConfigParser()
        self.config.read("config.ini")
        self.region = self.config.get("main", "aws_region")
        self.access_key_id = self.config.get("main", "aws_access_key_id")
        self.secret_access_key = self.config.get("main", "aws_secret_access_key")


    def test_ec2_connection(self):
        ec2 = ec2_operations(region = self.region, access_key_id = self.access_key_id, secret_access_key = self.secret_access_key)
        self.assertIsNotNone(ec2["ftpserver2"])

    def test_cluster(self):
        c = Cluster(config = 'aws.hosts')
        self.assertEqual(c.getNode('testbox'), c.nodes[0])