import requests
from datetime import datetime
from . import support as  sup
import pytz

class InstManagement:
    
    
    def __init__(self, R):
         self.base_url = R.url
         self.headers = sup.create_header(R.logon_token)
         self.Audit = Audit()
        
    
    def get_job_count(self):
        url = f"{self.base_url}/bionbi/job/"
        params = {}
        
        # Get the current date and time in UTC
        start_date = datetime.now(pytz.utc)
        
        # Format the start_date in the required format
        params['startDate'] = start_date.strftime("%m/%d/%Y %H:%M:%S")
        
        response = requests.get(url, headers=self.headers, params=params)
    
        # Debugging lines to print the request URL and response content
        print("Request URL:", response.request.url)
        print("Response content:", response.content)
    
        return sup._handle_response(response)
       
    

class Audit :
    pass


class InstSupport:
    pass
    
