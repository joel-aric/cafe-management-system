import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Menu
menu = {
    'Pizza': 400,
    'Pasta': 300,
    'Burger': 250,
    'Coffee': 450,
    'Salad': 250
}

order = {}

GST_PERCENT = 5
DISCOUNT_PERCENT = 10

# Main Window
root = tk.Tk()
root.title("Cafe Management System")
root.geometry("600x700")
root.config(bg="#f4f4f4")

# ---------- Functions ----------
def add_item():
    item = item_entry.get()
    qty = qty_entry.get()

    if item not in menu:
        messagebox.showerror("Error", "Item not available")
        return

    if not qty.isdigit() or int(qty) <= 0:
        messagebox.showerror("Error", "Enter valid quantity")
        return

    qty = int(qty)
    order[item] = order.get(item, 0) + qty
    update_order()

def remove_item():
    item = item_entry.get()
    if item in order:
        del order[item]
        update_order()
    else:
        messagebox.showerror("Error", "Item not in order")

def update_order():
    order_list.delete(0, tk.END)
    subtotal = 0

    for item, qty in order.items():
        price = menu[item] * qty
        subtotal += price
        order_list.insert(tk.END, f"{item} x {qty} = Rs {price}")

    gst = subtotal * GST_PERCENT / 100
    discount = subtotal * DISCOUNT_PERCENT / 100
    total = subtotal + gst - discount

    subtotal_label.config(text=f"Subtotal: Rs {subtotal}")
    gst_label.config(text=f"GST (5%): Rs {gst:.2f}")
    discount_label.config(text=f"Discount (10%): Rs {discount:.2f}")
    total_label.config(text=f"Total Bill: Rs {total:.2f}")

def clear_order():
    order.clear()
    update_order()

def generate_receipt():
    if not order:
        messagebox.showerror("Error", "No order found")
        return

    name = name_entry.get()
    if name == "":
        messagebox.showerror("Error", "Enter customer name")
        return

    time = datetime.now().strftime("%d-%m-%Y  %H:%M:%S")

    receipt = f"------ Cafe Receipt ------\n"
    receipt += f"Customer: {name}\n"
    receipt += f"Date & Time: {time}\n\n"

    subtotal = 0
    for item, qty in order.items():
        price = menu[item] * qty
        subtotal += price
        receipt += f"{item} x {qty} = Rs {price}\n"

    gst = subtotal * GST_PERCENT / 100
    discount = subtotal * DISCOUNT_PERCENT / 100
    total = subtotal + gst - discount

    receipt += f"\nSubtotal: Rs {subtotal}"
    receipt += f"\nGST (5%): Rs {gst:.2f}"
    receipt += f"\nDiscount (10%): Rs {discount:.2f}"
    receipt += f"\nTotal Payable: Rs {total:.2f}"
    receipt += "\n--------------------------"

    # Save receipt
    with open("receipt.txt", "w") as file:
        file.write(receipt)

    messagebox.showinfo("Receipt", receipt)

# ---------- UI ----------
tk.Label(root, text="Cafe Management System",
         font=("Arial", 20, "bold"),
         bg="#f4f4f4").pack(pady=10)

# Customer
tk.Label(root, text="Customer Name:", bg="#f4f4f4").pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

# Menu
menu_text = "\n".join([f"{i} : Rs {p}" for i, p in menu.items()])
tk.Label(root, text="MENU", font=("Arial", 14, "bold"),
         bg="#f4f4f4").pack()
tk.Label(root, text=menu_text, bg="#f4f4f4").pack(pady=5)

# Inputs
tk.Label(root, text="Item Name:", bg="#f4f4f4").pack()
item_entry = tk.Entry(root)
item_entry.pack()

tk.Label(root, text="Quantity:", bg="#f4f4f4").pack()
qty_entry = tk.Entry(root)
qty_entry.pack()

# Buttons
tk.Button(root, text="Add Item", width=25,
          bg="green", fg="white",
          command=add_item).pack(pady=5)

tk.Button(root, text="Remove Item", width=25,
          bg="orange",
          command=remove_item).pack(pady=5)

# Order List
tk.Label(root, text="Order Details",
         font=("Arial", 14, "bold"),
         bg="#f4f4f4").pack(pady=5)

order_list = tk.Listbox(root, width=50, height=8)
order_list.pack()

# Bill Section
subtotal_label = tk.Label(root, text="Subtotal: Rs 0", bg="#f4f4f4")
subtotal_label.pack()

gst_label = tk.Label(root, text="GST (5%): Rs 0", bg="#f4f4f4")
gst_label.pack()

discount_label = tk.Label(root, text="Discount (10%): Rs 0", bg="#f4f4f4")
discount_label.pack()

total_label = tk.Label(root, text="Total Bill: Rs 0",
                       font=("Arial", 14, "bold"),
                       bg="#f4f4f4")
total_label.pack(pady=10)

# Final Buttons
tk.Button(root, text="Generate Receipt & Save",
          bg="blue", fg="white",
          width=30,
          command=generate_receipt).pack(pady=5)

tk.Button(root, text="Clear Order",
          bg="red", fg="white",
          width=30,
          command=clear_order).pack(pady=5)

tk.Button(root, text="Exit",
          width=30,
          command=root.destroy).pack(pady=5)

root.mainloop()