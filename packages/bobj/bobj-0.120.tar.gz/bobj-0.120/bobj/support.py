def _handle_response(response):
     print ("0-----------------------")
     print (response.text)
     status_code = response.status_code
     response_data = response.json()        
     if status_code not in [200, 201]:
         raise SystemExit(f"{response_data['message']}")    
     # Extract entries if available
     entries = response_data.get('entries', [])
     
     return entries


def create_header(logon_token):
     header = {
                 'Content-Type': 'application/xml',
                 'Accept': 'application/json',
                 'X-SAP-LogonToken': logon_token,
             }
     return header