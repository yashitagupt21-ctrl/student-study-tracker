
import json
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest.mock import patch

import storage


class TestStudyTrackerStorage(unittest.TestCase):

    def setUp(self):
        # Create a temporary folder for test data.
        self.temp_dir = TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "test_data.json"

        # Redirect storage operations to the temporary file.
        self.file_patcher = patch.object(
            storage, "DATA_FILE", self.test_file
        )
        self.file_patcher.start()

    def tearDown(self):
        self.file_patcher.stop()
        self.temp_dir.cleanup()

    def test_load_data_when_file_does_not_exist(self):
        data = storage.load_data()

        self.assertEqual(data, {
            "study_sessions": [],
            "tasks": []
        })

    def test_save_and_load_study_session(self):
        sessions = [
            {
                "subject": "Python",
                "topic": "Functions",
                "date": "2026-10-13",
                "duration": 60
            }
        ]
        tasks = []

        storage.save_data(sessions, tasks)
        loaded_data = storage.load_data()

        self.assertEqual(loaded_data["study_sessions"], sessions)
        self.assertEqual(loaded_data["tasks"], tasks)

    def test_save_and_load_tasks(self):
        sessions = []
        tasks = [
            {
                "description": "Complete Python project",
                "completed": False
            }
        ]

        storage.save_data(sessions, tasks)
        loaded_data = storage.load_data()

        self.assertEqual(loaded_data["tasks"], tasks)

    def test_saved_file_contains_valid_json(self):
        storage.save_data([], [])

        with self.test_file.open("r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertIn("study_sessions", data)
        self.assertIn("tasks", data)

        
from study_tracker import (
    create_study_session,
    calculate_subject_totals,
    create_task,
    mark_task_completed,
)


class TestStudyTrackerLogic(unittest.TestCase):

    def test_create_valid_study_session(self):
        session = create_study_session(
            "Python", "Functions", "2026-10-13", 60
        )
        self.assertEqual(session["subject"], "Python")
        self.assertEqual(session["duration"], 60)

    def test_reject_empty_subject(self):
        with self.assertRaises(ValueError):
            create_study_session(
                " ", "Functions", "2026-10-13", 60
            )

    def test_reject_invalid_date(self):
        with self.assertRaises(ValueError):
            create_study_session(
                "Python", "Functions", "13-10-2026", 60
            )

    def test_reject_non_positive_duration(self):
        with self.assertRaises(ValueError):
            create_study_session(
                "Python", "Functions", "2026-10-13", 0
            )

    def test_calculate_subject_totals(self):
        sessions = [
            {"subject": "Python", "duration": 60},
            {"subject": "Maths", "duration": 30},
            {"subject": "Python", "duration": 45},
        ]
        totals = calculate_subject_totals(sessions)
        self.assertEqual(totals, {"Python": 105, "Maths": 30})

    def test_create_task(self):
        task = create_task("Complete assignment")
        self.assertEqual(task["description"], "Complete assignment")
        self.assertFalse(task["completed"])

    def test_reject_empty_task(self):
        with self.assertRaises(ValueError):
            create_task("   ")

    def test_mark_task_completed(self):
        tasks = [
            {"description": "Study Python", "completed": False}
        ]
        mark_task_completed(tasks, 1)
        self.assertTrue(tasks[0]["completed"])

    def test_reject_invalid_task_number(self):
        tasks = [
            {"description": "Study Python", "completed": False}
        ]
        with self.assertRaises(ValueError):
            mark_task_completed(tasks, 2)



if __name__ == "__main__":
    unittest.main()