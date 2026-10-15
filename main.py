
# Import the functions that handle study sessions and tasks.
# Their actual implementation will be in study_tracker.py.
from study_tracker import (
    add_study_session,
    view_study_sessions,
    view_subject_summary,
    add_task,
    view_tasks,
    complete_task,
)


def display_menu():
    """Display the available actions to the user."""

    # Print a heading and the available menu options.
    print("\n" + "=" * 38)
    print("        STUDENT STUDY TRACKER")
    print("=" * 38)
    print("1. Add a study session")
    print("2. View all study sessions")
    print("3. View study time by subject")
    print("4. Add a task")
    print("5. View tasks")
    print("6. Mark a task as completed")
    print("7. Exit")
    print("=" * 38)


def main():
    """Control the main flow of the application."""

    # Repeat the menu until the user chooses to exit.
    while True:
        display_menu()

        # Read the user's choice and remove extra spaces.
        choice = input("Enter your choice: ").strip()

        # Call the appropriate function based on the user's choice.
        if choice == "1":
            add_study_session()

        elif choice == "2":
            view_study_sessions()

        elif choice == "3":
            view_subject_summary()

        elif choice == "4":
            add_task()

        elif choice == "5":
            view_tasks()

        elif choice == "6":
            complete_task()

        elif choice == "7":
            # Stop the loop and end the application.
            print("Thank you for using Student Study Tracker!")
            break

        else:
            # Handle choices that are not in the menu.
            print("Invalid choice. Please enter a number from 1 to 7.")


# Start the application only when this file is run directly.
# Importing main.py from another module will not automatically run main().
if __name__ == "__main__":
    main()
