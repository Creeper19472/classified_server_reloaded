# -*- coding: utf-8 -*-

display_name = 'Classified Server'

desktop_mode = False

"""
If the value of this option is set to True, some functions
that may block the running of the program will be enabled.
May cause obstacles to automated deployment systems.

"""

enable_ipv4 = True
# IPv4.

bind4_address = ('0.0.0.0', 5104)
# Set the address that the server listens to.

enable_ipv6 = False

bind6_address = ('::', 5104)

database_prefix = 'cfs_'

language = "zh_CN"
