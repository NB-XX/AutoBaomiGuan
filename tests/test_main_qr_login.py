import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main


class MainQrLoginTests(unittest.TestCase):
    def test_get_user_credentials_uses_qr_login_when_selected(self):
        with patch.object(main, "load_credentials", return_value=None), \
             patch("builtins.input", side_effect=["1", "unused-password"]), \
             patch("builtins.print"), \
             patch.object(main.login, "qr_login", return_value="qr-token", create=True), \
             patch.object(main.login, "login", return_value="password-token"), \
             patch.object(main, "save_credentials") as save_credentials:
            login_name, password, token = main.get_user_credentials()

        self.assertEqual((login_name, password, token), ("扫码登录用户", "", "qr-token"))
        save_credentials.assert_called_once_with("扫码登录用户", "", "qr-token")

    def test_saved_qr_credentials_can_have_empty_password(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            credentials_file = Path(tmp_dir) / "credentials.json"

            with patch.object(main, "CREDENTIALS_FILE", str(credentials_file)), \
                 patch.object(main.logging, "info"):
                main.save_credentials("扫码登录用户", "", "qr-token")
                saved = json.loads(credentials_file.read_text())

        self.assertEqual(saved["loginName"], "扫码登录用户")
        self.assertEqual(saved["passWord"], "")
        self.assertEqual(saved["token"], "qr-token")


if __name__ == "__main__":
    unittest.main()
