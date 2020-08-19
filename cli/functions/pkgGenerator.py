# -*- coding: UTF-8 -*-

class gpkg:
    def Message(Title, Msg, Code=200):
        Package = {
            'Code': Code,
            'Title': Title,
            'Message': Msg
                }
        return Package
