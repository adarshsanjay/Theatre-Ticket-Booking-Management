from tkinter import *
from tkinter import messagebox as msg
import mysql.connector as ms

#SQL Commands
myCon = ms.connect(host="localhost", user="root",passwd="root",port=3306)
myCur = myCon.cursor()
myCur.execute("create database if not exists project")
myCur.execute("use project")
myCur.execute("create table if not exists movies(moviename varchar(50), cost int(3))")
myCur.execute("create table if not exists admin(username varchar(15), password varchar(20))")
myCur.execute("create table if not exists shows(showtime varchar(5), movie varchar(50))")
myCur.execute("create table if not exists ticket_details(Username varchar(30), Mobile_number int(10), Movie_name varchar(30), Seats varchar(3),Cost varchar(5))")

#Entry Screen
def enterScreen():
    tk = Tk()
    tk.title("Mr.Ticket")
    tk.geometry("800x800")
    tk.configure(background="lavender")
    Button(tk, text="Admin Login", command=admin,padx=25, pady=19,bg='light blue',font=('Arial',12)).place(x=322, y=190)
    Button(tk,command=signinPage,text='Admin Sign-up',padx=20, pady=19,bg='light yellow',font=('Arial',12)).place(x=320, y=65)
    Button(tk,command=booking,text='Book tickets',padx=30, pady=19,bg='light green',font=('Arial',12)).place(x=320,y=320)
    Button(tk,command=avail,text='Available movies',padx=20,pady=20,bg='light pink',font=('Arial',12)).place(x=315,y=450)
    tk.mainloop()

#Admin Login Page
def loginPage():
    def submit(un, pwd):
        tk.destroy()
        myCur.execute("SELECT * FROM admin")
        value = myCur.fetchall()

        for i in range(len(value)):
            if value[i][0] == un:
                if value[i][1] == pwd:
                    msg.showinfo(title='Alert', message='Login successful')
                    main()
                    break

                else:
                    msg.showinfo(title='Alert', message='Incorrect password')
                    break
        else:
            msg.showinfo(title='Alert', message='User not registered')
    tk = Tk()
    tk.geometry("800x800")
    tk.configure(background="lavender")
    tk.title("Login")

    Label(tk, text="Enter username: ").place(x=5, y=10)
    un = Entry(tk)
    un.place(x=115, y=10)

    Label(tk, text="Enter password: ").place(x=5, y=55)
    pwd = Entry(tk, show='*')
    pwd.place(x=115, y=55)

    sub = Button(tk, text="Submit", command=lambda: submit(
        str(un.get()), str(pwd.get())))
    sub.place(x=5, y=105)

    tk.mainloop()

#Admin Sign-In Page
def signinPage():

    def submit(un, pwd):
        tk.destroy()
        myCur.execute("insert into admin values(%s,%s)", (un, pwd))
        myCon.commit()
        msg.showinfo(title='Alert', message='Sign up successful')

    tk = Tk()
    tk.geometry("800x800")
    tk.configure(background="lavender")
    tk.title("Sign Up")
    Label(tk, text="Enter username: ").place(x=5, y=10)
    un = Entry(tk)
    un.place(x=115, y=10)

    Label(tk, text="Enter password: ").place(x=5, y=55)
    pwd = Entry(tk, show='*')
    pwd.place(x=115, y=55)

    sub = Button(tk, text="Submit", command=lambda: submit(
        str(un.get()), str(pwd.get())))
    sub.place(x=5, y=105)

    tk.mainloop()

#Available Movies
def avail():
    tk = Tk()
    tk.geometry("800x800")
    tk.configure(background="lavender")
    myCur.execute("SELECT * FROM movies")

    i = 0
    for student in myCur:
        for j in range(len(student)):
            e = Entry(tk, width=15, fg='blue')
            e.grid(row=i, column=j)
            e.insert(END, student[j])
        i += 1

    Button(tk, command=booking, text="Go to booking screen",font=('Arial',10)).place(x=15, y=80)
    tk .mainloop()

#Ticket Booking Screen
def booking():
    tk = Tk()
    tk.geometry("800x800")
    tk.configure(background="lavender")
    tk.title("Booking")

    myCur.execute("SELECT * FROM movies")
    e = Label(tk, width=15, text='Slno', borderwidth=3,relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=0)

    e = Label(tk, width=18, text='Movie', borderwidth=3,relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=1)

    e = Label(tk, width=18, text='Cost', borderwidth=3,relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=2)

    i = 1
    for movieName in myCur:
        print(movieName)
        e = Entry(tk, width=15, fg='blue')
        e.grid(row=i, column=0)
        e.insert(END, i)
        e.config(state=DISABLED)

        b = Button(tk, text=movieName[0], width=15,
                   fg='blue', command=lambda k=movieName[0]: seat(k))
        b.grid(row=i, column=1)

        p = Entry(tk, width=18, fg='blue')
        p.grid(row=i, column=2)
        p.insert(END, movieName[1])
        p.config(state=DISABLED)

        i += 1

    tk.mainloop()

#Seat Selection
def seat(m):
    l = [m]
    def printin(o):
        l.append(o)
        print(l)
    tk = Tk()
    tk.title("Seats")
    for i in range(10):
        for j in range(10):
            s = Button(tk, text=chr(65+i)+str(j))
            s.config(command=lambda k = s['text']: printin(k))
            s.grid(row=i, column=j)	
    Button(tk,text='Done',command=lambda:pay(l)).grid()
    tk.mainloop()

#Payment Screen and Ticket details
def pay(l):
    def submit():
        cos=0
        myCur.execute("SELECT * FROM movies")
        result = myCur.fetchall()
        for row in result:
            if row[0]==l[0]:
                cos=(len(l)-1)*row[1]
        print(cos,len(l)-1)
        m=str(l[1:])
        msg.showinfo('TICKET','Name:' +name.get()+'\nMobile number:' +mobileno.get()+'\nMovie:' +l[0]+'\nSeats:' +m+'\nCost:' +str(cos))
        print(m)
        k=l[1:]
        for i in k:
            print(i)
            myCur.execute("Insert into ticket_details values(%s,%s,%s,%s,%s)",(name.get(),mobileno.get(),l[0],i,cos))
        myCon.commit()
    tk = Tk()
    tk.geometry("800x800")
    tk.configure(background="lavender")
    tk.title("Payment")
    Label(tk,text='Enter your name:',font=('Arial',13)).place(x=100,y=163)
    name=Entry(tk)
    name.place(x=250,y=166)
    Label(tk,text='Enter your mobile number:',font=('Arial',13)).place(x=100,y=220)
    mobileno=Entry(tk)
    mobileno.place(x=320,y=220)
    Button(tk,text='Submit',command=submit,padx=17,pady=10,font=('Arial',12)).place(x=100,y=280)
    tk.mainloop()

#Admin Login Verification
def admin():
    def adminLogin(un,id):
        tk.destroy()
        myCur.execute("SELECT * FROM admin")
        value = myCur.fetchall()
        print(value)
        for i in range(len(value)):
            if value[i][0] == un:
                if int(value[i][1]) == int(id):
                    msg.showinfo(title='Alert', message='Login successful')
                    adminPage()
                    break
                else:
                    msg.showinfo(title='Alert', message='Incorrect ID')
                    break
        else:
            msg.showinfo(title='Alert', message='User not registered')
    tk = Tk()
    tk.geometry("800x800")
    tk.configure(background="lavender")
    tk.title("Admin")
    Label(tk,text='Enter username',font=('Arial',12)).place(x=360,y=70)
    e1 = Entry(tk)
    e1.place(x=330,y=100,width=170,height=25)
    Label(tk,text='Enter password',font=('Arial',12)).place(x=360,y=150)
    e2 = Entry(tk,)
    e2.place(x=332,y=178,width=170,height=25) 
    Button(tk,command=lambda:adminLogin(e1.get(),e2.get()),text='Login',font=('Arial',15)).place(x=380,y=250)   
    tk.mainloop()

#Options for Admin to add and delete movies
def adminPage():
    tk = Tk()
    tk.geometry("800x800")
    tk.configure(background="lavender")
    tk.title("Admin")
    Button(tk,text='Add movie',command=addMovie,padx=20,pady=15,font=('Arial',13)).place(x=350,y=50)
    Button(tk,text='Delete movie',command=deleteMovie,padx=20,pady=16,font=('Arial',13)).place(x=343,y=140)
    Button(tk,text='Add show',command=addShow,padx=20,pady=14,font=('Arial',13)).place(x=352,y=240)
    Button(tk,text='Delete show',command=deleteShow,padx=20,pady=16,font=('Arial',13)).place(x=345,y=337)
    tk.mainloop()

#Adding Movies
def addMovie():
    def addMovieSubmit(moviename,cost):
        tk.destroy()
        myCur.execute("insert into movies values(%s,%s)",(moviename,cost))
        myCon.commit()
        msg.showinfo(title='Alert', message='Movie added successfully')
    

    tk = Tk()
    tk.geometry("800x800")
    tk.configure(background="lavender")
    tk.title("Add Movie")

    Label(tk, text="Movie Name: ").place(x=5, y=10)
    un = Entry(tk)
    un.place(x=115, y=10)

    Label(tk, text="Cost: ").place(x=5, y=55)
    pwd = Entry(tk)
    pwd.place(x=115, y=55)

    sub = Button(tk, text="Submit", command=lambda: addMovieSubmit(str(un.get()), str(pwd.get())))
    sub.place(x=5, y=105)

    tk.mainloop()

#Deleting Movies
def deleteMovie():
    def deleteMovieSubmit(moviename):
        tk.destroy()
        myCur.execute("delete from movies where movieName=%s",(moviename,))
        myCon.commit()
        msg.showinfo(title='Alert', message='Movie deleted successfully')
    
    tk = Tk()
    tk.geometry("800x800")
    tk.configure(background="lavender")
    tk.title("Delete Movie")

    Label(tk, text="Movie Name: ").place(x=5, y=10)
    un = Entry(tk)
    un.place(x=115, y=10)

    sub = Button(tk, text="Submit", command=lambda:deleteMovieSubmit(un.get()))
    sub.place(x=5, y=90)

    tk.mainloop()

def addShow():
    def addShowSubmit(showtime,movie):
        tk.destroy()
        myCur.execute("insert into shows values(%s,%s)",(showtime,movie))
        myCon.commit()
        msg.showinfo(title='Alert', message='Show added successfully')
    

    tk = Tk()
    tk.geometry("800x800")
    tk.configure(background="lavender")
    tk.title("Add Show")

    Label(tk, text="Show Time: ").place(x=5, y=10)
    un = Entry(tk)
    un.place(x=115, y=10)

    Label(tk, text="Movie Name: ").place(x=5, y=55)
    pwd = Entry(tk)
    pwd.place(x=115, y=55)

    sub = Button(tk, text="Submit", command=lambda: addShowSubmit(str(un.get()), str(pwd.get())))
    sub.place(x=5, y=105)

    tk.mainloop()

def deleteShow():
    def deleteShowSubmit(showtime):
        tk.destroy()
        myCur.execute("delete from shows where showTime=%s",(showtime,))
        myCon.commit()
        msg.showinfo(title='Alert', message='Show deleted successfully')
    

    tk = Tk()
    tk.geometry("800x800")
    tk.configure(background="lavender")
    tk.title("Delete Show")

    Label(tk, text="Show Time: ").place(x=5, y=10)
    un = Entry(tk)
    un.place(x=115, y=10)

    sub = Button(tk, text="Submit", command=lambda: deleteShowSubmit(str(un.get())))
    sub.place(x=5, y=105)


    tk.mainloop()

enterScreen()


