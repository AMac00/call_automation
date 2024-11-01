'''
Created on 11-Sep1-2013

@author: smaturi
'''

import logging
import camelot
from camelot import camlogger
import time
from unittest2 import TestCase
from camelot.response import EndpointType

log = camlogger.getLogger('BasicCallWithoutEvents')
log.setLevel(logging.INFO)


class BasicCallWithoutEvents(TestCase):

    def setUp(self):

        cam_serv = camelot.create_camelot_server('10.106.248.199', '5004')
        if cam_serv is None:
            log.debug("couldn't get camelot-og server, may be camelot-og \
             server is not running")
            raise camelot.CamelotError("couldn't get camelot-og server"
                                       "may be camelot-og server is not running")
        log.debug("Server Compat Version: %s" %
                  cam_serv.get_compat_versions())
        self.ep1 = cam_serv.create_new_endpoint(
            EndpointType.SIPX, 'SEPBAACBAAC7003')
        self.ep2 = cam_serv.create_new_endpoint(
            EndpointType.SIPX, 'SEPBAACBAAC7004')

    def tearDown(self):
        log.debug("out of service ep1: %s" % self.ep1.outofservice())
        log.debug("uninit ep1: %s" % self.ep1.uninit())
        time.sleep(3)

        log.debug("out of service ep2: %s" % self.ep2.outofservice())
        log.debug("uninit ep2: %s" % self.ep2.uninit())

        camelot.stop_all()

        time.sleep(10)

    def test_basic_call_with_out_events(self):
        log.debug("New Endpoint: %s" % self.ep1)
        log.debug("Set Config: %s" %
                  self.ep1.config('sip.phone.ip', '10.20.1.3'))
        log.debug("Get Config: %s" % self.ep1.config('sip.phone.ip'))

        log.debug("Set Config: %s" %
                  self.ep1.config('sip.phone.tftpip', '10.20.1.21'))
        log.debug("Get Config: %s" % self.ep1.config('sip.phone.tftpip'))

        log.debug("Set Config: %s" %
                  self.ep1.config('sip.phone.deviceid', '1'))
        log.debug("Get Config: %s" % self.ep1.config('sip.phone.deviceid'))

        log.debug("init ep1: %s" % self.ep1.init())
        log.debug("inservice ep1: %s" % self.ep1.inservice())

        log.debug("New Endpoint: %s" % self.ep2)
        log.debug("Set Config: %s" %
                  self.ep2.config('sip.phone.ip', '10.20.1.3'))
        log.debug("Get Config: %s" % self.ep2.config('sip.phone.ip'))

        log.debug("Set Config: %s" %
                  self.ep2.config('sip.phone.tftpip', '10.20.1.21'))
        log.debug("Get Config: %s" % self.ep2.config('sip.phone.tftpip'))

        log.debug("Set Config: %s" %
                  self.ep2.config('sip.phone.deviceid', '1'))
        log.debug("Get Config: %s" % self.ep2.config('sip.phone.deviceid'))

        log.debug("init ep2: %s" % self.ep2.init())
        log.debug("inservice ep2: %s" % self.ep2.inservice())

        time.sleep(5)
        log.info('Successfully Initialized EP1 and EP2')
        log.info("EP1 INFO : %s" % self.ep1.get_info())
        log.info("EP2 INFO : %s" % self.ep1.get_info())

        log.info('Placing call from EP1 -> EP2')
        call_ref = self.ep1.place_call(
            dial_str=self.ep2.get_lines()[0]['full_address'])
        log.info("EP1 place_call Reference: %s" % call_ref)

        time.sleep(5)

        log.info('Calls on EP2: %s' % self.ep2.get_calls())

        call_ref_to_ans = self.ep2.get_calls()[0]['call_ref']

        log.info("EP2 answer_call : %s" % self.ep2.answer(call_ref_to_ans))

        time.sleep(1)

        log.info("EP1 CALLS : %s" % self.ep1.get_calls())
        log.info("EP2 CALLS : %s" % self.ep2.get_calls())

        log.debug("EP1 STREAMS : %s" % self.ep1.get_streams())
        log.debug("EP2 STREAMS : %s" % self.ep2.get_streams())

        time.sleep(15)

        log.info("EP2 endcall : %s" % self.ep2.endcall(call_ref_to_ans))

        time.sleep(1)

        log.info("EP1 CALLS : %s" % self.ep1.get_calls())
        log.info("EP2 CALLS : %s" % self.ep2.get_calls())

        log.debug("EP1 STREAMS : %s" % self.ep1.get_streams())
        log.debug("EP2 STREAMS : %s" % self.ep2.get_streams())


# this connects the protocol to a server runing on port 8000
# def main():
    # logging.basicConfig()
    # logging.setLevel(logging.DEBUG)
    # conn = Connection('10.106.248.199', 5004, 'test')
    # conn.init_connection('tet_id')


# this only runs if the module was *not* imported
# if __name__ == '__main__':
#    main()
