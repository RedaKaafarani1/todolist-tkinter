# initialise tkinter 
from tkinter import *
from tkinter import ttk
import os
import json

STORAGE_PATH = "../storage/data.json"
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

# create the main window
def fetch_user():
    # check if data.json exists
    if os.path.exists(STORAGE_PATH):
        with open(STORAGE_PATH, "r") as f:
            # find user in the file
            data = json.load(f)
            if "user" in data:
                return data["user"]["name"]
            else:
                return None
    else:
        print("No user found")
        return None
    
def save_user(name):
    # check if data.json exists
    if os.path.exists(STORAGE_PATH):
        with open(STORAGE_PATH, "w") as f:
            json.dump({"user": {"name": name}}, f)
    else:
        print("Could not save user")
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
    ttk.Button(
        frame,
        text="Create",
        command=lambda: save_user(name_entry.get())
    ).grid(column=2, row=2, padx=(10, 0))
    
    # Center the frame in the window
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    return name_entry.get()

def main_window(root, frame):
    
    user = fetch_user()

    if (user is None):
        user = create_user(root, frame)

    if (user is None):
        print("Could not find or create user")
        # abort the program
        exit(1)

    # create the main window
    ttk.Label(frame, text=f"Hello, {user}!", font=("Helvetica", 16, "bold")).grid(column=0, row=0)
    ttk.Label(frame, text=f"Here is your todo list:").grid(column=0, row=1)


    return root, frame



def main():
    # create the main window, 100x100
    root = Tk()
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    frame = ttk.Frame(root, padding="10")
    frame.grid()
    root.title("TODO List")

    # call the main window
    main_window(root, frame)

    root.mainloop()

if __name__ == "__main__":
    main()