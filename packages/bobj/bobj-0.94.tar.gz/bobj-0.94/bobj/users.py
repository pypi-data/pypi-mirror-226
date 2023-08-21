
import requests
from datetime import datetime, timedelta


# Endpoints for user management
LIST_USERS_ENDPOINT = "/v1/users"  # Get a list of users
CREATE_USER_ENDPOINT = "/v1/users/user"  # Create a new user
USER_DETAILS_ENDPOINT = "/v1/users/{user_id}"  # Get, modify or delete user details by user_id

class UserManagement:
    
    def __init__(self, R):
        self.base_url = R.url
        self.headers = UserSupport.create_header(R.logon_token)
   
    def list_all_users(self):  # 1
        all_users, page_number, page_size = [], 1, 500
        while True:
            url = self.base_url + LIST_USERS_ENDPOINT
            params = {'page': page_number, 'pagesize': page_size}
            response = requests.get(url, headers=self.headers, params=params)
            entries = UserSupport._handle_response(response)
            all_users.extend(entries)
            if len(entries) < page_size:
                break
            page_number += 1
        return all_users


    def list_paginated_users(self, page_number, page_size): #2
        url = self.base_url + LIST_USERS_ENDPOINT
        params = {'page': page_number, 'pagesize': page_size}
        response = requests.get(url, headers=self.headers, params=params)
        return UserSupport._handle_response(response)

    def get_user_id(self, name): #3
        url = self.base_url + LIST_USERS_ENDPOINT
        params = {'name': name}
        response = requests.get(url, headers=self.headers, params=params)
        user_data = UserSupport._handle_response(response)
        print (user_data)
        print ("feel free to delete this print statement and above")
        return user_data[0]['id'] if user_data else None

    def create_user(self, **kwargs):#4
        kwargs = UserSupport._validate_user_data(**kwargs)
        user_data = UserSupport._construct_user_data(**kwargs)
        url = self.base_url + CREATE_USER_ENDPOINT
        response = requests.post(url, headers=self.headers, data=user_data)
        return UserSupport._handle_response(response)

    def modify_user_details(self, name, **kwargs):#5
        user_id = self.get_user_id(name)
        if user_id is None:
            raise Exception("User not found")
        user_data = UserSupport._construct_user_data(name = name , **kwargs)
        url = self.base_url + USER_DETAILS_ENDPOINT.format(user_id=user_id)
        response = requests.put(url, headers=self.headers, data=user_data)
        return UserSupport._handle_response(response)


    def reset_user_password(self, name, new_password):#6
        user_id = self.get_user_id(name)
        if user_id is None:
            raise Exception("User not found")
        user_data_xml = UserSupport._construct_user_data(name, new_password) # Calling UserSupport method
        url = self.base_url + USER_DETAILS_ENDPOINT.format(user_id=user_id)
        response = requests.put(url, headers=self.headers, data=user_data_xml)
        return UserSupport._handle_response(response)

    def delete_user(self, name):#7
        user_id = self.get_user_id(name)
        if user_id is None:
            raise Exception("User not found")
        url = self.base_url + USER_DETAILS_ENDPOINT.format(user_id=user_id)
        response = requests.delete(url, headers=self.headers)
        return UserSupport._handle_response(response)

    def deactivate_user(self, name, disable=True):  # Added disable parameter
        user_id = self.get_user_id(name)
        if user_id is None:
            raise Exception("User not found")
        user_data = UserSupport._construct_user_data(name=name, disabled=disable)
        url = self.base_url + USER_DETAILS_ENDPOINT.format(user_id=user_id)
        response = requests.put(url, headers=self.headers, data=user_data)
    
        # Print debugging information
        print("Response Text:", response.text)

    
    
        return UserSupport._handle_response(response)

    def find_inactive_users_by_days(self, days):#9
        days_ago = datetime.now() - timedelta(days=days)
        days_ago = days_ago.isoformat() + "Z"
        url = self.base_url + LIST_USERS_ENDPOINT       
        params = {'updated': f'{days_ago},'}  # Note the removal of the comma inside the string
        response = requests.get(url, headers=self.headers, params=params)
        return UserSupport._handle_response(response)
    




class UserSupport:
    
    @staticmethod
    def _validate_user_data(**kwargs):
        mandatory_fields = ["password", "name"]
        missing_fields = [field for field in mandatory_fields if field not in kwargs]
        if missing_fields:
            raise ValueError(f"Missing mandatory fields: {', '.join(missing_fields)}")
        kwargs.setdefault("forcepasswordchange", True)
        kwargs.setdefault("nameduser", False)
        kwargs.setdefault("passwordexpire", True)
        for key, value in kwargs.items():
            if isinstance(value, bool):
                kwargs[key] = "true" if value else "false"
        return kwargs
    
    @staticmethod
    def _construct_user_data(name=None, password=None, **kwargs):
        if name:
            kwargs['name'] = name
        if password:
            kwargs['password'] = password
    
        # Convert boolean values to string
        for key, value in kwargs.items():
            if isinstance(value, bool):
                kwargs[key] = "true" if value else "false"
                
        # Define the keys that should be of type "bool"
        bool_keys = ["forcepasswordchange", "nameduser", "passwordexpire", "disabled"]
        
        # If 'name' is in kwargs, handle it first
        attrs = []
        if 'name' in kwargs:
            attrs.append('<attr name="name" type="string">{}</attr>'.format(kwargs['name']))
            del kwargs['name'] # Remove it so it doesn't get processed again
    
        # Handle the remaining attributes
        for key, value in kwargs.items():
            attr_type = "bool" if key in bool_keys else "string"
            attrs.append('<attr name="{key}" type="{attr_type}">{value}</attr>'.format(key=key, attr_type=attr_type, value=value))
        
        # Combine attrs and create the final XML with the specific xmlns attributes
        user_data_xml = (
            '<entry xmlns="http://www.w3.org/2005/Atom">'
            '<content type="application/xml">'
            '<attrs>'
            '{attrs}'
            '</attrs>'
            '</content></entry>'.format(attrs='\n'.join(attrs))
        )
        return user_data_xml



    @staticmethod
    def _handle_response(response):
        status_code = response.status_code
        response_data = response.json()        
        if status_code not in [200, 201]:
            raise SystemExit(f"{response_data['message']}")    
        # Extract entries if available
        entries = response_data.get('entries', [])
        
        return entries


    @staticmethod
    def create_header(logon_token):
        header = {
                    'Content-Type': 'application/xml',
                    'Accept': 'application/json',
                    'X-SAP-LogonToken': logon_token,
                }
        return header
    






