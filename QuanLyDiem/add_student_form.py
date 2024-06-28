from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

class AddStudentForm(Toplevel):
    def __init__(self, parent, db_connection, callback=None):
        super().__init__(parent)
        self.title("Thêm học sinh")
        self.geometry("1280x720")

        self.db_connection = db_connection
        self.callback = callback

        label_name = Label(self, text="Họ và tên:")
        label_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_name = Entry(self, width=30)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)

        label_ngaysinh = Label(self, text="Ngày sinh (YYYY-MM-DD):")
        label_ngaysinh.grid(row=1, column=0, padx=10, pady=10)
        self.entry_ngaysinh = Entry(self, width=30)
        self.entry_ngaysinh.grid(row=1, column=1, padx=10, pady=10)

        label_gioitinh = Label(self, text="Giới tính:")
        label_gioitinh.grid(row=2, column=0, padx=10, pady=10)
        self.gioitinh_var = StringVar(self)
        self.gioitinh_var.set("Nam")
        gioitinh_options = ["Nam", "Nữ"]
        self.entry_gioitinh = OptionMenu(self, self.gioitinh_var, *gioitinh_options)
        self.entry_gioitinh.grid(row=2, column=1, padx=10, pady=10)

        label_diachi = Label(self, text="Địa chỉ:")
        label_diachi.grid(row=3, column=0, padx=10, pady=10)
        self.entry_diachi = Entry(self, width=30)
        self.entry_diachi.grid(row=3, column=1, padx=10, pady=10)

        label_lop = Label(self, text="Lớp:")
        label_lop.grid(row=4, column=0, padx=10, pady=10)
        self.entry_lop = Entry(self, width=30)
        self.entry_lop.grid(row=4, column=1, padx=10, pady=10)

        button_save = Button(self, text="Lưu", command=self.save_student)
        button_save.grid(row=5, column=0, columnspan=2, padx=10, pady=20)

        button_edit = Button(self, text="Sửa", command=self.edit_student)
        button_edit.grid(row=6, column=0, padx=10, pady=10)

        button_delete = Button(self, text="Xóa", command=self.delete_student)
        button_delete.grid(row=6, column=1, padx=10, pady=10)

        button_logout = Button(self, text="Thoát", command=self.close_form)
        button_logout.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "HoTen", "NgaySinh", "GioiTinh", "DiaChi", "Lop"),
                                 show="headings", height=15)
        self.tree.grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky=(N, S, W, E))

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=3, rowspan=4, sticky=(N, S, E))
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.heading("ID", text="ID")
        self.tree.heading("HoTen", text="Họ và tên")
        self.tree.heading("NgaySinh", text="Ngày sinh")
        self.tree.heading("GioiTinh", text="Giới tính")
        self.tree.heading("DiaChi", text="Địa chỉ")
        self.tree.heading("Lop", text="Lớp")

        self.load_students()

    def load_students(self):
        try:
            self.tree.delete(*self.tree.get_children())
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT HocSinh.ID, HocSinh.HoTen, HocSinh.NgaySinh, HocSinh.GioiTinh, HocSinh.DiaChi, Lop.TenLop FROM HocSinh JOIN Lop ON HocSinh.LopID = Lop.ID")
            students = cursor.fetchall()
            for student in students:
                self.tree.insert("", "end", values=student)
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Lỗi: {err}")

    def save_student(self):
        hoten = self.entry_name.get()
        ngaysinh = self.entry_ngaysinh.get()
        gioitinh = self.gioitinh_var.get()
        diachi = self.entry_diachi.get()
        lop = self.entry_lop.get()

        if hoten and ngaysinh and gioitinh and diachi and lop:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("SELECT ID FROM Lop WHERE TenLop = %s", (lop,))
                lop_id = cursor.fetchone()

                if lop_id:
                    sql = "INSERT INTO HocSinh (HoTen, NgaySinh, GioiTinh, DiaChi, LopID) VALUES (%s, %s, %s, %s, %s)"
                    values = (hoten, ngaysinh, gioitinh, diachi, lop_id[0])
                    cursor.execute(sql, values)
                    self.db_connection.commit()
                    messagebox.showinfo("Thêm học sinh", "Thêm học sinh thành công!")
                    self.load_students()
                else:
                    messagebox.showerror("Lỗi", "Không tìm thấy lớp học.")
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi: {err}")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin học sinh.")

    def edit_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn học sinh để sửa.")
            return

        item = self.tree.item(selected_item)
        student_id = item["values"][0]

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT HoTen, NgaySinh, GioiTinh, DiaChi, LopID FROM HocSinh WHERE ID = %s", (student_id,))
            student_details = cursor.fetchone()

            if student_details:
                edit_dialog = Toplevel(self)
                edit_dialog.title("Sửa thông tin học sinh")
                edit_dialog.geometry("400x300")

                Label(edit_dialog, text="Họ và tên:").grid(row=0, column=0, padx=10, pady=5)
                entry_name = Entry(edit_dialog, width=30)
                entry_name.insert(0, student_details[0])
                entry_name.grid(row=0, column=1, padx=10, pady=5)

                Label(edit_dialog, text="Ngày sinh (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
                entry_ngaysinh = Entry(edit_dialog, width=30)
                entry_ngaysinh.insert(0, student_details[1])
                entry_ngaysinh.grid(row=1, column=1, padx=10, pady=5)

                Label(edit_dialog, text="Giới tính:").grid(row=2, column=0, padx=10, pady=5)
                gioitinh_var = StringVar(edit_dialog)
                gioitinh_var.set(student_details[2])
                gioitinh_options = ["Nam", "Nữ"]
                entry_gioitinh = OptionMenu(edit_dialog, gioitinh_var, *gioitinh_options)
                entry_gioitinh.grid(row=2, column=1, padx=10, pady=5)

                Label(edit_dialog, text="Địa chỉ:").grid(row=3, column=0, padx=10, pady=5)
                entry_diachi = Entry(edit_dialog, width=30)
                entry_diachi.insert(0, student_details[3])
                entry_diachi.grid(row=3, column=1, padx=10, pady=5)

                Label(edit_dialog, text="Lớp:").grid(row=4, column=0, padx=10, pady=5)
                entry_lop = Entry(edit_dialog, width=30)
                cursor.execute("SELECT TenLop FROM Lop WHERE ID = %s", (student_details[4],))
                lop_name = cursor.fetchone()[0]
                entry_lop.insert(0, lop_name)
                entry_lop.grid(row=4, column=1, padx=10, pady=5)

                def save_changes():
                    new_name = entry_name.get()
                    new_ngaysinh = entry_ngaysinh.get()
                    new_gioitinh = gioitinh_var.get()
                    new_diachi = entry_diachi.get()
                    new_lop = entry_lop.get()

                    if new_name and new_ngaysinh and new_gioitinh and new_diachi and new_lop:
                        try:
                            cursor.execute("SELECT ID FROM Lop WHERE TenLop = %s", (new_lop,))
                            lop_id = cursor.fetchone()

                            if lop_id:
                                update_sql = "UPDATE HocSinh SET HoTen = %s, NgaySinh = %s, GioiTinh = %s, DiaChi = %s, LopID = %s WHERE ID = %s"
                                update_values = (new_name, new_ngaysinh, new_gioitinh, new_diachi, lop_id[0], student_id)
                                cursor.execute(update_sql, update_values)
                                self.db_connection.commit()
                                messagebox.showinfo("Thông báo", "Cập nhật thông tin thành công!")
                                self.load_students()
                                edit_dialog.destroy()
                            else:
                                messagebox.showerror("Lỗi", "Không tìm thấy lớp học.")
                        except mysql.connector.Error as err:
                            messagebox.showerror("Lỗi", f"Lỗi: {err}")
                    else:
                        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin học sinh.")

                Button(edit_dialog, text="Lưu", command=save_changes).grid(row=5, column=0, columnspan=2, padx=10, pady=10)
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin học sinh.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Lỗi: {err}")

    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn học sinh để xóa.")
            return

        if messagebox.askyesno("Xác nhận xóa", "Bạn có chắc muốn xóa học sinh này?"):
            item = self.tree.item(selected_item)
            student_id = item["values"][0]

            try:
                cursor = self.db_connection.cursor()
                cursor.execute("DELETE FROM HocSinh WHERE ID = %s", (student_id,))
                self.db_connection.commit()
                messagebox.showinfo("Thông báo", "Xóa học sinh thành công!")
                self.load_students()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi: {err}")

    def close_form(self):
        if self.callback:
            self.callback()
        self.destroy()
