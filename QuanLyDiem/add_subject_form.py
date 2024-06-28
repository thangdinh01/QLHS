from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class AddSubjectForm(Toplevel):
    def __init__(self, parent, db_connection, callback):
        super().__init__(parent)
        self.title("Thêm môn học")
        self.geometry("800x600")

        self.db_connection = db_connection
        self.callback = callback

        label_name = Label(self, text="Tên môn học:")
        label_name.grid(row=1, column=0, padx=10, pady=10)
        self.entry_name = Entry(self, width=30)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10)

        button_save = Button(self, text="Thêm môn học", command=self.save_subject)
        button_save.grid(row=2, column=0, columnspan=2, pady=10)

        # Treeview for displaying subject information
        self.tree = ttk.Treeview(self, columns=("ID", "TenMonHoc"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("TenMonHoc", text="Tên môn học")
        self.tree.grid(row=3, column=0, columnspan=2, pady=10, sticky='nsew')

        button_edit = Button(self, text="Sửa môn học", command=self.edit_subject)
        button_edit.grid(row=4, column=0, pady=10)

        button_delete = Button(self, text="Xóa môn học", command=self.delete_subject)
        button_delete.grid(row=4, column=1, pady=10)

        button_logout = Button(self, text="Thoát", command=self.close_form)
        button_logout.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.load_subjects()

    def load_subjects(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM MonHoc")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def save_subject(self):
        name = self.entry_name.get()

        if name:
            try:
                cursor = self.db_connection.cursor()
                sql = "INSERT INTO MonHoc (TenMonHoc) VALUES (%s)"
                cursor.execute(sql, (name,))
                self.db_connection.commit()
                messagebox.showinfo("Thông báo", "Thêm môn học thành công!")
                self.load_subjects()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi: {err}")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên môn học.")

    def edit_subject(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn môn học để sửa.")
            return

        item = self.tree.item(selected_item)
        subject_id = item["values"][0]
        subject_name = item["values"][1]

        edit_dialog = Toplevel(self)
        edit_dialog.title("Sửa môn học")
        edit_dialog.geometry("400x200")

        Label(edit_dialog, text="Tên môn học:").grid(row=0, column=0, padx=10, pady=5)
        entry_name = Entry(edit_dialog, width=30)
        entry_name.insert(0, subject_name)
        entry_name.grid(row=0, column=1, padx=10, pady=5)

        def save_changes():
            new_name = entry_name.get()

            if new_name:
                try:
                    cursor = self.db_connection.cursor()
                    update_sql = "UPDATE MonHoc SET TenMonHoc = %s WHERE ID = %s"
                    cursor.execute(update_sql, (new_name, subject_id))
                    self.db_connection.commit()
                    messagebox.showinfo("Thông báo", "Cập nhật thông tin thành công!")
                    self.load_subjects()
                    edit_dialog.destroy()
                except mysql.connector.Error as err:
                    messagebox.showerror("Lỗi", f"Lỗi: {err}")
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập tên môn học.")

        Button(edit_dialog, text="Lưu", command=save_changes).grid(row=1, column=0, columnspan=2, pady=10)

    def delete_subject(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn môn học để xóa.")
            return

        if messagebox.askyesno("Xác nhận xóa", "Bạn có chắc muốn xóa môn học này?"):
            item = self.tree.item(selected_item)
            subject_id = item["values"][0]

            try:
                cursor = self.db_connection.cursor()
                cursor.execute("DELETE FROM MonHoc WHERE ID = %s", (subject_id,))
                self.db_connection.commit()
                messagebox.showinfo("Thông báo", "Xóa môn học thành công!")
                self.load_subjects()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi: {err}")

    def close_form(self):
        if self.callback:
            self.callback()
        self.destroy()
