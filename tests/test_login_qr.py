import json
import unittest
from unittest.mock import Mock, patch

import login


class QrLoginTests(unittest.TestCase):
    def test_parse_qr_token_extracts_token_from_reference_payload(self):
        qr_payload = json.dumps({
            "action": "login",
            "params": {"qrToken": "qr-token-123"}
        })

        self.assertEqual(login.parse_qr_token(qr_payload), "qr-token-123")

    def test_parse_qr_token_rejects_payload_without_qr_token(self):
        qr_payload = json.dumps({"params": {}})

        with self.assertRaisesRegex(ValueError, "qrToken"):
            login.parse_qr_token(qr_payload)

    def test_get_qr_code_returns_content_and_token(self):
        qr_payload = json.dumps({
            "action": "login",
            "params": {"qrToken": "qr-token-456"}
        })
        response = Mock(status_code=200)
        response.json.return_value = {"data": {"data": qr_payload}}

        with patch.object(login.session, "post", return_value=response) as post:
            qr_content, qr_token = login.get_qr_code()

        self.assertEqual(qr_content, qr_payload)
        self.assertEqual(qr_token, "qr-token-456")
        post.assert_called_once_with(
            "https://www.baomi.org.cn/portal/main-api/v2/spc/getQrToken.do",
            headers={"siteId": "95"},
        )

    def test_check_qr_login_returns_nested_status_code(self):
        response = Mock(status_code=200)
        response.json.return_value = {"data": {"data": 1}}

        with patch.object(login.session, "post", return_value=response) as post:
            status = login.check_qr_login("qr-token-789")

        self.assertEqual(status, 1)
        post.assert_called_once_with(
            "https://www.baomi.org.cn/portal/api/v2/spc/checkQrToken.do",
            params={"qrToken": "qr-token-789"},
        )

    def test_qr_login_returns_token_when_scan_is_confirmed(self):
        with patch.object(login, "get_qr_code", return_value=("qr-content", "qr-token"), create=True), \
             patch.object(login, "print_terminal_qr", create=True) as print_qr, \
             patch.object(login, "check_qr_login", return_value=1, create=True) as check_status, \
             patch("builtins.print"), \
             patch("time.sleep") as sleep:
            token = login.qr_login(poll_interval=0)

        self.assertEqual(token, "qr-token")
        print_qr.assert_called_once_with("qr-content")
        check_status.assert_called_once_with("qr-token")
        sleep.assert_not_called()

    def test_qr_login_refreshes_when_qr_code_expires(self):
        with patch.object(
            login,
            "get_qr_code",
            side_effect=[("old-content", "old-token"), ("new-content", "new-token")],
            create=True,
        ) as get_qr_code, \
             patch.object(login, "print_terminal_qr", create=True) as print_qr, \
             patch.object(login, "check_qr_login", side_effect=[-1, 1], create=True), \
             patch("builtins.print"), \
             patch("time.sleep"):
            token = login.qr_login(poll_interval=0)

        self.assertEqual(token, "new-token")
        self.assertEqual(get_qr_code.call_count, 2)
        print_qr.assert_any_call("old-content")
        print_qr.assert_any_call("new-content")


if __name__ == "__main__":
    unittest.main()
