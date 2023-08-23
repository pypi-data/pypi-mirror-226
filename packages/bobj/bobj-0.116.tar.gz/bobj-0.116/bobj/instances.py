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
        start_date = datetime(1900, 1, 1)  # Default start date
        end_date = datetime.utcnow()  # Using current UTC time
    
        # Formatting the dates
        params['startDate'] = start_date.strftime("%m/%d/%Y %H:%M:%S")
        params['endDate'] = end_date.strftime("%m/%d/%Y %H:%M:%S")
    
        # Making the GET request
        response = requests.get(url, headers=self.headers, params=params)
        
        # Debugging information
        print("URL:", url)
        print("Parameters:", params)
        
        return sup._handle_response(response)


       
    

class Audit :
    pass


class InstSupport:
    pass
    
