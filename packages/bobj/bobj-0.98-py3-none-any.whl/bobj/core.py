
import requests
from .users import UserManagement
from .groups import GroupManagement

from . import login, users, folders, groups, instances, publications



class validate:
    def __init__(self, url, **kwargs):
        self._session = requests.Session()
        
        self.login = login._bovalidation(url, **kwargs)
        self.users = UserManagement(self.login) # Directly instantiate UserManagement
        self.groups = GroupManagement(self.login) # Directly instantiate GroupManagement



        
