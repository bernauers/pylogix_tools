from pylogix import PLC
with PLC() as comm:
    print("Enter PLC IPv4 address to read tags from")
    print("Example: 192.168.10.8\n")
    comm.IPAddress = input()
    tags = comm.GetTagList(False)
    
    for i in tags.Value:
        print(i.TagName, i.DataType)
    
    comm.Close()