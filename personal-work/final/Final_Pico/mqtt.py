import time
import network
# from time import sleep
from umqtt.simple import MQTTClient

SSID = "KMD658_Group_4"
PASSWORD = "00000000"
BROKER_IP = "192.168.4.253"

class Mqtt:
    def __init__(self,topic, ssid, password):
        self.topic = topic
        self.ssid = ssid
        self.password = password
        self.wlan = None
        self.mqtt_client = None
        self.data = None
        self.connect_wlan_flag = False
        self.connect_mqtt_flag = False
        self.data_flag = False
        self.error_flag = False
        self.stop_flag = False
        # self.message = None
        # self.stop_flag = True
        
    def has_data(self):
        if self.data != None:
            return True
        else:
            return False
    
    def connect_wlan(self):
    # Connecting to the group WLAN
        if self.connect_wlan_flag == False:
            self.wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True)
            self.wlan.connect(self.ssid, self.password)
            print("")
            # Attempt to connect once per second
            while self.wlan.isconnected() == False:
                print("Connecting... ")
                time.sleep(1)
                # if self.wlan.isconnected() == True:
            if self.wlan.isconnected() == True:
                self.connect_wlan_flag = True
                # print("Connect success")
                print("Connection successful. Pico IP:", self.wlan.ifconfig()[0])
                
        # Print the IP address of the Pico
            
            # print("Connection successful. Pico IP:", self.wlan.ifconfig()[0])
    
    def connect_mqtt(self):
        if self.connect_mqtt_flag == False and self.connect_wlan_flag == True:
            self.mqtt_client = MQTTClient("", BROKER_IP)
            self.mqtt_client.connect(clean_session=True)
            self.connect_mqtt_flag = True
            print("Connect Successfully to MQTT")
        # return mqtt_client
        
    def convert_data_to_message(self):
        
        self.message = f"""
        {
            "mean_hr" : "{self.data["mean_hr"]}", 
            "mean_ppi" : "{self.data["mean_ppi"]}", 
            "rmssd" : "{self.data["rmssd"]}", 
            "sdnn" : "{self.data["sdnn"]}", 
        }
        """
    
    def add_data(self,data):
        self.data = data
        self.data_flag = True
        
    def publish_data(self):
        try:
            # print("data" ,data)
            if self.connect_mqtt_flag == True and self.stop_flag == False:

                    # mean_hr_message = f"mean_hr: {self.data["mean_hr"]}"
                    # mean_ppi_message = f"mean_ppi: {self.data["mean_ppi"]}"
                    # rmssd_message = f"rmssd: {self.data["rmssd"]}"
                    # sdnn_message = f"sdnn: {self.data["sdnn"]}"

                    self.mqtt_client.publish(self.topic, self.data)
                    # self.mqtt_client.publish(self.topic, mean_hr_message)
                    # self.mqtt_client.publish(self.topic, mean_ppi_message)
                    # self.mqtt_client.publish(self.topic, rmssd_message)
                    # self.mqtt_client.publish(self.topic, sdnn_message)

                    print(f"Sending to MQTT: {self.topic} -> {self.data}")
                    # print(f"Sending to MQTT: {self.topic} -> {mean_hr_message}")
                    # print(f"Sending to MQTT: {self.topic} -> {mean_ppi_message}")
                    # print(f"Sending to MQTT: {self.topic} -> {rmssd_message}")
                    # print(f"Sending to MQTT: {self.topic} -> {sdnn_message}")
                    
                    time.sleep(2)
                    print("Done")
                    self.stop_flag = True
                    
        except Exception as e:
                print(f"Failed to send MQTT message: {e}")
                self.error_flag = True
                
    def reset_data(self):
        # self.data = None
        self.wlan = None
        self.mqtt_client = None
        # self.message = None
    
    def run(self):
        # self.add_data(data)
        if self.has_data() and self.stop_flag == False:
            # print("here")
            self.connect_wlan()
        # Connect to MQTT
            try:
                self.connect_mqtt()                
            except Exception as e:
                print(f"Failed to connect to MQTT: {e}")
                self.error_flag = True
                self.stop_flag = True

            self.publish_data()
            self.data_flag  = False
            self.stop_flag = True
            
    def default_setting(self):
        # self.stop_flag = False
        self.connect_wlan_flag = False
        self.connect_mqtt_flag = False
        self.error_flag = False
        self.stop_flag = False
        self.reset_data()