from tkinter import *
from tkinter import messagebox
from homepage import HomePage
import mysql.connector

window = Tk()
window.title("Đăng nhập")
window.geometry("400x300")

try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="01626164598vip1",
        database="quanlydiemthpt"
    )
    print("Connected to MySQL database!")
except mysql.connector.Error as err:
    messagebox.showerror("Lỗi kết nối", f"Lỗi: {err}")
    exit()

def validate_login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "admin" and password == "1":
        messagebox.showinfo("Đăng nhập", "Đăng nhập thành công!")
        open_homepage()
    else:
        messagebox.showerror("Đăng nhập", "Đăng nhập thất bại. Vui lòng thử lại.")

def open_homepage():
    window.withdraw()
    homepage = HomePage(db_connection)
    homepage.protocol("WM_DELETE_WINDOW", on_closing)
    homepage.mainloop()

def on_closing():
    db_connection.close()
    window.quit()


label_username = Label(window, text="Tên đăng nhập:")
label_username.pack(pady=5)
entry_username = Entry(window)
entry_username.pack(pady=5)

label_password = Label(window, text="Mật khẩu:")
label_password.pack(pady=5)
entry_password = Entry(window, show="*")
entry_password.pack(pady=5)

button_login = Button(window, text="Đăng nhập", command=validate_login)
button_login.pack(pady=10)


window.mainloop()


