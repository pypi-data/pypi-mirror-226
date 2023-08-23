import requests
from datetime import datetime
from . import support as  sup
import pytz

class InstManagement:
    
    
    def __init__(self, R):
         self.base_url = R.url
         self.headers = sup.create_header(R.logon_token)
         self.Audit = Audit()
        
    
    from datetime import datetime

    def get_job_count(self):
        url = f"{self.base_url}/bionbi/job/"
        params = {}
        start_date = datetime.today()
        end_date = datetime.utcnow()  # Current time in UTC
    
        params['startDate'] = start_date.strftime("%m/%d/%Y 00:00:00")
        params['endDate'] = end_date.strftime("%m/%d/%Y %H:%M:%S")
    
        print("URL:", url)  # Debugging print statement
        print("Parameters:", params)  # Debugging print statement
    
        response = requests.get(url, headers=self.headers, params=params)
    
        print("Response Status Code:", response.status_code)  # Debugging print statement
        print("Response Content:", response.content)  # Debugging print statement
    
        return sup._handle_response(response)

       
    

class Audit :
    pass


class InstSupport:
    pass
    
