from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class AddScoreForm(Toplevel):
    def __init__(self, parent, db_connection, callback=None):
        super().__init__(parent)
        self.title("Nhập điểm")
        self.geometry("1280x720")

        self.db_connection = db_connection
        self.callback = callback

        label_student = Label(self, text="Học sinh:")
        label_student.grid(row=0, column=0, padx=10, pady=10)
        self.student_combobox = ttk.Combobox(self, width=30)
        self.student_combobox.grid(row=0, column=1, padx=10, pady=10)

        label_subject = Label(self, text="Môn học:")
        label_subject.grid(row=1, column=0, padx=10, pady=10)
        self.subject_combobox = ttk.Combobox(self, width=30)
        self.subject_combobox.grid(row=1, column=1, padx=10, pady=10)

        label_score_hk1 = Label(self, text="Điểm học kỳ 1:")
        label_score_hk1.grid(row=2, column=0, padx=10, pady=10)
        self.entry_score_hk1 = Entry(self, width=30)
        self.entry_score_hk1.grid(row=2, column=1, padx=10, pady=10)

        label_score_hk2 = Label(self, text="Điểm học kỳ 2:")
        label_score_hk2.grid(row=3, column=0, padx=10, pady=10)
        self.entry_score_hk2 = Entry(self, width=30)
        self.entry_score_hk2.grid(row=3, column=1, padx=10, pady=10)

        label_school_year = Label(self, text="Năm học:")
        label_school_year.grid(row=4, column=0, padx=10, pady=10)
        self.entry_school_year = Entry(self, width=30)
        self.entry_school_year.grid(row=4, column=1, padx=10, pady=10)

        button_save = Button(self, text="Nhập điểm", command=self.save_score)
        button_save.grid(row=5, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "HocSinh", "MonHoc", "DiemThiHK1", "DiemThiHK2", "DiemTBMon", "NamHoc"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("HocSinh", text="Học sinh")
        self.tree.heading("MonHoc", text="Môn học")
        self.tree.heading("DiemThiHK1", text="Điểm HK1")
        self.tree.heading("DiemThiHK2", text="Điểm HK2")
        self.tree.heading("DiemTBMon", text="Điểm TB môn")
        self.tree.heading("NamHoc", text="Năm học")
        self.tree.grid(row=6, column=0, columnspan=2, pady=10, sticky='nsew')

        button_edit = Button(self, text="Sửa điểm", command=self.edit_score)
        button_edit.grid(row=7, column=0, pady=10)

        button_delete = Button(self, text="Xóa điểm", command=self.delete_score)
        button_delete.grid(row=7, column=1, pady=10)

        button_logout = Button(self, text="Thoát", command=self.close_form)
        button_logout.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        self.load_data()

    def load_data(self):
        self.load_students()
        self.load_subjects()
        self.load_scores()

    def load_students(self):
        self.student_combobox['values'] = []
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT ID, HoTen FROM HocSinh")
        students = cursor.fetchall()
        student_list = []
        for student in students:
            student_list.append(f"{student[0]} - {student[1]}")
        self.student_combobox['values'] = student_list

    def load_subjects(self):
        self.subject_combobox['values'] = []
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT ID, TenMonHoc FROM MonHoc")
        subjects = cursor.fetchall()
        subject_list = []
        for subject in subjects:
            subject_list.append(f"{subject[0]} - {subject[1]}")
        self.subject_combobox['values'] = subject_list

    def load_scores(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT Diem.DiemID, HocSinh.HoTen, MonHoc.TenMonHoc, Diem.DiemThiHK1, Diem.DiemThiHK2, Diem.DiemTBMon, Diem.NamHoc "
                       "FROM Diem "
                       "JOIN HocSinh ON Diem.HocSinhID = HocSinh.ID "
                       "JOIN MonHoc ON Diem.MonHocID = MonHoc.ID")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def save_score(self):
        student = self.student_combobox.get()
        subject = self.subject_combobox.get()
        score_hk1 = self.entry_score_hk1.get()
        score_hk2 = self.entry_score_hk2.get()
        school_year = self.entry_school_year.get()

        if student and subject and score_hk1 and score_hk2 and school_year:
            student_id = student.split(" - ")[0]  # Extract the ID part
            subject_id = subject.split(" - ")[0]  # Extract the ID part
            try:
                cursor = self.db_connection.cursor()

                avg_score = (float(score_hk1) + float(score_hk2)) / 2.0
                sql = "INSERT INTO Diem (HocSinhID, MonHocID, DiemThiHK1, DiemThiHK2, DiemTBMon, NamHoc) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (student_id, subject_id, score_hk1, score_hk2, avg_score, school_year))
                self.db_connection.commit()
                messagebox.showinfo("Thông báo", "Nhập điểm thành công!")
                self.load_scores()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi: {err}")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")

    def edit_score(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn điểm để sửa.")
            return

        item = self.tree.item(selected_item)
        score_id = item["values"][0]

        score_hk1 = item["values"][3]
        score_hk2 = item["values"][4]
        school_year = item["values"][6]

        edit_dialog = Toplevel(self)
        edit_dialog.title("Sửa điểm")
        edit_dialog.geometry("400x300")

        Label(edit_dialog, text="Điểm học kỳ 1:").grid(row=2, column=0, padx=10, pady=5)
        entry_score_hk1 = Entry(edit_dialog, width=30)
        entry_score_hk1.grid(row=2, column=1, padx=10, pady=5)

        Label(edit_dialog, text="Điểm học kỳ 2:").grid(row=3, column=0, padx=10, pady=5)
        entry_score_hk2 = Entry(edit_dialog, width=30)
        entry_score_hk2.grid(row=3, column=1, padx=10, pady=5)

        Label(edit_dialog, text="Năm học:").grid(row=4, column=0, padx=10, pady=5)
        entry_school_year = Entry(edit_dialog, width=30)
        entry_school_year.grid(row=4, column=1, padx=10, pady=5)

        self.load_students()
        self.load_subjects()


        entry_score_hk1.insert(0, score_hk1)
        entry_score_hk2.insert(0, score_hk2)
        entry_school_year.insert(0, school_year)

        def save_changes():

            new_score_hk1 = entry_score_hk1.get()
            new_score_hk2 = entry_score_hk2.get()
            new_school_year = entry_school_year.get()

            if new_score_hk1 and new_score_hk2 and new_school_year:

                try:
                    cursor = self.db_connection.cursor()

                    new_avg_score = (float(new_score_hk1) + float(new_score_hk2)) / 2.0
                    sql = "UPDATE Diem SET DiemThiHK1 = %s, DiemThiHK2 = %s, DiemTBMon = %s, NamHoc = %s WHERE DiemID = %s"
                    cursor.execute(sql, (
                    new_score_hk1, new_score_hk2, new_avg_score, new_school_year,
                    score_id))
                    self.db_connection.commit()
                    messagebox.showinfo("Thông báo", "Cập nhật điểm thành công!")
                    self.load_scores()
                    edit_dialog.destroy()
                except mysql.connector.Error as err:
                    messagebox.showerror("Lỗi", f"Lỗi: {err}")
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")

        button_save_changes = Button(edit_dialog, text="Lưu thay đổi", command=save_changes)
        button_save_changes.grid(row=5, column=0, columnspan=2, pady=10)

    def delete_score(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn điểm để xóa.")
            return

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa điểm này?")
        if confirm:
            item = self.tree.item(selected_item)
            score_id = item["values"][0]
            try:
                cursor = self.db_connection.cursor()
                sql = "DELETE FROM Diem WHERE DiemID = %s"
                cursor.execute(sql, (score_id,))
                self.db_connection.commit()
                messagebox.showinfo("Thông báo", "Xóa điểm thành công!")
                self.load_scores()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi: {err}")

    def close_form(self):
        if self.callback:
            self.callback()
        self.destroy()

class ViewScoresForm(Toplevel):
    def __init__(self, parent, db_connection, callback=None):
        super().__init__(parent)
        self.title("Xem điểm")
        self.geometry("1280x720")

        self.db_connection = db_connection
        self.callback = callback

        self.tree = ttk.Treeview(self, columns=("ID", "HocSinh", "MonHoc", "DiemThiHK1", "DiemThiHK2", "DiemTBMon", "NamHoc"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("HocSinh", text="Học sinh")
        self.tree.heading("MonHoc", text="Môn học")
        self.tree.heading("DiemThiHK1", text="Điểm HK1")
        self.tree.heading("DiemThiHK2", text="Điểm HK2")
        self.tree.heading("DiemTBMon", text="Điểm TB môn")
        self.tree.heading("NamHoc", text="Năm học")
        self.tree.pack(pady=10, expand=True)

        button_refresh = Button(self, text="Làm mới", command=self.load_scores)
        button_refresh.pack(pady=10)

        button_close = Button(self, text="Đóng", command=self.close_form)
        button_close.pack(pady=10)

        self.load_scores()

    def load_scores(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT Diem.DiemID, HocSinh.HoTen, MonHoc.TenMonHoc, Diem.DiemThiHK1, Diem.DiemThiHK2, Diem.DiemTBMon, Diem.NamHoc "
                       "FROM Diem "
                       "JOIN HocSinh ON Diem.HocSinhID = HocSinh.ID "
                       "JOIN MonHoc ON Diem.MonHocID = MonHoc.ID")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def close_form(self):
        if self.callback:
            self.callback()
        self.destroy()

