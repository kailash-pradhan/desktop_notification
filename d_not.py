
from tkinter import *
from plyer import notification
from tkinter import messagebox
from PIL import Image, ImageTk
import time
from datetime import datetime
import mysql.connector



mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="notifications"
) 


t = Tk()
t.title('Notifier')
t.geometry("500x300")
img = Image.open("notify-label.png")
tkimage = ImageTk.PhotoImage(img)

def is_valid_datetime(dt_str):
    try:
        datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False
  
# get details
def get_details():
    get_title = title.get()
    get_msg = msg.get()
    get_time = time1.get() 
    # print(get_title,get_msg, tt)

    if get_title == "" or get_msg == "" or get_time == "":
        messagebox.showerror("Alert", "All fields are required!")
    else:
        if not is_valid_datetime(get_time):
            messagebox.showerror("Invalid Datetime", "Please enter a valid datetime in yyyy-mm-dd HH:MM:SS format.")
            return
        # convert entered datetime to datetime object
        entered_dt = datetime.strptime(get_time, '%Y-%m-%d %H:%M:%S')
        
        # get current datetime system
        current_dt = datetime.now()

        if entered_dt <= current_dt:
            messagebox.showerror("Invalid Datetime", "Please enter a datetime greater than the current datetime system.")
            return
        
        messagebox.showinfo("Success","Notification has been successfully set.")
        mycursor = mydb.cursor()
        sql = "INSERT INTO notifications (title, description, datetime) VALUES (%s, %s, %s)"
        val = (get_title, get_msg, get_time)
        mycursor.execute(sql, val)
        mydb.commit()



        
img_label = Label(t, image=tkimage).grid()

# Label - Title
t_label = Label(t, text="Title to Notify",font=("poppins", 10))
t_label.place(x=12, y=70)

# ENTRY - Title
title = Entry(t, width="25",font=("poppins", 13))
title.place(x=123, y=70)

# Label - Message
m_label = Label(t, text="Display Message", font=("poppins", 10))
m_label.place(x=12, y=120)

# ENTRY - Message
msg = Entry(t, width="40", font=("poppins", 13))
msg.place(x=123,height=30, y=120)

# Label - Time
time_label = Label(t, text="Set DateTime", font=("poppins", 10))
time_label.place(x=12, y=175)

# ENTRY - Time
time1 = Entry(t, width="25", font=("poppins", 13))
time1.place(x=123, y=175)

# Label - Time Constraint
time_label = Label(t, text="Please enter a valid datetime in yyyy-mm-dd HH:MM:SS format.", font=("poppins", 10))
time_label.place(x=12, y=200)





# Button
but = Button(t, text="SET NOTIFICATION", font=("poppins", 10, "bold"), fg="#ffffff", bg="#528DFF", width=20,
             relief="raised",
             command=get_details)
but.place(x=170, y=230)

t.resizable(0,0)
t.mainloop()

   