'''
Created on 11-Sep1-2013


@author: smaturi
'''

import logging
import camelot
from camelot import camlogger
import time
from unittest2 import TestCase
from camelot.events import EventType, InfoEventType, StationEventType
from camelot.response import EndpointState, EndpointType, CallState

ep1_inservice = False
ep2_inservice = False

ep2_ringing = False

ep1 = None
ep2 = None

log = camlogger.getLogger('BasicCallWithEvents')
log.setLevel(logging.INFO)

# this event _callback is registered for endpoint1


def ep1_event_callback(event):
    global ep1, ep1_inservice
    if event.event_type == EventType.INFO_EVENT and event.event_sub_type == InfoEventType.STATE:
        if event.endpoint_id == ep1.ep_id:
            info_state = ep1.get_info()['state']
            if info_state == EndpointState.IN_SERVICE:
                ep1_inservice = True

# This _callback is registered on camelot-og server object


def server_event_callback(event):
    global ep2, ep2_inservice, ep2_ringing
    log.debug('server level Received Event: %s' % event)
    if event.event_type == EventType.INFO_EVENT and event.event_sub_type == InfoEventType.STATE:
        if event.endpoint_id == ep2.ep_id:
            info_state = ep2.get_info()['state']
            if info_state == EndpointState.IN_SERVICE:
                ep2_inservice = True
    elif event.event_type == EventType.STATION_EVENT:
        if event.endpoint_id == ep2.ep_id and event.event_sub_type == StationEventType.RING:
            ep2_ringing = True


class BasicCallWithEvents(TestCase):

    def setUp(self):
        global ep1, ep2, ep1_inservice, ep2_inservice, ep2_ringing

        cam_serv = camelot.create_camelot_server('10.106.248.199', '5004')
        if cam_serv is None:
            log.debug("couldn't get camelot-og server, may be camelot-og \
             server is not running")
            raise camelot.CamelotError("couldn't get camelot-og server"
                                       "may be camelot-og server is not running")
        log.debug("Server Compat Version: %s" %
                  cam_serv.get_compat_versions())
        ep1 = cam_serv.create_new_endpoint(
            EndpointType.SIPX, 'SEPBAACBAAC7003')
        ep2 = cam_serv.create_new_endpoint(
            EndpointType.SIPX, 'SEPBAACBAAC7004')
        if ep1 is None or ep2 is None:
            raise camelot.CamelotError("endpoint creation is failed \n")
        ep1.register_event_callback(ep1_event_callback)

        cam_serv.register_event_callback(server_event_callback)

    def tearDown(self):
        global ep1, ep2, ep1_inservice, ep2_inservice, ep2_ringing
        log.debug("out of service ep1: %s" % ep1.outofservice())
        log.debug("uninit ep1: %s" % ep1.uninit())
        time.sleep(3)

        log.debug("out of service ep2: %s" % ep2.outofservice())
        log.debug("uninit ep2: %s" % ep2.uninit())

        camelot.stop_all()

        time.sleep(10)

    def test_basic_call_with_events(self):
        global ep1, ep2, ep1_inservice, ep2_inservice, ep2_ringing
        log.debug("New Endpoint: %s" % ep1)

        log.debug("Set Config: %s" % ep1.config('sip.phone.ip', '10.20.1.3'))
        log.debug("Get Config: %s" % ep1.config('sip.phone.ip'))

        log.debug("Set Config: %s" %
                  ep1.config('sip.phone.tftpip', '10.20.1.21'))
        log.debug("Get Config: %s" % ep1.config('sip.phone.tftpip'))

        log.debug("Set Config: %s" % ep1.config('sip.phone.deviceid', '1'))
        log.debug("Get Config: %s" % ep1.config('sip.phone.deviceid'))

        ep1.start_info_events()
        ep1.start_station_events()

        log.debug("init ep1: %s" % ep1.init())
        log.debug("inservice ep1: %s" % ep1.inservice())

        # waiting for ep1 to get into service
        for i in range(10):
            if ep1_inservice:
                break
            time.sleep(1)

        self.assertTrue(ep1_inservice, 'EP1 could not be get in to service')

        log.info('EP1 is in service now')

        log.debug("New Endpoint: %s" % ep2)
        log.debug("Set Config: %s" % ep2.config('sip.phone.ip', '10.20.1.3'))
        log.debug("Get Config: %s" % ep2.config('sip.phone.ip'))

        log.debug("Set Config: %s" %
                  ep2.config('sip.phone.tftpip', '10.20.1.21'))
        log.debug("Get Config: %s" % ep2.config('sip.phone.tftpip'))

        log.debug("Set Config: %s" % ep2.config('sip.phone.deviceid', '1'))
        log.debug("Get Config: %s" % ep2.config('sip.phone.deviceid'))

        ep2.start_info_events()
        ep2.start_station_events()

        log.debug("init ep1: %s" % ep2.init())
        log.debug("inservice ep1: %s" % ep2.inservice())

        # waiting for ep2 to get into service
        for i in range(10):
            if ep2_inservice:
                break
            time.sleep(1)

        self.assertTrue(ep2_inservice, 'EP2 could not be get in to service')
        log.info('EP2 is in service now')

        log.debug("EP1 INFO : %s" % ep1.get_info())
        log.debug("EP2 INFO : %s" % ep1.get_info())

        # call_ref = ep1.place_call(dial_str='7002')
        call_ref = ep1.place_call(dial_str=ep2.get_lines()[0]['full_address'])
        log.debug("EP1 place_call : %s" % call_ref)

        # Wait for ringing event on ep2
        for i in range(10):
            if ep2_ringing:
                break
            time.sleep(1)

        self.assertTrue(ep2_ringing, 'On EP2 ringing event is not received')
        log.info('On EP2 ringing event is received')

        call_ref_to_ans = None
        # Fetching the ringing call on ep2
        for call in ep2.get_calls():
            if call['state'] == CallState.INCOMING:
                call_ref_to_ans = call['call_ref']

        log.debug("EP1 place_call : %s" % call_ref_to_ans)

        log.debug("EP2 answer_call : %s" % ep2.answer(call_ref_to_ans))

        time.sleep(1)

        log.debug("EP1 CALLS : %s" % ep1.get_calls())
        log.debug("EP2 CALLS : %s" % ep2.get_calls())

        log.debug("EP1 STREAMS : %s" % ep1.get_streams())
        log.debug("EP2 STREAMS : %s" % ep2.get_streams())

        time.sleep(15)

        log.debug("EP2 endcall : %s" % ep2.endcall(call_ref_to_ans))

        time.sleep(1)

        log.debug("EP1 CALLS : %s" % ep1.get_calls())
        log.debug("EP2 CALLS : %s" % ep2.get_calls())

        log.debug("EP1 STREAMS : %s" % ep1.get_streams())
        log.debug("EP2 STREAMS : %s" % ep2.get_streams())

        ep1.stop_info_events()
        ep2.stop_info_events()
        ep1.stop_station_events()
        ep2.stop_station_events()
