
from argparse import _MutuallyExclusiveGroup
from cgitb import text
import json
from multiprocessing.sharedctypes import Value
import random
import threading
import tkinter
import tkinter.messagebox
from PIL import ImageTk, Image
import tkinter.ttk
import mysql.connector
from pkg_resources import empty_provider
#--------------Global Declaration--------------------
global c_id
global atc_variable
global cart_dict
global fnv1,fnv2,fnv3,fnv4,fnv5
global fnv_list
global textExample
global addtocart
global quantity
global newwins1
global mycursor
global total_price
global prod
global s
global o, coupon_code
global fprice
global orderid,paymentid,reid
global delid
global quanid,prodid
global cid_already
delid=0
reid=0
paymentid=0
orderid=0
fprice={1:0,2:0,3:0}
total_price={1:[],2:[],3:[]}
top = tkinter.Tk()
top.title('Big Bazaar')
top.geometry('850x900')
top.resizable(width=0, height=0)
c_id=1
cid_already=False
with open('data.json', 'w') as f:
    print("")
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="Big_Bazaar"
)
mycursor = mydb.cursor(buffered=True)
cart_dict={}
coupon_code={"GETFLAT10":10,"LOYAL100":15,"GETDIS20":20}
def write_json(id,x,c_id,filename='cart.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        d=file_data[str(c_id)]
        d[id]=x
        file_data[str(c_id)]=d
        file.seek(0)
        json.dump(file_data, file, indent = 4)
#---------------------------------

fnv1=Image.open("Images/Lemon.png")
fnv2=Image.open("Images/Onion.png")
fnv3=Image.open("Images/tomato.png")
fnv4=Image.open("Images/capsicum.png")
fnv5=Image.open("Images/apple.png")

fnv_list=[fnv1,fnv2,fnv3,fnv4,fnv5]

c2_1 = Image.open("Images/Bread.png")
c2_2 = Image.open("Images/cupcake.png")
c2_3 = Image.open("Images/Pao.png")
global fnv_list2
fnv_list2 = [c2_1,c2_2,c2_3]

c3_1 = Image.open("Images/Milk.png")
c3_2 = Image.open("Images/Amul.png")
c3_3 = Image.open("Images/Cheese.png")
global fnv_list3
fnv_list3 = [c3_1,c3_2,c3_3]

c4_1 = Image.open("Images/Lays.png")
c4_2 = Image.open("Images/Namkeen.png")
c4_3 = Image.open("Images/df.png")
global fnv_list4
fnv_list4 = [c4_1,c4_2,c4_3]

c5_1 = Image.open("Images/Denimjeans.png")
c5_2 = Image.open("Images/T-shirt.png")
c5_3 = Image.open("Images/Shorts.png")
global fnv_list5
fnv_list5 = [c5_1,c5_2,c5_3]

c6_1 = Image.open("Images/Ipad.png")
c6_2 = Image.open("Images/Fitness.png")
c6_3 = Image.open("Images/Mobilephone.png")
global fnv_list6
fnv_list6 = [c6_1,c6_2,c6_3]
prod = {"Lemon":fnv1,"Onion":fnv2,"Tomato":fnv3,"Capsicum":fnv4,"Apple":fnv5
,"Bread":c2_1,"Cupcake":c2_2,"Pao":c2_3
,"Milk":c3_1,"Butter":c3_2,"Cheese":c3_3,
"CreamOnion":c4_1,"Namkeen":c4_2,"DarkFantasy":c4_3,
"DenimJeans":c5_1,"T-shirt":c5_2,"Shorts":c5_3,"IpadAir":c6_1,
"Fitnesstracker":c6_2,"Smartphone":c6_3}
quanid={1:[],2:[],3:[]}
prodid={1:[],2:[],3:[]}

#---------------------------------
#---------------------------------
path="Images/bigbazaarlogo.png"
temp=Image.open(path)
k=temp.resize((850,125),Image.Resampling.LANCZOS)
img=ImageTk.PhotoImage(k)
my_label=tkinter.Label(image=img)
my_label.pack()
#---------------------------------



textExample=tkinter.Text(top, height=1,width=20)
textExample.pack()
textExample.place(x=30,y=135)
result=textExample.get("1.0","end")
def addtocart():
    global quantity
    global c_id
    newwins1=tkinter.Toplevel(top,background="black")
    newwins1.title("Add to Cart")
    newwins1.geometry('300x270')
    temp=prod[str(atc_variable)]
    k=temp.resize((300,250),Image.Resampling.LANCZOS)
    img=ImageTk.PhotoImage(k)
    my_labell=tkinter.Label(newwins1,image=img)
    my_labell.pack()
    tkinter.Label(newwins1, text = str(atc_variable),background='orange').place(x = 30,y = 230) 
    tkinter.Label(newwins1, text = "Quantity",background='orange').place(x = 100,y = 230) 
    quantity = tkinter.Entry(newwins1,width = 4,selectbackground="blue",selectborderwidth='2px')
    quantity.place(x = 160,y = 233)

    def checkavail():
        global temp_price,atc_variable
        lp=["CreamOnion","IpadAir","DarkFantasy","DenimJeans","Fitnesstracker"]
        if atc_variable in lp:
            if atc_variable=="CreamOnion":
                atc_variable="Cream & Onion"
            if atc_variable=="IpadAir":
                atc_variable="Ipad Air"
            if atc_variable=="DarkFantasy":
                atc_variable="Dark Fantasy"
            if atc_variable=="DenimJeans":
                atc_variable="Denim Jeans"
            if atc_variable=="Fitnesstracker":
                atc_variable="Fitness tracker"

        mycursor.execute("select Quantity,Product_ID from Product where Item_name='%s'"%atc_variable)
        myresult = mycursor.fetchall()
        product_id = myresult[0][1]
        mycursor.execute("select json_value(Item_info,'$.Price') as state from Product where Item_name='%s'"%atc_variable)
        tuple_price = mycursor.fetchall()
        price=tuple_price[0][0]
        print(type(price))
        if myresult[0][0]<int(quantity.get()) :
            newwins1.destroy()
            tkinter.messagebox.showwarning("Not Available","Enter a valid Amount . Only "+str(myresult[0][0])+" units are Available !! ")
        else:
            tkinter.messagebox.showinfo("Cart Alert !!", "%s is Added to Cart"%atc_variable)
            remainder = myresult[0][0]-int(quantity.get())

            mycursor.execute("UPDATE Product SET Quantity = %d WHERE Item_name= '%s'"%(remainder,atc_variable))
            mycursor.execute("select * from Cart where Customer_ID= %d"%c_id)
            mycursor.execute("select Total_price from Cart where Customer_ID=%d"%c_id)
            temp_price = float(price)*int(quantity.get())
            total_price[c_id].append(temp_price)
            quanid[c_id].append(int(quantity.get()))
            prodid[c_id].append(atc_variable)
            print("this is prodid")
            print(prodid.get(c_id))
            write_json(str(product_id),int(quantity.get()),c_id)
    atc = tkinter.Button(newwins1,text ='Add to Cart',background="red",command=checkavail,height=2)
    atc.pack()
    atc.place(x=210,y=210)
    
    newwins1.mainloop()
    

def searchresult():
    global atc_variable
    result=textExample.get("1.0","end")
    if result.find(":stock") != -1:
        newwins1s=tkinter.Toplevel(top)
        newwins1s.title("Inventory")
        newwins1s.geometry('300x600')
        mycursor.execute("Select Item_name,Quantity,RANK () OVER ( Order BY Quantity DESC ) As Index_no From Product;")
        x=mycursor.fetchall()
        yx=20
        for i in range(0,len(x)):
            tkinter.Label(newwins1s, text = str(x[i]),background='orange',width=30).place(x = 50,y = yx) 
            yx=yx+25
            

    if result.find(":coupon") != -1:
        newwins1s=tkinter.Toplevel(top)
        newwins1s.title("Coupons")
        newwins1s.geometry('300x100')
        mycursor.execute("Select Coupon_name, Coupon_Discount,RANK () OVER ( Order BY Coupon_Discount Desc) As Index_no From Coupon_code;")
        x=mycursor.fetchall()
        yx=20
        for i in range(0,len(x)):

            tkinter.Label(newwins1s, text = str(x[i][0]),background='orange',width=10).place(x = 30,y = yx)
            tkinter.Label(newwins1s, text = str(x[i][1]),background='orange',width=10).place(x = 120,y = yx)
            tkinter.Label(newwins1s, text = str(x[i][2]),background='orange',width=10).place(x = 210,y = yx)
            yx=yx+25
    else:
        only_alpha = ""
        for char in result:
            if char.isalpha():
                only_alpha += char

        mycursor.execute("SELECT * FROM Product WHERE Item_name='%s'"%only_alpha)
        myresult = mycursor.fetchall()
        atc_variable=only_alpha
        addtocart()

B = tkinter.Button(top, text ="Search",bg='orange',height=1,width=10, command = searchresult)
B.pack()
B.place(x=200,y=132)

'''
Changing Images
'''

path1="Images/1.jpeg"
path2="Images/2.jpeg"
path3="Images/3.jpeg"
path4="Images/4.jpeg"
path5="Images/5.jpeg"
temp1=Image.open(path1)
temp2=Image.open(path2)
temp3=Image.open(path3)
temp4=Image.open(path4)
temp5=Image.open(path5)
k1=temp1.resize((830,250),Image.Resampling.LANCZOS)
k2=temp2.resize((830,250),Image.Resampling.LANCZOS)
k3=temp3.resize((830,250),Image.Resampling.LANCZOS)
k4=temp4.resize((830,250),Image.Resampling.LANCZOS)
k5=temp5.resize((830,250),Image.Resampling.LANCZOS)
img1=ImageTk.PhotoImage(k1)
img2=ImageTk.PhotoImage(k2)
img3=ImageTk.PhotoImage(k3)
img4=ImageTk.PhotoImage(k4)
img5=ImageTk.PhotoImage(k5)
global image_list, count
count = -1
image_list = [img1,img2,img3,img4,img5] 
my_canvas = tkinter.Canvas(top, width=920, height=250, highlightthickness=0)
my_canvas.pack(fill="both", expand=True)
my_canvas.create_image(0,0, image=image_list[0], anchor='nw')
my_canvas.place(x=12,y=165)
def next():
	global count
	if count == 4:
		my_canvas.create_image(0,0, image=image_list[0], anchor='nw')		
		count = 0
	else:
		my_canvas.create_image(0,0, image=image_list[count+1], anchor='nw')	
		count += 1

	top.after(3000, next)
next()

'''
Category buttons
'''

def fav():
    newwin = tkinter.Toplevel(top)
    newwin.title('Fruits & Vegetable')
    newwin.geometry("300x250") 
    newwin.resizable(0, 0)
    mycursor.execute("select * from Product where json_value(Item_info,'$.Category_ID')='1'")
    myresult = mycursor.fetchall()

    temp=Image.open("Images/fnv.png")
    img=ImageTk.PhotoImage(temp)
    my_label=tkinter.Label(newwin,image=img)
    my_label.pack()

    photo1 = tkinter.PhotoImage(file = r"Images/Lemon.png")
    photo2 = tkinter.PhotoImage(file = r"Images/Onion.png")
    photo3 = tkinter.PhotoImage(file = r"Images/Tomato.png")
    photo4 = tkinter.PhotoImage(file = r"Images/Capsicum.png")
    photo5 = tkinter.PhotoImage(file = r"Images/Apple.png")
    photoimage1 = photo1.subsample(7,8)
    photoimage2 = photo2.subsample(7,8)
    photoimage3 = photo3.subsample(13,25)
    photoimage4 = photo4.subsample(7,8)
    photoimage5 = photo5.subsample(7,8)

    def a():
        global atc_variable
        atc_variable="Lemon"
        addtocart()
    fb1= tkinter.Button(newwin,text="Lemon",image = photoimage1,command=a,compound = tkinter.LEFT)
    fb1.pack()
    fb1.place(x=0,y=25)

    def b():
        global atc_variable
        atc_variable="Onion"
        addtocart()
    fb2= tkinter.Button(newwin,text="Onion",image = photoimage2,command=b,compound = tkinter.LEFT)
    fb2.pack()
    fb2.place(x=0,y=65)

    def c():
        global atc_variable
        atc_variable="Tomato"
        addtocart()
    fb3= tkinter.Button(newwin,text="Tomato",image = photoimage3,command=c,compound = tkinter.LEFT)
    fb3.pack()
    fb3.place(x=0,y=105)

    def d():
        global atc_variable
        atc_variable="Capsicum"
        addtocart()
    fb4= tkinter.Button(newwin,text="Capsicum",image = photoimage4,command=d,compound = tkinter.LEFT)
    fb4.pack()
    fb4.place(x=0,y=150)

    def e():
        global atc_variable
        atc_variable="Apple"
        addtocart()
    fb5= tkinter.Button(newwin,text="Apple",image = photoimage5,command=e,compound = tkinter.LEFT)
    fb5.pack()
    fb5.place(x=0,y=190)

    print(myresult)
    def delwindow():
        newwin.destroy()
    button = tkinter.Button(newwin,text ='Click and Quit',command=delwindow)
    button.pack()
    button.place(x=200,y=215)
    newwin.mainloop()
def bky():
    newwin = tkinter.Toplevel(top)
    newwin.title('Bakery')
    newwin.geometry("200x200") 
    newwin.resizable(0, 0) 
    temp=Image.open("Images/Bakery.png")
    img=ImageTk.PhotoImage(temp)
    my_label=tkinter.Label(newwin,image=img)
    my_label.pack()
    photo2 = tkinter.PhotoImage(file = r"Images/cupcake.png")
    photo3 = tkinter.PhotoImage(file = r"Images/Pao.png")
    photoimage2 = photo2.subsample(7,8)
    photoimage3 = photo3.subsample(7,8)
    def a():
        global atc_variable
        atc_variable="Bread"
        addtocart()
    photo1 = tkinter.PhotoImage(file = r"Images/Bread.png")
    photoimage1 = photo1.subsample(6,10)
    fb1= tkinter.Button(newwin,text="Bread",image = photoimage1,command=a,compound = tkinter.LEFT,background="orange")
    fb1.pack()
    fb1.place(x=0,y=65)

    def b():
        global atc_variable
        atc_variable="Cupcake"
        addtocart()
    fb2= tkinter.Button(newwin,text="cupcake",image = photoimage2,command=b,compound = tkinter.LEFT,background="orange")
    fb2.pack()
    fb2.place(x=0,y=100)

    def c():
        global atc_variable
        atc_variable="Pao"
        addtocart()
    fb3= tkinter.Button(newwin,text="Pao",image = photoimage3,command=c,compound = tkinter.LEFT,background="orange")
    fb3.pack()
    fb3.place(x=0,y=140)
    def delwindow():
        newwin.destroy()
    button = tkinter.Button(newwin,text ='Click and Quit',command=delwindow)
    button.pack()
    button.place(x=100,y=170)
    newwin.mainloop()
def dry():
    newwin = tkinter.Toplevel(top)
    newwin.title('Dairy')
    newwin.geometry("300x200") 
    newwin.resizable(0, 0)
    #mycursor.execute("select * from Product where json_value(Item_info,'$.Category_ID')='1'")
    #myresult = mycursor.fetchall()
    temp=Image.open("Images/Dairy.png")
    img=ImageTk.PhotoImage(temp)
    my_label=tkinter.Label(newwin,image=img)
    my_label.pack()
    photo1 = tkinter.PhotoImage(file = ("Images/Milk.png"))
    photo2 = tkinter.PhotoImage(file = ("Images/Butter.png"))
    photo3 = tkinter.PhotoImage(file = ("Images/Cheese.png"))

    photoimage1 = photo1.subsample(7,7)
    photoimage2 = photo2.subsample(7,7)
    photoimage3 = photo3.subsample(7,7)

    def a():
        global atc_variable
        atc_variable="Milk"
        addtocart()
    fb1= tkinter.Button(newwin,text="Milk",image = photoimage1,command=a,compound = tkinter.LEFT)
    fb1.pack()
    fb1.place(x=0,y=55)

    def b():
        global atc_variable
        atc_variable="Butter"
        addtocart()
    fb2= tkinter.Button(newwin,text="Amul",image = photoimage2,command=b,compound = tkinter.LEFT)
    fb2.pack()
    fb2.place(x=0,y=105)

    def c():
        global atc_variable
        atc_variable="Cheese"
        addtocart()
    fb3= tkinter.Button(newwin,text="Cheese",image = photoimage3,command=c,compound = tkinter.LEFT)
    fb3.pack()
    fb3.place(x=0,y=150)
    def delwindow():
        newwin.destroy()
    button = tkinter.Button(newwin,text ='Click and Quit',command=delwindow)
    button.pack()
    button.place(x=200,y=165)
    newwin.mainloop()
def snks():
    newwin = tkinter.Toplevel(top)
    newwin.title('Snacks')
    newwin.geometry("250x200") 
    newwin.resizable(0, 0) 
    temp=Image.open("Images/Snacks.png")
    img=ImageTk.PhotoImage(temp)
    my_label=tkinter.Label(newwin,image=img)
    my_label.pack()
    photo2 = tkinter.PhotoImage(file = r"Images/Lays.png")
    photo3 = tkinter.PhotoImage(file = r"Images/df.png")
    photoimage2 = photo2.subsample(7,8)
    photoimage3 = photo3.subsample(7,8)
    def a():
        global atc_variable
        atc_variable="Namkeen"
        addtocart()
    photo1 = tkinter.PhotoImage(file = r"Images/Namkeen.png")
    photoimage1 = photo1.subsample(6,6)
    fb1= tkinter.Button(newwin,text="Namkeen",image = photoimage1,command=a,compound = tkinter.LEFT,background="orange")
    fb1.pack()
    fb1.place(x=0,y=45)

    def b():
        global atc_variable
        atc_variable="CreamOnion"
        addtocart()
    fb2= tkinter.Button(newwin,text="Cream & Onion",image = photoimage2,command=b,compound = tkinter.LEFT,background="orange")
    fb2.pack()
    fb2.place(x=0,y=80)

    def c():
        global atc_variable
        atc_variable="DarkFantasy"
        addtocart()
    fb3= tkinter.Button(newwin,text="Dark Fantasy",image = photoimage3,command=c,compound = tkinter.LEFT,background="orange")
    fb3.pack()
    fb3.place(x=0,y=120)
    def delwindow():
        newwin.destroy()
    button = tkinter.Button(newwin,text ='Click and Quit',command=delwindow)
    button.pack()
    button.place(x=100,y=170)
    newwin.mainloop()

def clths():
    newwin = tkinter.Toplevel(top)
    newwin.title('Snacks')
    newwin.geometry("250x200") 
    newwin.resizable(0, 0) 
    temp=Image.open("Images/Clothes.png")
    img=ImageTk.PhotoImage(temp)
    my_label=tkinter.Label(newwin,image=img)
    my_label.pack()
    photo2 = tkinter.PhotoImage(file = r"Images/T-shirt.png")
    photo3 = tkinter.PhotoImage(file = r"Images/Shorts.png")
    photoimage2 = photo2.subsample(6,7)
    photoimage3 = photo3.subsample(6,7)
    def a():
        global atc_variable
        atc_variable="DenimJeans"
        addtocart()
    photo1 = tkinter.PhotoImage(file = r"Images/Denimjeans.png")
    photoimage1 = photo1.subsample(15,35)
    fb1= tkinter.Button(newwin,text="Denim Jeans",image = photoimage1,command=a,compound = tkinter.LEFT,background="orange")
    fb1.pack()
    fb1.place(x=0,y=25)

    def b():
        global atc_variable
        atc_variable="T-shirt"
        addtocart()
    fb2= tkinter.Button(newwin,text="T-shirt",image = photoimage2,command=b,compound = tkinter.LEFT,background="orange")
    fb2.pack()
    fb2.place(x=0,y=80)

    def c():
        global atc_variable
        atc_variable="Shorts"
        addtocart()
    fb3= tkinter.Button(newwin,text="Shorts",image = photoimage3,command=c,compound = tkinter.LEFT,background="orange")
    fb3.pack()
    fb3.place(x=0,y=130)
    def delwindow():
        newwin.destroy()
    button = tkinter.Button(newwin,text ='Click and Quit',command=delwindow)
    button.pack()
    button.place(x=100,y=170)
    newwin.mainloop()
def elc():
    newwin = tkinter.Toplevel(top)
    newwin.title('Electronics')
    newwin.geometry("250x200") 
    newwin.resizable(0, 0) 
    temp=Image.open("Images/elec.png")
    img=ImageTk.PhotoImage(temp)
    my_label=tkinter.Label(newwin,image=img)
    my_label.pack()
    photo2 = tkinter.PhotoImage(file = r"Images/Fitness.png")
    photo3 = tkinter.PhotoImage(file = r"Images/Mobilephone.png")
    photoimage2 = photo2.subsample(6,7)
    photoimage3 = photo3.subsample(6,7)
    def a():
        global atc_variable
        atc_variable="IpadAir"
        addtocart()
    photo1 = tkinter.PhotoImage(file = r"Images/Ipad.png")
    photoimage1 = photo1.subsample(8,9)
    fb1= tkinter.Button(newwin,text="Ipad Air",image = photoimage1,command=a,compound = tkinter.LEFT,background="orange")
    fb1.pack()
    fb1.place(x=0,y=25)

    def b():
        global atc_variable
        atc_variable="Fitnesstracker"
        addtocart()
    fb2= tkinter.Button(newwin,text="Fitness tracker",image = photoimage2,command=b,compound = tkinter.LEFT,background="orange")
    fb2.pack()
    fb2.place(x=0,y=60)

    def c():
        global atc_variable
        atc_variable="Smartphone"
        addtocart()
    fb3= tkinter.Button(newwin,text="Smartphone",image = photoimage3,command=c,compound = tkinter.LEFT,background="orange")
    fb3.pack()
    fb3.place(x=0,y=110)
    def delwindow():
        newwin.destroy()
    button = tkinter.Button(newwin,text ='Click and Quit',command=delwindow)
    button.pack()
    button.place(x=100,y=170)
    newwin.mainloop()

class create_dict(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value
def getkeys(c_id,filename='cart.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        dict=file_data[str(c_id)]
        s=list(dict.keys())
        return s
def get_values(c_id,filename='cart.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        dict=file_data[str(c_id)]
        o=list(dict.values())
        return o
fv   = tkinter.Button(top, text ="F & V",bg='orange',height=1,width=10, command = fav)
bry  = tkinter.Button(top, text ="Bakery",bg='orange',height=1,width=10, command = bky)
dary = tkinter.Button(top, text ="Dairy",bg='orange',height=1,width=10, command = dry)
snk  = tkinter.Button(top, text ="Snacks",bg='orange',height=1,width=10, command = snks)
clth = tkinter.Button(top, text ="Clothes",bg='orange',height=1,width=10, command = clths)
elec = tkinter.Button(top, text ="Electronics",bg='orange',height=1,width=10, command = elc)
s=getkeys(c_id)
o=get_values(c_id)
fv.pack()
fv.place(x=440,y=132)
bry.pack()
bry.place(x=520,y=132)
dary.pack()
dary.place(x=600,y=132)
snk.pack()
snk.place(x=680,y=132)
clth.pack()
clth.place(x=760,y=132)
elec.pack()
elec.place(x=370,y=132)

#----------------Cart-------------------


def jsonadd(c_id,filename='cart.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        dict=file_data[str(c_id)]
        mycursor.execute("INSERT INTO cart (Customer_ID,Item_info, Total_price) VALUES(%d,'{}',%d)"%(c_id,sum(total_price[c_id])))
        insert = "UPDATE cart SET Item_info = %s WHERE Customer_ID="+str(c_id)+";"
        mycursor.execute(insert, (json.dumps(dict),))

        print("Done")
        return 1
        #mycursor.execute(insert, (json.dumps(new_blog),))

def jsonupdate(c_id,filename='cart.json'):
    with open(filename,'r+') as file:   
        file_data = json.load(file)
        dict=file_data[str(c_id)]
        insert = "UPDATE cart SET Item_info = %s WHERE Customer_ID="+str(c_id)+";"
        mycursor.execute(insert, (json.dumps(dict),))

        print("Done")
        return 1
    #con.commit()
    #print(r)
def orderhisdel(orderid):
    global delid
    delid=delid+1
    mycursor.execute("INSERT INTO Order_history(Order_ID,Customer_ID,Payment_ID,Order_Date) values (1,%d,%d,'2022-04-12')"%(c_id,paymentid))
    mycursor.execute("INSERT INTO Delivery VALUES (%d,%d,%d,'Not Delivered',96734314)"%(delid,c_id,orderid))

    def updatedel(x):
        mycursor.execute("update Delivery SET Order_Status='Delivered' where Delivery_ID=%d"%x)
        print("S")
    timer = threading.Timer(15.0, updatedel,args=(delid,) )
    timer.start()



def order():
    global orderid
    orderid=orderid+1
    mycursor.execute("INSERT INTO _Order_ (Order_ID,Payment_ID, Customer_ID,Amount,Item_info,Order_Date) VALUES(%d,%d,%d,'%s','{}','2022-04-27')"%(int(orderid),int(paymentid),int(c_id),str(fprice[c_id])))
    mycursor.execute("UPDATE _Order_ SET Item_info =(SELECT Item_info FROM Cart WHERE Cart.Customer_ID = _Order_.Customer_ID)")
    orderhisdel(orderid)
def emptycart(c_id):
    total_price[c_id]=[]
    quanid[c_id]=[]
    prodid[c_id]=[]

def userinfo():
    global c_id
    global cid_already
    newwin = tkinter.Toplevel(top)
    newwin.title('User Info')
    newwin.geometry("210x120") 
    newwin.resizable(0, 0)
    def calc():
        global cid_already
        if(cid_already):
            jsonupdate(c_id)
        else:
            jsonadd(c_id)
            cid_already=True
    thread = threading.Thread(target=calc)
    thread.start()
    def open_cart():
        if 1==1:
            global s,o,prodid,quanid
            newwin = tkinter.Toplevel(top)
            newwin.geometry("400x400")
            newwin.title('300')
            mydict = create_dict()
            mycursor.execute("SELECT DISTINCT json_key FROM Cart,json_table(json_keys(Item_info),'$[*]' COLUMNS(json_key JSON PATH '$')) t;")
            result = mycursor.fetchall()

            
            #--------------------------------------------------------------------------------
            def pures(x):
                only_alpha = ""
                for char in x:
                    if char.isalpha():
                        only_alpha += char
                return only_alpha

            for i in range (0,len(s)):
                temp=s[i]
                s[i]=int(temp)
            
            list_prod_names=[]
            count=0
            for i in s:
                mycursor.execute("SELECT Item_name from Product where Product_ID=%d"%s[count])
                count+=1
                result = mycursor.fetchall()
                list_prod_names.append(result[0][0])
            #---------------------------------------------------------------------------------

            serial = tkinter.Label(newwin, text = "Serial No.").place(x = 10, y = 40)  
            prod_name=tkinter.Label(newwin, text = "Product Name").place(x = 80, y = 40)
            prod_quantiy=tkinter.Label(newwin, text = "Product Quantity").place(x = 220, y = 40)
            ys=40
            seno=0
            list_prod_names=prodid.get(c_id)
            for i in list(prodid.get(c_id)):
                ys=ys+20
                seno=seno+1
                serial_no=tkinter.Label(newwin, text =seno).place(x = 10, y = ys)
                name_label=tkinter.Label(newwin, text =i).place(x = 80, y = ys)
            xs=40
            for i in list(prodid.get(c_id)):
                xs=xs+20
                quantity_label=tkinter.Label(newwin, text =i).place(x = 260, y = xs)
            totalsp=tkinter.Label(newwin, text = "Total Price").place(x = 80, y = xs+40)
            line1=tkinter.Label(newwin, text ="---------------").place(x = 240, y = xs+20)
            printp=tkinter.Label(newwin, text =sum(total_price[c_id])).place(x = 240, y = xs+40)
            fprice[c_id]=sum(total_price[c_id])
            def coupon():
                global couponb,totalp
                only_alpha = ""
                for char in couponb.get():
                    if char.isalnum():
                        only_alpha += char
                cpnc=list(coupon_code.keys())
                print(only_alpha)
                if only_alpha in cpnc:
                    tmp = fprice.get(c_id)
                    print(tmp)
                    fprice[c_id]=(tmp*(100-(coupon_code.get(only_alpha))))/100
                    k=tkinter.Label(newwin, text =str(fprice[c_id])).place(x = 240, y = xs+40)
            


            global couponb
            coupon_button   = tkinter.Button(newwin, text ="Enter Coupon",bg='orange',height=1,width=10, command = coupon)
            coupon_button.pack()
            coupon_button.place(x=8,y=280)
            couponb = tkinter.Entry(newwin,width = 15,selectbackground="blue",selectborderwidth='2px')
            couponb.place(x = 105,y = 283)
            couponchosen=couponb.get()


            def payment():
                newwin.destroy()
                newwin2 = tkinter.Toplevel(top)
                newwin2.geometry("300x150")
                newwin2.title('Payment')
                payment_method   = tkinter.Label(newwin2, text ="Enter a Payment Method",bg='orange',height=1,width=19)
                payment_method.pack()
                payment_method.place(x=15,y=20)
                global payment_m
                payment_m = tkinter.Entry(newwin2,width = 15,selectbackground="blue",selectborderwidth='2px')
                payment_m.place(x = 180,y = 25)
                global paymentid
                paymentid=random.randint(99999,9999999)
                def add_payment():
                    emptycart(c_id)
                    if len(couponchosen)==0:
                        mycursor.execute("INSERT INTO Payment(Payment_ID,Customer_ID,Amount,Payment_method) VALUES (%d,%d,%d,'%s')"%(paymentid,int(c_id),float(fprice[c_id]),payment_m.get()))
                    else:
                        mycursor.execute("insert into Payment(Payment_ID,Customer_ID,Amount,Payment_method,Coupon_code) VALUES (%d,%d,%f,'%s','%s')"%(paymentid,c_id,fprice[c_id],payment_m.get(),couponb.get()))
                    order()
                    tkinter.messagebox.showinfo(title="Order Placed",message="Your order has been placed , Thank you for Choosing us !!!")
                    newwin2.destroy
                payment_method   = tkinter.Button(newwin2, text ="Proceed to pay",bg='red',height=1,width=19, command = add_payment)
                payment_method.pack()
                payment_method.place(x=65,y=70)
                
                
                    

            
            pay_button   = tkinter.Button(newwin, text ="Proceed to Payment",bg='red',height=2,width=20, command = payment)
            pay_button.pack()
            pay_button.place(x=20,y=340)
            
            newwin.mainloop()
            
    def orderhistory():

        newwin2 = tkinter.Toplevel(top)
        newwin2.geometry("500x400")
        newwin2.title('Payment')
        mycursor.execute("select * from Order_history where Customer_ID = %d"%c_id)
        values= mycursor.fetchall()

        if len(values)==0:
            tkinter.messagebox.showinfo(title='Order History',message="No order's placed till now !!")
            newwin2.destroy()
        else:
            oh1=tkinter.Label(newwin2, text ="Sno.",bg='orange',height=1,width=5).place(x=10,y=20)
            oh2=tkinter.Label(newwin2, text ="Order ID",bg='orange',height=1,width=10).place(x=60,y=20)
            oh3=tkinter.Label(newwin2, text ="Payment ID",bg='orange',height=1,width=15).place(x=150,y=20)
            oh4=tkinter.Label(newwin2, text ="Date",bg='orange',height=1,width=15).place(x=320,y=20)
            xy=20
            x1=10
            x2=60
            x3=150
            x4=320
            
            for i in range (0,len(values)):
                xy=xy+22
                oh1=tkinter.Label(newwin2, text =str(i+1),height=1,width=5).place(x=x1,y=20+22)
                oh2=tkinter.Label(newwin2, text =str(values[i][0]),height=1,width=10).place(x=x2,y=xy)
                oh3=tkinter.Label(newwin2, text =str(values[i][2]),height=1,width=15).place(x=x3,y=xy)
                oh4=tkinter.Label(newwin2, text =str(values[i][3]),height=1,width=15).place(x=x4,y=xy)

            def returnor():
                global reid
                reid=reid+1
                only_alpha=""
                for char in ordsid.get():
                        if char.isnumeric:
                            only_alpha += char
                mycursor.execute("insert into Return_order values (%d,%d)"%(reid,int(only_alpha)))
                tkinter.messagebox.showinfo(title="Return Order",message="ORder will be returned !!")
                newwin2.destroy()



        return_button = tkinter.Button(newwin2, text ="Enter return ID : ",bg='red',height=2,width=20, command = returnor)
        return_button.pack()
        return_button.place(x=20,y=340)
        ordsid = tkinter.Entry(newwin2,width =15,selectbackground="blue",selectborderwidth='2px')
        ordsid.place(x=190,y=350)

            


    def profile():
        newwin2 = tkinter.Toplevel(newwin)
        newwin2.geometry("300x260")
        newwin2.title('Profile')
        mycursor.execute("select * from Customer where Customer_ID = %d"%c_id)
        values= mycursor.fetchall()

        oh1=tkinter.Label(newwin2, text ="Customer ID",bg='orange',height=1,width=15).place(x=40,y=20)
        oh2=tkinter.Label(newwin2, text ="Name",bg='orange',height=1,width=15).place(x=40,y=60)
        oh3=tkinter.Label(newwin2, text ="Address",bg='orange',height=1,width=15).place(x=40,y=100)
        oh4=tkinter.Label(newwin2, text ="Email_ID",bg='orange',height=1,width=15).place(x=40,y=140)
        oh4=tkinter.Label(newwin2, text ="Username",bg='orange',height=1,width=15).place(x=40,y=180)
        yx=20
        for i in range (0,len(values[0])-1):
            ohh=tkinter.Label(newwin2, text =values[0][i],bg='brown',height=1,width=15).place(x=150,y=yx)
            print(values[0][i])
            yx=yx+40
        def ph():
            newwin3= tkinter.Toplevel(newwin2)
            newwin3.geometry("150x150")
            newwin3.title('Profile')
            mycursor.execute("select Phone_Number from Telephone_number where Customer_ID=%d"%c_id)
            x=mycursor.fetchall()
            print(x[1][0])
            yx=20
            for i in range(len(x)):
                oh3=tkinter.Label(newwin3, text =str(x[i][0]),bg='magenta',height=1,width=15).place(x=30,y=yx)
                yx=yx+40
        df   = tkinter.Button(newwin2, text ="Telephone",bg='red',height=1,width=10, command = ph)
        df.pack()
        df.place(x=100,y=220)   

    cart_button   = tkinter.Button(newwin, text ="Cart",bg='orange',height=1,width=10, command = open_cart)
    order_history   = tkinter.Button(newwin, text ="Order History",bg='orange',height=1,width=10, command = orderhistory)
    profile   = tkinter.Button(newwin, text ="Profile",bg='orange',height=1,width=10, command = profile)
    cart_button.pack()
    cart_button.place(x=8,y=10)
    order_history.pack()
    order_history.place(x=8,y=50)
    profile.pack()
    profile.place(x=8,y=90)
    temp9=Image.open("Images/user.png")
    k9=temp9.resize((100,100),Image.Resampling.LANCZOS)
    img9=ImageTk.PhotoImage(k9)
    my_label6=tkinter.Label(newwin,image=img9)
    my_label6.pack()
    my_label6.place(x=100,y=10)
    newwin.mainloop()



photo = tkinter.PhotoImage(file = r"Images/user.png")
photoimage = photo.subsample(7,8)
c= tkinter.Button(top,image = photoimage,command=userinfo,compound = tkinter.LEFT)
c.pack()
c.place(x=810,y=40)



'''
Deals of the day Text
'''

text = tkinter.Text(top,width=18,height=1,bg='#9796F0')
text.insert(tkinter.INSERT, "DEALS OF THE DAY !!!")
text.configure(font=("Algerian",30,"italic"))
text.place(x=230,y=400)

'''
Deals of the day Photos
'''
path6="Images/sp1.jpeg"
path7="Images/sp2.jpeg"
path8="Images/sp3.jpeg"
path9="Images/sp4.jpeg"
temp6=Image.open(path6)
temp7=Image.open(path7)
temp8=Image.open(path8)
temp9=Image.open(path9)
k6=temp6.resize((200,250),Image.Resampling.LANCZOS)
k7=temp7.resize((200,250),Image.Resampling.LANCZOS)
k8=temp8.resize((200,250),Image.Resampling.LANCZOS)
k9=temp9.resize((200,250),Image.Resampling.LANCZOS)
img6=ImageTk.PhotoImage(k6)
img7=ImageTk.PhotoImage(k7)
img8=ImageTk.PhotoImage(k8)
img9=ImageTk.PhotoImage(k9)
my_label6=tkinter.Label(image=img6)
my_label6.pack()
my_label6.place(x=20,y=540)

my_label8=tkinter.Label(image=img8)
my_label8.pack()
my_label8.place(x=220,y=460)

my_label7=tkinter.Label(image=img7)
my_label7.pack()
my_label7.place(x=440,y=550)

my_label9=tkinter.Label(image=img9)
my_label9.pack()
my_label9.place(x=660,y=460)

top.mainloop()



