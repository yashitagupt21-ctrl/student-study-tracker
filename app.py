
from flask import Flask, render_template, request, redirect, url_for, flash

import study_tracker
from storage import load_data, save_data

app = Flask(__name__)
app.secret_key = "study-tracker-local-key"


@app.route("/")
def home():
    data = load_data()

    study_sessions = data["study_sessions"]
    tasks = data["tasks"]

    total_minutes = sum(
        session["duration"] for session in study_sessions
    )

    subject_totals = study_tracker.calculate_subject_totals(
        study_sessions
    )

    return render_template(
        "index.html",
        study_sessions=study_sessions,
        tasks=tasks,
        total_hours=total_minutes // 60,
        remaining_minutes=total_minutes % 60,
        total_sessions=len(study_sessions),
        completed_tasks=sum(
            1 for task in tasks if task["completed"]
        ),
        subject_totals=subject_totals
    )


@app.route("/add-session", methods=["POST"])
def add_session():
    try:
        session = study_tracker.create_study_session(
            request.form.get("subject", ""),
            request.form.get("topic", ""),
            request.form.get("study_date", ""),
            request.form.get("duration", "")
        )

        data = load_data()
        data["study_sessions"].append(session)

        save_data(data["study_sessions"], data["tasks"])
        flash("Study session saved successfully!", "success")

    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("home"))


@app.route("/add-task", methods=["POST"])
def add_task():
    try:
        task = study_tracker.create_task(
            request.form.get("task", "")
        )

        data = load_data()
        data["tasks"].append(task)

        save_data(data["study_sessions"], data["tasks"])
        flash("Task added successfully!", "success")

    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("home"))


@app.route("/complete-task/<int:task_number>", methods=["POST"])
def complete_task(task_number):
    try:
        data = load_data()

        study_tracker.mark_task_completed(
            data["tasks"], task_number
        )

        save_data(data["study_sessions"], data["tasks"])
        flash("Task completed!", "success")

    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)


