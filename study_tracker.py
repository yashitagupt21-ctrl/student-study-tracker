
from datetime import datetime

from storage import load_data, save_data


# ---------------- DATA INITIALIZATION ----------------

saved_data = load_data()
study_sessions = saved_data["study_sessions"]
tasks = saved_data["tasks"]


def save_current_data():
    """Save the current sessions and tasks."""
    save_data(study_sessions, tasks)


# ---------------- CORE LOGIC ----------------

def create_study_session(subject, topic, session_date, duration):
    """Validate study-session details and return a session dictionary."""

    subject = subject.strip()
    topic = topic.strip()

    if not subject:
        raise ValueError("Subject cannot be empty.")

    if not topic:
        raise ValueError("Topic cannot be empty.")

    try:
        datetime.strptime(session_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be valid and use YYYY-MM-DD format.")

    try:
        duration = int(duration)
    except (ValueError, TypeError):
        raise ValueError("Duration must be a whole number.")

    if duration <= 0:
        raise ValueError("Duration must be greater than zero.")

    return {
        "subject": subject,
        "topic": topic,
        "date": session_date,
        "duration": duration
    }


def calculate_subject_totals(sessions):
    """Return total study minutes for each subject."""

    totals = {}

    for session in sessions:
        subject = session["subject"]
        totals[subject] = totals.get(subject, 0) + session["duration"]

    return totals


def create_task(description):
    """Validate a task description and return a new task."""

    description = description.strip()

    if not description:
        raise ValueError("Task description cannot be empty.")

    return {
        "description": description,
        "completed": False
    }


def mark_task_completed(task_list, task_number):
    """Mark a task as completed using its one-based number."""

    try:
        task_number = int(task_number)
    except (ValueError, TypeError):
        raise ValueError("Task number must be a whole number.")

    if task_number < 1 or task_number > len(task_list):
        raise ValueError("Invalid task number.")

    task = task_list[task_number - 1]

    if task["completed"]:
        raise ValueError("This task is already completed.")

    task["completed"] = True


# ---------------- STUDY SESSION INTERFACE ----------------

def add_study_session():
    """Collect input and add a study session."""

    print("\n--- Add Study Session ---")

    subject = input("Enter subject: ")
    topic = input("Enter topic: ")
    session_date = input("Enter date (YYYY-MM-DD): ")
    duration = input("Enter duration in minutes: ")

    try:
        session = create_study_session(
            subject, topic, session_date, duration
        )
    except ValueError as error:
        print(error)
        return

    study_sessions.append(session)
    save_current_data()
    print("Study session added successfully!")


def view_study_sessions():
    """Display all recorded study sessions."""

    print("\n--- All Study Sessions ---")

    if not study_sessions:
        print("No study sessions recorded yet.")
        return

    for index, session in enumerate(study_sessions, start=1):
        print(f"\nSession {index}")
        print(f"Subject: {session['subject']}")
        print(f"Topic: {session['topic']}")
        print(f"Date: {session['date']}")
        print(f"Duration: {session['duration']} minutes")


def view_subject_summary():
    """Display total study time for each subject."""

    print("\n--- Study Time by Subject ---")

    if not study_sessions:
        print("No study sessions recorded yet.")
        return

    totals = calculate_subject_totals(study_sessions)

    for subject, total_minutes in sorted(totals.items()):
        hours = total_minutes // 60
        minutes = total_minutes % 60
        print(f"{subject}: {hours} hours, {minutes} minutes")


# ---------------- TASK INTERFACE ----------------

def add_task():
    """Collect input and add a task."""

    print("\n--- Add Task ---")

    description = input("Enter task description: ")

    try:
        task = create_task(description)
    except ValueError as error:
        print(error)
        return

    tasks.append(task)
    save_current_data()
    print("Task added successfully!")


def view_tasks():
    """Display tasks and their completion status."""

    print("\n--- Your Tasks ---")

    if not tasks:
        print("No tasks added yet.")
        return

    for index, task in enumerate(tasks, start=1):
        status = "Completed" if task["completed"] else "Pending"
        print(f"{index}. {task['description']} [{status}]")


def complete_task():
    """Ask the user which task to complete."""

    print("\n--- Complete Task ---")

    if not tasks:
        print("No tasks available to complete.")
        return

    view_tasks()
    task_number = input("Enter the task number to complete: ")

    try:
        mark_task_completed(tasks, task_number)
    except ValueError as error:
        print(error)
        return

    save_current_data()
    print("Task marked as completed!")
