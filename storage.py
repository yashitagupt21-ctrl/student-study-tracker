
import json
from pathlib import Path

# Store the data file in the same directory as this Python file.
DATA_FILE = Path(__file__).parent / "data.json"


def load_data():
    """Load saved study sessions and tasks from JSON."""

    # Return empty records when the file does not exist yet.
    if not DATA_FILE.exists():
        return {"study_sessions": [], "tasks": []}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        # Check that the saved data has the expected structure.
        if not isinstance(data, dict):
            raise ValueError("Saved data must be a JSON object.")

        sessions = data.get("study_sessions")
        tasks = data.get("tasks")

        if not isinstance(sessions, list) or not isinstance(tasks, list):
            raise ValueError("Saved sessions and tasks must be lists.")

        return {
            "study_sessions": sessions,
            "tasks": tasks
        }

    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(
            f"Could not load valid study tracker data: {error}"
        ) from error


def save_data(study_sessions, tasks):
    """Save study sessions and tasks to JSON."""

    data = {
        "study_sessions": study_sessions,
        "tasks": tasks
    }

    # Write readable JSON rather than one long line.
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)