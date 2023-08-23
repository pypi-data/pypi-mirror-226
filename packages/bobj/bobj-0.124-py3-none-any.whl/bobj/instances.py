import requests
from datetime import datetime
from . import support as  sup


class InstManagement:
    
    
    def __init__(self, R):
         self.base_url = R.url
         self.headers = sup.create_header(R.logon_token)
         self.Audit = Audit()
        
    
    

    def get_job_count(self):
        url = f"{self.base_url}/bionbi/job"
        params = {}
        start_date = datetime(1900, 1, 1)  # Default start date
        end_date = datetime.utcnow()  # Using current UTC time
    
        # Formatting the dates
        params['startDate'] = start_date.strftime("%m/%d/%Y %H:%M:%S")
        params['endDate'] = end_date.strftime("%m/%d/%Y %H:%M:%S")
    
        # Making the GET request
        response = requests.get(url, headers=self.headers, params=params)
        
        print("URL:", url)
        print("Parameters:", params)
        
        return sup._handle_response(response)
    
    def get_job_list(self, start_date=None, end_date=None, page=1, page_size=5, filter_vals=None):
        url = f"{self.base_url}/bionbi/job/list"
        params = {}
    
        # If start_date and end_date are provided, format them in the required format
        
        start_date = datetime(1900, 1, 1)  # Default start date
        end_date = datetime(2099, 1, 1)  # Using current UTC time
        
        if start_date:
            params['startDate'] = start_date.strftime("%m/%d/%Y %H:%M:%S")
        if end_date:
            params['endDate'] = end_date.strftime("%m/%d/%Y %H:%M:%S")
    
        # Optional parameters for pagination and filtering
        if page:
            params['page'] = page
        if page_size:
            params['pageSize'] = page_size
        if filter_vals:
            params['filterVals'] = ','.join(filter_vals)
    
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
    
