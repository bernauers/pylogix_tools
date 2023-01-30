#!/usr/bin/env python3

#20JAN2023

#Discover and Audit rack script

from pylogix import PLC
import pandas as pd
import socket
import os

class tool:
    #set variables for the class
    def __init__(self):
        self.iplist = []
        self.device_data = []
        self.module_data = []
        self.dflag = False
        self.mflag = False
        self.errorFlag=False

        #get hostname, will be used to filter out duplicates during discovery
        self.computer_name = (socket.gethostname()).upper()
        #set the path to the desktop on the host
        self.desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

    #pylogix functions
    def devices(self):
        self.dflag = True
        global device_df
        with PLC() as comm:
            devices = comm.Discover()
            for device in devices.Value:
                if self.computer_name in device.ProductName:
                    pass
                else:
                    #add discovered IP address to list
                    self.iplist.append(device.IPAddress)
                    #add device data to list with headers
                    self.device_data.append({'IPAddress': device.IPAddress, 'ProductCode': device.ProductName + ' ' + str(device.ProductCode), 'Vendor/Device ID': device.Vendor + ' ' + str(device.DeviceID), 'Revision/Serial': device.Revision + ' '  + device.SerialNumber})
                #return a dataframe with gathered device data
                device_df = pd.DataFrame(self.device_data)

            print("dflag Vlaue:" + str(self.dflag))

            return device_df
        
    def modules(self):
        self.mflag = True
        global module_df
        with PLC() as comm:
            for a in self.iplist:
                    comm.IPAddress = a
                    for i in range(17):
                        try:
                            #try different slots and get module properties using the discovered ips
                            prop = comm.GetModuleProperties(i)
                            #filter out the slots with nothing
                            if prop.Value.ProductName == None:
                                pass
                            else:
                                #add the data to a list
                                self.module_data.append({'IPAddress': a, 'Slot': i, 'ProductName': prop.Value.ProductName, 'Revision': prop.Value.Revision})
                        except KeyError:
                            self.errorFlag = True
                        except:
                            print("NOT a KeyError")
            
            #return a dataframe with module data list
            module_df = pd.DataFrame(self.module_data)
            
            print("mflag Value:" + str(self.mflag))

            #convert revision from being stored as text to a float
            module_df['Revision'] = module_df['Revision'].astype(float)
            return module_df

    def file_create(self):    
        #write the dataframes from above to an excel file
        with pd.ExcelWriter(os.path.join(self.desktop, 'plc_data.xlsx')) as writer:
            if self.dflag is True or self.mflag is True:
                if self.dflag is True:
                    device_df.to_excel(writer, sheet_name = "Devices", index = False)
                if self.mflag is True:
                    module_df.to_excel(writer, sheet_name = "Rack Audit", index = False)
            else:
                pass
