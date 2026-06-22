import unittest
from unittest.mock import Mock, patch

import main


class MainCourseConfigTests(unittest.TestCase):
    def test_exam_menu_uses_current_course_packet_id(self):
        course_manager = Mock()
        course_manager.complete_exam.return_value = True

        with patch.object(main, "display_course_menu", side_effect=["3", "0"]), \
             patch("builtins.print"):
            main.handle_course_menu(course_manager)

        course_manager.complete_exam.assert_called_once_with("312bc914-8e11-421b-b9bc-e900fe1a4e50")


if __name__ == "__main__":
    unittest.main()
