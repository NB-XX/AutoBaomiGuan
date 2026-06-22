import unittest
from unittest.mock import Mock, patch

import course


class CourseExamConfigTests(unittest.TestCase):
    def test_complete_exam_uses_dynamic_exam_id_when_available(self):
        manager = course.CourseManager(Mock(), "token")
        manager.get_exam_answers = Mock(return_value=None)
        manager.get_exam_info = Mock(
            return_value={"data": [{"examId": "dynamic-exam-id"}]}
        )

        with patch.object(course.logging, "error"), \
             patch("builtins.print"):
            result = manager.complete_exam("course-packet-id")

        self.assertFalse(result)
        manager.get_exam_info.assert_called_once_with("course-packet-id")
        # 拿到动态 ID 后用它请求试卷
        called_exam_id = manager.get_exam_answers.call_args.args[0]
        self.assertEqual(called_exam_id, "dynamic-exam-id")

    def test_complete_exam_falls_back_to_default_exam_id(self):
        manager = course.CourseManager(Mock(), "token")
        manager.get_exam_answers = Mock(return_value=None)
        manager.get_exam_info = Mock(return_value=None)

        with patch.object(course.logging, "error"), \
             patch.object(course, "DEFAULT_EXAM_ID", "fallback-id"), \
             patch("builtins.print"):
            result = manager.complete_exam("course-packet-id")

        self.assertFalse(result)
        manager.get_exam_info.assert_called_once_with("course-packet-id")
        # 动态获取失败时回退到默认考试 ID
        called_exam_id = manager.get_exam_answers.call_args.args[0]
        self.assertEqual(called_exam_id, "fallback-id")


if __name__ == "__main__":
    unittest.main()
