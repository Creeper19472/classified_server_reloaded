# -*- coding: UTF-8 -*-
import time


class GeneratePackage(object):
    def __init__(self, required_client_version, server_info):
        self.rcv = required_client_version
        self.sinfo = server_info
        
    def FileNotFound(self, Msg="Ooops! File Not Found."):
        Package = {
            "Code": 404,
            "Message": Msg,
            "required_client_version": self.rcv,
            "server_info": self.sinfo,
            "server_time": time.asctime()
            }
        return Package

    def Forbidden(self, Msg="Forbidden!"):
        Package = {
            "Code": 403,
            "Message": Msg,
            "required_client_version": self.rcv,
            "server_info": self.sinfo,
            "server_time": time.asctime()
            }
        return Package

    def BadRequest(self, Msg="Bad Request"):
        Package = {
            "Code": 400,
            "Title": "Bad_Request",
            "Message": Msg,
            "required_client_version": self.rcv,
            "server_info": self.sinfo,
            "server_time": time.asctime()
            }
        return Package

    def Message(self, Title, Msg, Code=200):
        Package = {
            "Code": Code,
            "Title": Title,
            "Message": Msg,
            "required_client_version": self.rcv,
            "server_info": self.sinfo,
            "server_time": time.asctime()
            }
        return Package
