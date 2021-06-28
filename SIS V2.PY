from tkinter import *
from tkinter import ttk
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3


def Database():
    global conn, cursor
   
    conn = sqlite3.connect("student_database.db")
    cursor = conn.cursor()
   
    cursor.execute("""CREATE TABLE IF NOT EXISTS student (
        STU_ID TEXT,
        STU_NAME TEXT, 
        STU_GENDER TEXT, 
        STU_YEAR INTEGER, 
        STU_COURSE TEXT
        )""")


def register():
        Database()
        id=ID_text.get()
        name=Name_text.get()
        gender=Gender_text.get()
        course=Course_text.get()
        year=Year_text.get()

        if id=='' or name=='' or gender==''or course=='' or year=='':
            tkMessageBox.showinfo("Warning","fill the empty field!!!")
        else:
        
            conn.execute('INSERT INTO student (STU_ID,STU_NAME,STU_COURSE,STU_YEAR,STU_GENDER) VALUES (?,?,?,?,?)',(id,name,course,year,gender));
            conn.commit()
            tkMessageBox.showinfo("Message","Stored successfully")
            DisplayData()
            conn.close()

    

def Delete():
    Database()
    if not tree.selection():
        tkMessageBox.showwarning("Warning","Select data to delete")
    else:
        result =tkMessageBox.askquestion('Confirm', 'Are you sure you want to delete this record?',icon="warning")
        if result == 'yes':
            conn = sqlite3.connect("student_database.db")
            cursor = conn.cursor()
            for selecteditem in tree.selection():
                cursor.execute("DELETE FROM student WHERE STU_ID=?",(tree.set(selecteditem,'#1'),))
                conn.commit()
                tree.delete(selecteditem)
            conn.close()

def SearchRecord():
    Database()
    if Search_text.get() != "":
        tree.delete(*tree.get_children())
        cursor=conn.execute("SELECT * FROM student WHERE STU_ID LIKE ?", ('%' + str(Search_text.get()) + '%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def DisplayData():
    Database()
    tree.delete(*tree.get_children())
    cursor=conn.execute("SELECT * FROM student")
    fetch=cursor.fetchall()
    for data in fetch:
        tree.insert('','end',values=(data))
    cursor.close()
    conn.close()



def DisplayForm():

    def Exit():
            Exit=tkMessageBox.askyesno("Student Information System","Confirm if you want to exit")
            if Exit > 0:
                window.destroy()
                return

    def Clear():
        tree.delete(*tree.get_children())
        entry_search.delete(0,END)
        entry_name.delete(0,END)
        entry_gender.delete(0,END)
        entry_course.delete(0,END)
        entry_year.delete(0,END)
        entry_id.delete(0,END)
    
    def Update():
        d1=ID_text.get()
        d2=Name_text.get()
        d3=Gender_text.get()
        d4=Year_text.get()
        d5=Course_text.get()

        if not tree.selection():
            tkMessageBox.showwarning("Warning","Select data to delete")
        else:
            result =tkMessageBox.askquestion('Confirm', 'Are you sure you want to update this record?',icon="warning")
            if result == 'yes':
                for selected in tree.selection():
                    entry_id.insert(0,selected)
                    entry_name.insert(0,selected)
                    entry_gender.insert(0,selected)
                    entry_course.insert(0,selected)
                    entry_year.insert(0,selected)

                    conn = sqlite3.connect("student_database.db")
                    cursor = conn.cursor()
                    cursor=conn.execute("UPDATE student SET STU_ID=?,STU_NAME=?,STU_GENDER=?,STU_YEAR=?,STU_COURSE=? WHERE STU_ID=?",(d1,d2,d3,d4,d5,tree.set(selected,'#1')))
                    conn.commit()
                    cursor.close()
                    DisplayData()
                    conn.close()

        entry_search.delete(0,END)
        entry_name.delete(0,END)
        entry_gender.delete(0,END)
        entry_course.delete(0,END)
        entry_year.delete(0,END)
        entry_id.delete(0,END)

    
    def get_selected_row(event): 
        entry_search.delete(0,END)
        entry_name.delete(0,END)
        entry_gender.delete(0,END)
        entry_course.delete(0,END)
        entry_year.delete(0,END)
        entry_id.delete(0,END)

        selected=tree.focus()
        values=tree.item(selected,'values')
        entry_id.insert(0,values[0])
        entry_name.insert(0,values[1])
        entry_gender.insert(0,values[2])
        entry_year.insert(0,values[3])
        entry_course.insert(0,values[4])
        entry_name.focus()

    #----------------------------------------------------
    window= Tk()
    window.geometry("800x430")
    window.title("Student Information System")
    global tree
    global SEARCH
    global Name_text,Gender_text,Course_text,Year_text,ID_text,Search_text
    #-----------------------Label and Entries---------------------------------------------
    Name_text= StringVar()
    Gender_text= StringVar()
    Course_text= StringVar()
    Year_text= StringVar()
    ID_text= StringVar()
    Search_text=StringVar()

    label_name=Label(window,text="Name")
    label_name.grid(row=0,column=2)
    entry_name=Entry(window,textvariable=Name_text)
    entry_name.grid(row=0,column=3)

    label_gender=Label(window,text="Gender")
    label_gender.grid(row=1,column=2)
    entry_gender=Entry(window,textvariable=Gender_text)
    list1=['F','M']
    droplist = OptionMenu(window,Gender_text,*list1)
    droplist.config(width=15)
    Gender_text.set('F')
    droplist.grid(row=1,column=3)

    label_course=Label(window,text="Course")
    label_course.grid(row=0,column=4)
    entry_course=Entry(window,textvariable=Course_text)
    list3=['BSCS','BSIT','BSCA','BSBIO']
    droplist = OptionMenu(window,Course_text,*list3)
    droplist.config(width=15)
    Course_text.set('BSCS')
    droplist.grid(row=0,column=5)

    label_year=Label(window,text="Year level")
    label_year.grid(row=1,column=4)
    entry_year=Entry(window,textvariable=Year_text)
    list2=['1','2','3','4']
    droplist = OptionMenu(window,Year_text,*list2)
    droplist.config(width=15)
    Year_text.set('1')
    droplist.grid(row=1,column=5)

    label_id=Label(window,text="ID no.")
    label_id.grid(row=0,column=6)
    entry_id=Entry(window,textvariable=ID_text)
    entry_id.grid(row=0,column=7)

    label_space=Label(window,text="             ")
    label_space.grid(row=2,column=2)

    label_searchId=Label(window,text="ID no.")
    label_searchId.grid(row=3,column=3)
    entry_search=Entry(window,textvariable=Search_text)
    entry_search.grid(row=3,column=4)

    label_space1=Label(window,text="            ")
    label_space1.grid(row=4,column=0)

    #-----------------------BUTTONS-----------------
    button_search=Button(window,text="Search",width=12,command=SearchRecord)
    button_search.grid(row=3,column=5)

    button_display=Button(window,text="Display All",width=12, command=DisplayData)
    button_display.grid(row=6,column=2)

    button_add=Button(window,text="Add",width=12,command=register)
    button_add.grid(row=6,column=3)

    button_update=Button(window,text="Update",width=12,command=Update)
    button_update.grid(row=6,column=4)

    button_delete=Button(window,text="Delete",width=12,command=Delete)
    button_delete.grid(row=6,column=5)

    button_delete=Button(window,text="Clear",width=12,command=Clear)
    button_delete.grid(row=6,column=6)


    button_delete=Button(window,text="Exit",width=12,command=Exit)
    button_delete.grid(row=6,column=7)

    #--------------------------TREE VIEW------------------------
    tree = ttk.Treeview(window,selectmode='browse')
    tree.place(x=10,y=170)
    vsb= ttk.Scrollbar(window, orient ="vertical",command=tree.yview)
    vsb.place(x=769,y=170,height=225)
    tree.configure(yscrollcommand=vsb.set)
    tree.bind('<ButtonRelease-1>',get_selected_row)
    tree["columns"]=("1","2","3","4","5")

    tree["show"]="headings"
    tree.column("1",width =150,anchor='c') 
    tree.column("2",width =150,anchor='c') 
    tree.column("3",width =150,anchor='c') 
    tree.column("4",width =150,anchor='c')
    tree.column("5",width =150,anchor='c') 

    tree.heading("1",text="ID no.")
    tree.heading("2",text="Name")
    tree.heading("3",text="Gender")
    tree.heading("4",text="Year")
    tree.heading("5",text="Course")

    DisplayData()


DisplayForm()
if __name__=='__main__':
 mainloop()
