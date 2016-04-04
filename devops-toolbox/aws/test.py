import unittest
from ec2_operations import ec2_operations

class test(unittest.TestCase):

    def test_ec2_connection(self):
        ec2 = ec2_operations(region = 'us-west-2', access_key_id = '*****', secret_access_key = '******')
        self.assertIsNotNone(ec2.getInstance("ftpserver2"))