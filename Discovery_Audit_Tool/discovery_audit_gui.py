#!/usr/bin/env python3

#21JAN2023

#Discover and Audit rack script with GUI implemenation

from tkinter import *
from tkinter import ttk
import library.discovery_audit as script

#instance of the tool class
tool_ins = script.tool()

#functions
def start():
    root.mainloop()

#update this to display an error message
# NEED TO WORK OUT THE ERROR DETAILS 24JAN2023
    if tool_ins.errorFlag is True:
        print("ERROR!")

def destory():
    root.destroy()

def checkbox_callback():
    if var.get() == 1:
        ip_entry.config(state="normal")
        #ip_entry.insert(0, "IP Address")
        if ip_entry.get():
            tool_ins.iplist.append(ip_entry.get())

    else:
        ip_entry.config(state="disable")

def ipentry_callback(address):
    address = ip_value.get()
    
    if var.get() == 1:
        if ip_entry.get():
            tool_ins.iplist.append(address)
            ip_list_label.config(text=str(tool_ins.iplist))

root = Tk()
root.title("Discover & Audit Tool")
frm=ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Discover PLCs on Network or Audit PLC rack", justify=CENTER).grid(columnspan=2)
frm.grid_columnconfigure(0, weight=1)
frm.grid_columnconfigure(1, weight=1)
devices_button = ttk.Button(frm, text="Discover", command=tool_ins.devices, width= 20).grid(row=1, column=0, padx=5, pady=5, sticky=W)
modules_button = ttk.Button(frm, text="Audit Racks", command=tool_ins.modules, width=20).grid(row=1, column=1, padx=5, pady= 5, sticky=W)

#check button will be used to manually enter an ip to audit. 
var= IntVar()
ip_rb = ttk.Checkbutton(frm, text="Provide IPs", variable=var, onvalue=1, offvalue=0, command=checkbox_callback).grid(row=2, column=1, sticky=E)
ip_value = StringVar()
ip_entry=ttk.Entry(frm, textvariable=ip_value)
ip_entry.grid(row=4, column=1, padx=5, pady=5, sticky=E)
ip_entry.config(state="disable")
ip_entry.bind("<Return>", ipentry_callback)

#display entered ip for user
ip_list_label = ttk.Label(frm, text="")
ip_list_label.grid(row=5, column=1)


if __name__ == '__main__':
    
    start()
    
    if tool_ins.dflag is True or tool_ins.mflag is True:
        tool_ins.file_create()
