import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QTableWidgetItem
from PyQt5 import uic,QtWidgets
import sqlite3

class WindowTodo(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UiMain.ui',self)
        self.state="new"
        self.con = sqlite3.connect('todo.db')
        self.cur = self.con.cursor()

        self.btnSave.setEnabled(False)
        self.btnDelete.setEnabled(False)
        
        self.btnNew.clicked.connect(self.AddNew)
        self.btnSave.clicked.connect(self.Save)
        self.btnDelete.clicked.connect(self.Delete)
        self.tblTodo.itemSelectionChanged.connect(self.selectedRow)
        self.FillTable()

    def AddNew(self):
        self.state="new"
        self.txtTitle.setText("")
        self.txtDescription.setText("")
        self.btnSave.setEnabled(True)
        self.txtTitle.setFocus()

    def Save(self):
        if(self.state=="new"):
            widgetDate = self.dateDate.date()
            selectedDate =str(widgetDate.day())+"/"+str(widgetDate.month())+"/"+str(widgetDate.year())
            self.cur.execute("insert into todo (title,description,todotime) values (?, ?, ?)", (self.txtTitle.text(), self.txtDescription.toPlainText(),selectedDate))
            self.con.commit()
            self.FillTable()
        if(self.state=="edit"):
            widgetDate = self.dateDate.date()
            selectedDate =str(widgetDate.day())+"/"+str(widgetDate.month())+"/"+str(widgetDate.year())
            self.cur.execute("update todo set title=?,description=?,todotime=? where id=?", (self.txtTitle.text(), self.txtDescription.toPlainText(),selectedDate,self.id))
            self.con.commit()
            self.FillTable()
        self.btnSave.setEnabled(False)
        self.btnDelete.setEnabled(False)
        

    def Delete(self):
        try:
            row = self.tblTodo.currentRow()
            id = self.tblTodo.item(row, 0).text()
            self.cur.execute("delete from todo where id=?",(id,))
            self.con.commit()
            self.FillTable()
            self.btnSave.setEnabled(False)
            self.btnDelete.setEnabled(False)
        except:
            print("error")

    def FillTable(self):
        self.cur.execute("SELECT * FROM todo")

        rows = self.cur.fetchall()
        self.tblTodo.setColumnCount(4)
        self.tblTodo.setHorizontalHeaderLabels(['id','Title', 'Description','ToDoDate'])
    
        self.tblTodo.setRowCount(0)
        for row in rows:
            inx = rows.index(row)
            self.tblTodo.insertRow(inx)
            # add more if there is more columns in the database.
            self.tblTodo.setItem(inx, 0, QTableWidgetItem(str(row[0])))
            self.tblTodo.setItem(inx, 1, QTableWidgetItem(str(row[1])))
            self.tblTodo.setItem(inx, 2, QTableWidgetItem(str(row[2])))
            self.tblTodo.setItem(inx, 3, QTableWidgetItem(str(row[3])))
        header = self.tblTodo.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    def selectedRow(self):
        try:   
            self.state="edit"
            row = self.tblTodo.currentRow()
            self.id = self.tblTodo.item(row, 0).text()
            self.txtTitle.setText(self.tblTodo.item(row, 1).text())
            self.txtDescription.setText(self.tblTodo.item(row, 2).text())
            self.btnSave.setEnabled(True)
            self.btnDelete.setEnabled(True)
        except:
            print("error")

app=QApplication(sys.argv)
window = WindowTodo()
window.show()
sys.exit(app.exec_())