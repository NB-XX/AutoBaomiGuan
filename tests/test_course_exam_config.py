import unittest
from unittest.mock import Mock, patch

import course


class CourseExamConfigTests(unittest.TestCase):
    def test_complete_exam_uses_default_exam_id_when_configured(self):
        manager = course.CourseManager(Mock(), "token")
        manager.get_exam_answers = Mock(return_value=None)

        with patch.object(manager, "get_exam_info") as get_exam_info, \
             patch.object(course.logging, "error"):
            result = manager.complete_exam("course-packet-id")

        self.assertFalse(result)
        get_exam_info.assert_not_called()
        manager.get_exam_answers.assert_called_once()
        self.assertEqual(manager.get_exam_answers.call_args.args[0], "8ad5bd4d9d483dde019e3e1066f60035")


if __name__ == "__main__":
    unittest.main()
