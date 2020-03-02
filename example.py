# -*- coding: utf-8 -*-
import requests
import os,json,re,time
from AutoServer import AutoServer

#Author:nobodyknowsme
#unfinishing

#connect to your device with address
a = AutoServer(address="http://192.168.1.236:8080/")

#tap coordinate(123,123)
a.tap(123,123)

#swipe from coordinate(10,20) to coordinate(10,500)
a.swipe(10,20,10,500)

#type text
a.input("hello AutoServer")

#click by text value"start Server",if there are lots of findings,will click the first of findings.
a.Text("Start Server")

#click by reousrce-id value"com.android.launcher3:id/folder_icon_name",if there are lots of findings,will click the first of findings.
a.Id("com.android.launcher3:id/folder_icon_name")

#click by content-desc value"back",if there are lots of findings,will click the first of findings.
a.Desc("back")

#click by class value"android.widget.FrameLayout",if there are lots of findings,will click the first of findings.
a.Class("android.widget.FrameLayout")

#funtion of statements below is the same,you can try to imitate it.
a.KeyValue("text","Start Server")
a.KeyValue(key= "text",value="Start Server")
a.Text("Start Server")

#......

