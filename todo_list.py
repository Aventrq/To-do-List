import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json

def save_data():
    listbox_items = listbox.get(0, tk.END)
    completed_listbox_items = completed_listbox.get(0, tk.END)

    data = {
        "listbox": listbox_items,
        "completed_listbox": completed_listbox_items
    }

    with open('listbox_data.json', 'w') as f:
        json.dump(data, f)
    print("Data saved successfully!")

def load_data():
    global original_tasks
    try:
        with open('listbox_data.json', 'r') as f:
            data = json.load(f)

        listbox.delete(0, tk.END)
        completed_listbox.delete(0, tk.END)

        original_tasks = data['listbox']

        for item in data['listbox']:
            listbox.insert(tk.END, item)

        for item in data['completed_listbox']:
            completed_listbox.insert(tk.END, item)
        
        print("Data loaded successfully!")
    except FileNotFoundError:
        print("No saved data found.")

def add_task():
    task = entry.get()
    priority = priority_var.get()
    if task and 'Type task:' not in task:
        formatted_task = f"{task} - {priority}"
        original_tasks.append(formatted_task)
        listbox.insert(tk.END, formatted_task)
        entry.delete(0, tk.END)
        refresh_listbox()
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def del_task():
    try:
        selected_index = listbox.curselection()[0]
        task_to_remove = listbox.get(selected_index)
        original_tasks.remove(task_to_remove)
        listbox.delete(selected_index)
        refresh_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to delete.")

def complete_task():
    try:
        selected_index = listbox.curselection()[0]
        selected_text = listbox.get(selected_index)
        original_tasks.remove(selected_text)
        listbox.delete(selected_index)
        completed_listbox.insert(tk.END, selected_text)
        refresh_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to complete.")

def search_tasks(event=None):
    query = search_entry.get().lower()
    global current_query
    current_query = query
    refresh_listbox()

def refresh_listbox():
    listbox.delete(0, tk.END)
    
    if current_query and 'Search tasks...' not in current_query:
        filtered_tasks = [task for task in original_tasks if current_query in task.lower()]
        for task in filtered_tasks:
            listbox.insert(tk.END, task)
    else:
        for task in original_tasks:
            listbox.insert(tk.END, task)

def sort_tasks():
    tasks = listbox.get(0, tk.END)
    
    def get_sort_key(task):
        if 'high' in task.lower():
            priority = 0
        elif 'medium' in task.lower():
            priority = 1
        else:
            priority = 2
        
        name = task.split(' - ')[0]
        
        return (priority, name.lower())
    
    sorted_tasks = sorted(tasks, key=get_sort_key)
    
    listbox.delete(0, tk.END)
    for task in sorted_tasks:
        listbox.insert(tk.END, task)

def on_focus_in(event):
    if event.widget.get() == 'Type task:':
        event.widget.delete(0, tk.END)
        event.widget.config(fg='black')

def on_focus_out(event):
    if event.widget.get() == '':
        event.widget.insert(0, 'Type task:')
        event.widget.config(fg='grey')

def on_search_focus_in(event):
    if search_entry.get() == 'Search tasks...':
        search_entry.delete(0, tk.END)
        search_entry.config(fg='black')

def on_search_focus_out(event):
    if search_entry.get() == '':
        search_entry.insert(0, 'Search tasks...')
        search_entry.config(fg='grey')

def update_original_tasks():
    global original_tasks
    original_tasks = listbox.get(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("To-Do List")
root.geometry("600x450")

# Initialize list and search query
original_tasks = []
current_query = ''

# Create and place the search entry box
search_entry = tk.Entry(root, fg='grey')
search_entry.insert(0, 'Search tasks...')
search_entry.bind('<FocusIn>', on_search_focus_in)
search_entry.bind('<FocusOut>', on_search_focus_out)
search_entry.bind('<KeyRelease>', search_tasks)
search_entry.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="ew")

# Create and place the entry box
entry = tk.Entry(root, fg='grey')
entry.insert(0, 'Type task:')
entry.bind('<FocusIn>', on_focus_in)
entry.bind('<FocusOut>', on_focus_out)
entry.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

# Create and place the dropdown menu for priority using ttk.Combobox
priority_options = ["High", "Medium", "Low"]
priority_var = tk.StringVar(value='Medium')  # Default priority
priority_dropdown = ttk.Combobox(root, textvariable=priority_var, values=priority_options)
priority_dropdown.grid(row=1, column=2, padx=10, pady=10, sticky='ew')

# Create Listboxes
listbox = tk.Listbox(root, width=30, height=10)
completed_listbox = tk.Listbox(root, width=30, height=10)

# Place the Listboxes
listbox.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
completed_listbox.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

# Create and place buttons
add_button = tk.Button(root, text="Add Task", command=add_task)
del_button = tk.Button(root, text="Delete Task", command=del_task)
comp_button = tk.Button(root, text="Task Completed", command=complete_task)
sort_button = tk.Button(root, text="Sort Tasks", command=sort_tasks)
save_button = tk.Button(root, text="Save", command=save_data)

# Ensure all buttons are of the same size
button_width = max(add_button.cget('width'), del_button.cget('width'), comp_button.cget('width'), sort_button.cget('width'), save_button.cget('width'))
add_button.config(width=button_width)
del_button.config(width=button_width)
comp_button.config(width=button_width)
sort_button.config(width=button_width)
save_button.config(width=button_width)

# Place buttons in a grid layout
add_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
del_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
comp_button.grid(row=3, column=2, padx=5, pady=5, sticky="ew")
sort_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
save_button.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

# Configure column and row weights
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=0)
root.grid_rowconfigure(4, weight=0)

# Load data when the app starts
load_data()

root.mainloop()
