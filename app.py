import json
import os
from datetime import datetime
import sys

TASKS_FILE = 'tasks.json'

def init_tasks_file():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as file:
            json.dump({"projects": [], "tasks": []}, file)

def read_data():
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

def write_data(data):
    with open(TASKS_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def add_project(project_name):
    data = read_data()
    projects = data["projects"]
    project_id = len(projects) + 1
    new_project = {
        "id": project_id,
        "name": project_name
    }
    projects.append(new_project)
    write_data(data)
    print(f"Project added successfully (ID: {project_id})")

def add_task(project_id, description):
    data = read_data()
    tasks = data["tasks"]

    # Check if the project exists
    project_exists = any(project['id'] == project_id for project in data['projects'])
    if not project_exists:
        print(f"Project with ID {project_id} does not exist.")
        return

    task_id = len(tasks) + 1
    new_task = {
        "id": task_id,
        "projectId": project_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(new_task)
    write_data(data)
    print(f"Task added successfully under project {project_id} (ID: {task_id})")

def update_task(task_id, new_description):
    data = read_data()
    tasks = data["tasks"]
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            write_data(data)
            print(f"Task {task_id} updated successfully.")
            return
    print(f"Task with ID {task_id} not found.")

def delete_task(task_id):
    data = read_data()
    tasks = data["tasks"]
    tasks = [task for task in tasks if task['id'] != task_id]
    data["tasks"] = tasks
    write_data(data)
    print(f"Task {task_id} deleted successfully.")

def mark_task_status(task_id, status):
    data = read_data()
    tasks = data["tasks"]
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            write_data(data)
            print(f"Task {task_id} marked as {status}.")
            return
    print(f"Task with ID {task_id} not found.")

def list_tasks(project_id=None, status=None):
    data = read_data()
    tasks = data["tasks"]
    if project_id:
        tasks = [task for task in tasks if task['projectId'] == project_id]
    if status:
        tasks = [task for task in tasks if task['status'] == status]
    for task in tasks:
        print(f"{task['id']}: {task['description']} [{task['status']}] (Created: {task['createdAt']}, Updated: {task['updatedAt']})")

def list_projects():
    data = read_data()
    projects = data["projects"]
    for project in projects:
        print(f"{project['id']}: {project['name']}")

def main():
    init_tasks_file()
    args = sys.argv[1:]

    if not args:
        print("Please provide a command.")
        return

    command = args[0]
    if command == 'add-project':
        if len(args) < 2:
            print("Please provide a project name.")
        else:
            add_project(" ".join(args[1:]))
    elif command == 'add-task':
        if len(args) < 3:
            print("Please provide project ID and task description.")
        else:
            try:
                project_id = int(args[1])
                description = " ".join(args[2:])
                add_task(project_id, description)
            except ValueError:
                print("Invalid project ID.")
    elif command == 'update-task':
        if len(args) < 3:
            print("Please provide task ID and new description.")
        else:
            try:
                task_id = int(args[1])
                new_description = " ".join(args[2:])
                update_task(task_id, new_description)
            except ValueError:
                print("Invalid task ID.")
    elif command == 'delete-task':
        if len(args) < 2:
            print("Please provide task ID to delete.")
        else:
            try:
                task_id = int(args[1])
                delete_task(task_id)
            except ValueError:
                print("Invalid task ID.")
    elif command == 'mark-in-progress':
        if len(args) < 2:
            print("Please provide task ID to mark as in-progress.")
        else:
            try:
                task_id = int(args[1])
                mark_task_status(task_id, 'in-progress')
            except ValueError:
                print("Invalid task ID.")
    elif command == 'mark-done':
        if len(args) < 2:
            print("Please provide task ID to mark as done.")
        else:
            try:
                task_id = int(args[1])
                mark_task_status(task_id, 'done')
            except ValueError:
                print("Invalid task ID.")
    elif command == 'list-tasks':
        if len(args) > 1:
            if args[1].isdigit():
                list_tasks(project_id=int(args[1]))
            else:
                list_tasks(status=args[1])
        else:
            list_tasks()
    elif command == 'list-projects':
        list_projects()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
