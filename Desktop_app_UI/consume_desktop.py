import base64
from io import BytesIO

import requests
import tkinter as tk
from tkinter import messagebox
import json
from tkinter import filedialog
from PIL import Image, ImageTk

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Post Sender App")
        #self.master.resizable(False, False)

        # User Input Label and field
        tk.Label(master, text="username:").grid(row=0)
        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=0, column=1, pady=10)

        # Password input label and field
        tk.Label(master, text="password:").grid(row=1)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=1, column=1)

        # Login button
        self.post_button_login = tk.Button(master, text="Login", command=self.login)
        self.post_button_login.grid(row=3, column=1, sticky="W")

        # Logout button
        self.post_button_logout = tk.Button(master, text="Logout", command=self.logout, state=tk.DISABLED)
        self.post_button_logout.grid(row=3, column=1, sticky="E")

        tk.Label(master, text="Profile Info", font=("Helvetica", 16, "bold")).grid(row=4, column=1)

        tk.Label(master, text="Slug   :").grid(row=5, column=0, padx=10, pady=5)
        self.what_label = tk.Label(master, text="What?")
        self.what_label.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(master, text="Location   :").grid(row=6, column=0, padx=10, pady=5)
        self.where_label = tk.Label(master, text="Where?")
        self.where_label.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(master, text="Job   :").grid(row=7, column=0, padx=10, pady=5)
        self.which_label = tk.Label(master, text="Which?")
        self.which_label.grid(row=7, column=1, padx=10, pady=5)

        tk.Label(master, text="Profile Picture   :").grid(row=8, column=0, padx=10, pady=5)
        self.profile_picture_label = tk.Label(master)
        self.profile_picture_label.grid(row=8, column=1, padx=10, pady=5)

        tk.Label(master, text="Send a post", font=("Helvetica", 16, "bold")).grid(row=9, column=1)

        # Caption input label and field
        title_label = tk.Label(master, text="Title:")
        title_label.grid(row=10)
        self.title_entry = tk.Text(master, width=30, height=1, state=tk.DISABLED)
        self.title_entry.grid(row=10, column=1)

        # Content input layer and field
        content_label = tk.Label(master, text="Content:")
        content_label.grid(row=11, pady=10)
        self.content_entry = tk.Text(master, width=30, height=5, state=tk.DISABLED)
        self.content_entry.grid(row=11, column=1, pady=10)

        # Create image upload button
        self.upload_button = tk.Button(master, text="Image", command=self.load_image, state=tk.DISABLED)
        self.upload_button.grid(row=12, column=0, pady=10)

        # Label for show image
        self.image_label = tk.Label(master)
        self.image_label.grid(row=12, column=1, pady=10)

        # SelectBar
        tk.Label(master, text="").grid(row=13, pady=10)
        self.category_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE, exportselection=False, height=3)
        self.category_listbox.insert(1, "Data Structures and Algorithms")
        self.category_listbox.insert(2, "Software Architecture")
        self.category_listbox.insert(3, "Database Management")
        self.category_listbox.grid(row=13, column=1)
        self.category_scrollbar = tk.Scrollbar(master)
        self.category_scrollbar.grid(row=13, column=2, sticky="NS", pady=10)
        self.category_listbox.config(yscrollcommand=self.category_scrollbar.set)
        self.category_scrollbar.config(command=self.category_listbox.yview)

        # Submit button
        self.post_button = tk.Button(master, text="Post ", command=self.post, state=tk.DISABLED)
        self.post_button.grid(row=13, pady=10)

        self.token = None
        self.csrftoken = None

        self._image = None

        self.profile_image_ = None

    def load_image(self):
            # File Open Screen
            file_path = filedialog.askopenfilename()

            # Get Image and Resize
            img = Image.open(file_path)
            img = self.resize(img, 150)

            # Show image in the label
            self.image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.image)

            # Convert image to base64
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())

            # Creating a request in JSON format
            self._image = encoded_string.decode('utf-8')

    def resize(self, img, height_):
        # Original size
        width, height = img.size

        new_height = height_

        # Calculate width to keep proportions
        new_width = int((new_height / height) * width)

        # Resize
        img = img.resize((new_width, new_height))

        return img


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Send POST request to login to API
        url = "http://127.0.0.1:8001/api/accounts/login/"
        data = {"username": username, "password": password}
        response = requests.post(url, data=data)

        if response.status_code == 200:
            self.token = response.cookies["sessionid"]
            self.csrftoken = response.cookies["csrftoken"]

            # Enable title, content, category and submit button
            self.post_button_logout.config(state="normal")
            self.post_button_login.config(state=tk.DISABLED)
            self.title_entry.config(state="normal")
            self.content_entry.config(state="normal")
            self.category_listbox.config(state="normal")
            self.post_button.config(state="normal")
            self.upload_button.config(state="normal")
            self.image_label.config(state="normal")

            messagebox.showinfo("success", "login")

            url = "http://127.0.0.1:8001/api/profiles"
            headers = {
                "Cookie": f"sessionid={self.token}; csrftoken={self.csrftoken}",
                "X-CSRFToken": self.csrftoken,
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:  # HTTP 200 OK
                response_data = response.json()
                image__ = response_data['data']['user_profile']['profile_img']
                image_url = "http://127.0.0.1:8001" + image__
                response = requests.get(image_url)
                img_ = Image.open(BytesIO(response.content))

                img_ = self.resize(img_, 50)

                self.profile_image_ = ImageTk.PhotoImage(img_)
                self.profile_picture_label.config(image=self.profile_image_)
                slug = response_data['data']['user_profile']['slug']
                location = response_data['data']['user_profile']['location']
                job = response_data['data']['user_profile']['job']
                self.what_label.config(text=slug)
                self.where_label.config(text=location)
                self.which_label.config(text=job)

            else:
                print("Error:", response.status_code, response.reason)

            return True
        else:
            messagebox.showerror("error", "login failed")
            return False

    def logout(self):
        # Send GET request to log out of API
        url = "http://127.0.0.1:8001/api/accounts/logout/"
        headers = {
            "Cookie": f"sessionid={self.token};csrftoken={self.csrftoken}",
            "X-CSRFToken": self.csrftoken
        }
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            # Delete token and csrftoken values
            self.token = None
            self.csrftoken = None

            # Disable title, content, category and submit button
            self.post_button_login.config(state="normal")
            self.post_button_logout.config(state=tk.DISABLED)
            self.title_entry.config(state=tk.DISABLED)
            self.content_entry.config(state=tk.DISABLED)
            self.category_listbox.config(state=tk.DISABLED)
            self.post_button.config(text="Post", state=tk.DISABLED, command=self.post)
            self.upload_button.config(state=tk.DISABLED)
            self.image_label.config(state=tk.DISABLED)

            self.profile_image_ = None
            self.image = None
            self.what_label.config(text="What?")
            self.where_label.config(text="Where?")
            self.which_label.config(text="Which?")

            messagebox.showinfo("success", "logout")
        else:
            messagebox.showerror("error", "logout failed")

    def post(self):
        image = self._image

        # Get title and content values
        title = self.title_entry.get("1.0", "end-1c")
        content = self.content_entry.get("1.0", "end-1c")

        # Kategorileri seç
        row_dict = {'Data Structures and Algorithms': 1, 'Software Architecture': 2, 'Database Management': 3}
        selected_categories = []
        for idx in self.category_listbox.curselection():
            row_text = self.category_listbox.get(idx)
            row_number = row_dict[row_text]
            selected_categories.append(row_number)

        # Send POST request to API
        url = "http://127.0.0.1:8001/api/posts"
        headers = {
            "Cookie": f"sessionid={self.token}; csrftoken={self.csrftoken}",
            "X-CSRFToken": self.csrftoken,
            "Content-Type": "application/json"
        }
        data = {
            "Title": title,
            "message": content,
            "select[]": selected_categories,
            "image": image
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)

        # İsteğin durumunu kontrol et
        if response.status_code == 201:

            messagebox.showinfo("success", "Posted")
        else:
            messagebox.showerror("error", "Post failed")


root = tk.Tk()
app = App(root)
root.mainloop()