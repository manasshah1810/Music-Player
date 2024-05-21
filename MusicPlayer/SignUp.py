import mysql.connector
import tkinter as tk
from PIL import ImageTk, Image
import subprocess

def submit():
    try:
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="playlist_db")
        c1 = mydb.cursor()
        sql = "INSERT INTO login VALUES (%s, %s)"
        v1 = e1.get()
        v2 = e2.get()
        c1.execute(sql, (v1, v2))
        mydb.commit()
        print("Data inserted successfully")
        subprocess.Popen(["python", "Name.py"])
        mydb.close()
        exit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def clear():
    e1.delete(0, END)
    e2.delete(0, END)



root = tk.Tk()
root.geometry('436x806')
root.configure(bg='black')
root.title('Sign Up')

# Open and resize the image
image1 = Image.open('Music.webp')
image1 = image1.resize((300, 300))

# Convert Image object into PhotoImage object
image1 = ImageTk.PhotoImage(image1)

# Create and position the label for the image
label_image = tk.Label(root, image=image1, bg='black')
label_image.place(x=66, y=5)

# Create and position the label for text
l1 = tk.Label(root, text='Sign Up Now', bg='black', fg='white', font=('Comic Sans MS', 20, 'bold'))
l1.place(x=130, y=310)

l2 = tk.Label(root, text='Username', bg='black', fg='white', font=('Comic Sans MS', 25, 'bold'))
l2.place(x=55, y=390)

username= tk.StringVar()
e1 = tk.Entry(root,textvariable=username,width=30)
e1.place(x=230,y=410)

l3 = tk.Label(root, text='Password', bg='black', fg='white', font=('Comic Sans MS', 25, 'bold'))
l3.place(x=55, y=460)

password= tk.StringVar()
e2 = tk.Entry(root,textvariable=password,width=30,show='*')
e2.place(x=230,y=480)

b1 = tk.Button(root,text='Submit',bg='black',fg='white',highlightbackground='#fff',padx=5,pady=5,font=('Comic Sans MS', 15, 'bold'),command=submit)
b1.place(x=130,y=550)

btn1 = tk.Button(root, text="Clear", bg='black',fg='white',highlightbackground='#fff',padx=5,pady=5,font=('Comic Sans MS', 15, 'bold'),command=clear)
btn1.place(x=230,y=550)

root.mainloop()
