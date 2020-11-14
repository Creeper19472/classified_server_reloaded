# -*- coding: UTF-8 -*-


class gpkg:
    def FileNotFound(Msg="Ooops! File Not Found."):
        Package = {"Code": 404, "Message": Msg}
        return Package

    def Forbidden(Msg="Forbidden!"):
        Package = {"Code": 403, "Message": Msg}
        return Package

    def BadRequest(Msg="Bad Request"):
        Package = {"Code": 400, "Title": "Bad_Request", "Message": Msg}
        return Package

    def Message(Title, Msg, Code=200):
        Package = {"Code": Code, "Title": Title, "Message": Msg}
        return Package
