# This file is used to store the data for the todo list

import json

class Store:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_data(self):
        try:
            with open(self.file_name, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error getting data: {e}")
            return None

    def set_data(self, data):
        try:
            with open(self.file_name, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error setting data: {e}")