from tkinter import *
from tkinter import ttk
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3


def Database():
    global conn, cursor
   
    conn = sqlite3.connect("student_database.db")
    cursor = conn.cursor()
   
    command1="""CREATE TABLE IF NOT EXISTS student ( 

    	STU_ID INTEGER NOT NULL,
    	STU_NAME VARCHAR(100) NOT NULL, 
    	STU_GENDER VARCHAR(1)NOT NULL, 
    	STU_YEAR INTEGER NOT NULL, 
    	STU_COURSE VARCHAR(10)

    	)"""
    cursor.execute(command1)

    command2="""CREATE TABLE IF NOT EXISTS course(

    	STU_COURSE VARCHAR(10) NOT NULL,
    	COURSE VARCHAR(100) NOT NULL

    	)""" 
    cursor.execute(command2)

   



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
        cursor=conn.execute("SELECT STU_ID,STU_NAME,STU_GENDER,STU_YEAR,course.STU_COURSE,course.COURSE FROM student INNER JOIN course ON course.STU_COURSE=student.STU_COURSE WHERE STU_ID LIKE ?", ('%' + str(Search_text.get()) + '%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def DisplayData():
	Database()
	tree.delete(*tree.get_children())
	cursor=conn.execute("SELECT STU_ID,STU_NAME,STU_GENDER,STU_YEAR,course.STU_COURSE,course.COURSE FROM student INNER JOIN course ON course.STU_COURSE=student.STU_COURSE")
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

	def register():

		window1= Toplevel()
		window1.geometry("400x400")
		window1.title("Register Student")

		global entry_id,entry_name,entry_course,entry_gender,entry_year
		global droplist


		def Add():

			Database()
			id=ID_text.get()
			name=Name_text.get()
			gender=Gender_text.get()
			course=Course_text.get()
			year=Year_text.get()

			if id=='' or name=='' or gender==''or course=='' or year=='':
				tkMessageBox.showinfo("Warning","fill the empty field!")
				window1.destroy()
				register()
			else:
				conn.execute('INSERT INTO student (STU_ID,STU_NAME,STU_COURSE,STU_YEAR,STU_GENDER) VALUES (?,?,?,?,?)',(id,name,course,year,gender));
				conn.commit()
				tkMessageBox.showinfo("Message","Stored successfully")
				DisplayData()
				conn.close()
				entry_search.delete(0,END)
				entry_name.delete(0,END)
				entry_gender.delete(0,END)
				entry_course.delete(0,END)
				entry_year.delete(0,END)
				entry_id.delete(0,END)
				window1.destroy()
	

		label_id=Label(window1,text="ID no.")
		label_id.place(x=115,y=50)
		entry_id=Entry(window1,textvariable=ID_text)
		entry_id.place(x=155,y=50)

		label_name=Label(window1,text="Name")
		label_name.place(x=115,y=90)
		entry_name=Entry(window1,textvariable=Name_text)
		entry_name.place(x=155,y=90)

		label_gender=Label(window1,text="Gender")
		label_gender.place(x=109,y=125)
		entry_gender=Entry(window1,textvariable=Gender_text)
		list1=['F','M']
		droplist = OptionMenu(window1,Gender_text,*list1)
		droplist.config(width=15)
		Gender_text.set('F')
		droplist.place(x=150,y=120)

		label_course=Label(window1,text="Course")
		label_course.place(x=110,y=160)
		entry_course=Entry(window1,textvariable=Course_text)
		list2=['BSCS','BSIT','BSCA','BSIS']
		droplist= OptionMenu(window1,Course_text,*list2)
		droplist.config(width=15)
		Course_text.set('BSCS')
		droplist.place(x=150,y=160)

		label_year=Label(window1,text="Year level")
		label_year.place(x=120,y=190)
		entry_year=Entry(window1,textvariable=Year_text)
		list3=['1','2','3','4']
		droplist= OptionMenu(window1,Year_text,*list3)
		droplist.config(width=15)
		Year_text.set('1')
		droplist.place(x=150,y=190)

		button_add=Button(window1,text="Add",width=12,command=Add)
		button_add.place(x=150,y=280)

		window1.mainloop()
	
	def Update():

		if not tree.selection():
			tkMessageBox.showwarning("Warning","Select data to delete")
		else:
			result =tkMessageBox.askquestion('Confirm', 'Are you sure you want to update this record?',icon="warning")
			if result == 'yes':
				window2= Toplevel()
				window2.geometry("400x400")
				window2.title("Update Student")

				global entry_id,entry_name,entry_course,entry_gender,entry_year


				def update1():
					Database()
					d1=ID_text.get()
					d2=Name_text.get()
					d3=Gender_text.get()
					d4=Year_text.get()
					d5=Course_text.get()

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
					window2.destroy()
					



				label_id=Label(window2,text="ID no.")
				label_id.place(x=115,y=50)
				entry_id=Entry(window2,textvariable=ID_text)
				entry_id.place(x=155,y=50)
				label_name=Label(window2,text="Name")
				label_name.place(x=115,y=90)
				entry_name=Entry(window2,textvariable=Name_text)
				entry_name.place(x=155,y=90)

				label_gender=Label(window2,text="Gender")
				label_gender.place(x=109,y=125)
				entry_gender=Entry(window2,textvariable=Gender_text)
				list1=['F','M']
				droplist = OptionMenu(window2,Gender_text,*list1)
				droplist.config(width=15)
				Gender_text.set('F')
				droplist.place(x=150,y=120)
				
				label_course=Label(window2,text="Course")
				label_course.place(x=110,y=160)
				entry_course=Entry(window2,textvariable=Course_text)
				list2=['BSCS','BSIT','BSCA','BSIS']
				droplist= OptionMenu(window2,Course_text,*list2)
				droplist.config(width=15)
				Course_text.set('BSCS')
				droplist.place(x=150,y=160)
				
				label_year=Label(window2,text="Year level")
				label_year.place(x=95,y=199)
				entry_year=Entry(window2,textvariable=Year_text)
				list3=['1','2','3','4']
				droplist= OptionMenu(window2,Year_text,*list3)
				droplist.config(width=15)
				droplist.place(x=150,y=200)


				button_update=Button(window2,text="Update",width=12,command=update1)
				button_update.place(x=150,y=280)

				window2.mainloop()

	
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

	#--------------------------------------COURSE WINDOW-------------------------
	def Course_list():
		window3= Tk()
		window3.geometry("450x250")
		window3.title("Course List")

		def DisplayCourse():
			Database()
			tree2.delete(*tree2.get_children())
			cursor=conn.execute("SELECT * FROM course")
			fetch=cursor.fetchall()
			for data in fetch:
				tree2.insert('','end',values=(data))
			cursor.close()
			conn.close()


		#----------------------TREE---------------------------

		tree2= ttk.Treeview(window3,selectmode='browse')
		tree2.place(x=10,y=10)
		vsb= ttk.Scrollbar(window3, orient ="vertical",command=tree.yview)
		vsb.place(x=430,y=10,height=225)
		tree2.configure(yscrollcommand=vsb.set)
		tree2["columns"]=("1","2")

		tree2["show"]="headings"
		tree2.column("1",width =100,anchor='c') 
		tree2.column("2",width =300,anchor='c')

		tree2.heading("1",text="Course Code")
		tree2.heading("2",text="Course")

		DisplayCourse()

		window3.mainloop()





	#----------------------------------------------------
	window= Tk()
	window.geometry("800x430")
	window.title("Student Information System")
	global tree,tree2
	global SEARCH
	global Name_text,Gender_text,Course_text,Year_text,ID_text,Search_text,courselist_text


	Search_text=StringVar()
	Name_text= StringVar()
	Gender_text= StringVar()
	Course_text= StringVar()
	Year_text= StringVar()
	ID_text= StringVar()
	courselist_text=StringVar()

	

	entry_name=Entry(window,textvariable=Name_text)
	entry_gender=Entry(window,textvariable=Gender_text)
	entry_course=Entry(window,textvariable=Course_text)
	entry_year=Entry(window,textvariable=Year_text)
	entry_id=Entry(window,textvariable=ID_text)



	label_space=Label(window,text="             ")
	label_space.grid(row=2,column=2)

	label_searchId=Label(window,text="ID no.")
	label_searchId.grid(row=3,column=1)
	entry_search=Entry(window,textvariable=Search_text)
	entry_search.grid(row=3,column=2)

	label_space1=Label(window,text="            ")
	label_space1.grid(row=4,column=0)

	#-----------------------BUTTONS-----------------
	button_search=Button(window,text="Search",width=10,command=SearchRecord)
	button_search.grid(row=3,column=3)

	button_display=Button(window,text="Display All",width=12, command=DisplayData)
	button_display.place(x=120,y=100)

	button_add=Button(window,text="Add",width=12,command=register)
	button_add.place(x=260,y=100)

	button_update=Button(window,text="Update",width=12,command=Update)
	button_update.place(x=420,y=100)

	button_delete=Button(window,text="Delete",width=10,command=Delete)
	button_delete.grid(row=3,column=4)

	button_clear=Button(window,text="Clear",width=9,command=Clear)
	button_clear.place(x=620,y=130)

	button_exit=Button(window,text="Exit",width=9,command=Exit)
	button_exit.place(x=700,y=130)

	button_clear=Button(window,text="Course List",width=10,command=Course_list)
	button_clear.place(x=700,y=20)

	#--------------------------TREE VIEW------------------------


	tree = ttk.Treeview(window,selectmode='browse')
	tree.place(x=10,y=170)
	vsb= ttk.Scrollbar(window, orient ="vertical",command=tree.yview)
	vsb.place(x=769,y=170,height=225)
	tree.configure(yscrollcommand=vsb.set)
	tree.bind('<ButtonRelease-1>',get_selected_row)
	tree["columns"]=("1","2","3","4","5","6")

	tree["show"]="headings"
	tree.column("1",width =110,anchor='c') 
	tree.column("2",width =130,anchor='c') 
	tree.column("3",width =50,anchor='c') 
	tree.column("4",width =50,anchor='c')
	tree.column("5",width =100,anchor='c') 
	tree.column("6",width =310,anchor='c') 

	tree.heading("1",text="ID no.")
	tree.heading("2",text="Name")
	tree.heading("3",text="Gender")
	tree.heading("4",text="Year")
	tree.heading("5",text="Course Code")
	tree.heading("6",text="Course")


	DisplayData()


DisplayForm()
if __name__=='__main__':
 mainloop()
