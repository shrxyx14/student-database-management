from tkinter import *
import time
import ttkthemes
from tkinter import ttk ,messagebox,filedialog                            #helps in applying theme on button
from PIL import ImageTk
import pymysql
import pandas                                                             #converts datalist into tabular form

#functionality part

def toplevel_data(title,button_text,command):
    global idEntry,nameEntry,mobileEntry,emailEntry,addressEntry,genderEntry,dobEntry,screen,listdata
    screen = Toplevel()
    screen.title(title)
    screen.resizable(0, 0)
    screen.grab_set()

    idLabel = Label(screen, text='ID', font=('times new roman', 14))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)  # W for west
    idEntry = Entry(screen, font=('roman', 14))
    idEntry.grid(row=0, column=1, padx=30, pady=15)

    if(button_text=='Add' or button_text=='Update'):
        idEntry.config(state=DISABLED)

    nameLabel = Label(screen, text='Name', font=('times new roman', 14))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)  # W for west
    nameEntry = Entry(screen, font=('roman', 14))
    nameEntry.grid(row=1, column=1, padx=30, pady=15)

    mobileLabel = Label(screen, text='Mobile No', font=('times new roman', 14))
    mobileLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    mobileEntry = Entry(screen, font=('roman', 14))
    mobileEntry.grid(row=2, column=1, padx=30, pady=15)

    emailLabel = Label(screen, text='Email id', font=('times new roman', 14))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('roman', 14))
    emailEntry.grid(row=3, column=1, padx=30, pady=15)

    addressLabel = Label(screen, text='Address', font=('times new roman', 14))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(screen, font=('roman', 14))
    addressEntry.grid(row=4, column=1, padx=30, pady=15)

    genderLabel = Label(screen, text='Gender', font=('times new roman', 14))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(screen, font=('roman', 14))
    genderEntry.grid(row=5, column=1, padx=30, pady=15)

    dobLabel = Label(screen, text='D.O.B', font=('times new roman', 14))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(screen, font=('roman', 14))
    dobEntry.grid(row=6, column=1, padx=30, pady=15)

    screen_button = ttk.Button(screen,text=button_text,command=command)
    screen_button.grid(row=7, columnspan=2, pady=15)


    if(title=='Update Student'):
        indexing = studentTable.focus()
        content = studentTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        mobileEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])

def clock():
    date = time.strftime('%d/%m/%y')                       #Y for entire year
    currenttime = time.strftime('%H:%M:%S')
    #f is used to concatenate string with a variable
    datetimeLabel.config(text=f'    Date: {date} \n   Time: {currenttime}')
    #to continuous update time
    datetimeLabel.after(1000,clock)                    #in miliseconds


count=0
text=''
def slider():
    global text,count                                      #to update variable value inside the function
    if count==len(s):
        count = 0
        text = ''
    text = text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300,slider)

def connect_database():
    def connect():
        global mycursor,con
        try:
            con = pymysql.connect(host=hostEntry.get(),user=usernameEntry.get(),password=passwordEntry.get())
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error','Invalid Details!!',parent=connectWindow)
            return
        try:
            query = 'create database StudentManagementSystem'
            mycursor.execute(query)
            query = 'use StudentManagementSystem'
            mycursor.execute(query)
            query = 'create table student(id serial primary key, name varchar(50), mobile varchar(10),' \
            'email varchar(50), address varchar(100), gender varchar(20), dob varchar(20), date_added date, time_added time)'
            mycursor.execute(query)
        except:
            query = 'use StudentManagementSystem'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'Database Connection Established!', parent=connectWindow)
        connectWindow.destroy()
        addStudentButton.config(state=NORMAL)
        searchStudentButton.config(state=NORMAL)
        deleteStudentButton.config(state=NORMAL)
        updateStudentButton.config(state=NORMAL)
        showStudentButton.config(state=NORMAL)
        exportStudentButton.config(state=NORMAL)


    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0,0)

    hostnameLabel = Label(connectWindow,text='Host Name',font=('times new roman',20))
    hostnameLabel.grid(row=0,column=0,pady=15,padx=30)

    hostEntry = Entry(connectWindow,font=('roman',15),bd=2)
    hostEntry.grid(row=0,column=1,padx=30,pady=15)

    usernameLabel = Label(connectWindow, text='User Name', font=('times new roman', 20))
    usernameLabel.grid(row=1, column=0, pady=10, padx=30)

    usernameEntry = Entry(connectWindow, font=('roman', 15), bd=2)
    usernameEntry.grid(row=1, column=1, padx=30, pady=10)

    passwordLabel = Label(connectWindow, text='Password', font=('times new roman', 20))
    passwordLabel.grid(row=2, column=0, pady=10, padx=30)

    passwordEntry = Entry(connectWindow, font=('roman', 15), bd=2)
    passwordEntry.grid(row=2, column=1, padx=30, pady=10)

    connectButton = ttk.Button(connectWindow,text='CONNECT',command=connect)
    connectButton.grid(row=3,columnspan=2,pady=15)


def add_data():
    if(nameEntry.get()=='' or mobileEntry.get()=='' or emailEntry.get()=='' or addressEntry.get()=='' or genderEntry.get()=='' or dobEntry.get()==''):
        messagebox.showerror('Error','All fields are required!!',parent=screen)
    else:
        query='insert into student(name,mobile,email,address,gender,dob,date_added,time_added) values(%s,%s,%s,%s,%s,%s,current_date,current_time)'
        mycursor.execute(query,(nameEntry.get(),mobileEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get()))
        con.commit()
        result = messagebox.askyesno('Success','Data added successfully. Do you want to clean the form?',parent=screen)
        print(result)
        if result:
            idEntry.delete(0,END)
            nameEntry.delete(0,END)
            mobileEntry.delete(0, END)
            emailEntry.delete(0, END)
            addressEntry.delete(0, END)
            genderEntry.delete(0, END)
            dobEntry.delete(0, END)
        else:
            pass

        query = 'select * from student'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        print(fetched_data)
        studentTable.delete(*studentTable.get_children())
        #to convert tuple into a list
        for data in fetched_data:
            datalist = list(data)
            #insert data into Treeview
            #rootnode, every data to be inserted at the end, values inside datalist to be displayed
            studentTable.insert('',END,values=datalist)


def search_data():
    # name=%s or mobile=%s or email= %s or address=%s or gender=%s or dob=%s
    #nameEntry.get(),mobileEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get()
    query='Select * from student where id=%s or name=%s or mobile=%s or email=%s or address=%s or gender=%s or dob=%s'
    mycursor.execute(query,(idEntry.get(),nameEntry.get(),mobileEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:                                               #can be done with tuple also
        studentTable.insert('',END,values=data)

def delete_student():
    indexing = studentTable.focus()
    content = studentTable.item(indexing)               #content is dictionary
    content_id = content['values'][0]                                #values is key
    query = 'delete from student where id=%s'
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Deleted',f'ID {content_id} is deleted successfully!')
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('',END,values=data)

def update_data():
    query= "update student set name=%s,mobile=%s,email=%s,address=%s,gender=%s,dob=%s,date_added=current_date,time_added=current_time where id=%s"
    mycursor.execute(query,(nameEntry.get(),mobileEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get(),listdata[0]))
    con.commit()
    messagebox.showinfo('Success',f'Id {listdata[0]} is modified successfully!',parent=screen)
    screen.destroy()
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('',END,values=data)

def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studentTable.get_children()
    newlist = []
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    table = pandas.DataFrame(newlist,columns=['ID','Name','Mobile No','Email Id','Address','Gender','DOB','Added Date','Added Time'])
    #(path, to not see row nos. index=False)
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved successfully!')

def iexit():
    ans = messagebox.askyesno('Confirm','Are you sure you want to exit?')
    if ans:
        root.destroy()
    else:
        pass

#GUI Part
root = ttkthemes.ThemedTk()

root.get_themes()
root.set_theme('radiance')

root.geometry('1174x680+100+50')
root.resizable(0,0)
root.title('Student Management System')

datetimeLabel = Label(root,font=('times new roman',18))
datetimeLabel.place(x=5,y=5)
clock()
s = 'Student Management System'
sliderLabel = Label(root,font=('arial',30),width=30)
sliderLabel.place(x=237,y=5)
slider()

connectButton = ttk.Button(root,text='Connect to Database',command=connect_database)
connectButton.place(x=980,y=5)

leftFrame = Frame(root)
leftFrame.place(x=50,y=80,width=300,height=580)

logo_image = ImageTk.PhotoImage(file='students.png')
logo_Label = Label(leftFrame,image=logo_image)
logo_Label.grid(row=0,column=0)

#lambda otherwise the function will be called automatically
addStudentButton = ttk.Button(leftFrame,text='Add Student',width=25,state=DISABLED,command=lambda :toplevel_data('Add Student','Add',add_data))
addStudentButton.grid(row=1,column=0,pady=15)

searchStudentButton = ttk.Button(leftFrame,text='Search Student',width=25,state=DISABLED,command=lambda :toplevel_data('Search Student','Search',search_data))
searchStudentButton.grid(row=2,column=0,pady=15)

deleteStudentButton = ttk.Button(leftFrame,text='Delete Student',width=25,state=DISABLED,command=delete_student)
deleteStudentButton.grid(row=3,column=0,pady=15)

updateStudentButton = ttk.Button(leftFrame,text='Update Student',width=25,state=DISABLED,command=lambda :toplevel_data('Update Student','Update',update_data))
updateStudentButton.grid(row=4,column=0,pady=15)

showStudentButton = ttk.Button(leftFrame,text='Show Student',width=25,state=DISABLED,command=show_student)
showStudentButton.grid(row=5,column=0,pady=15)

exportStudentButton = ttk.Button(leftFrame,text='Export Data',width=25,state=DISABLED,command=export_data)
exportStudentButton.grid(row=6,column=0,pady=15)

exitButton = ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitButton.grid(row=7,column=0,pady=15)


rightFrame = Frame(root)
rightFrame.place(x=330,y=80,width=820,height=580)

scrollBarX = Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame,orient=VERTICAL)              #by default vertical

studentTable = ttk.Treeview(rightFrame,columns=('Id','Name','Mobile No.','Email','Address','Gender',
                                 'D.O.B','Added Date','Added Time'),
                            xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)
#configuring scrollbars
scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

#packing table and scrollbars to the frame
scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)
studentTable.pack(fill=BOTH,expand=1)

studentTable.heading('Id',text='ID')
studentTable.heading('Name',text='Name')
studentTable.heading('Mobile No.',text='Mobile No.')
studentTable.heading('Email',text='Email Address')
studentTable.heading('Address',text='Address')
studentTable.heading('Gender',text='Gender')
studentTable.heading('D.O.B',text='D.O.B')
studentTable.heading('Added Date',text='Added Date')
studentTable.heading('Added Time',text='Added Time')

studentTable.column('Id',width=60,anchor=CENTER)
studentTable.column('Name',width=150,anchor=CENTER)
studentTable.column('Mobile No.',width=150,anchor=CENTER)
studentTable.column('Email',width=200,anchor=CENTER)
studentTable.column('Address',width=150,anchor=CENTER)
studentTable.column('Gender',width=100,anchor=CENTER)
studentTable.column('D.O.B',width=150,anchor=CENTER)
studentTable.column('Added Date',width=150,anchor=CENTER)
studentTable.column('Added Time',width=150,anchor=CENTER)

style = ttk.Style()
#foreground,background,fieldbackground
style.configure('Treeview',rowheight=30,font=('times new roman',12),background='white',fieldbackground='white')
style.configure('Treeview.Heading',font=('times new roman',12))


studentTable.config(show='headings')


root.mainloop()