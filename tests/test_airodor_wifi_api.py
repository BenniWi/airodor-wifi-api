"""This module provides tests for the airodor module"""

import unittest
from datetime import datetime
from unittest.mock import MagicMock

from yarl import URL

from airodor_wifi_api import airodor


def _make_response(text: str, ok: bool = True) -> MagicMock:
    """Create a mock requests.Response with the given text and ok status."""
    r = MagicMock()
    r.ok = ok
    r.text = text
    return r


class TestAirodorApi(unittest.TestCase):
    """This module provides tests for the airodor module"""

    def test_get_base_url(self):
        """
        Test that the base url is correct
        """
        result = airodor.get_base_api_url(host="192.168.2.122", port=80)
        self.assertEqual(result, URL("http://192.168.2.122:80/msg?Function="))

    def test_get_base_url_hostname_and_custom_port(self):
        """
        Test base url with hostname and custom port
        """
        result = airodor.get_base_api_url(host="mydevice.local", port=8866)
        self.assertEqual(result, URL("http://mydevice.local:8866/msg?Function="))

    def test_get_request_url_write(self):
        """
        Test to write a mode to a group
        """
        result = airodor.get_request_url(
            host="192.168.2.122",
            port=80,
            action=airodor.VentilationAction.WRITE_MODE,
            group=airodor.VentilationGroup.A,
            mode=airodor.VentilationModeSet.ALTERNATING_MAX,
        )
        self.assertEqual(result, URL("http://192.168.2.122/msg?Function=WA4"))
        result = airodor.get_request_url(
            host="192.168.2.122",
            port=80,
            action=airodor.VentilationAction.WRITE_MODE,
            group=airodor.VentilationGroup.A,
            mode=airodor.VentilationModeSet.ALTERNATING_MED,
        )
        self.assertEqual(result, URL("http://192.168.2.122/msg?Function=WA2"))

    def test_get_request_url_read(self):
        """
        Test to read a mode from a group
        """
        result = airodor.get_request_url(
            host="192.168.2.122",
            port=80,
            action=airodor.VentilationAction.READ_MODE,
            group=airodor.VentilationGroup.A,
        )
        self.assertEqual(result, URL("http://192.168.2.122/msg?Function=RA"))
        result = airodor.get_request_url(
            host="192.168.2.122",
            port=80,
            action=airodor.VentilationAction.READ_MODE,
            group=airodor.VentilationGroup.B,
        )
        self.assertEqual(result, URL("http://192.168.2.122/msg?Function=RB"))

    def test_interpret_answer(self):
        """
        Test to interpret the answer from the module
        """
        a, b = airodor.interpret_answer(_make_response("RB0"))
        self.assertEqual(a, airodor.VentilationGroup.B)
        self.assertEqual(b, airodor.VentilationModeRead.OFF)

        a, b = airodor.interpret_answer(_make_response("RA66"))
        self.assertEqual(a, airodor.VentilationGroup.A)
        self.assertEqual(b, airodor.VentilationModeRead.INSIDE_MAX)

        # test reading a "set" value, might occur right after setting and reading the mode
        a, b = airodor.interpret_answer(_make_response("RA64"))
        self.assertEqual(a, airodor.VentilationGroup.A)
        self.assertEqual(b, airodor.VentilationModeSet.INSIDE_MAX)

        a, b = airodor.interpret_answer(_make_response("MAOK"))
        self.assertEqual(a, airodor.VentilationGroup.A)
        self.assertEqual(b, True)

        a, b = airodor.interpret_answer(_make_response("MBNOOK"))
        self.assertEqual(a, airodor.VentilationGroup.B)
        self.assertEqual(b, False)

        a, b = airodor.interpret_answer(_make_response("SAOK"))
        self.assertEqual(a, airodor.VentilationGroup.A)
        self.assertEqual(b, True)

        a, b = airodor.interpret_answer(_make_response("SBNOOK"))
        self.assertEqual(a, airodor.VentilationGroup.B)
        self.assertEqual(b, False)

    def test_interpret_answer_timed_off(self):
        """Test that TIMED_OFF (128) is correctly recognized."""
        a, b = airodor.interpret_answer(_make_response("RB128"))
        self.assertEqual(a, airodor.VentilationGroup.B)
        self.assertEqual(b, airodor.VentilationModeRead.TIMED_OFF)

    def test_interpret_answer_timed_off_unknown_fallback(self):
        """Test that values > 128 fall back to TIMED_OFF_UNKNOWN."""
        a, b = airodor.interpret_answer(_make_response("RA130"))
        self.assertEqual(a, airodor.VentilationGroup.A)
        self.assertEqual(b, airodor.VentilationModeRead.TIMED_OFF_UNKNOWN)

        a, b = airodor.interpret_answer(_make_response("RB200"))
        self.assertEqual(a, airodor.VentilationGroup.B)
        self.assertEqual(b, airodor.VentilationModeRead.TIMED_OFF_UNKNOWN)

    def test_interpret_answer_unknown_mode(self):
        """Test that values not in any enum and <= 128 fall back to UNKNOWN."""
        a, b = airodor.interpret_answer(_make_response("RA99"))
        self.assertEqual(a, airodor.VentilationGroup.A)
        self.assertEqual(b, airodor.VentilationModeRead.UNKNOWN)

    def test_get_request_url_set_timer(self):
        """
        Test to set a timer for a group
        """
        result = airodor.get_request_url(
            host="192.168.2.122",
            port=80,
            action=airodor.VentilationAction.SET_OFF_TIMER,
            group=airodor.VentilationGroup.A,
            mode=3,
        )
        self.assertEqual(result, URL("http://192.168.2.122/msg?Function=SA3"))
        result = airodor.get_request_url(
            host="192.168.2.122",
            port=80,
            action=airodor.VentilationAction.SET_OFF_TIMER,
            group=airodor.VentilationGroup.B,
            mode=12,
        )
        self.assertEqual(result, URL("http://192.168.2.122/msg?Function=SB12"))

    def test_get_request_url_hostname_and_port(self):
        """
        Test URL construction with hostname and custom port
        """
        result = airodor.get_request_url(
            host="mydevice.local",
            port=8866,
            action=airodor.VentilationAction.READ_MODE,
            group=airodor.VentilationGroup.A,
        )
        self.assertEqual(result, URL("http://mydevice.local:8866/msg?Function=RA"))

    def test_timer_list(self):
        ventlist = airodor.VentilationTimerList()
        ventlist.add_list_item(
            # 1.11.2011 11:11:11 -> fourth entry
            datetime(year=2011, month=11, day=1, hour=11, minute=11, second=11),
            airodor.VentilationGroup.A,
            airodor.VentilationModeSet.INSIDE_MAX,
        )
        ventlist.add_list_item(
            # 1.10.2011 11:11:11 -> third entry
            datetime(year=2011, month=10, day=1, hour=11, minute=11, second=11),
            airodor.VentilationGroup.A,
            airodor.VentilationModeSet.ALTERNATING_MAX,
        )
        ventlist.add_list_item(
            # 1.11.2010 11:11:10 -> first entry
            datetime(year=2010, month=11, day=1, hour=11, minute=11, second=10),
            airodor.VentilationGroup.A,
            airodor.VentilationModeSet.ALTERNATING_MED,
        )
        ventlist.add_list_item(
            # 1.11.2010 11:11:11 -> second entry
            datetime(year=2010, month=11, day=1, hour=11, minute=11, second=11),
            airodor.VentilationGroup.A,
            airodor.VentilationModeSet.ALTERNATING_MIN,
        )

        # order of VentilationMode should be:
        # ALTERNATING_MED, ALTERNATING_MIN, ALTERNATING_MAX, INSIDE_MAX
        self.assertEqual(ventlist.timer_list[0].mode, airodor.VentilationModeSet.ALTERNATING_MED)
        self.assertEqual(ventlist.timer_list[1].mode, airodor.VentilationModeSet.ALTERNATING_MIN)
        self.assertEqual(ventlist.timer_list[2].mode, airodor.VentilationModeSet.ALTERNATING_MAX)
        self.assertEqual(ventlist.timer_list[3].mode, airodor.VentilationModeSet.INSIDE_MAX)
