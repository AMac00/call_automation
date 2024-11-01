from unittest2 import TestCase
from camelot.encoder.encoder_helper import CamelotEncodeHelper


class TestCamelotEncodeHelper(TestCase):

    def setUp(self):
        self.cam_help = CamelotEncodeHelper()

    def tearDown(self):
        self.cam_help = None

    def test_get_endpoint_create_msg(self):
        self.assertEqual(
            self.cam_help.get_endpoint_create_msg('sipx', 'SEPMAC'),
            'c:00000000:000c:sipx SEPMAC@')

    def test_get_endpoint_create_msg_multiple(self):
        self.assertEqual(
            self.cam_help.get_endpoint_create_msg(
                'sipx', 'SEPMAC', 'param1', 'param2'),
            'c:00000000:001a:sipx SEPMAC param1 param2@')
