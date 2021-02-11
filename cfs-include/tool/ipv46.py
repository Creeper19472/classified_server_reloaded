# -*- coding: utf-8 -*-

__author__ = "tianzhh_lynn"

import socket

class IPvStatus():
    def __init__(self, ip):
        self.ip = ip
        
    def ipv4(self):
        try:
            socket.inet_pton(socket.AF_INET, self.ip)
        except AttributeError:
            try:
                socket.inet_aton(self.ip)
            except socket.error:
                return False
            return self.ip.count('.') == 3
        except socket.error:
            return False
        return True

    def ipv6(self):
        try:
            socket.inet_pton(socket.AF_INET6, self.ip)
        except socket.error:
            return False
        return True
    
    def is_ip(self):
        if self.ipv4() or self.ipv6():
            return True
        else:
            return False
