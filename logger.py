import sys
import os
import time
from config import getConfig

def initLogging():
    global bdLogFileObject
    global bdLogLevel 
    bdLogLevel= int(getConfig("logLevel"))
    bdLogFileObject = open(os.getcwd() + "/blenderDungeon.log", "w+")

initLogging()

def log(_level, _process, _subProcess, _activity, _entry):
    if(bdLogLevel >= _level):
        formattedEntry = "[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "][" + _process + "]"
        if(_subProcess != ""):
            formattedEntry = formattedEntry + "[" + _subProcess + "]"
        if(_activity != ""):
            formattedEntry = formattedEntry + "[" + _activity + "]"
        formattedEntry = formattedEntry + " " + _entry + "\n"
        bdLogFileObject.write(formattedEntry)
        bdLogFileObject.flush()
        #print(formattedEntry, end="", flush = True)
        print(formattedEntry)