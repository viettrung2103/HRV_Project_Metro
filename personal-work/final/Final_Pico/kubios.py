import urequests as requests
import ujson
import network
import time
# import secret


APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a"
# APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3b"
CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
# CLIENT_ID = "3pjgjdmamlj759te85icf0lucc"
CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"
# CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlee"

LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login"
TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token"
REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login"
ANALYSIS_URL = "https://analysis.kubioscloud.com/v2/analytics/analyze"

class Kubios:

    def __init__(self):
        # self.apikey = apikey
        # self.client_id = client_id
        # self.client_secret = client_secret
        # self.login_url = login_url
        # self.token_url = token_url
        # self.redirect_uri = redirect_uri
        # self.analysis_url =analysis_url
        # self.login_response = None
        # self.analysis_response = None
        self.result = None
        # self.access_token = None
        # self.dataset = None
        self.ppi_list = []
        self.stop_flag = False
        self.error_flag = False
        # self.error_message = ""
        
    def default_setting(self):
        # self.login_response = None
        # self.analysis_response = None
        self.result = None
        # self.access_token = None
        # self.dataset = None
        self.ppi_list = []
    
    def create_login_response(self):
        try:
            print("create login response")
            login_response = requests.post(
                url = TOKEN_URL,
                data = 'grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
                headers = {'Content-Type':'application/x-www-form-urlencoded'},
                auth = (CLIENT_ID, CLIENT_SECRET))
            json_login_response =login_response.json()
            access_token = json_login_response["access_token"]
            # self.login_response = json_login_response
            return access_token
        
        except Exception as e:
            print(f"Failed to login to Kubios Server: {e}")
            self.error_flag = True
            self.stop_flag = True
    

    def add_ppi_list(self,ppi_list):
        if self.ppi_list == []:
            self.ppi_list = ppi_list
            
    def create_data_set(self):
        if self.stop_flag == False:
            if self.ppi_list != []:
                print("create data set")
                dataset = {
                    "type"      : "RRI",
                    "data"      : self.ppi_list,
                    "analysis"  : {
                        "type":"readiness"
                    }
                }
                return dataset
            
    def create_analysis_response(self, dataset, access_token):
        try:
            print("create analysis response")
            analysis_response = requests.post(
                # url = "https://analysis.kubioscloud.com/v2/analytics/analyze",
                url = ANALYSIS_URL,
                headers = { "Authorization": "Bearer {}".format(access_token), #use access token to access your Kubios Cloud analysis session
                "X-Api-Key": APIKEY},
                json = dataset) #dataset will be automatically converted to JSON by the urequests library

            json_analysis_response = analysis_response.json()
            # self.analysis_response = json_analysis_response
            # print(self.analysis_response)
            print(json_analysis_response)
            self.stop_flag = True
            time.sleep(3) 
            return json_analysis_response
        except Exception as e:
            print(f"Failed to login to Kubios Server: {e}")
            self.error_flag = True
            self.stop_flag = True
        # print(self.analysis_response)
        
    def analyse(self):
            print("analyse")
                # return json_login_response, access_token
            access_token  = self.create_login_response()
            # self.add_ppi_list(ppi_list)
            dataset = self.create_data_set()
            json_analysis_response = self.create_analysis_response(dataset, access_token)
            
            return json_analysis_response
            
    def validate_response(self, json_analysis_reponse):
        if self.stop_flag == False:
            print("validate")
            if json_analysis_reponse != None:
                if analysis_response["status"] == "ok":
                    self.error_flag = False
                else:
                    self.error_flag = True
                    self.stop = True
            else:
                self.error_flag = True
                self.stop_flag = True
            
    def saving_result(self, json_analysis_reponse):
        if self.result == None:
            self.result = {
                "artefact_level"    : json_analysis_reponse['analysis']["artefact_level"],
                "create_timestamp"  : json_analysis_reponse['analysis']["create_timestamp"],
                "mean_hr_bpm"       : json_analysis_reponse['analysis']["mean_hr_bpm"],
                "mean_rr_ms"        : json_analysis_reponse['analysis']["mean_rr_ms"],
                "rmssd_ms"          : json_analysis_reponse['analysis']["rmssd_ms"],
                "sdnn_ms"           : json_analysis_reponse['analysis']["sdnn_ms"],
                "sns_index"         : json_analysis_reponse['analysis']["sns_index"],
                "pns_index"         : json_analysis_reponse['analysis']["pns_index"],
            }
        
    def create_response(self):
        try:
            response = requests.post(
                url = TOKEN_URL,
                data = 'grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
                headers = {'Content-Type':'application/x-www-form-urlencoded'},
                auth = (CLIENT_ID, CLIENT_SECRET))
            response = response.json() 
            #Parse JSON response into a python dictionary 
            access_token = response["access_token"] 
    #Parse access token #Interval data to be sent to Kubios Cloud. Replace with your own data: intervals = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800] 
    # #Create the dataset dictionary HERE # Make the readiness analysis with the given data 
            dataset = { 
            "type": "RRI",
            "data": self.ppi_list,
            "analysis": {"type": "readiness"} 
            }
            response = requests.post(
            url = "https://analysis.kubioscloud.com/v2/analytics/analyze",
            headers = { "Authorization": "Bearer {}".format(access_token), #use access token to access your Kubios Cloud analysis session 
                        "X-Api-Key": APIKEY},
            json = dataset) #dataset will be automatically converted to JSON by the urequests library 
            response = response.json()
            return response
        
        except Exception as e:
            print(f"Failed to login to Kubios Server: {e}")
            
            self.error_flag = True
            self.stop_flag = True
            
    def run(self):
        print("start kubios")
        # print(self.stop_flag)
        if self.stop_flag == False:
            response = self.create_response()
            # json_analysis_reponse = self.analyse()
            # self.validate_response(json_analysis_reponse)
            # print("analysis" ,self.analysis_response)
            if self.error_flag == False:
                print("save result")
                self.saving_result(response)
                print(self.result)
                self.stop_flag = True

    def on(self):
        self.error_flag = False
        self.stop_flag = False
        pass
    
    def off(self):
        self.stop_flag = True