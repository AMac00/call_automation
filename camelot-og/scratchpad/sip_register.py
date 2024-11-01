import logging
import camelot
from camelot import camlogger
import time
from camelot.events import EventType, InfoEventType, StationEventType
from camelot.response import EndpointState, EndpointType, CallState


ep1_inservice = False

def ep1_event_callback(event):
    global ep1, ep1_inservice
    if event.event_type == EventType.INFO_EVENT and event.event_sub_type == InfoEventType.STATE:
        if event.endpoint_id == ep1.ep_id:
            info_state = ep1.get_info()['state']
            if info_state == EndpointState.IN_SERVICE:
                ep1_inservice = True


def outservice():
    global ep1
    print('Putting end point into OUtService -------------------')
    __return__ = ep1.outofservice()
    print("-{0}".format(__return__))

    for i in range(10):
        __return__ = ep1.get_info()['state']
        print("-{0}".format(__return__))
        time.sleep(1)


CamelotServerIp = "10.38.228.239"
CamelotServerPort = 5000

CcmIp = "10.38.228.28"

__phone_model__ = 3

# Phone 9971
if __phone_model__ == 1:
    __phone__ = {
    "__mac__" : "SEP000000581023",
    "__model_type__" : "14",
    "__model_pro__" :"sipx"
    }
# Phone 7861
if __phone_model__ == 2:
    __phone__ = {
    "__mac__" : "SEP000000581028",
    "__model_type__" : "623",
    "__model_pro__" :"sipx"
    }
# Phone 7961
if __phone_model__ == 3:
    __phone__ = {
    "__mac__" : "SEP000000581027",
    "__model_type__" : "5",
    "__model_pro__" :"sipx"
    }


serv = camelot.create_camelot_server(CamelotServerIp, CamelotServerPort)
serv.log_mask(moduleid="*",level="debug_5",device="file")
serv.log_mask(moduleid="*",level="debug_1",device="console")


params = {'sip.phone.ip': CamelotServerIp,
'sip.phone.tftpip': CcmIp,
'sip.phone.deviceid': __phone__["__model_type__"]}

ep1 = serv.create_new_endpoint(__phone__["__model_pro__"],__phone__["__mac__"])
ep1.config_ep_dict(params)
__return__ = ep1.init()
print("-{0}".format(__return__))


#check current status
info_state = ep1.get_info()['state']
if info_state is not EndpointState.IN_SERVICE:
    __return__ = ep1.inservice()
    print("-{0}".format(__return__))
    ep1.inservice()
    # ep1.register_event_callback(ep1_event_callback)



for i in range(10):
    if ep1_inservice is True:
        print("Phone is in service :)")
        break
    print("Sleeping {0}".format(str(i)))
    time.sleep(1)


print("Current state = {0}".format(ep1.get_info()['state']))

time.sleep(120)


# If you want to put the device out of service
# outservice()



