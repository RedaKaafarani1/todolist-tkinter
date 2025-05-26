# initialise tkinter 
from tkinter import *
from tkinter import ttk
from store import Store

STORE = Store("storage/data.json")
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

# create the main window
def fetch_user():
    data = STORE.get_data()
    if data is not None:
        return data["user"]["name"]
    else:
        return None


def create_user(root, frame):
    # Configure the frame with padding
    frame.configure(padding="20")
    # Welcome message
    ttk.Label(
        frame, 
        text="Welcome to Todo List!",
        font=("Helvetica", 16, "bold")
    ).grid(column=0, row=0, columnspan=3, pady=(0, 20))
    
    # Subtitle
    ttk.Label(
        frame,
        text="Seems like you are new here!",
        font=("Helvetica", 12)
    ).grid(column=0, row=1, columnspan=3, pady=(0, 20))
    
    # Name entry section
    ttk.Label(
        frame,
        text="Enter your name:",
        font=("Helvetica", 10)
    ).grid(column=0, row=2, padx=(0, 10))
    
    name_entry = ttk.Entry(frame, width=30)
    name_entry.grid(column=1, row=2, padx=10)
    
    # Create button
    def on_create():
        name = name_entry.get().strip()
        if name:  # Only proceed if name is not empty
            STORE.set_data({"user": {"name": name}})
            # Clear all widgets from the frame
            for widget in frame.winfo_children():
                widget.destroy()
            # Show main window content
            main_window(root, frame)
    
    ttk.Button(
        frame,
        text="Create",
        command=on_create
    ).grid(column=2, row=2, padx=(10, 0))

def add_todo(frame, user_data, todo_entry, no_data_label, add_button):
    # check if todos entry exists
    if "todos" not in user_data:
        user_data["todos"] = []
    # check if todos entry is empty
    if todo_entry.get().strip() == "":
        return
    # add the new todo as a dict with checked state
    user_data["todos"].append({"text": todo_entry.get().strip(), "checked": False})
    # save the user data to the store
    STORE.set_data({"user": user_data})
    # check if there is data and delete the label "looks like you have no todos yet!"
    if "todos" in user_data and len(user_data["todos"]) > 0:
        if no_data_label is not None:
            no_data_label.destroy()
    todo_entry.delete(0, END)
    add_button.configure(state="disabled")
    display_todos(frame, user_data)

def make_toggle_callback(idx, var, user_data):
    def toggle():
        user_data["todos"][idx]["checked"] = var.get()
        STORE.set_data({"user": user_data})
    return toggle

def display_todos(frame, user_data):
    # create new frame for the todos
    todos_frame = ttk.Frame(frame, padding="10", style="lightgray.TFrame")
    todos_frame.configure(borderwidth=2, relief="solid")
    todos_frame.grid(column=1, row=5, padx=5, pady=5, sticky="nsew")  # Centered with main content
    todos_frame.grid_columnconfigure(0, weight=1)
    todos_frame.grid_columnconfigure(1, weight=2)
    todos_frame.grid_columnconfigure(2, weight=1)
    # check if todos exists
    if "todos" in user_data:
        todos = user_data["todos"]
        ttk.Label(
            todos_frame,
            text="List:",
            font=("Helvetica", 12)
        ).grid(column=0, row=0, pady=(5, 0), sticky="w")  # Left-aligned in the box
        for index, todo in enumerate(todos):
            ttk.Label(
                todos_frame,
                text=f"{index + 1}. {todo['text']}"
            ).grid(column=0, row=1 + index, pady=(5, 0), sticky="w")  # Left-aligned in the box
            var = BooleanVar(value=todo.get("checked", False))
            check_box = ttk.Checkbutton(
                todos_frame,
                variable=var,
                style="green.TCheckbutton",
                command=make_toggle_callback(index, var, user_data)
            )
            check_box.grid(column=1, row=1 + index, pady=(5, 0), sticky="w")

def main_window(root, frame):
    user = fetch_user()
    no_data_label = None

    if user is None:
        create_user(root, frame)
        return

    ttk.Label(frame, text=f"Hello, {user}!", font=("Helvetica", 16, "bold")).grid(column=1, row=0)

    # fetch user data
    user_data = STORE.get_data()["user"]
    # check if user data exists
    if user_data is not None:
        # check if todos exists
        if "todos" in user_data:
            display_todos(frame, user_data)
        else:
            no_data_label = ttk.Label(frame, text="Looks like you have no todos yet!", foreground="red", justify="center")
            no_data_label.grid(column=1, row=1, pady=(5, 0))
    else:
        print("No user data found")
        exit()
    
    # add a button to add a new todo
    ttk.Label(frame, text="Add a new todo:", font=("Helvetica", 12, "bold"), justify="center").grid(column=1, row=2, pady=(5, 0))
    todo_entry = ttk.Entry(frame, width=30)
    todo_entry.grid(column=1, row=3, padx=10)
    # disable add button if todo entry is empty
    add_button = ttk.Button(frame, text="Add")
    add_button.grid(column=1, row=4, pady=(10, 0))
    add_button.configure(state="disabled")
    add_button.config(cursor="hand2", command= lambda: add_todo(frame,user_data, todo_entry, no_data_label, add_button))
    # enable add button if todo entry is not empty
    todo_entry.bind("<KeyRelease>", lambda event: add_button.configure(state="normal" if todo_entry.get().strip() else "disabled"))
    return root, frame

def main():
    # create the main window, width X height
    root = Tk()
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    frame = ttk.Frame(root, style="gray.TFrame", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    frame.grid()
    frame.grid_propagate(False)
    # center the frame
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=2)
    frame.grid_columnconfigure(2, weight=1)
    root.title("TODO List")

    # call the main window
    main_window(root, frame)

    root.mainloop()

if __name__ == "__main__":
    main()