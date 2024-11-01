import camelot
import time

CamelotServerIp = "10.38.228.239"
CamelotServerPort = 5000

CcmIp = "10.38.228.28"

__testphone__ = "7961"


if '9971' in __testphone__:
    ep1Mac = "SEP000000581023"
    ep2Mac = "SEP000000581024"
    __model_type__ = "14"
    __model_pro__ = "sipx"
# # JABBER -
# if 'jabber' in __testphone__:
#     ep1Mac = "CSFHARRIS"
#     ep2Mac = "CSFJARMIJO"
#     __model_type__ = "38"
#     __model_pro__ = "sipx"
# #
# # 7971 -
# if '7971' in __testphone__:
#     ep1Mac = "SEP000000581025"
#     ep2Mac = "SEP000000581026"
#     __model_type__ = "3"
#     __model_pro__ = "sipx"
# #
# 7961 -  ( 5, 6, 30018)
if '7961' in __testphone__:
    ep1Mac = "SEP000000581027"
    __model_type__ = '30018'
    __model_pro__ = "sks"
#
# # 7861 -
# if '7861' in __testphone__:
#     ep1Mac = "SEP000000581028"
#     __model_type__ = '623'
#     __model_pro__ = "sipv"


serv = camelot.create_camelot_server(CamelotServerIp, CamelotServerPort)
serv.log_mask(moduleid="*",level="debug_5",device="file")
serv.log_mask(moduleid="*",level="debug_1",device="console")


print("Create endpoint {0} - {1}".format(__model_pro__,ep1Mac))

ep1 = serv.create_new_endpoint(__model_pro__, ep1Mac)
__return__ = ep1.get_info()

if "sip" in __model_pro__ :
    __return__ = ep1.get_device_config('2')
    print("sip - {0}".format(__return__))
    ep1.config('sip.phone.ip', CamelotServerIp)
    ep1.config('sip.phone.httpip',CcmIp)
    ep1.config('sip.phone.deviceid',__model_type__)
    __return__ = ep1.config("sip.phone.ip")
    print("update return is {0}".format(__return__))
else:
    print("Test")
    #ep1.config('phone.ipv4address',CamelotServerIp)
    # __return__ = ep1.get_info()
    # print("update return is {0}".format(__return__))
    #ep1.config('skinny.phone.ip',CamelotServerIp)



__outservice__ = 0

if __outservice__ == 1:
    print("UNReg {0}".format(ep1Mac))
    __return__ = ep1.init()
    print("-{0}".format(__return__))
    __return__ = ep1.outofservice()
    print("-{0}".format(__return__))
    __return__ = ep1.reset_to_default(serv)
    print("-{0}".format(__return__))



if __outservice__ == 0:
    print("Reg {0}".format(ep1Mac))
    try:
        __return__ = ep1.init()
        print("init = {0}".format(ep1.get_info()))
    except :
        print("Error Raised = {0}".format(ep1.get_info()))
    #time.sleep(1)
    try:
        __return__ = ep1.config("skinny.phone.devicetype", __model_type__)
        print("test 1 = {0}".format(__return__))
        __return__ = ep1.inservice()
        print("services status ={0}".format(__return__))
        time.sleep(5)
        __return__ = ep1.get_info()
        print("services status 2 ={0}".format(__return__))
    except:
        print("Error Raised = {0}".format(ep1.get_info()))



