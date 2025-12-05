import os
import json


def createtask(filename):
    """Create a new task file and write a description."""
    print("\nCreating new task...\n")
    description = input("Enter task description:\n").strip()
    status = input("Enter status (done / not done / in progress):\n").strip().lower()
    with open(filename, "w") as f:
        json.dump({"description": description, "status" : status} , f, indent=4)
    print("\nTask created successfully!\n")


def alreadyexisttask(filename):
    """Open existing task, show description, allow update.
       If file doesn't exist, create it by calling createtask().
    """
    if os.path.exists(filename):
        # Safe load (handle empty or invalid JSON)
        if os.path.getsize(filename) == 0:
            data = {"description": ""}
        else:
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {"description": ""}

        print("\nExisting description:", data.get("description", "No description found."))
        print("\nEnter new description (or press Enter to keep existing):")
        desc = input().strip()
        if desc == "":
            desc = data.get("description", "")

        print("Enter new status (done / not done / in progress). Press Enter to keep existing:")
        status = input().strip().lower()
        if status == "":
            status = data["status"]


        with open(filename, "w") as f:
            json.dump({"description": desc}, f, indent=4)

        print("\nTask updated successfully!\n")
    else:
        # File not found → create it
        createtask(filename)


def show_all_tasks():
    files = [f for f in os.listdir() if f.endswith(".json")]

    if not files:
        print("No tasks found.")
        return

    print("\nAll Saved Tasks:\n")

    for file in files:
        print(f"📌 File: {file}")

        try:
            with open(file, "r") as f:
                data = json.load(f)
            description = data.get("description", "No description")
            status = data.get("status", "not set")

            print(f"  Description: {description}")
            print(f"  Status: {status}\n")

        except:
            print("  (Error reading file - resetting it)")
            print("  Description: Not available")
            print("  Status: Not available\n")

        print()



def delete_task():
    # List all JSON task files
    files = [f for f in os.listdir() if f.endswith(".json")]

    if not files:
        print("\nNo tasks found to delete.\n")
        return

    print("\nAvailable tasks:\n")
    for index, file in enumerate(files, start=1):
        print(f"{index}. {file}")

    # Ask user which file to delete
    choice = input("\nEnter task number to delete (or 'q' to cancel): ").strip()

    if choice.lower() == "q":
        print("Cancelled.\n")
        return

    if not choice.isdigit():
        print("Invalid input. Enter number only.\n")
        return

    choice = int(choice)

    if choice < 1 or choice > len(files):
        print("Invalid task number.\n")
        return

    file_to_delete = files[choice - 1]

    # Confirm deletion
    confirm = input(f"Are you sure you want to delete '{file_to_delete}'? (y/n): ").strip().lower()

    if confirm == "y":
        os.remove(file_to_delete)
        print(f"\nTask '{file_to_delete}' deleted successfully!\n")
    else:
        print("Deletion cancelled.\n")


def list_done_tasks():
    files = [f for f in os.listdir() if f.endswith(".json")]

    print("\nTasks that are DONE:\n")

    for file in files:
        try:
            with open(file, "r") as f:
                data = json.load(f)

            if data.get("status") == "done":
                print(f"- {file}: {data.get('description')}")
        except:
            continue


def list_not_done_tasks():
    files = [f for f in os.listdir() if f.endswith(".json")]

    print("\nTasks that are NOT DONE:\n")

    for file in files:
        try:
            with open(file, "r") as f:
                data = json.load(f)

            if data.get("status") == "not done":
                print(f"- {file}: {data.get('description')}")
        except:
            continue


def list_in_progress_tasks():
    files = [f for f in os.listdir() if f.endswith(".json")]

    print("\nTasks IN PROGRESS:\n")

    for file in files:
        try:
            with open(file, "r") as f:
                data = json.load(f)

            if data.get("status") == "in progress":
                print(f"- {file}: {data.get('description')}")
        except:
            continue





# ---- MAIN LOOP ----
while True:
    print("Press 1 to create/open task, or q/quit to exit.")
    print("Press 2 to show created task")
    print("Press 3 to delete task")

    userinput = input("Your choice: ").strip().lower()

    if userinput == "1":
        raw_name = input("Add task name:\n").strip()
        if raw_name == "":
            print("Task name cannot be empty. Try again.\n")
            continue
        filename = raw_name + ".json"
        # Call the logic immediately
        alreadyexisttask(filename)

    elif userinput == "2":
        show_all_tasks()

    elif userinput == "3":
        delete_task()

    elif userinput == "4":
        list_done_tasks()

    elif userinput == "5":
        list_not_done_tasks()

    elif userinput == "6":
        list_in_progress_tasks()

    elif userinput in ("q", "quit"):
        print("Exiting program. Goodbye!")
        break

    

    else:
        print("Wrong input — try again.\n")
