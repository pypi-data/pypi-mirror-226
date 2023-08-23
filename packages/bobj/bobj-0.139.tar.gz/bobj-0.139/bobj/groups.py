import requests
from .users import UserManagement
from . import support as  sup



class GroupManagement:

    def __init__(self, R):
        self.base_url = R.url
        self.headers = sup.create_header(R.logon_token)
        self.users = UserManagement(R)
        self.Audit = Audit()



    def list_all_user_groups(self): #1
        all_groups, page_number, page_size = [], 1, 100
        while True:
            url = self.base_url + sup.LIST_GROUPS_ENDPOINT
            print (url)
            params = {'page': page_number, 'pagesize': page_size}
            response = requests.get(url, headers=self.headers, params=params)
            group_data = sup._handle_response(response)
            all_groups.extend(group_data)
            if len(group_data) < page_size:
                break
            page_number += 1
        return all_groups

    def list_user_groups_paginated(self, page_number, page_size): #2
        url = self.base_url + sup.LIST_GROUPS_ENDPOINT
        params = {'page': page_number, 'pagesize': page_size}
        response = requests.get(url, headers=self.headers, params=params)
        return sup._handle_response(response)

    def get_group_id(self, group_name): #3
        url = self.base_url + sup.LIST_GROUPS_ENDPOINT
        response = requests.get(url, headers=self.headers, params={'name': group_name})
        user_group_data = sup._handle_response(response)
        group_id = user_group_data[0]['id'] if user_group_data else None
        if group_id is None :
            raise SystemExit(f"No such group named {group_name} found in repositery")
        return group_id

    def create_group(self, name, description=""): #4
        group_data = GroupSupport._construct_group_data(name=name, description=description)
        url = self.base_url + sup.CREATE_GROUP_ENDPOINT
        response = requests.post(url, headers=self.headers, data=group_data)
        return sup._handle_response(response)

    def get_group_details(self, name):#5
        url = self.base_url + sup.GROUP_DETAILS_ENDPOINT.format(group_id=self.get_group_id(name))
        response = requests.get(url, headers=self.headers)
        return sup._handle_response(response)

    def list_all_USERS_IN_GROUP(self, group_name): #6
        all_group_users, page_number, page_size = [], 1, 500
        while True:
            url = self.base_url + sup.USERS_IN_GROUP.format(group_id=self.get_group_id(group_name))
            params = {'page': page_number, 'pagesize': page_size}
            response = requests.get(url, headers=self.headers, params=params)
            users_data = sup._handle_response(response)
            all_group_users.extend(users_data)
            if len(users_data) < page_size:
                break
            page_number += 1
        return all_group_users

    def list_paginated_USERS_IN_GROUP(self, group_name, page_number, page_size):#7
        url = self.base_url + sup.USERS_IN_GROUP.format(group_id=self.get_group_id(group_name))
        params = {'page': page_number, 'pagesize': page_size}
        response = requests.get(url, headers=self.headers, params=params)
        return sup._handle_response(response)

    def add_users_to_group(self, group_name, user_name):
        user_id = self.users.get_user_id(user_name)
        url = self.base_url + sup.USERS_IN_GROUP.format(group_id=self.get_group_id(group_name))
        user_data = GroupSupport.create_xml_body("string", str(user_id))
        self.headers['Content-Type'] = 'application/xml'
        response = requests.put(url, headers=self.headers, data=user_data)
        return sup._handle_response(response)

    def remove_users_from_group(self, group_name, user_name):
        user_id = self.users.get_user_id(user_name)
        url = self.base_url + sup.USERS_IN_GROUP.format(group_id=self.get_group_id(group_name))
        user_data = GroupSupport.create_xml_body("string", str(user_id))
        response = requests.delete(url, headers=self.headers, data=user_data)
        return sup._handle_response(response)

    def list_user_groups_in_user_group(self, group_name):#10
        url = self.base_url + sup.LIST_SUBGROUPS_IN_GROUP_ENDPOINT.format(group_id=self.get_group_id(group_name))
        response = requests.get(url, headers=self.headers)
        return sup._handle_response(response)

    # def modify_user_group_details(self, group_name, description):
    #     url = self.base_url + sup.GROUP_DETAILS_ENDPOINT.format(group_id=self.get_group_id(group_name))
    #     attributes_data = ''.join(f'<attr name="{attr_name}" type="{attr_type}">{attr_value}</attr>' for attr_name, attr_type, attr_value in attributes)
    #     body = f'<entry xmlns="http://www.w3.org/2005/Atom"><content type="application/xml"><attrs xmlns="http://www.sap.com/rws/bip">{attributes_data}</attrs></content></entry>'
    #     response = requests.put(url, headers=self.headers, data=body)
    #     return sup._handle_response(response)

    def delete_group(self, group_name): #12
        url = self.base_url + sup.GROUP_DETAILS_ENDPOINT.format(group_id=self.get_group_id(group_name))
        response = requests.delete(url, headers=self.headers)
        return sup._handle_response(response)


class Audit :
    def group_with_no_user():
        pass

class GroupSupport:

    
    @staticmethod
    def create_xml_body(element_type, element_value):
        attr_element = f'<attr name="id" type="{element_type}">{element_value}</attr>'
        attrs_element = f'<attrs>{attr_element}</attrs>'
        content_element = f'<content type="application/xml">{attrs_element}</content>'
        entry_element = f'<entry>{content_element}</entry>'
        return f'<feed xmlns="http://www.w3.org/2005/Atom"><title type="text">usergroup</title>{entry_element}</feed>'

  
    @staticmethod
    def _construct_group_data(name=None, description=None, **kwargs):
        if name:
            kwargs['name'] = name
        if description:  # Fixed typo here
            kwargs['description'] = description
    
        # Convert boolean values to string
        for key, value in kwargs.items():
            if isinstance(value, bool):
                kwargs[key] = "true" if value else "false"
    
        # Create XML attributes from kwargs
        attrs = [f'<attr name="{key}" type="string">{value}</attr>' for key, value in kwargs.items()]
    
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

