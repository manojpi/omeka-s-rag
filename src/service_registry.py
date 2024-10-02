import logging

from constant import app_name

class ServiceRegistry:

    def __init__(self):
        self.services = {}
    
    def register(self, name, service):
        self.services[name] = service
    
    def get(self, name):
        return self.services.get(name, None)

service_registry = ServiceRegistry()


logger = logging.getLogger(app_name)
service_registry.register('logger', logger)