ClientOnlineSid=["1","2","a","b"]
curClientSid=""
def findCli(sid):
    for index,i in enumerate(ClientOnlineSid):
        if(sid==i):
            return index
print(findCli("a"))
