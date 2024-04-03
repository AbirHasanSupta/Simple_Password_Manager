from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generating_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
               't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letter = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letter + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    web = website_entry.get()
    em = email_entry.get()
    pas = password_entry.get()
    new_data = {
        web: {
            "email": em,
            "password": pas
        }
    }

    if len(web) == 0 or len(pas) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty!")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
        except:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- All List Show ------------------------------- #


def all_list():
    user_input = askstring("Info", "Enter the password to access your info.")
    if user_input == "password":
        try:
            with open("data.json", mode="r") as data_file:
                content = json.load(data_file)
                na = []

                for i, k in content.items():
                    ka = [f"Name: {i}, Email: {k["email"]}, Password: {k["password"]}"]
                    na += ka
                kak = "\n".join(na)
                messagebox.showinfo(title="All Passwords", message=f"{kak}")
        except:
            messagebox.showinfo(title="All Passwords", message="Your List is Empty.")
    else:
        messagebox.showerror(title="Oops", message="Wrong password!")

# ---------------------------- Empty List ------------------------------- #


def empty_list():
    user_input = askstring("Delete Info", "Enter the password to delete all your info.")
    if user_input == "password":
        with open("data.json", mode="w") as data_file:
            data_file.truncate()
        messagebox.showinfo(title="Important Information", message="Your Password list has been deleted")

    else:
        messagebox.showerror(title="Oops", message="Wrong password!")


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    search_data = website_entry.get()
    try:
        with open("data.json") as data_file:
            content = json.load(data_file)
    except:
        messagebox.showinfo(title="Error!", message="Password Manager is empty!")
    else:
        if search_data in content:
            messagebox.showinfo(title=search_data, message=f"Email: {content[search_data]["email"]} \n"
                                                f"Password: {content[search_data]["password"]} ")
        else:
            messagebox.showinfo(title="Oops!", message=f"No details for {search_data} exists.")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="#e7daf4")

canvas = Canvas(height=200, width=200, bg="#e4d5f3")
logo_photo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_photo)
canvas.grid(column=1, row=0)

website = Label(text="Website:", bg="#e7daf4")
website.grid(column=0, row=1)
email_username = Label(text="Email/Username:", bg="#e7daf4")
email_username.grid(column=0, row=2)
password_label = Label(text="Password:", bg="#e7daf4")
password_label.grid(column=0, row=3)

website_entry = Entry(width=33)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry = Entry(width=52)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "example@gmail.com")
password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)

generate_password = Button(text="Generate Password", command=generating_password, bg="#c7a7e9", highlightthickness=0)
generate_password.grid(column=2, row=3)
search = Button(text="Search", width=15, command=find_password, highlightthickness=0, bg="#c7a7e9")
search.grid(column=2, row=1)
add = Button(text="Add", width=42, command=save_password, highlightthickness=0, bg="#c7a7e9")
add.grid(column=1, row=4, columnspan=2)


show_list = Button(text="My Passwords", bg="#dd6e8b", command=all_list)
show_list.grid(row=6, column=2)
delete_list = Button(text="Empty list", bg="#dd6e8b", command=empty_list, font=("Ariel", 7, "bold"))
delete_list.grid(row=7, column=2)

window.mainloop()
