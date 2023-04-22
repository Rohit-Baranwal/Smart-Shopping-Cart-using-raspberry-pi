# Smart shopping cart based on barcode scanner which used as to recognise the details of the product
# and weigh scale(load cell and hx711) as to verifies the weight for authentication purpose

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkinter import ttk
from tkinter import simpledialog
import json
import os
from datetime import datetime
from escpos.printer import Serial
from hx711 import HX711
import RPi.GPIO as GPIO


now = datetime.now()

dt_string = now.strftime("%b/%d/%Y %H:%M:%S")

GPIO.setmode(GPIO.BCM)

hx = HX711(dout_pin=6, pd_sck_pin=5)

################ PRINTER PART##################

# function which returns the weight


def get_weight():
    hx.zero()
    # gonna take 100 readings and take the mean value
    reading = hx.get_data_mean(readings=100)

    known_weight = float(total_weight)
    ratio = (reading/known_weight)
    # just doing Calibrating for getting almost correct weight
    hx.set_scale_ratio(ratio)
    weight = hx.get_weight_mean()
    return weight


def print_receipt():
    """ 9600 Baud, 8N1, Flow Control Enabled """
    p = Serial(devfile='/dev/serial0',
               baudrate=9600,
               bytesize=8,
               parity='N',
               stopbits=1,
               timeout=1.00,
               dsrdtr=True)
    p.text("Hello World\n")

    p.text("\n")
    p.set(
        align="center",
        font="a",
        width=1,
        height=1,
    )

    # Printing the image
    p.image("C:/Users/Nikita/Downloads/image-modified.jpeg",
            impl="bitImageColumn")

    # printing the initial data
    p.set(width=2,
          height=2,
          align="center",)

    p.text(" ===============\n")
    p.text("Tax Invoice\n")
    p.text(" ===============\n")

    p.set(width=1,
          height=1,
          align="left",)

    p.text("SCOE DIGEST\n")
    p.text("Shaitan Gali,\n")
    p.text("khatra mahal,\n")
    p.text("LOCATION : shamshan ke samne\n")
    p.text("TEL : 0141222585\n")
    p.text("GSTIN : 08AAMFT88558855\n")
    p.text("Bill No. : \n\n")
    p.text("DATE : ")
    p.text(dt_string)
    p.text("\n")
    p.text("CASHIER : \n")

    p.text(" ===========================\n")
    p.text("S.No     ITEM   QTY   PRICE\n")
    p.text(" -------------------------------\n")

    i = 0
    for code, product in cart.items():
        product_name = product['name']
        product_quantity = product['quantity']
        product_price = product['price']
        text_F = (
            f"(i+1) {product_name}  {product_quantity}   {product_price}")
        print(text_F)
        p.text(text_F)

    # need to change

    ##############
    p.text(" -------------------------------\n")
    p.set(
        # underline=0,
        align="right",
    )
    p.text("     SUBTOTAL:  ")
    # p.text(totalCostS)
    p.text(total_price)
    p.text("\n")
    p.text("     DISCOUNT:  0\n")
    Tax = (total_price * 0.18)
    p.text("     GST @ 18%:  ")
    p.text(Tax)
    p.text("\n")
    p.text(" ===========================\n")
    Total = Tax + total_price
    p.set(align="center",)
    p.text("    BILL TOTAL: ")
    p.text(Total)

    # p.text(totalCostS)
    p.text("\n")

    p.text(" --------------------------\n")

    p.text("THANK YOU\n")
    p.set(width=2,
          height=2,
          align="center",)
    p.text(" ===============\n")

    p.text("Please scan\nto Pay\n")

    p.text(" ===============\n")

    p.set(
        align="center",
        font="a",
        width=1,
        height=1,
        density=2,
        invert=0,
        smooth=False,
        flip=False,
    )
    p.qr("9076265887@paytm", native=True, size=12)
    p.text("\n")

    # p.barcode('123456', 'CODE39')

    # if your printer has paper cuting facility then you can use this function
    p.cut()
    print("printing done")


##############################################

# Dictionary variable that stores product data with barcodes as keys
product_data = {
    "8906108618609": {"name": "apple", "quantity": 1, "original_price": 0.50, "price": 0.50, "weight": 30},
    "S1957132": {"name": "banana", "quantity": 1, "original_price": 0.25, "price": 0.25, "weight": 60},
    "D2050222": {"name": "cherry", "quantity": 1, "original_price": 1.00, "price": 1.00, "weight": 70},
    "S1950133": {"name": "orange", "quantity": 1, "original_price": 0.75, "price": 0.75, "weight": 50},
    # Add more products with their barcodes and data here
}

# global cart

cart = {}

# total_price = 1


################ Functions#####
def addtoCart():
    # barcode = barcode_entry.get()
    barcodes = simpledialog.askstring(
        title="Barcode values", prompt="Enter products barcodes seperated by spaces to add them in cart")
    if not barcodes:
        return

    for barcode in barcodes.split(' '):
        if barcode in cart:
            cart[barcode]["quantity"] += 1
           #  cart[barcode]["price"] = cart[barcode]["original_price"] * cart[barcode]["quantity"]
            print(cart[barcode])

        elif barcode in product_data:
            cart[barcode] = {"name": product_data[barcode]["name"],
                             "quantity": 1,
                             "price": product_data[barcode]["price"],
                             "orignal_price": product_data[barcode]["original_price"],
                             "weight": product_data[barcode]["weight"]}

            # cart.append(product_data[barcode])
            print(cart[barcode])
        else:
            print("Item Not Found")

    update_display()


def addCart():

    print("Already called while starting Buying")


'''
    barcode = input("Scan the Barcode")

    addItem(barcode)
    
    ERROR FOUND HERE

    
    total_price = sum(product["price"] for product in cart)
    print(total_price)
    '''


def removeItems():
   # barcode = barcode_entry.get()
    barcodes = simpledialog.askstring(
        title="Barcode values", prompt="Enter cart products barcodes seperated by spaces to remove them")
    if not barcodes:
        return
    for barcode in barcodes.split(' '):
        if barcode in cart:
            if cart[barcode]["quantity"] > 1:
                cart[barcode]["quantity"] -= 1
                print("Product removed by quantity")
            else:
                del cart[barcode]
                print("Product removed from the list")
        else:
            print("Product not found in cart")

    update_display()


def update_display():
    print("UPDATING")
    global total_weight
    global total_price
    total_weight = 0
    total_price = 0
    for row in shoppingtable.get_children():
        shoppingtable.delete(row)
    for barcode in cart:
        name = cart[barcode]["name"]
        quantity = cart[barcode]["quantity"]

        # to finding the total weight of the cart product
        weight = cart[barcode]["weight"]
        tweight = weight * quantity
        total_weight += tweight
        print(total_weight)
        # to finding the total price of the product present in the cart
        price = cart[barcode]["orignal_price"]
        priceP = price * quantity
        cart[barcode]["price"] = priceP
        total_price += priceP
        # print(" Price chages", cart[barcode]["price"])
        frontlabel.config(text=f"Total: {total_price} ₹")
        # frontlabel = Label(DataEntryFrame, text="TOTAL: " + str(total_price), width=30, font=('arial',10,'italic bold'), bg='gold2')
        shoppingtable.insert("", END, values=(name, quantity, priceP))
    else:
        tatal_price = 0
        frontlabel.config(text=f"Total: {total_price} ₹")


def extShopping():
    weigh = get_weight()
    if (weigh <= (total_weight + 5)):
        print_receipt()
    else:
        messagebox.showerror(
            "Unsuccessfull!!!",
            "The total weight of product you purchased is not matched as weight of product in the cart!!!"
        )
    cart = {}
    update_display()


'''
    if os.path.isfile('cart_data.json'):
        with open('cart_data.json', 'r') as op:
            tempData = json.load(op)
    else:
        tempData = []

    tempData.append(cart)
    with open('cart_data.json', 'w') as op:
        json.dump(tempData, op)

    res = messagebox.askyesno(
        'Notification', 'Cart data addedto json. Do you want to exit?')
    # res = messagebox.askyesno(cart)

    if (res == True):
        root.destroy()
        cart = {}
        update_display()
'''
######################################################################


root = Tk()
root.title("Shooping Product Cart")
root.config(bg='#856ff8')
root.geometry('470x270')

###################################
ss = "SMART SHOPPING CART"

SliderLabel = Label(root, text=ss, font=(
    'chiller', 15, 'italic bold'), relief=RIDGE, borderwidth=2, width=30, bg='cyan')
SliderLabel.place(x=10, y=5)


# barcode_entry = Entry(root, width=20)
# barcode_entry.pack(side=TOP,padx=5)


# left side

ShowDataFrame = Frame(root, bg='#856ff8', relief=RIDGE, borderwidth=5)
ShowDataFrame.place(x=0, y=40, width=340, height=230)

# show items data
style = ttk.Style()
style.configure('Treeview.Heading', font=('arial', 9, 'bold'))
style.configure('Treeview', font=('arial', 8, 'italic bold'),
                background='cyan', foreground='black')
scroll_y = Scrollbar(ShowDataFrame, orient=VERTICAL)
# scroll_x = Scrollbar(ShowDataFrame, orient=HORIZONTAL)
shoppingtable = Treeview(ShowDataFrame, column=(
    'name', 'quantity', 'price'), yscrollcommand=scroll_y)
# scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)
# scroll_x.config(command=shoppingtable.xview)
scroll_y.config(command=shoppingtable.yview)
shoppingtable.heading("name", text="name")
shoppingtable.heading("quantity", text="quantity")
shoppingtable.heading("price", text="price")
shoppingtable['show'] = "headings"
shoppingtable.column('name', width=180)
shoppingtable.column('quantity', width=40)
shoppingtable.column('price', width=60)
shoppingtable.pack(fill=BOTH, expand=1)

# total_price= 0

# addtoCart()


# right side

DataEntryFrame = Frame(root, bg='gold2', relief=RIDGE, borderwidth=3)
DataEntryFrame.place(x=345, y=40, width=120, height=230)

# Buttons
frontlabel = Label(DataEntryFrame, text="Total: 0 ₹", width=30,
                   font=('arial', 10, 'italic bold'), bg='gold2')
frontlabel.pack(side=TOP, expand=True)

addbtn1 = Button(DataEntryFrame, text="ADD ITEMS", width=25, command=addtoCart, font=(
    'arial', 9, 'bold'), bd=3, bg='skyblue3', activebackground='blue', relief=RIDGE, activeforeground='white')
addbtn1.pack(side=TOP, expand=True)


addbtn2 = Button(DataEntryFrame, text="REMOVE ITEM", width=25, command=removeItems, font=(
    'arial', 9, 'bold'), bd=3, bg='skyblue3', activebackground='blue', relief=RIDGE, activeforeground='white')
addbtn2.pack(side=TOP, expand=True)


addbtn3 = Button(DataEntryFrame, text="DONE SHOPPING", width=25, command=extShopping, font=(
    'arial', 9, 'bold'), bd=3, bg='skyblue3', activebackground='blue', relief=RIDGE, activeforeground='white')
addbtn3.pack(side=TOP, expand=True)

root.mainloop()
