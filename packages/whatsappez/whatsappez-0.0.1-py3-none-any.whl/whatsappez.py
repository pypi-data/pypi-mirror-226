import base64
import json
import requests

class WhatsApp:
    def __init__(self, ip, base64_authentic,password):
        self.ip = ip
        self.base64_authentic = base64_authentic
        self.user = self.User(self.ip, self.base64_authentic)
        self.jwt_token = self.user.adminLogin(password)  # Call adminLogin on the user instance
        self.message = self.Message(self.ip, self.jwt_token)

    class Message:
        def __init__(self, ip, jwt_token):
            self.ip = ip
            self.jwt_token = jwt_token

        def send(self, payload):
            try:
                url = self.ip + "/v1/messages"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.post(url, headers=headers, json=payload, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in sending text message")
                return str(e)

        def read(self, message_id):
            try:
                url = f"{self.ip}/v1/messages/{message_id}"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                payload = {
                    "status": "read"
                }
                response = requests.put(url, headers=headers, json=payload, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in marking message as read")
                return str(e)

    class User:
        def __init__(self, ip, base64_authentic):
            self.ip = ip
            self.base64_authentic = base64_authentic

        def adminLogin(self, password):
            try:
                url = self.ip + "/v1/users/login"
                payload = {"new_password": password}
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic ' + self.base64_authentic
                }
                response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
                rs = response.text
                json_data = json.loads(rs)
                self.jwt_token = json_data["users"][0]["token"]
                return self.jwt_token
            except Exception as e:
                print("Error:", e)
                print("Error in updating authkey")
                return str(e)
        
        def userLogin(self, username, password):
            try:
                url = self.ip + "/v1/users/login"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic ' + base64.b64encode((username + password).encode()).decode()
                }
                response = requests.post(url, headers=headers, data=json.dumps({}), verify=False)
                rs = response.text
                json_data = json.loads(rs)
                self.jwt_token = json_data["users"][0]["token"]
                return self.jwt_token
            except Exception as e:
                print("Error:", e)
                print("Error in user login")
                return str(e)
            
        def createUser(self, username, password):
            try:
                url = self.ip + "/v1/users"
                payload = {
                    "username": username,
                    "password": password
                }
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.post(url, headers=headers, json=payload, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in creating user")
                return str(e)
            
        def getAdmin(self, admin_username):
            try:
                url = self.ip + f"/v1/users/{admin_username}"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.get(url, headers=headers, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in getting admin details")
                return str(e)
        
        def getUser(self, username):
            try:
                url = self.ip + f"/v1/users/{username}"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.get(url, headers=headers, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in getting user details")
                return str(e)
        

        def updateUser(self, new_password):
            try:
                url = self.ip + "/v1/users/admin"
                payload = {
                    "password": new_password
                }
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.put(url, headers=headers, json=payload, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in updating user details")
                return str(e)
        

        def deleteUser(self, username):
            try:
                url = self.ip + f"/v1/users/{username}"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.delete(url, headers=headers, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in deleting user")
                return str(e)
 
        def logoutUser(self):
            try:
                url = self.ip + "/v1/users/logout"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.post(url, headers=headers, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in logging out user")
                return str(e)
            

    class Settings:
        def __init__(self, ip, jwt_token):
            self.ip = ip
            self.jwt_token = jwt_token

        def getSettings(self):
            try:
                url = self.ip + "/v1/settings/application"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.get(url, headers=headers, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in getting settings")
                return str(e)

        def getShards(self):
            try:
                url = self.ip + "/v1/account/shards"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.get(url, headers=headers, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in getting shards")
                return str(e)

        
        def setShards(self, country_code, phone_number, shards, two_step_pin):
            try:
                url = self.ip + "/v1/account/shards"
                payload = {
                    "cc": country_code,
                    "phone_number": phone_number,
                    "shards": shards,
                    "pin": two_step_pin
                }
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.post(url, headers=headers, json=payload, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in setting shards")
                return str(e)


        def updateWebhook(self, webhook_url):
            try:
                url = self.ip + "/v1/settings/application"
                payload = {
                    "webhooks": {
                        "url": webhook_url
                    }
                }
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.patch(url, headers=headers, json=payload, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in updating webhook")
                return str(e)
            
        def updateSettings(self, settings_payload):
            try:
                url = self.ip + "/v1/settings/application"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.patch(url, headers=headers, json=settings_payload, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in updating settings")
                return str(e)
            
        def getMediaProvider(self):
            try:
                url = f"{self.ip}/v1/settings/application/media/providers"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.get(url, headers=headers, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in getting media providers")
                return str(e)
            
        def deleteAppSettings(self):
            try:
                url = f"{self.ip}/v1/settings/application"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.delete(url, headers=headers, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in deleting application settings")
                return str(e)
        

        def deleteMediaProvider(self, provider_name):
            try:
                url = f"{self.ip}/v1/settings/application/media/providers/{provider_name}"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.delete(url, headers=headers, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in deleting media provider")
                return str(e)
            

        def updateMediaProvider(self, provider_name, new_config):
            try:
                url = f"{self.ip}/v1/settings/application/media/providers"
                payload = [
                    {
                        "name": provider_name,
                        "type": "www",
                        "config": new_config
                    }
                ]
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.post(url, headers=headers, json=payload, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in updating media provider")
                return str(e)

        def backupSettings(self, backup_password):
            try:
                url = f"{self.ip}/v1/settings/backup"
                payload = {
                    "password": backup_password
                }
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.post(url, headers=headers, json=payload, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in initiating backup")
                return str(e)
            
        
        def restoreSettings(self, restore_password, restore_data):
            try:
                url = f"{self.ip}/v1/settings/restore"
                payload = {
                    "password": restore_password,
                    "data": restore_data
                }
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.post(url, headers=headers, json=payload, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in restoring settings")
                return str(e)
            
        def getProfile(self):
            try:
                url = f"{self.ip}/v1/settings/business/profile"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.get(url, headers=headers, verify=False)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in getting business profile")
                return str(e)
            
        def setProfile(self, profile_data):
            try:
                url = f"{self.ip}/v1/settings/business/profile"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                payload = json.dumps(profile_data)
                response = requests.post(url, headers=headers, data=payload)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in setting business profile")
                return str(e)
        

        def getComplianceInfo(self):
            try:
                url = f"{self.ip}/v1/settings/business/compliance_info"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.get(url, headers=headers)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in getting compliance info")
                return str(e)

        def setComplianceInfo(self, entity_name, entity_type, entity_type_custom, is_registered,
                             customer_care_email, customer_care_landline, customer_care_mobile,
                             grievance_officer_name, grievance_officer_email, grievance_officer_landline,
                             grievance_officer_mobile):
            try:
                url = f"{self.ip}/v1/settings/business/compliance_info"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                payload = {
                    "entity_name": entity_name,
                    "entity_type": entity_type,
                    "entity_type_custom": entity_type_custom,
                    "is_registered": is_registered,
                    "customer_care_details": {
                        "email": customer_care_email,
                        "landline_number": customer_care_landline,
                        "mobile_number": customer_care_mobile
                    },
                    "grievance_officer_details": {
                        "name": grievance_officer_name,
                        "email": grievance_officer_email,
                        "landline_number": grievance_officer_landline,
                        "mobile_number": grievance_officer_mobile
                    }
                }
                response = requests.post(url, headers=headers, json=payload)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in setting compliance info")
                return str(e)


        def getProfileAbout(self):
            try:
                url = f"{self.ip}/v1/settings/profile/about"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.get(url, headers=headers)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in getting profile about")
                return str(e)
            
        def getProfilePhotoBinary(self):
            try:
                url = f"{self.ip}/v1/settings/profile/photo"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.get(url, headers=headers)
                return response.content  # Return the binary content of the image
            except Exception as e:
                print("Error:", e)
                print("Error in getting profile photo binary")
                return None
        
        def getProfilePhotoURL(self):
            try:
                url = f"{self.ip}/v1/settings/profile/photo?format=link"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.jwt_token
                }
                response = requests.get(url, headers=headers)
                return response.json()
            except Exception as e:
                print("Error:", e)
                print("Error in getting profile photo URL")
                return None
            
        def set_profile_about(self, about_text):
            url = f"{self.base_url}/profile/about"
            payload = json.dumps({
                "text": about_text
            })
            response = requests.patch(url, headers=self.headers, data=payload)
            return response.text

        def set_profile_photo(self, file_contents):
            url = f"{self.base_url}/profile/photo"
            headers = {
                'Content-Type': 'image/jpeg',
                **self.headers
            }
            response = requests.post(url, headers=headers, data=file_contents)
            return response.text
        
        def enable_two_step(self, pin):
            url = f"{self.base_url}/account/two-step"
            payload = json.dumps({
                "pin": pin
            })
            response = requests.post(url, headers=self.headers, data=payload)
            return response.text

    class Registration:
        def __init__(self, auth_token):
            self.auth_token = auth_token
            self.base_url = "https://65.0.184.246:9090/v1/account"

        def request_code(self, cc, phone_number, method, cert):
            endpoint = ""
            payload = json.dumps({
                "cc": cc,
                "phone_number": phone_number,
                "method": method,
                "cert": cert
            })          
            url = f"{self.base_url}/{endpoint}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.auth_token}'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            response_json = response.json()  # Parse response content as JSON
            return response_json
        
        def verify_registration(self, code):
            endpoint = "verify"
            payload = json.dumps({
                "code": code
            })

            url = f"{self.base_url}/{endpoint}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.auth_token}'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            response_json = response.json()  # Parse response content as JSON
            return response_json
        
        
