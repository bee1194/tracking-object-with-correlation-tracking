import sys
from PyQt5.QtCore import pyqtSlot, QDir
from PyQt5.QtWidgets import QApplication,QDialog, QFileDialog
from PyQt5 import uic
from oop import oop
class dat(QDialog):
	def __init__(self):
		super(dat, self).__init__()
		uic.loadUi('py.ui',self)

		self.btn_wc.clicked.connect(self.wc_clicked)
		self.btn_br1.clicked.connect(self.br1_clicked)
		self.btn_br2.clicked.connect(self.br2_clicked)
		self.btn_ok.clicked.connect(self.ok_clicked)
		
		self.sb.setRange(1,10)
		self.sb.setValue(4)
		self.dsb.setRange(1.1,3)
		self.dsb.setSingleStep(0.1)
		self.dsb.setValue(1.3)

		self.sb_2.setRange(10,100)
		self.sb_2.setValue(20)
		self.sb_2.setSingleStep(2)

		self.sb_3.setRange(10,100)
		self.sb_3.setValue(20)
		self.sb_3.setSingleStep(2)

		self.sp_port.setValue(0)
		self.sp_port.setSingleStep(1)

	@pyqtSlot()
	def wc_clicked(self):
		s1=self.le_tr.text()
		s2=self.le_name.text()
		if not s1:
			print ("Do nothing")
		if not s2:
			print("Do nothing")
		else:
			self.obj = oop( s1, s2, self.sp_port.value(), self.dsb.value(), self.sb.value(), self.sb_2.value(), self.sb_3.value() )	
			self.obj.detectAndTrackMultipleObjs()

	@pyqtSlot()
	def br1_clicked(self):
		print ("clicked browe1 button")
		fileName, _ = QFileDialog.getOpenFileName(self, 'Single File', QDir.currentPath() , '*.xml')
		self.le_tr.setText(fileName)
	@pyqtSlot()
	def br2_clicked(self):
		print ("clicked browe2 button")
		options = QFileDialog.Options()
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;*.mp4;;*.3gp;;*.avi", options=options)
		self.le_v.setText(fileName)
	@pyqtSlot()
	def ok_clicked(self):
		print("clicked OK button")
		s1=self.le_name.text()
		s2=self.le_tr.text()
		s3=self.le_v.text()
		if not s2:
			print("Do nothing")
		if not s3:
			print("Do nothing")
		if not s1:
			print("Do nothing")
		else:	
			obj = oop( s2, s1, s3, self.dsb.value(), self.sb.value(), self.sb_2.value(), self.sb_3.value() )
			obj.detectAndTrackMultipleObjs()

if __name__ == '__main__':
	app=QApplication(sys.argv)
	window=dat()
	window.setWindowTitle("DETECT AND TRACKING")
	window.show()
	sys.exit(app.exec_())