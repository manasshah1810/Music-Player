import mysql.connector
import tkinter as tk
from PIL import ImageTk, Image
import subprocess

def login():
    try:
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="playlist_db")
        c1 = mydb.cursor()
        username = e1.get()
        password = e2.get()
        sql = "SELECT * FROM login WHERE username = %s AND password = %s"
        c1.execute(sql, (username, password))
        result = c1.fetchone()
        if result:
            print("Login successful")
            subprocess.Popen(["python", "Name.py"])
            exit()
        else:
            l4.config(text="Invalid username or password")
        mydb.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def clear():
    e1.delete(0, tk.END)
    e2.delete(0, tk.END)
    l4.config(text="")

root = tk.Tk()
root.geometry('436x806')
root.configure(bg='black')
root.title('Login')

image1 = Image.open('Music.webp')
image1 = image1.resize((300, 300))
image1 = ImageTk.PhotoImage(image1)

label_image = tk.Label(root, image=image1, bg='black')
label_image.place(x=66, y=5)

l1 = tk.Label(root, text='Login', bg='black', fg='white', font=('Comic Sans MS', 20, 'bold'))
l1.place(x=180, y=310)

l2 = tk.Label(root, text='Username', bg='black', fg='white', font=('Comic Sans MS', 25, 'bold'))
l2.place(x=55, y=400)

e1 = tk.Entry(root, width=30)
e1.place(x=230, y=420)

l3 = tk.Label(root, text='Password', bg='black', fg='white', font=('Comic Sans MS', 25, 'bold'))
l3.place(x=55, y=460)

e2 = tk.Entry(root, width=30, show='*')
e2.place(x=230, y=480)

l4 = tk.Label(root, text='', bg='black', fg='white', font=('Comic Sans MS', 15, 'bold'))
l4.place(x=55, y=550)

b1 = tk.Button(root, text='Login', bg='black', fg='white', highlightbackground='#fff', padx=5, pady=5, font=('Comic Sans MS', 15, 'bold'), command=login)
b1.place(x=120, y=590)

btn1 = tk.Button(root, text="Clear", bg='black', fg='white', highlightbackground='#fff', padx=5, pady=5, font=('Comic Sans MS', 15, 'bold'), command=clear)
btn1.place(x=240, y=590)

root.mainloop()
