# -*- coding: utf-8 -*-

import socket, uuid, M2Crypto


"""
License.py

首先，感谢你阅读这一内嵌在本代码文件中的说明。
这是一个激活程序，目的是为了控制本项目的使用（即获得激活文件后才能使用软件），
采用的方法是RSA私钥加密公钥解密。
这一代码文件本身的诞生历时半年，直到本次更新才最终被加入。
我们希望使用者能够在使用这一项目之前向我们索要激活文件。在你的申请请求中，你可能需要包含以下信息：

    MAC地址（若之后地址更换，需要重新获取激活文件）；

这一信息应该很容易找到。
另外，在未来，获得激活码可能需要一定的费用（为了维持开发的继续），这笔费用应该不会太高。
但是若使用者实在缺少资金且有一定技术基础，也可以按照以下方式破解本激活系统：

方法一
    

"""

class LicenseClass:
    def get_mac_address(): 
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
        return ":".join([mac[e:e+2] for e in range(0,11,2)])

if __name__ == '__main__':
    print(LicenseClass.get_mac_address())
