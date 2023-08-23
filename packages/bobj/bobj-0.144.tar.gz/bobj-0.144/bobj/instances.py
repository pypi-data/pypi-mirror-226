import requests
from datetime import datetime
from . import support as  sup


class InstManagement:
    
    
    def __init__(self, R):
         self.base_url = R.url
         self.headers = sup.create_header(R.logon_token)
         self.Audit = Audit()
        
    
    

    from datetime import datetime

    def get_job_count(self, start_date=None, end_date=None):
        url = f"{self.base_url}/bionbi/job"
        params = {}
        
        # Default values
        start_date = start_date or datetime(2023, 8, 22)
        end_date = end_date or datetime(2900, 1, 1)
    
        # Formatting the dates
        params['startDate'] = start_date.strftime("%m/%d/%Y %H:%M:%S")
        params['endDate'] = end_date.strftime("%m/%d/%Y %H:%M:%S")
    
        # Making the GET request
        response = requests.get(url, headers=self.headers, params=params)
    
        print("URL:", url)
        print("Parameters:", params)
    
        return sup._handle_response(response)  # Assuming sup._handle_response is defined elsewhere

    

    def get_job_list(self, start_date=None, end_date=None, page=1, page_size=50):
        url = f"{self.base_url}/bionbi/job/list"
        params = {}
        
        # Default values for start and end dates
        start_date = start_date or datetime(2023, 8, 22)  # Default start date
        end_date = end_date or datetime(2900, 1, 1)  # Default end date
    
        # Formatting the dates
        params['startDate'] = start_date.strftime("%m/%d/%Y %H:%M:%S")
        params['endDate'] = end_date.strftime("%m/%d/%Y %H:%M:%S")
    
        # Optional parameters for pagination
        params['page'] = page
        params['pageSize'] = page_size
        
        # Making the GET request
        response = requests.get(url, headers=self.headers, params=params)
    
        # Debugging information
        print("URL:", url)
        print("Parameters:", params)
    
        return sup._handle_response(response)  # Assuming sup._handle_response is defined elsewhere




       
    

class Audit :
    pass


class InstSupport:
    pass
    
