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

    #funtion for control device
    def tap(self,x,y):
        result = requests.get(self.address+"shellr?cmd="+"input tap "+ str(x)+" "+str(y) ).text
        print(result)
        return result

    def swipe(self,x1,y1,x2,y2):
        result = requests.get(self.address+"shellr?cmd="+"input swipe "+ str(x1)+" "+str(y1)+ " "+str(x2)+" "+str(y2) ).text
        print(result)
        return result

    def input(self,text):
        result = requests.get(self.address+"shellr?cmd="+"input text "+str(text) ).text
        print(result)
        return result

    #basic control
    def wakeup(self):
        result = requests.get(self.address+"shellr?cmd="+"adb shell input keyevent 26" ).text
        print(result)
        return result

    def sleep(self):
        result = requests.get(self.address+"shellr?cmd="+"adb shell input keyevent 82" ).text
        print(result)
        return result

    def keyevent(self,keyevent):
        result = requests.get(self.address+"shellr?cmd="+"input keyevent "+ keyevent).text
        print(result)
        return result

    def shell(self,code):
        result = requests.get(self.address+"shellr?cmd="+code).text
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

    def KeyValueNodeList(self,key,value,rtformat="str"):
        result = json.loads(requests.get(self.address + "getnodelistbykeyvalue?key=" + key + "&value=" + value).text)
        if rtformat == "raw":
            return result
        elif rtformat == "str":
            return result["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'

    def KeyValueMultiple(self,dicdata,action="tap"):
        NodeListList = []
        for k, v in dicdata.items():
            NodeListList.append(self.KeyValueNodeList(k,v))
        return self.findsame(NodeListList)


    #return simple bound/get simple bound and tap
    def KeyValue(self,key,value,rtformat="str",action="tap"):
        if action == "tap":
            bound = json.loads(requests.get(self.address + "getboundbykeyvalue?key=" + key + "&value=" + value).text)
            print(bound)
            x = self.bounds2center(bound['data'])[0]
            y = self.bounds2center(bound['data'])[1]
            result = self.tap(x, y)
        elif action == "null":
            result = json.loads(requests.get(self.address + "getboundbykeyvalue?key=" + key + "&value=" + value).text)
            print(result)
            result = result['data']
        else:
            result = '{"data":"action argument is incorrect","errorCode":200,"isSuccess"false}'
        if rtformat == "str":
            return result
        elif rtformat == "str":
            return json.loads(result)["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'
    def Text(self,v,rtformat="str",action="tap"):
        if action == "tap":
            result = self.KeyValue("text",v,rtformat)
            return result
        elif action == "null":
            result = self.KeyValue("text",v,rtformat,action="null")
        else:
            result = '{"data":"your argument is incorrect","errorCode":200,"isSuccess"false}'
        return result
    def Id(self,v,action="tap"):
        if action == "tap":
            result = self.KeyValue("resource-id",v)
            return result
        elif action == "null":
            result = self.KeyValue("resource-id",v,action="null")
        else:
            result = '{"data":"your argument is incorrect","errorCode":200,"isSuccess"false}'
        return result
    def Desc(self,v,action="tap"):
        if action == "tap":
            result = self.KeyValue("content-desc",v)
            return result
        elif action == "null":
            result = self.KeyValue("content-desc",v,action="null")
        else:
            result = '{"data":"your argument is incorrect","errorCode":200,"isSuccess"false}'
        return result
    def Class(self,v,action="tap"):
        if action == "tap":
            result = self.KeyValue("class",v)
            return result
        elif action == "null":
            result = self.KeyValue("class",v,action="null")
        else:
            result = '{"data":"your argument is incorrect","errorCode":200,"isSuccess"false}'
        return result
    def Package(self,v,action="tap"):
        if action == "tap":
            result = self.KeyValue("package",v)
            return result
        elif action == "null":
            result = self.KeyValue("package",v,action="null")
        else:
            result = '{"data":"your argument is incorrect","errorCode":200,"isSuccess"false}'
        return result
    #not so useful
    def Checkable(self,v,action="tap"):
        if action == "tap":
            result = self.KeyValue("checkable",v)
            return result
        elif action == "null":
            result = self.KeyValue("checkable",v,action="null")
        else:
            result = '{"data":"your argument is incorrect","errorCode":200,"isSuccess"false}'
        return result


    #return bounds/return bound list
    def KeyValueBounds(self,key,value,rtformat="str"):
        result = json.loads(requests.get(self.address + "getboundsbykeyvalue?key=" + key + "&value=" + value).text)
        if rtformat == "raw":
            return result
        elif rtformat == "str":
            return result["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'
    def TextBounds(self,v,rtformat="str"):
        result = json.loads(requests.get(self.address + "getboundsbykeyvalue?key=text&value=" + v).text)
        if rtformat == "raw":
            return result
        elif rtformat == "str":
            return result["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'
    def IdBounds(self,v,rtformat="str"):
        result = json.loads(requests.get(self.address + "getboundsbykeyvalue?key=resource-id&value=" + v).text)
        if rtformat == "raw":
            return result
        elif rtformat == "str":
            return result["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'
    def DescBounds(self,v,rtformat="str"):
        result = json.loads(requests.get(self.address + "getboundsbykeyvalue?key=content-desc&value=" + v).text)
        if rtformat == "raw":
            return result
        elif rtformat == "str":
            return result["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'
    def ClassBounds(self,v,rtformat="str"):
        result = json.loads(requests.get(self.address + "getboundsbykeyvalue?key=class&value=" + v).text)
        if rtformat == "raw":
            return result
        elif rtformat == "str":
            return result["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'
    def PackageBounds(self,v,rtformat="str"):
        result = json.loads(requests.get(self.address + "getboundsbykeyvalue?key=package&value=" + v).text)
        if rtformat == "raw":
            return result
        elif rtformat == "str":
            return result["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'
    #not so useful
    def CheckableBounds(self,v,rtformat="str"):
        result = json.loads(requests.get(self.address + "getboundsbykeyvalue?key=checkable&value=" + v).text)
        if rtformat == "raw":
            return result
        elif rtformat == "str":
            return result["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'


    # return nodelist
    def TextNodeList(self, v, rtformat="str"):
        result = json.loads(requests.get(self.address + "getnodelistbykeyvalue?key=text&value=" + v).text)
        if rtformat == "raw":
            return result
        elif rtformat == "str":
            return result["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'
    def IdNodeList(self, v, rtformat="str"):
        result = json.loads(requests.get(self.address + "getnodelistbykeyvalue?key=resource-id&value=" + v).text)
        if rtformat == "raw":
            return result
        elif rtformat == "str":
            return result["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'
    def DescNodeList(self, v, rtformat="str"):
        result = json.loads(requests.get(self.address + "getnodelistbykeyvalue?key=content-desc&value=" + v).text)
        if rtformat == "raw":
            return result
        elif rtformat == "str":
            return result["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'
    def ClassNodeList(self, v, rtformat="str"):
        result = json.loads(requests.get(self.address + "getnodelistbykeyvalue?key=class&value=" + v).text)
        if rtformat == "raw":
            return result
        elif rtformat == "str":
            return result["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'
    def PackageNodeList(self, v, rtformat="str"):
        result = json.loads(requests.get(self.address + "getnodelistbykeyvalue?key=package&value=" + v).text)
        if rtformat == "raw":
            return result
        elif rtformat == "str":
            return result["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'
    # not so useful
    def CheckableNodeList(self, v, rtformat="str"):
        result = json.loads(requests.get(self.address + "getnodelistbykeyvalue?key=checkable&value=" + v).text)
        if rtformat == "raw":
            return result
        elif rtformat == "str":
            return result["data"]
        else:
            return '{"data":"rtformat argument is incorrect","errorCode":200,"isSuccess"false}'


