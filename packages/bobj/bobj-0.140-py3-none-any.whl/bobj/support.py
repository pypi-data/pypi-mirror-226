

# Endpoints for user management
LIST_USERS_ENDPOINT = "/v1/users"  # Get a list of users
CREATE_USER_ENDPOINT = "/v1/users/user"  # Create a new user
USER_DETAILS_ENDPOINT = "/v1/users/{user_id}"  # Get, modify or delete user details by user_id


LIST_GROUPS_ENDPOINT = "/v1/usergroups"
CREATE_GROUP_ENDPOINT = "/v1/usergroups/usergroup"
GROUP_DETAILS_ENDPOINT = "/v1/usergroups/{group_id}"
USERS_IN_GROUP = "/v1/usergroups/{group_id}/users"
LIST_SUBGROUPS_IN_GROUP_ENDPOINT = "/v1/usergroups/{group_id}/usergroups"


CMS_QUERY = "/v1/cmsquery?pagesize=99999" 


def _handle_response(response):
    # print ("0-----------------------")
    # print (response.text)
    status_code = response.status_code
    response_data = response.json()        
    if status_code not in [200, 201]:
        raise SystemExit(f"{response_data['message']}")    
    # Extract entries if available
    entries = response_data.get('entries', [])
    if entries is not None:
        return entries
     
    metadata = response_data.get('__metadata')
    if metadata is not None:
        metadata.pop('uri', None)
        return metadata
    
    feed = response_data.get('feed', [])
    if feed is not None:
       return feed
    
    return response.text

def create_header(logon_token):
     header = {
                 'Content-Type': 'application/xml',
                 'Accept': 'application/json',
                 'X-SAP-LogonToken': logon_token,
             }
     return header
 
    

def generate_query_data(query):
    return f'<attrs><attr name="query" type="string">{query}</attr></attrs>'

    
 
user_id = "SI_ID"
user_name = "SI_NAME"
fullname = "SI_USERFULLNAME"

user_groups = "SI_USERGROUPS"


kind = "SI_KIND"
named_user = "SI_NAMEDUSER"

last_login = "SI_LASTLOGONTIME"
created_at = "SI_CREATION_TIME"

system_db = "CI_SYSTEMOBJECTS"
