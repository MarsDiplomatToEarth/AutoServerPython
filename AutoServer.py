# -*- coding: utf-8 -*-
import requests
import os,json,re,time

#Author: nobodyknowsme
#unfinishing

class AutoServer:
    def __init__(self, address,timeout=5):
        if "http://" not in address:
            address = "http://"+address
        else:
            pass
        if address[-1] == "/":
            pass
        else:
            address = address + "/"
        self.address = address
        self.timeout = timeout
        try:
            # i dont know why timeout is not working.
            checkisonoroff = requests.get(self.address + "root", timeout=3)
            print("device " + self.address.replace("http://","").replace("/","") + " is online")
        except:
            print("device " + self.address.replace("http://","").replace("/","") + " is off\nplease download the apk from github, run it on your rooted device and open it")
            exit()

    #function for use
    def requestdata(self,url):
        return json.loads(requests.get(url).text)["data"]


    #funtion for control device
    def tsleep(self,t):
        time.sleep(t)

    def tap(self,x,y):
        result = requests.get(self.address+"shell?cmd="+"input tap "+ str(x)+" "+str(y) ).text
        print(result)
        return result

    def tapbound(self,b):
        result = requests.get(self.address+"shell?cmd="+"input tap "+ str(b[0])+" "+str(b[1]) ).text
        print(result)
        return result

    def swipe(self,x1,y1,x2,y2):
        result = requests.get(self.address+"shell?cmd="+"input swipe "+ str(x1)+" "+str(y1)+ " "+str(x2)+" "+str(y2) ).text
        print(result)
        return result

    def input(self,text):
        result = requests.get(self.address+"shell?cmd="+"input text '"+str(text)+"'" ).text
        print(result)
        return result

    def inputu(self,text):
        result = requests.get(self.address+"input?str='"+str(text)+"'" ).text
        print(result)
        return result

    #basic control
    def wakeup(self):
        result = requests.get(self.address+"shell?cmd="+"adb shell input keyevent 26" ).text
        print(result)
        return result

    def sleep(self):
        result = requests.get(self.address+"shell?cmd="+"adb shell input keyevent 82" ).text
        print(result)
        return result

    def keyevent(self,keyevent):
        result = requests.get(self.address+"shell?cmd="+"input keyevent "+ keyevent).text
        print(result)
        return result

    def shell(self,code):
        result = requests.get(self.address+"shell?cmd="+code).text
        print(result)
        return result

    #function for filtering
    def findsame(self,jsonlist):
        returnlist = []
        #print(jsonlist[0])
        for i in jsonlist[0]:
            for li in jsonlist:
                if i in li:
                    returnlist.append(i)
        #print(returnlist)
        for i in jsonlist[0]:
            t = 1
            while t < len(jsonlist):
                t = t + 1
                try:
                    returnlist.remove(i)
                except:
                    pass
        #print(returnlist)
        return returnlist

    def bounds2center(self,bounds):
        b1 = bounds.split(",")[0]
        b2 = bounds.split(",")[1]
        b3 = bounds.split(",")[2]
        b4 = bounds.split(",")[3]
        centerx = str( (int(b1) + int(b3))/2 )
        centery = str( (int(b2) + int(b4))/2 )
        return [centerx,centery]

    def KeyValueNodeList(self,key,value):
        result = json.loads(requests.get(self.address + "getnodelistbykeyvalue?key=" + key + "&value=" + value).text)
        return result

    def KeyValueMultiple(self,dicdata,action="tap"):
        NodeListList = []
        for k, v in dicdata.items():
            NodeListList.append(self.KeyValueNodeList(k,v))
        return self.findsame(NodeListList)


    #return simple bound/get simple bound and tap
    def KeyValue(self,key,value,action="tap"):
        if action == "tap":
            bound = self.requestdata(self.address + "getboundbykeyvalue?key=" + key + "&value=" + value)
            #print(bound)
            x = self.bounds2center(bound)[0]
            y = self.bounds2center(bound)[1]
            result = self.tap(x, y)
        elif action == "null":
            result = self.requestdata(self.address + "getboundbykeyvalue?key=" + key + "&value=" + value)
            #print(result)
            result = result
        else:
            result = 'action argument is incorrect'
        return result
    def Text(self,v,action="tap"):
        if action == "tap":
            result = self.KeyValue("text",v)
        elif action == "null":
            result = self.KeyValue("text",v,action="null")
        else:
            result = 'your argument is incorrect'
        return result
    def Desc(self,v,action="tap"):
        if action == "tap":
            result = self.KeyValue("content-desc",v)
        elif action == "null":
            result = self.KeyValue("content-desc",v,action="null")
        else:
            result = 'your argument is incorrect'
        return result
    def Id(self,v,action="tap"):
        if action == "tap":
            result = self.KeyValue("resource-id",v)
        elif action == "null":
            result = self.KeyValue("resource-id",v,action="null")
        else:
            result = 'your argument is incorrect'
        return result

    #return bound list
    def KeyValueBounds(self,key,value):
        result = self.requestdata(self.address + "getboundsbykeyvalue?key=" + key + "&value=" + value)
        return result
    def TextBounds(self,v):
        result = self.requestdata(self.address + "getboundsbykeyvalue?key=text&value=" + v)
        return result
    def IdBounds(self,v):
        result = self.requestdata(self.address + "getboundsbykeyvalue?key=resource-id&value=" + v)
        return result
    def DescBounds(self,v):
        result = self.requestdata(self.address + "getboundsbykeyvalue?key=content-desc&value=" + v)
        return result
    def TextNodeList(self, v):
        result = self.requestdata(self.address + "getnodelistbykeyvalue?key=text&value=" + v)
        return result
    def IdNodeList(self, v):
        result = self.requestdata(self.address + "getnodelistbykeyvalue?key=resource-id&value=" + v)
        return result
    def DescNodeList(self, v):
        result = self.requestdata(self.address + "getnodelistbykeyvalue?key=content-desc&value=" + v)
        return result
    def TextNode(self, v):
        result = self.requestdata(self.address + "getnodebykeyvalue?key=text&value=" + v)
        return result
    def IdNode(self, v):
        result = self.requestdata(self.address + "getnodebykeyvalue?key=resource-id&value=" + v)
        return result
    def DescNode(self, v):
        result = self.requestdata(self.address + "getnodebykeyvalue?key=content-desc&value=" + v)
        return result
