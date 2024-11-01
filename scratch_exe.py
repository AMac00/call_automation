from __fun_cucm__ import cucm_functions
from __fun_phone__ import phone_functions
# Import Environment based configuration elements
from configuration import baseconfig
import os


# files = os.listdir(os.getcwd())
# for file in files:
#     if ".log" in file:
#         os.remove(os.path.join(os.getcwd(), file))
#         print("Remove log name = {0}".format(file))
#
#
# # Test
# cm = cucm_functions()
# __return__ = cm.phones_build(baseconfig)
#
# phone = phone_functions()
# __return__ = phone.register_phones(baseconfig)

