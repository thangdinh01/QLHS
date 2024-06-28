from tkinter import *
from add_student_form import AddStudentForm
from add_class_form import AddClassForm
from add_subject_form import AddSubjectForm
from add_score_form import AddScoreForm, ViewScoresForm

class HomePage(Tk):
    def __init__(self, db_connection):
        super().__init__()
        self.title("Trang chủ")
        self.geometry("1280x720")

        self.db_connection = db_connection

        label_title = Label(self, text="Chào mừng bạn đến với Quản lý điểm!", font=("Helvetica", 16))
        label_title.pack(pady=10)

        button_add_student = Button(self, text="Thêm học sinh", command=self.open_add_student_form)
        button_add_student.place(x=20, y=40, width=100, height=25)

        button_add_class = Button(self, text="Thêm lớp học", command=self.open_add_class_form)
        button_add_class.place(x=20, y=80, width=100, height=25)

        button_add_subject = Button(self, text="Thêm môn học", command=self.open_add_subject_form)
        button_add_subject.place(x=20, y=120, width=100, height=25)

        button_add_score = Button(self, text="Nhập điểm", command=self.open_add_score_form)
        button_add_score.place(x=20, y=160, width=100, height=25)

        button_view_scores = Button(self, text="Xem điểm", command=self.open_view_scores_form)
        button_view_scores.place(x=20, y=200, width=100, height=25)

        button_logout = Button(self, text="Đăng xuất", command=self.logout)
        button_logout.place(x=20, y=500, width=100, height=25)

    def open_add_student_form(self):
        self.withdraw()
        add_student_window = AddStudentForm(self, self.db_connection, self.show_homepage)
        add_student_window.grab_set()

    def open_add_class_form(self):
        self.withdraw()
        add_class_window = AddClassForm(self, self.db_connection, self.show_homepage)
        add_class_window.grab_set()

    def open_add_subject_form(self):
        self.withdraw()
        add_subject_window = AddSubjectForm(self, self.db_connection, self.show_homepage)
        add_subject_window.grab_set()

    def open_add_score_form(self):
        self.withdraw()
        add_score_window = AddScoreForm(self, self.db_connection, self.show_homepage)
        add_score_window.grab_set()

    def open_view_scores_form(self):
        self.withdraw()
        view_scores_window = ViewScoresForm(self, self.db_connection, self.show_homepage)
        view_scores_window.grab_set()

    def show_homepage(self):
        self.deiconify()

    def logout(self):
        self.quit()
