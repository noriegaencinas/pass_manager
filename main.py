from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
from cryptography.fernet import Fernet
import base64

def login():
    def verificar():
        username = username_entry.get()
        password = password_entry.get()

        # Verificar las credenciales (en este caso, simplemente verificamos si el usuario y la contraseña son "admin")
        if username == "admin" and password == "admin":
            # Abrir la ventana principal del administrador de contraseñas si las credenciales son correctas
            login_window.destroy()
            open_password_manager()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    # Crear la ventana de inicio de sesión
    login_window = Tk()
    login_window.title("Login")
    login_window.config(padx=20, pady=20)

    # Etiqueta y campo de entrada para el nombre de usuario
    username_label = Label(login_window, text="Username:")
    username_label.grid(column=0, row=0)
    username_entry = Entry(login_window, width=30)
    username_entry.grid(column=1, row=0)
    username_entry.focus()

    # Etiqueta y campo de entrada para la contraseña
    password_label = Label(login_window, text="Password:")
    password_label.grid(column=0, row=1)
    password_entry = Entry(login_window, width=30, show="*")
    password_entry.grid(column=1, row=1)

    # Botón de inicio de sesión
    login_button = Button(login_window, text="Login", command=verificar)
    login_button.grid(column=1, row=2)

    login_window.mainloop()

# ---------------------------- UI SETUP -------------------------------
def open_password_manager():
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
                # Obtener la contraseña cifrada del diccionario
                encrypted_password = my_data[website_name]['password']

                # Descifrar la contraseña
                key = load_or_generate_key()
                decrypted_password = decrypt_text(encrypted_password, key)

                # Mostrar la información con la contraseña descifrada
                inf = f"Email: {my_data[website_name]['email']} \n" \
                      f"Password: {decrypted_password}"
                messagebox.showinfo(title=website_name, message=inf)
            else:
                messagebox.showinfo(title="Site was not found", message="Site was not found")

    # ---------------------------- PASSWORD GENERATOR ------------------------------- #
    def generate_password():
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u',
                   'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                   'P',
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

    # ---------------------------- ENCRYPTION ------------------------------- #

    # Función para generar una clave de cifrado
    def generate_key():
        return Fernet.generate_key()

    # Función para cargar la clave de cifrado desde un archivo o generar una nueva si no existe
    def load_or_generate_key():
        try:
            with open("key.key", "rb") as key_file:
                key = key_file.read()
        except FileNotFoundError:
            key = generate_key()
            with open("key.key", "wb") as key_file:
                key_file.write(key)
        return key

    # Función para cifrar una cadena de texto
    def encrypt_text(text, key):
        f = Fernet(key)
        return f.encrypt(text.encode()).decode()

    # Función para descifrar una cadena de texto cifrada
    def decrypt_text(encrypted_text, key):
        f = Fernet(key)
        return f.decrypt(encrypted_text.encode()).decode()

    # ---------------------------- SAVE PASSWORD ------------------------------- #
    def add_button():
        web_text = website_entry.get()
        mail_text = email_username_entry.get()
        pass_text = password_entry.get()

        # Cifrar la contraseña antes de guardarla
        key = load_or_generate_key()
        encrypted_password = encrypt_text(pass_text, key)

        new_data = {
            web_text: {
                "email": mail_text,
                "password": encrypted_password
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

login()
