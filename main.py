from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- SEARCH THROUGH THE DATA -------------------------- #
def search_button():
    website_name = website_entry.get().lower()
    try:
        with open(file="data.json", mode="r") as file:
            my_data = json.load(file)
    except:
        messagebox.showinfo(title="No data file found", message="No data file found")
        pass
    else:
        if website_name in my_data:
            inf = f"Email: {my_data[website_name]['email']} \n" \
                  f"Password: {my_data[website_name]['password']}"
            messagebox.showinfo(title=website_name, message=inf)
        else:
            messagebox.showinfo(title="Site was not found", message="Site was not found")



# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list += [random.choice(letters) for char in range(nr_letters)]

    password_list += [random.choice(symbols) for char in range(nr_symbols)]

    password_list += [random.choice(numbers) for char in range(nr_numbers)]

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password_entry.get())


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_button():
    web_text = website_entry.get()
    mail_text = email_username_entry.get()
    pass_text = password_entry.get()
    new_data = {
        web_text: {
            "email": mail_text,
            "password": pass_text
        }
    }
    if web_text == '' or mail_text == '' or pass_text == '':
        messagebox.showerror(title="Error", message="You should not leave any fields empty")
    else:
        try:
            with open(file="data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open(file="data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open(file="data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(pady=20, padx=20)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

website_label = Label(text="Website: ")
website_label.grid(column=0, row=1)
website_entry = Entry(width=33)
website_entry.grid(column=1, row=1)
website_entry.focus()

search_button = Button(text="Search Button", command=search_button, width=14)
search_button.grid(column=2, row=1)

email_username_label = Label(text="Email/Username: ")
email_username_label.grid(column=0, row=2)
email_username_entry = Entry(width=51)
email_username_entry.insert(0, "example@mail.com")
email_username_entry.grid(column=1, row=2, columnspan=2)

password_label = Label(text="Password: ")
password_label.grid(column=0, row=3)
password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)

generate_password_button = Button(text="Generate Password", command=generate_password, width=14)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=43, command=add_button)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
