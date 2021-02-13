# -*- coding: UTF-8 -*-


class gpkg:
    def Message(msgtype, msg, **kwargs):
        Package = {
            "Msg": msg,
            "Type": msgtype,
            "Data": {}
            }
        if len(kwargs) == 0:
            return Package
        for x in kwargs:
            value = kwargs[x]
            Package['Data'][x] = value
        return Package

if __name__ == '__main__':
    print(gpkg.Message('example', test1='duck'))
