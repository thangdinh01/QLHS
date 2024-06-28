from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class AddClassForm(Toplevel):
    def __init__(self, parent, db_connection, callback=None):
        super().__init__(parent)
        self.title("Thêm lớp học")
        self.geometry("800x600")

        self.db_connection = db_connection
        self.callback = callback

        label_name = Label(self, text="Tên lớp:")
        label_name.grid(row=1, column=0, padx=10, pady=10)
        self.entry_name = Entry(self, width=30)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10)

        label_gvcn = Label(self, text="Giáo viên chủ nhiệm:")
        label_gvcn.grid(row=2, column=0, padx=10, pady=10)
        self.entry_gvcn = Entry(self, width=30)
        self.entry_gvcn.grid(row=2, column=1, padx=10, pady=10)

        button_save = Button(self, text="Thêm lớp", command=self.save_class)
        button_save.grid(row=3, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "TenLop", "GVCN"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("TenLop", text="Tên lớp")
        self.tree.heading("GVCN", text="Giáo viên chủ nhiệm")
        self.tree.grid(row=4, column=0, columnspan=2, pady=10, sticky='nsew')

        button_edit = Button(self, text="Sửa lớp", command=self.edit_class)
        button_edit.grid(row=5, column=0, pady=10)

        button_delete = Button(self, text="Xóa lớp", command=self.delete_class)
        button_delete.grid(row=5, column=1, pady=10)

        button_logout = Button(self, text="Thoát", command=self.close_form)
        button_logout.grid(row=5, column=2, pady=10)

        self.load_classes()

    def load_classes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM Lop")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def save_class(self):
        name = self.entry_name.get()
        gvcn = self.entry_gvcn.get()

        if name and gvcn:
            try:
                cursor = self.db_connection.cursor()
                sql = "INSERT INTO Lop (TenLop, GVCN) VALUES (%s, %s)"
                cursor.execute(sql, (name, gvcn))
                self.db_connection.commit()
                messagebox.showinfo("Thông báo", "Thêm lớp học thành công!")
                self.load_classes()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi: {err}")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin lớp học.")

    def edit_class(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn lớp để sửa.")
            return

        item = self.tree.item(selected_item)
        class_id = item["values"][0]
        class_name = item["values"][1]
        class_gvcn = item["values"][2]

        edit_dialog = Toplevel(self)
        edit_dialog.title("Sửa lớp học")
        edit_dialog.geometry("400x300")

        Label(edit_dialog, text="Tên lớp:").grid(row=0, column=0, padx=10, pady=5)
        entry_name = Entry(edit_dialog, width=30)
        entry_name.insert(0, class_name)
        entry_name.grid(row=0, column=1, padx=10, pady=5)

        Label(edit_dialog, text="Giáo viên chủ nhiệm:").grid(row=1, column=0, padx=10, pady=5)
        entry_gvcn = Entry(edit_dialog, width=30)
        entry_gvcn.insert(0, class_gvcn)
        entry_gvcn.grid(row=1, column=1, padx=10, pady=5)

        def save_changes():
            new_name = entry_name.get()
            new_gvcn = entry_gvcn.get()

            if new_name and new_gvcn:
                try:
                    cursor = self.db_connection.cursor()
                    update_sql = "UPDATE Lop SET TenLop = %s, GVCN = %s WHERE ID = %s"
                    cursor.execute(update_sql, (new_name, new_gvcn, class_id))
                    self.db_connection.commit()
                    messagebox.showinfo("Thông báo", "Cập nhật thông tin thành công!")
                    self.load_classes()
                    edit_dialog.destroy()
                except mysql.connector.Error as err:
                    messagebox.showerror("Lỗi", f"Lỗi: {err}")
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin lớp học.")

        Button(edit_dialog, text="Lưu", command=save_changes).grid(row=2, column=0, columnspan=2, pady=10)

    def delete_class(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn lớp để xóa.")
            return

        if messagebox.askyesno("Xác nhận xóa", "Bạn có chắc muốn xóa lớp học này?"):
            item = self.tree.item(selected_item)
            class_id = item["values"][0]

            try:
                cursor = self.db_connection.cursor()
                cursor.execute("DELETE FROM Lop WHERE ID = %s", (class_id,))
                self.db_connection.commit()
                messagebox.showinfo("Thông báo", "Xóa lớp học thành công!")
                self.load_classes()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi: {err}")

    def close_form(self):
        if self.callback:
            self.callback()
        self.destroy()
