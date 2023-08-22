import requests
from datetime import datetime

class InstManagement:
    
    
    def __init__(self, R):
         self.base_url = R.url
         self.headers = InstSupport.create_header(R.logon_token)
         self.Audit = Audit()
        
    
    def get_job_count(self):
        url = f"{self.base_url}/bionbi/job/"
        params = {}
        start_date = datetime.today()
        params['startDate'] = start_date.strftime("%m/%d/%Y 00:00:00")
        response = requests.get(url, params=params)
        
        return InstSupport._handle_response(response)
   
    

class Audit :
    pass


class InstSupport:
    
    @staticmethod
    def _handle_response(response):
        print(response.content)

        status_code = response.status_code
        response_data = response.json()
        print ("-----------------")
        print (response_data)
        
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
    
