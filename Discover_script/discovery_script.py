#!/usr/bin/env python3

#20JAN2023

#Discover and Audit rack script

from pylogix import PLC
import pandas as pd
import socket
import os

iplist = []
device_data = []
module_data = []

#get hostname, will be used to filter out duplicates during discovery
computer_name = (socket.gethostname()).upper()
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

#functions
def devices():
    with PLC() as comm:
        devices = comm.Discover()
        for device in devices.Value:
            if computer_name in device.ProductName:
                pass
            else:
                #add discovered IP address to list
                iplist.append(device.IPAddress)
                #add device data to list with headers
                device_data.append({'IPAddress': device.IPAddress, 'ProductCode': device.ProductName + ' ' + str(device.ProductCode), 'Vendor/Device ID': device.Vendor + ' ' + str(device.DeviceID), 'Revision/Serial': device.Revision + ' '  + device.SerialNumber})
            #return a dataframe with gathered device data
            device_df = pd.DataFrame(device_data)
        return device_df
        
def modules():
    with PLC() as comm:
        for a in iplist:
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
                            module_data.append({'IPAddress': a, 'Slot': i, 'ProductName': prop.Value.ProductName, 'Revision': prop.Value.Revision})
                    except:
                        print("An error occured.")
        #return a dataframe with module data list
        module_df = pd.DataFrame(module_data)
        #convert revision from being stored as text to a float
        module_df['Revision'] = module_df['Revision'].astype(float)
        return module_df

if __name__ == '__main__':
    device_df = devices()
    module_df = modules()
    
    #write the dataframes from above to an excel file
    with pd.ExcelWriter(os.path.join(desktop,'plc_data.xlsx')) as writer:
        device_df.to_excel(writer, sheet_name = "Devices", index = False)
        module_df.to_excel(writer, sheet_name = "Rack Audit", index = False)
