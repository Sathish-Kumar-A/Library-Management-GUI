from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from delete_dialoguebox import Ui_Dialog as ui_deletedialogue
from Addbook_dialogue import Ui_Dialog as ui_addbookdialogue
from Edit_dialogue import Ui_Dialog as ui_editdialogue
from Main_window import Ui_MainWindow
import muy_functions as lib
import Mongo as Mo
from stylesheets import main_style_sheet
class edit_Dialogue(QDialog):
    def __init__(self,parent=None):
        super(edit_Dialogue, self).__init__(parent)
        self.ui=ui_editdialogue()
        self.ui.setupUi(self)
        self.ui.okeditbtn.accepted.connect(self.accept)
        self.ui.okeditbtn.rejected.connect(self.reject)

class delete_Dialogue(QDialog):
    def __init__(self,parent=None):
        super(delete_Dialogue, self).__init__(parent)
        self.ui=ui_deletedialogue()
        self.ui.setupUi(self)
        self.ui.okdeletebtn.accepted.connect(self.accept)
        self.ui.okdeletebtn.rejected.connect(self.reject)

class add_Dialogue(QDialog):
    def __init__(self,parent=None):
        super(add_Dialogue, self).__init__(parent)
        self.ui=ui_addbookdialogue()
        self.ui.setupUi(self)
        self.ui.okeditbtn.accepted.connect(self.accept)
        self.ui.okeditbtn.rejected.connect(self.reject)

class Mainwindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(Mainwindow,self).__init__(parent)
        self.setupUi(self)
        #self.setStyleSheet(main_style_sheet)
        self.pushButton_2.pressed.connect(self.show_adddialogue)
        self.issued_table()
        self.unissued_table()
        self.all_table()
        self.edit_btn_3.clicked.connect(lambda :self.edit_book(self.issued_table_2))
        self.delete_btn_3.pressed.connect(lambda : self.delete_book(self.issued_table_2))
        self.refresh_btn_3.clicked.connect(lambda :self.issued_table())
        self.edit_btn_4.clicked.connect(lambda :self.edit_book(self.unissued_table_2))
        self.delete_btn_4.pressed.connect(lambda: self.delete_book(self.unissued_table_2))
        self.refresh_btn_4.clicked.connect(lambda: self.unissued_table())
        self.refreshall_btn.clicked.connect(lambda: self.all_table())
        self.find_btn.clicked.connect(lambda :self.search_book())



    def save_existing_book(self,ui):
        book={
            'id':int(ui.idinput.text()),
            'name':ui.nameinput.text(),
            'description':ui.descriptioninput.text(),
            'isbn':ui.isbninput.text(),
            'page_count':int(ui.pagecountinput.text()),
            'issued':ui.yesbtn.isChecked(),
            'author':ui.authorinput.text(),
            'year':int(ui.yearinput.text())
        }
        lib.update_book(book)
    def show_adddialogue(self):
        add_dlg=add_Dialogue()
        add_dlg.ui.okeditbtn.accepted.connect(lambda:self.save_book(add_dlg.ui))
        add_dlg.exec()
    def save_book(self,ui):
        new_book={
            'id':int(ui.idinput.text()),
            'name':ui.nameinput.text(),
            'description':ui.descriptioninput.text(),
            'isbn':ui.isbninput.text(),
            'page_count':int(ui.pagecountinput.text()),
            'issued':ui.yesbtn.isChecked(),
            'author':ui.authorinput.text(),
            'year':int(ui.yearinput.text())
        }
        for key in new_book:
            if new_book[key]==None or str(new_book[key])=="":
                return False
        lib.add_book(new_book)
    def issued_table(self):
        books=Mo.get_missuedbooks()
        self.issued_table_2.setRowCount(len(books))
        for index, book in enumerate(books):
            book = book.to_dict()
            for book_index, attr in enumerate(book):
                self.issued_table_2.setItem(index, book_index, QTableWidgetItem(str(book[str(attr)])))
                self.issued_table_2.item(index, book_index).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def unissued_table(self):
        books=lib.get_unissuedbooks()
        self.unissued_table_2.setRowCount(len(books))
        for index, book in enumerate(books):
            book = book.to_dict()
            for book_index, attr in enumerate(book):
                self.unissued_table_2.setItem(index, book_index, QTableWidgetItem(str(book[str(attr)])))
                self.unissued_table_2.item(index, book_index).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)


    def all_table(self):
        books=lib.load_books()
        self.searchall_books_widget.setRowCount(len(books))
        for index, book in enumerate(books):
            book = book.to_dict()
            for book_index, attr in enumerate(book):
                self.searchall_books_widget.setItem(index, book_index, QTableWidgetItem(str(book[str(attr)])))
                self.searchall_books_widget.item(index, book_index).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)


    def edit_book(self,table):
        selected_row=table.currentRow()
        if selected_row!= -1:
            book_id=int(table.item(selected_row,0).text())
            book=lib.find_books(book_id)
            dialog=edit_Dialogue()
            dialog.ui.idinput.setValue(int(book.id))
            dialog.ui.nameinput.setText(book.name)
            dialog.ui.descriptioninput.setText(book.description)
            dialog.ui.isbninput.setText(book.isbn)
            dialog.ui.pagecountinput.setValue(book.page_count)
            dialog.ui.yesbtn.setChecked(book.issued)
            if book.issued==False:
                dialog.ui.nobtn.setChecked(True)
            dialog.ui.authorinput.setText(book.author)
            dialog.ui.yearinput.setValue(book.year)
            dialog.ui.okeditbtn.accepted.connect(lambda :self.save_existing_book(dialog.ui))
            dialog.exec()
            self.issued_table()
            self.unissued_table()
    def delete_book(self,table):
        selected_row=table.currentRow()
        if selected_row!=-1:
            book_id=int(table.item(selected_row,0).text())
            dialog=delete_Dialogue()
            dialog.ui.okdeletebtn.accepted.connect(lambda:lib.deletebook(book_id))
            dialog.exec()
            self.issued_table()
            self.unissued_table()
    def search_book(self):
        if self.find_input.text()!='':
            book=lib.find_books(int(self.find_input.text()))
            if book!=None:
                self.issued_table_3.setRowCount(1)
                book=book.to_dict()
                for index, attr in enumerate(book):
                    self.issued_table_3.setItem(0, index, QTableWidgetItem(str(book[str(attr)])))
                    self.issued_table_3.item(0, index).setFlags(
                            Qt.ItemIsSelectable | Qt.ItemIsEnabled)



app=QApplication([])
window=Mainwindow()
window.show()
app.exec()