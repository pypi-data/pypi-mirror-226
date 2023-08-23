
import requests
from . import support as  sup




class UserManagement:
    
    def __init__(self, R):
        self.base_url = R.url
        self.headers = sup.create_header(R.logon_token)
        self.Audit = Audit(R)

   
    def list_all_users(self):  # 1
        all_users, page_number, page_size = [], 1, 500
        while True:
            url = self.base_url + sup.LIST_USERS_ENDPOINT
            params = {'page': page_number, 'pagesize': page_size}
            response = requests.get(url, headers=self.headers, params=params)
            entries = sup._handle_response(response)
            all_users.extend(entries)
            if len(entries) < page_size:
                break
            page_number += 1
        return all_users


    def list_paginated_users(self, page_number, page_size): #2
        url = self.base_url + sup.LIST_USERS_ENDPOINT
        params = {'page': page_number, 'pagesize': page_size}
        response = requests.get(url, headers=self.headers, params=params)
        return sup._handle_response(response)

    def get_user_id(self, user_name): #3
       url = self.base_url + sup.LIST_USERS_ENDPOINT
       response = requests.get(url, headers=self.headers, params={'name': user_name})
       user_data = sup._handle_response(response)
       user_id = next((item['id'] for item in user_data if item.get('name') == user_name), None)
       if user_id is None:
           raise SystemExit(f"No such user {user_name} found in repositery")
       return user_id


    def create_user(self, **kwargs):#4
        kwargs = UserSupport._validate_user_data(**kwargs)
        user_data = UserSupport._construct_user_data(**kwargs)
        url = self.base_url + sup.CREATE_USER_ENDPOINT
        response = requests.post(url, headers=self.headers, data=user_data)
        return sup._handle_response(response)

    def modify_user_details(self, user_name, **kwargs):#5
        user_id = self.get_user_id(user_name)
        if user_id is None:
            raise Exception("User not found")
        user_data = UserSupport._construct_user_data(name = user_name , **kwargs)
        url = self.base_url + sup.USER_DETAILS_ENDPOINT.format(user_id=user_id)
        response = requests.put(url, headers=self.headers, data=user_data)
        return sup._handle_response(response)


    def reset_user_password(self, user_name, new_password):#6
        user_id = self.get_user_id(user_name)
        if user_id is None:
            raise Exception("User not found")
        user_data_xml = UserSupport._construct_user_data(user_name, new_password) # Calling UserSupport method
        url = self.base_url + sup.USER_DETAILS_ENDPOINT.format(user_id=user_id)
        response = requests.put(url, headers=self.headers, data=user_data_xml)
        return sup._handle_response(response)

    def delete_user(self, user_name):#7
        user_id = self.get_user_id(user_name)
        if user_id is None:
            raise Exception("User not found")
        url = self.base_url + sup.USER_DETAILS_ENDPOINT.format(user_id=user_id)
        response = requests.delete(url, headers=self.headers)
        return sup._handle_response(response)

    def deactivate_user(self, user_name, disable=True):  #Not Working
        user_id = self.get_user_id(user_name)
        if user_id is None:
            raise Exception("User not found")
        user_data = UserSupport._construct_user_data(name=user_name, disabled=disable)
        url = self.base_url + sup.USER_DETAILS_ENDPOINT.format(user_id=user_id)
        response = requests.put(url, headers=self.headers, data=user_data)
        return sup._handle_response(response)


class Audit:
    
    def __init__(self, R):
        self.base_url = R.url
        self.headers = sup.create_header(R.logon_token)
                  
    def get_inactive_users(self, days):
        
        from datetime import datetime, timedelta
        cutoff_date = datetime.today() - timedelta(days=days)
        
        query = f"""SELECT  {sup.user_id}, {sup.last_login}, {sup.created_at}, {sup.user_name},{sup.named_user}
                            {sup.fullname},{sup.user_groups}
                            
                    FROM {sup.system_db}
                    
                    WHERE   {sup.kind}='User'
                            and ({sup.last_login} IS NULL
                            or {sup.last_login} BETWEEN '1900-01-01' AND '{cutoff_date.strftime('%Y-%m-%d')}')
                            and {sup.created_at} BETWEEN '1900-01-01' AND '{cutoff_date.strftime('%Y-%m-%d')}'"""

        query_data = sup.generate_query_data(query)
        url = self.base_url + sup.CMS_QUERY     
        response = requests.post(url, headers=self.headers, data=query_data)    
        return sup._handle_response(response)

        
    def user_with_no_access():
        pass
       


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
    def _construct_user_data(user_name=None, password=None, **kwargs):
        if user_name:
            kwargs['name'] = user_name
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



   
    






