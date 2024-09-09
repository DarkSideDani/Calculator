import sys
from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QGridLayout, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QWidget)

# Creating the instance of QApplication
app = QApplication([])
# Creating the app's GUI
window = QWidget()
window.setWindowTitle("DarkSide Calculator")
window.setGeometry(200,200,400,400)
helloMsg = QLabel("<h1>DSD</h1>", parent=window) # Uses HTML elements
helloMsg.move(60, 15) # Location of the helloMsg

layout = QGridLayout()
layout.addWidget(QPushButton("Button (0, 0)"), 0, 0)
layout.addWidget(QPushButton("Button (0, 1)"), 0, 1)
layout.addWidget(QPushButton("Button (0, 2)"), 0, 2)
layout.addWidget(QPushButton("Button (1, 0)"), 1, 0)
layout.addWidget(QPushButton("Button (1, 1)"), 1, 1)
layout.addWidget(QPushButton("Button (1, 2)"), 1, 2)
layout.addWidget(QPushButton("Button (2, 0)"), 2, 0)
layout.addWidget(
    QPushButton("Button (2, 1) + 2 Columns Span"), 2, 1, 1, 2
)
window.setLayout(layout)

#Show the GUI
window.show()
#Run the app event loop
sys.exit(app.exec())