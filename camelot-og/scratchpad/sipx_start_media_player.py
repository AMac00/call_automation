import camelot
import time

CamelotServerIp = "10.38.228.239"
CamelotServerPort = 5000

CcmIp = "10.38.228.28"

ep1Mac = "SEPDAAADAAA6001"
ep2Mac = "SEPDAAADAAA6002"

__testphone__ = "7971"
if '9971' in __testphone__:
	ep1Mac = "SEP000000581023"
	ep2Mac = "SEP000000581024"
# JABBER -
if 'jabber' in __testphone__:
	ep1Mac = "CSFHARRIS"
	ep2Mac = "CSFJARMIJO"
#
# 7971 -
if '7971' in __testphone__:
	ep1Mac = "SEP000000581025"
	ep2Mac = "SEP000000581026"
#
# 7961 -
if '7961' in __testphone__:
	ep1Mac = "SEP000000581027"
	ep2Mac = "SEP000000581028"
#

ep1line = 6001
ep2line = 6002


serv = camelot.create_camelot_server(CamelotServerIp, CamelotServerPort)
serv.log_mask(moduleid="*",level="debug_5",device="file")
serv.log_mask(moduleid="*",level="debug_5",device="console")

ep1 = serv.create_new_endpoint('sipx',ep1Mac)
ep1.config('sip.phone.ip',CamelotServerIp)
ep1.config('sip.phone.httpip',CcmIp)
ep1.config('sip.phone.deviceid','14')
ep1.init()
ep1.inservice()


ep2 = serv.create_new_endpoint('sipx',ep2Mac)
ep2.config('sip.phone.ip',CamelotServerIp)
ep2.config('sip.phone.httpip',CcmIp)
ep2.config('sip.phone.deviceid','14')
ep2.init()
ep2.inservice()

time.sleep(3)

print("ep1 state -> {0}".format(ep1.get_info()['state']))
print("ep2 state -> {0}".format(ep2.get_info()['state']))

ep2.enable_auto_answer()

def get_stream_ref(ep, direction, type, callref):
        ep.release_streams()
        streams = ep.get_streams()
        for stream in streams:
                if ( stream['CallId'] == callref and stream['Direction'] == direction and stream['Type'] == type ):
                        return stream['StrmID']

ep1callref = ep1.place_call(ep2.get_dn())

time.sleep(2)
print(ep1.get_calls())
print(ep2.get_calls())

ep2callref = ep2.get_calls()[0]['Id']

print("ep1 getstreams -> {0}".format(ep1.get_streams()))

print("ep2 getstreams -> {0}".format(ep2.get_streams()))

ep1streamref = get_stream_ref(ep1, direction = 'Tx', type = 'audio', callref = ep1callref)
ep2streamref = get_stream_ref(ep2, direction = 'Rx', type = 'audio', callref = ep2callref)

ep1.start_media_player(stream_ref=ep1streamref,encoding='wav',url='file://usr/local/camelot-og/lib/media/Record.wav')

print("ep1 get_stream_info for Tx -> {0}".format(ep1.get_stream_info(stream_ref=ep1streamref)))
print("ep2 get_stream_info for Rx -> {0}".format(ep2.get_stream_info(stream_ref=ep2streamref)))

time.sleep(2)

print("ep1 get_stream_info_ext for Tx -> {0}".format(ep1.get_stream_info_ext(stream_ref=ep1streamref)))
print("ep2 get_stream_info_ext for Rx -> {0}".format(ep2.get_stream_info_ext(stream_ref=ep2streamref)))

time.sleep(3)

print("ep1 get_stream_info_ext for Tx -> {0}".format(ep1.get_stream_info_ext(stream_ref=ep1streamref)))
print("ep2 get_stream_info_ext for Rx -> {0}".format(ep2.get_stream_info_ext(stream_ref=ep2streamref)))
