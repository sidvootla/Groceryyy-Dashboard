from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk
from tkinter import messagebox
import tkmacosx as tkm
import mysql.connector
from tkmacosx import Button
from tkcalendar import DateEntry
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as font_manager

class Dashboard:
    def __init__(self,root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  
        self.f = None
        self.sideframecol = "#8d99ae"
        self.root.geometry("1600x900+0+0")
        self.bgcol = "#1a264d"
        self.searchval = StringVar()
        self.root.title("SK Grocery")
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.rootframe = Frame(self.root,bg="grey")
        self.rootframe.place(x=0,y=0,width=self.screen_width,height=self.screen_height)

        self.sideframe = Frame(self.rootframe,bg=self.sideframecol)
        self.sideframe.place(x=0,y=0,height=self.screen_height,width=300)

        self.menuframe = Frame(self.rootframe,bg="#11172b")
        self.menuframe.place(x=300,y=0,height=80,width=self.screen_width)
        self.lbltitle = Label(self.menuframe,text="SK GROCERY",bg="#11172b",fg='white',font=("charter",30,"bold"))
        self.lbltitle.place(x=20,y=20)
        self.dashboardframe = Frame(self.rootframe,bg=self.bgcol)
        self.dashboardframe.place(x=300,y=80,height=self.screen_height,width=self.screen_width)
        self.refresh_button = Button(self.menuframe, text="Refresh", command=self.refresh_dashboard,fg='white',borderless=1,background="red")
        self.refresh_button.place(x=900, y=20, height=40, width=100)
        self.logout_button = Button(self.menuframe, text="Log Out",fg='white',borderless=1,background="red",command=self.logout)
        self.logout_button.place(x=1010, y=20, height=40, width=100)


        # Initialize the dashboard
        self.refresh_dashboard()
        #-------------------SIDEFRAME--------------------------------------
        self.btn1_path = "dbdicn.png"
        self.btn1 = Image.open(self.btn1_path)
        self.btn1 = self.btn1.resize((32, 32))  # Resize the image if necessary
        self.photo = ImageTk.PhotoImage(self.btn1)
        self.button = tkm.Button(self.sideframe, text="             Dashboard",bg=self.sideframecol,activebackground=self.sideframecol,activeforeground='lightblue',bd =0,relief=FLAT,focuscolor='',borderless=1,anchor='w',command = self.df,fg='white',font=("Charter", 14,'bold'))
        self.button.place(x=45,y=400,height=50,width=200)
        self.lbl1btn = Label(self.sideframe,image=self.photo,bg=self.sideframecol)
        self.lbl1btn.place(x=55,y=410)
        
        self.btn2_path = "manage.png"
        self.btn2 = Image.open(self.btn2_path)
        self.btn2 = self.btn2.resize((32, 32))  # Resize the image if necessary
        self.photo1 = ImageTk.PhotoImage(self.btn2)
        self.button1 = tkm.Button(self.sideframe, text="             Manage",bg=self.sideframecol,activebackground=self.sideframecol,activeforeground='lightblue',focuscolor='',borderless=1,anchor='w',command=self.managepage,fg='white',font=("Charter", 14,'bold'))
        self.button1.place(x=45,y=450,height=50,width=200)
        self.lbl2btn = Label(self.sideframe,image=self.photo1,bg=self.sideframecol)
        self.lbl2btn.place(x=55,y=458)

        self.btn3_path = "settings.png"
        self.btn3 = Image.open(self.btn3_path)
        self.btn3 = self.btn3.resize((32, 32))  # Resize the image if necessary
        self.photo2 = ImageTk.PhotoImage(self.btn3)
        self.button2 = tkm.Button(self.sideframe, text="             Settings",bg=self.sideframecol,activebackground=self.sideframecol,activeforeground='lightblue',focuscolor='',borderless=1,anchor='w',fg='white',font=("Charter", 14,'bold'))
        self.button2.place(x=45,y=500,height=50,width=200)
        self.lbl3btn = Label(self.sideframe,image=self.photo2,bg=self.sideframecol)
        self.lbl3btn.place(x=55,y=508)

        self.btn4_path = "logout.png"
        self.btn4 = Image.open(self.btn4_path)
        self.btn4 = self.btn4.resize((32, 32))  # Resize the image if necessary
        self.photo3 = ImageTk.PhotoImage(self.btn4)
        self.button3 = tkm.Button(self.sideframe, text="             Exit",bg=self.sideframecol,activebackground=self.sideframecol,activeforeground='lightblue',focuscolor='',borderless=1,anchor='w',command=self.logout,fg='white',font=("Charter", 14,'bold'))
        self.button3.place(x=45,y=550,height=50,width=200)
        self.lbl4btn = Label(self.sideframe,image=self.photo3,bg=self.sideframecol)
        self.lbl4btn.place(x=55,y=558)


        self.usericn = Image.open("user.png")
        self.usericn = self.usericn.resize((130,130)) 
        self.photo4 = ImageTk.PhotoImage(self.usericn)
        self.lbl5 = Label(self.sideframe,image=self.photo4,bg=self.sideframecol)
        self.lbl5.place(x=78,y=200)
        self.date_label = Label(self.sideframe, font=("Charter", 16,'bold'), pady=10,bg=self.sideframecol,fg='white')
        self.time_label = Label(self.sideframe, font=("Charter", 16,'bold'), pady=10,bg=self.sideframecol,fg='white')
        self.date_label.pack()
        self.time_label.pack()
        self.lbl = Label(self.sideframe,bg=self.sideframecol,text="Sam",fg='white', font=("Charter", 18,'bold'))
        self.lbl.place(x=125,y=340)
        self.update_time()
        self.df()
    def logout(self):
        messagebox.showinfo("Success","Logged Out Successfully")
        self.on_close()
        self.root.destroy()
    def refresh_dashboard(self):
        # Clear the existing graphs
        for widget in self.dashboardframe.winfo_children():
            widget.destroy()

        # Update the data and redraw the graphs
        self.df()
        self.data()
    def deletepage(self):
        for frame in self.dashboardframe.winfo_children():
            frame.destroy()
    def indicate(self,lb,page):
        self.deletepage()
        page()
    def on_close(self):
        # Properly close and destroy the matplotlib graphs
        plt.close('all')
        self.root.destroy()
    def df(self):
        self.deletepage()
        self.mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sam19113',
            # port='3306',
            database='vegetable_vendor')
        self.cursor = self.mydb.cursor()
        self.cursor.execute("""
            SELECT vegetables.vegetable_name, SUM(sales.quantity) AS total_quantity, SUM(sales.price) AS total_sales
            FROM sales
            JOIN vegetables ON sales.vegetable_id = vegetables.id
            GROUP BY vegetables.vegetable_name
#         """)
        total_sales_by_vegetable = self.cursor.fetchall()
        vegetable_names = [row[0] for row in total_sales_by_vegetable]
        # print(vegetable_names)
        total_quantities = [row[1] for row in total_sales_by_vegetable]
        total_sales = [row[2] for row in total_sales_by_vegetable]
        self.fig1 = plt.figure(figsize=(1.4,1.3))  # Adjust the figure size as desired

        # Bar chart for Total Sales by Vegetable
        plt.subplot(111)
        plt.bar(vegetable_names, total_quantities)
        plt.xlabel('Vegetable', fontsize=8)  # Adjust the font size
        plt.ylabel('Total Quantity', fontsize=8)  # Adjust the font size
        # plt.title('Total Sales by Vegetable', fontsize=6)  # Adjust the font size

        # Adjust font size of tick labels
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)

        # Define font properties for legend text
        font_prop = font_manager.FontProperties(size=6)

        # Adjust font size of legend text if legend exists
        legend = plt.gca().get_legend()
        if legend is not None:
            plt.setp(legend.get_texts(), fontproperties=font_prop)
        

        self.canvas = FigureCanvasTkAgg(self.fig1, master=self.dashboardframe)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=140, y=30,height=270,width=270)

    #------
        self.fig2 = plt.figure(figsize=(1.4,1.3))
# Pie chart for Top Selling Vegetables
        plt.subplot(111)
        plt.pie(total_quantities, labels=vegetable_names, autopct='%1.1f%%',textprops={'fontsize': 7})
        # plt.title('Top Selling Vegetables',size=3)
        plt.axis('equal')
        self.canvas = FigureCanvasTkAgg(self.fig2, master=self.dashboardframe)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=446,y=30,height=270,width=270)


        #-------------------line graph
        self.fig3 = plt.figure(figsize=(1.4, 1.3))
        plt.subplot(111)
        plt.plot(vegetable_names, total_quantities, label='Total Quantity', linewidth=1)  # Adjust the line width
        plt.plot(vegetable_names, total_sales, label='Total Sales', linewidth=1)  # Adjust the line width
        plt.xlabel('Vegetable', fontsize=6)  # Adjust the font size
        plt.ylabel('Quantity/Sales', fontsize=6)  # Adjust the font size
        plt.title('Total Sales vs Total Quantity', fontsize=8)  # Adjust the font size
        plt.xticks(fontsize=6)  # Adjust the font size and rotation
        plt.yticks(fontsize=6)  # Adjust the font size

        # Define font properties for legend text
        font_prop = font_manager.FontProperties(size=6)

        # Adjust font size of legend text if legend exists
        legend = plt.gca().get_legend()
        if legend is not None:
            plt.setp(legend.get_texts(), fontproperties=font_prop)

        self.canvas2 = FigureCanvasTkAgg(self.fig3, master=self.dashboardframe)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().place(x=750, y=30,height=270,width=270)
        self.data()
    def update_time(self):
        current_time = datetime.now()
        date = current_time.strftime("%d/%m/%y")
        time = current_time.strftime("%H:%M:%S")
        self.date_label.config(text=date)
        self.time_label.config(text=time)
        self.root.after(1000, self.update_time)
        pass
    #___________________________________________________________________________
    def on_entersrh(self,e):
        self.search.delete(0,'end')
    def on_leavesrh(self,e):
        name = self.search.get()
        if(name==''):
            self.search.insert(0,'Search')

    def managepage(self):
        # plt.close()
        self.deletepage()
        # self.lb = Label(self.dashboardframe,text="hello")
        # self.lb.pack() 
        self.search = ttk.Entry(self.dashboardframe,font=("Charter",15,"bold"),textvariable=self.searchval)
        self.search.place(x=250,y=20,width=600,height=50)
        self.searchbtn = Button(self.dashboardframe, text="Search",fg='white',borderless=1,background="red",activebackground='red',activeforeground='lightblue',command=self.onsearch)
        self.searchbtn.place(x=870,y=20,height=50)
        if not self.search.get() == 'Search':
            self.search.delete(0,'end')
            self.search.insert(0,'Search')
        self.allbtn = Button(self.dashboardframe, text="All",fg='white',borderless=1,background="red",activebackground='red',activeforeground='lightblue',command=self.all)
        self.allbtn.place(x=150,y=18,height=53 )
        self.search.bind('<FocusIn>',self.on_entersrh)
        self.search.bind('<FocusOut>',self.on_leavesrh)
        self.tree = ttk.Treeview(self.dashboardframe,)
        self.style = ttk.Style()
        self.style.theme_use("aqua")
        self.style.configure(".",font=('Times,12'))
        self.tree["columns"] =  ("id", "vegetable_name", "price", "cost_price")
        self.tree['show'] = 'headings'
        self.hsb = ttk.Scrollbar(orient="horizontal")
        self.hsb.configure(command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.hsb.set)
        self.hsb.pack(fill=X,side=BOTTOM)


        # self.tree.heading("#0", text="")
        # self.tree.heading("#1", text="id")
        # self.tree.heading("#2", text="vegetable name")
        # self.tree.heading("#3", text="price")
        # self.tree.heading("#4", text="cost price")
        self.tree.column("id", width=75,anchor=CENTER)
        self.tree.column("vegetable_name", width=75,anchor=CENTER)
        self.tree.column("price", width=75,anchor=CENTER)
        self.tree.column("cost_price", width=75,anchor=CENTER)   
        self.tree.heading("id",text="id",anchor=CENTER)   
        self.tree.heading("vegetable_name",text="vegetable name",anchor=CENTER)   
        self.tree.heading("price",text="price",anchor=CENTER)   
        self.tree.heading("cost_price",text="cost price",anchor=CENTER)   

        # self.tree.column("#1", width=0)
        # self.tree.column("#2", width=0)
        # self.tree.column("#3", width=0)
        # self.tree.column("#4", width=0)
        # self.tree.column("#5", width=0)
        self.cursor = self.mydb.cursor()
        self.cursor.execute("select * from vegetables order by id ",)
        # self.veg = self.cursor.fetchall()
        i =0 
        for ro in self.cursor:
            self.tree.insert('',i,text="",values=(ro[0],ro[1],ro[2],ro[3]))
            i=i+1
        self.tree.place(x=155,y=150,height=300,width=700)

        self.insertbtn = Button(self.dashboardframe, text="Insert",fg='white',borderless=1,background="red",activebackground='red',activeforeground='lightblue',command=lambda:self.insertdata(self.tree))
        self.insertbtn.place(x=155,y=450,width=233,height=50)
        self.deletebtn = Button(self.dashboardframe, text="Delete",fg='white',borderless=1,background="red",activebackground='red',activeforeground='lightblue',command=self.deletion)
        self.deletebtn.place(x=388,y=450,width=233,height=50)
        self.updatebtn = Button(self.dashboardframe, text="Update",fg='white',borderless=1,background="red",activebackground='red',activeforeground='lightblue',command=self.selectdata)
        self.updatebtn.place(x=621,y=450,width=233,height=50)
    def insertdata(self,tree):
        if self.f:
            self.f.destroy()
        self.eidval = StringVar()
        self.enameval = StringVar()
        self.ecostval = DoubleVar()
        self.ecostpriceval = DoubleVar()
        self.f = Frame(self.dashboardframe,bg="grey")
        self.f.place(x=155,y=500,height=150,width=700)

        self.eid = ttk.Entry(self.f,font=("Charter",15,),textvariable=self.eidval,width=15)
        self.eidlbl = Label(self.f,text="Enter Id:",font=("Charter",15,),bg="grey")
        self.eidlbl.grid(column=0,row=0,padx=10,pady=10)
        self.eid.grid(column=1,row=0,padx=10,pady=10)

        self.enamelbl = Label(self.f,text="Enter Vegetable Name:",font=("Charter",15,),bg="grey")
        self.ename = ttk.Entry(self.f,font=("Charter",15,),textvariable=self.enameval,width=15)
        self.enamelbl.grid(column=2,row=0,padx=10,pady=10)
        self.ename.grid(column=3,row=0,padx=10,pady=10)

        self.ecost = ttk.Entry(self.f,font=("Charter",15,),textvariable=self.ecostval,width=15)
        self.ecostlbl = Label(self.f,text="Enter Cost:",font=("Charter",15,),bg="grey")
        self.ecostlbl.grid(column=0,row=1,padx=10,pady=10)
        self.ecost.grid(column=1,row=1,padx=10,pady=10)


        self.ecostprice = ttk.Entry(self.f,font=("Charter",15,),textvariable=self.ecostpriceval,width=15)
        self.ecostpricelbl = Label(self.f,text="Enter Cost Price:",font=("Charter",15,),bg="grey")
        self.ecostpricelbl.grid(column=2,row=1,padx=10,pady=10)
        self.ecostprice.grid(column=3,row=1,padx=10,pady=10)
        self.ecost.delete(0, END)
        self.ecostprice.delete(0, END)
        self.addbtn = Button(self.f, text="ADD", command=self.insertion,fg='white',borderless=1,background="red")
        self.addbtn.place(x=200,y=100,width=100,height=40)
        self.cancelbtn = Button(self.f, text="CANCEL", command=self.f.destroy,fg='white',borderless=1,background="red")
        self.cancelbtn.place(x=300,y=100,width=100,height=40)
    def insertion(self):
        self.cursor.execute("insert into vegetables(id,vegetable_name,price,cost_price) values (%s,%s,%s,%s)",(self.eidval.get(),self.ename.get(),self.ecost.get(),self.ecostprice.get()))
        print(self.eidval.get())
        self.mydb.commit()
        self.tree.insert('','end',text="",values=(self.eidval.get(),self.ename.get(),self.ecost.get(),self.ecostprice.get()))
        messagebox.showinfo("Success","Data Inserted Successfully")
        self.f.destroy()
        self.all()
    def onsearch(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("select * from vegetables where vegetable_name = %s",(self.search.get(),))
        self.veg = self.cursor.fetchall()
        for vegetable in self.veg:
            self.tree.insert("", "end", values=vegetable)
    def all(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("select * from vegetables")
        i=0
        for ro in self.cursor:
            self.tree.insert('',i,text="",values=(ro[0],ro[1],ro[2],ro[3]))
            i=i+1


    def deletion(self):
        self.selecteditem = self.tree.selection()[0]
        uid = self.tree.item(self.selecteditem)['values'][0]
        del_query = "Delete from vegetables where id = %s"
        sel_data = (uid,)
        self.cursor.execute(del_query,sel_data)
        self.mydb.commit()
        self.tree.delete(self.selecteditem)
        messagebox.showinfo("Success","Data Deleted Successfully")
        self.all()
    def selectdata(self):
        # self.f.destroy()
        if self.f:
            self.f.destroy()
        self.eidval = StringVar()
        self.enameval = StringVar()
        self.ecostval = DoubleVar()
        self.ecostpriceval = DoubleVar()
        self.curItem = self.tree.focus()
        self.values = self.tree.item(self.curItem,"values")
        # print(values)
        self.f = Frame(self.dashboardframe,bg="grey")
        self.f.place(x=155,y=500,height=150,width=700)

        self.eid = ttk.Entry(self.f,font=("Charter",15,),textvariable=self.eidval,width=15)
        self.eidlbl = Label(self.f,text="Enter Id:",font=("Charter",15,),bg="grey")
        self.eidlbl.grid(column=0,row=0,padx=10,pady=10)
        self.eid.grid(column=1,row=0,padx=10,pady=10)

        self.enamelbl = Label(self.f,text="Enter Vegetable Name:",font=("Charter",15,),bg="grey")
        self.ename = ttk.Entry(self.f,font=("Charter",15,),textvariable=self.enameval,width=15)
        self.enamelbl.grid(column=2,row=0,padx=10,pady=10)
        self.ename.grid(column=3,row=0,padx=10,pady=10)

        self.ecost = ttk.Entry(self.f,font=("Charter",15,),textvariable=self.ecostval,width=15)
        self.ecostlbl = Label(self.f,text="Enter Cost:",font=("Charter",15,),bg="grey")
        self.ecostlbl.grid(column=0,row=1,padx=10,pady=10)
        self.ecost.grid(column=1,row=1,padx=10,pady=10)


        self.ecostprice = ttk.Entry(self.f,font=("Charter",15,),textvariable=self.ecostpriceval,width=15)
        self.ecostpricelbl = Label(self.f,text="Enter Cost Price:",font=("Charter",15,),bg="grey")
        self.ecostpricelbl.grid(column=2,row=1,padx=10,pady=10)
        self.ecostprice.grid(column=3,row=1,padx=10,pady=10)
        self.ecost.delete(0, END)
        self.ecostprice.delete(0, END)
        self.update = Button(self.f, text="Update",fg='white',borderless=1,background="red",command = self.update_data)
        self.update.place(x=200,y=100,width=100,height=40)
        self.cancbtn = Button(self.f, text="CANCEL", command=self.f.destroy,fg='white',borderless=1,background="red")
        self.cancbtn.place(x=300,y=100,width=100,height=40)

        self.eid.insert(0,self.values[0])
        self.ename.insert(0,self.values[1])
        self.ecost.delete(0, END)
        self.ecost.insert(0,self.values[2])
        self.ecostprice.delete(0, END)
        self.ecostprice.insert(0,self.values[3])

    def update_data(self):
        self.tree.item(self.curItem,values=(self.eidval.get(),self.ename.get(),self.ecost.get(),self.ecostprice.get()))
        self.cursor.execute("UPDATE vegetables set vegetable_name=%s,price=%s,cost_price = %s where id = %s",(self.ename.get(),self.ecost.get(),self.ecostprice.get(),self.values[0]))
        self.mydb.commit()
        messagebox.showinfo("Success","Data Updated Successfully")
        self.f.destroy()
        self.all()



    def data(self):
        # self.deletepage()
        self.cursor.execute("""
        SELECT SUM(sales.price) AS total_sales
        FROM sales
    """)
        total_sales_by_vegetable = self.cursor.fetchall()
        self.dataframe = Frame(self.dashboardframe,bg=self.bgcol)
        self.dataframe.place(x=230,y=300,height=500,width=self.screen_width)
        self.data1 = Label(self.dataframe, text="TOTAL EARNINGS\n ₹ {:.2f}".format(total_sales_by_vegetable[0][0]),bg='#8B1874',font=("charter",20,"bold"),fg='white',height=8,width=18,bd=3,relief=RAISED)
        self.data1.grid(row=0,column=0,padx=10,pady=10)
        self.cursor.execute("""
        SELECT vegetables.vegetable_name, SUM(sales.quantity) AS total_quantity
FROM sales
JOIN vegetables ON sales.vegetable_id = vegetables.id
GROUP BY vegetables.vegetable_name
ORDER BY total_quantity DESC LIMIT 1;
    """)
        most_sold_product = self.cursor.fetchone()
        self.data3 = Label(self.dataframe, text="Most Sold Item\n "+most_sold_product[0],bg='#B71375',font=("charter",20,"bold"),fg='white',height=8,width=18,bd=3,relief=RAISED)
        self.data3.grid(row=0,column=1,padx=10,pady=10)
        self.cursor.execute("""
        SELECT vegetables.vegetable_name, SUM(sales.quantity) AS total_quantity
FROM sales
JOIN vegetables ON sales.vegetable_id = vegetables.id
GROUP BY vegetables.vegetable_name
ORDER BY total_quantity ASC LIMIT 1;
    """)
        least_sold_product = self.cursor.fetchone()
        self.data3 = Label(self.dataframe, text="Least Sold Item\n "+least_sold_product[0],bg='#FC4F00',font=("charter",20,"bold"),fg='white',height=8,width=18,bd=3,relief=RAISED)
        self.data3.grid(row=0,column=2,padx=10,pady=10)

        self.cursor.execute("SELECT SUM((p.price - p.cost_price) * s.quantity) AS total_profit FROM sales s INNER JOIN vegetables p ON s.vegetable_id = p.id;")
        self.profit = self.cursor.fetchone()
        self.data4 = Label(self.dataframe, text="Profit\n ₹"+str(self.profit[0]),bg='#4C3A51',font=("charter",20,"bold"),fg='white',height=8,width=18,bd=3,relief=RAISED)
        self.data4.grid(row=1,column=0,padx=10,pady=10)

        self.cursor.execute("SELECT SUM((p.cost_price) * s.quantity) AS total_profit FROM sales s INNER JOIN vegetables p ON s.vegetable_id = p.id;")
        self.expenditure = self.cursor.fetchone()
        self.data5 = Label(self.dataframe, text="Expenditure\n ₹"+str(self.expenditure[0]),bg='#774360',font=("charter",20,"bold"),fg='white',height=8,width=18,bd=3,relief=RAISED)
        self.data5.grid(row=1,column=1,padx=10,pady=10)
        

        self.profitp = (float(self.profit[0])/float(self.expenditure[0]))*100
        self.data6 = Label(self.dataframe, text="Profit Percentage\n "+str(format(self.profitp, ".2f"))+"%",bg='#B25068',font=("charter",20,"bold"),fg='white',height=8,width=18,bd=3,relief=RAISED)
        self.data6.grid(row=1,column=2,padx=10,pady=10)


        
class Login:
    def on_enter(self,e):
        self.username_entry.delete(0,'end')
    def on_leave(self,e):
        name = self.username_entry.get()
        if(name==''):
            self.username_entry.insert(0,'Username')
    def on_enterp(self,e):
        self.psswd_entry.delete(0,'end')
        self.psswd_entry.configure(show="•")
    def on_leavep(self,e):
        name = self.psswd_entry.get()
        if(name==''):
            self.psswd_entry.configure(show="")
            self.psswd_entry.insert(0,'Password')


    def on_enterfgt(self,e):
        self.answer_entry.delete(0,'end')
    def on_leavefgt(self,e):
        name = self.answer_entry.get()
        if(name==''):
            self.answer_entry.insert(0,'Answer')
    def on_enternw(self,e):
        self.newpass_entry.delete(0,'end')
        self.newpass_entry.configure(show="•")
    def on_leavenw(self,e):
        name = self.newpass_entry.get()
        if(name==''):
            self.newpass_entry.configure(show="")
            self.newpass_entry.insert(0,'New Password')
            
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#fff")
        self.root.geometry("462x500+550+200")
        self.root.resizable(False,False)
        self.root.title("SK Grocery")


        login_frame = Frame(root,bg="#11172b")
        self.root.configure(background="white")
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        login_frame.place(x=0, y=0, height=self.screen_height, width=self.screen_width / 3+10)
        bg_lbl = Label(login_frame, bg="#11172b")
        bg_lbl.place(x=0, y=0, height=self.screen_height, width=self.screen_width / 3+10)



        self.username = StringVar()
        self.password = StringVar()
        self.answer = StringVar()
        self.newpass = StringVar()
        
        # username = Label(login_frame,text = "USERNAME",font=("charter",15,"bold"),fg="white",bg="#11172b")
        # username.grid(column=0,row=0)
        self.username_entry = ttk.Entry(login_frame,font=("Charter",15,"bold"),textvariable=self.username)
        self.username_entry.place(x=80,y=150,width=300,height=50)
        self.username_entry.insert(0,'Username')
        self.username_entry.bind('<FocusIn>',self.on_enter)
        self.username_entry.bind('<FocusOut>',self.on_leave)
        # self.psswd = Label(login_frame,text = "PASSWORD",font=("charter",15,"bold"),fg="white",bg="#11172b")
        # self.psswd.grid(column=0,row=1)
        self.psswd_entry = ttk.Entry(login_frame,font=("Charter",15,"bold"),textvariable=self.password,)
        self.psswd_entry.place(x=80,y=210,width=300,height=50)

        self.psswd_entry.insert(0,'Password')
        self.psswd_entry.bind('<FocusIn>',self.on_enterp)
        self.psswd_entry.bind('<FocusOut>',self.on_leavep)
        b1 = Button(login_frame, text="Log In", font=("charter", 15,"bold"), fg="white", bg="red",borderless=1,command=self.log,borderwidth=0)
        b1.place(x=80,y=300,width=300,height=50)
        b2 = Button(login_frame, text="Forgot Password", font=("charter", 12,"bold"), fg="white", bg="#11172b",borderless=1,command=self.open_child_window)
        b2.place(x=270,y=265,width=110,height=30)
        # self.btn_book_add.grid(row=0,column=1,padx=1,pady=13)

    def open_child_window(self):
        if self.username.get()=="":
            messagebox.showerror("Error","Please enter username")
        conn = mysql.connector.connect(host='localhost',user="root",password="sam19113",database="Project")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from login where username=%s",(self.username.get(),))
        row = my_cursor.fetchone()
        if row== None:
             messagebox.showerror("Error","Please enter valid username")
        else:
            self.root2 = Toplevel()
            self.root2.title("Forgot Password")
            self.root2.geometry("400x430+580+250")
            self.root2.resizable(False,False)

            self.screen_width = root.winfo_screenwidth()
            self.screen_height = root.winfo_screenheight()
            fgtframe = Frame(self.root2)
            fgtframe.place(x=0,y=0,width=self.screen_height,height=self.screen_height)
            bgfgt = Label(fgtframe,bg="#11172b")
            bgfgt.place(x=0,y=0,width=self.screen_height,height=self.screen_height)
            l = Label(self.root2,text="Choose The Security Question",font=("charter", 13,"bold"), fg="white", bg="#11172b")
            l.place(x=110,y=80)
            self.combo_sec = ttk.Combobox(self.root2,state="readonly",font=("Charter",13,"bold")) 
            self.combo_sec["values"] = ("Select","Pet Name","Birth Place","First Teacher's Name")
            self.combo_sec.current(0)
            self.combo_sec.place(x=110,y=110,width=200,height=40)

            self.answer_entry = ttk.Entry(fgtframe,font=("Charter",12,"bold"),textvariable=self.answer)
            self.answer_entry.place(x=110,y=170,width=200,height=40)
            if not self.answer_entry.get() == 'Answer':
                self.answer_entry.delete(0,'end')
                self.answer_entry.insert(0,'Answer')
            
            self.answer_entry.bind('<FocusIn>',self.on_enterfgt)
            self.answer_entry.bind('<FocusOut>',self.on_leavefgt)

            self.newpass_entry = ttk.Entry(fgtframe,font=("Charter",12,"bold"),textvariable=self.newpass)
            self.newpass_entry.place(x=110,y=220,width=200,height=40)
            if not self.newpass_entry.get() == "New Password":
                self.newpass_entry.delete(0,'end')
                self.newpass_entry.insert(0, 'New Password')
            self.newpass_entry.bind('<FocusIn>',self.on_enternw)
            self.newpass_entry.bind('<FocusOut>',self.on_leavenw)

            b3 = Button(fgtframe, text="Reset", font=("charter", 13,"bold"), fg="white", bg="red",borderless=1,command=self.reset)
            b3.place(x=110,y=270,width=200,height=40)
    def reset(self):
        conn = mysql.connector.connect(host='localhost',user="root",password="sam19113",database="Project")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from login where username=%s and security_answer=%s",(self.username.get(),self.answer.get()))
        row = my_cursor.fetchone()
        if row== None:
            messagebox.showerror("Error","Answer is Invalid")
        else:
            my_cursor.execute("update login set password =%s where username=%s",(self.newpass.get(),self.username.get()))
            messagebox.showinfo("Success","Password Reset Successfully")
            conn.commit()
            conn.close()  
            self.root2.destroy()

    def log(self):
            if self.username.get()=="" or self.password.get()=="" or self.password.get()=="Password" or self.username.get()=="Username":
                messagebox.showerror("Error","All Fields are Required")
            else:
                conn = mysql.connector.connect(host='localhost',user="root",password="sam19113",database="Project")
                my_cursor = conn.cursor()
                my_cursor.execute("select * from login where username=%s and password=%s",(self.username.get(),self.password.get()))
                row = my_cursor.fetchone()
                if row== None:
                    messagebox.showerror("Error","Invalid User Id or Password")
                else:
                    messagebox.showinfo("Success","Logged in Successfully")
                    self.newhomewindow = Toplevel(self.root)
                    self.home = Dashboard(self.newhomewindow)
                conn.commit()
                conn.close()  


if __name__ == "__main__":
    root = Tk()
    app = Login(root)
    root.mainloop()
