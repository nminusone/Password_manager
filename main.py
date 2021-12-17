from tkinter import *
from tkinter import messagebox
import random
from itertools import chain
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project

def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letter = [random.choice(letters) for num in range(nr_letters)]
    password_symbol = [random.choice(symbols) for x in range(nr_symbols)]
    password_number = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = list(chain(password_number, password_symbol, password_letter))
    # or just
    # password_list= password_number+ password_symbol+password_letter

    random.shuffle(password_list)
    password = "".join(password_list)
    # for char in password_list:
    #     password += char
    pass_entry.insert(0, f'{password}')
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = web_input.get()
    mail = username_entry.get()
    password = pass_entry.get()
    new_data = {website: {
        'email': mail,
        'password': password,
    }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title='Oops', message="Please don't leave any fields open")
    else:
        try:
            with open('data.json', 'r') as datafile:
                # json.dump(new_data, datafile, indent=4)
                # Reading old data
                data = json.load(datafile)
                data.update(new_data)
            with open('data.json', 'w') as datafile:
                json.dump(data, datafile, indent=4)
        except FileNotFoundError:
            with open('data.json', 'w') as datafile:
                # saving updated data
                json.dump(new_data, datafile, indent=4)
        finally:
            web_input.delete(0, END)
            pass_entry.delete(0, END)


def find_password():
    website = web_input.get()
    try:
        with open('data.json', 'r') as datafile:
            data = json.load(datafile)
    except FileNotFoundError:
        messagebox.showinfo(title='hol up', message='No Data File Found!')
    else:
        if website in data.keys():
            password = data[website]['password']
            email = data[website]['email']
            messagebox.showinfo(title=website, message=f'Email:{email}\nPassword:{password}')

        else:
            messagebox.showinfo(title='hol up', message=f'No details for that {website} exists')
    finally:
        web_input.delete(0, END)
        pass_entry.delete(0, END)


# ---------------------------- UI SETUP ---------------
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
bck_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=bck_img)
canvas.grid(row=0, column=1)

web_label = Label(text='Website:')
web_label.grid(row=1, column=0)

username_label = Label(text='Email/Username:')
username_label.grid(row=2, column=0)

pass_label = Label(text='Password:')
pass_label.grid(row=3, column=0)

web_input = Entry(width=35)
web_input.focus()
web_input.grid(row=1, column=1, columnspan=2, sticky='w')
web_input.get()

username_entry = Entry(width=54)
username_entry.insert(0, 'obmar2055@yahoo.com')
username_entry.grid(row=2, column=1, columnspan=2, sticky='w')
username_entry.get()

pass_entry = Entry(width=35)
pass_entry.grid(row=3, column=1, sticky='w')
pass_entry.get()

generate_button = Button(text='Generate Password', command=password_generator)
generate_button.grid(row=3, column=2, sticky='w')

add_button = Button(text='Add', width=45, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky='w')

search = Button(text='Search', command=find_password)
search.grid(row=1, column=2, columnspan=2, sticky='w')

window.mainloop()
