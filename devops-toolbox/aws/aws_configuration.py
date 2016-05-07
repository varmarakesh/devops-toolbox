from ConfigParser import SafeConfigParser

class aws_config:
    def __init__(self, config):
        self.config = SafeConfigParser()
        self.config.read(config)

    @property
    def aws_key_location(self):
        return self.config.get("main", "aws_key_location")

    @property
    def aws_region(self):
        return self.config.get("main", "aws_region")

    @property
    def aws_access_key_id(self):
        return self.config.get("main", "aws_access_key_id")

    @property
    def aws_secret_access_key(self):
        return self.config.get("main", "aws_secret_access_key")

    @property
    def aws_image_id(self):
        return self.config.get("main", "aws_image_id")

    @property
    def aws_key_name(self):
        return self.config.get("main", "aws_key_name")

    @property
    def aws_instance_type(self):
        return self.config.get("main", "aws_instance_type")

    @property
    def aws_security_group(self):
        return self.config.get("main", "aws_security_group")

    @property
    def aws_user(self):
        return self.config.get("main", "aws_user")
