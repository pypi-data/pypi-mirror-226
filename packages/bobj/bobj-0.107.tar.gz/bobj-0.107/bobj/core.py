
import requests

from .login import bovalidation
from .users import UserManagement
from .groups import GroupManagement
from .instances import InstManagement

from . import folders, publications



class validate:
    def __init__(self, url, **kwargs):
        self._session = requests.Session()
        
        self.login = bovalidation(url, **kwargs)
        self.users = UserManagement(self.login) # Directly instantiate UserManagement
        self.groups = GroupManagement(self.login) # Directly instantiate GroupManagement
        self.instances = InstManagement(self.login) # Directly instantiate InstanceManagement



        
