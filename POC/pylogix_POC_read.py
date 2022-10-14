#!/usr/bin/env python3

from pylogix import PLC
with PLC() as comm:
    comm.IPAddress = 'IP_Address'
    ret = comm.Read('tag_name')
    print("tagname:"+ str(ret.TagName)+'\n', "value:"+ str(ret.Value)+'\n', "status:"+ str(ret.Status)+'\n')
    
    comm.Close()
