import sys
import requests
from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40
ERROR_MSG = "ERROR"

class PyCalcWindow(QMainWindow):
    """main window (GUI or view)."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DSD Calc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        
        # Set the background color to black and text to white using stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: black;
            }
            QLineEdit {
                background-color: black;
                color: white;
                border: 2px solid gray;
            }
            QPushButton {
                background-color: gray;
                color: white;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: darkgray;
            }
        """)

        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()
        
    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)
        
    def _createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QGridLayout()
        keyBoard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]

        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)

        self.generalLayout.addLayout(buttonsLayout)
        
    def setDisplayText(self, text): # Set the display's text
        self.display.setText(text)
        self.display.setFocus()
        
    def displayText(self):
        return self.display.text() # Get the display's Text
    
    def clearDisplay(self):
        self.setDisplayText("") # Clear the display
        
        
def evaluateExpression(expression):
    """Evaluate an expression (Model)."""
    try:
        # Send a POST request to the backend API with the expression
        response = requests.post("http://127.0.0.1:5000/calculate", json={"expression": expression})
        # Parse the JSON response
        response_json = response.json()
        # Return the result if successful, or an error message if something goes wrong
        if 'result' in response_json:
            return response_json['result']
        else:
            return ERROR_MSG
    except Exception as e:
        print("Error:", str(e)) # Error logger
        return ERROR_MSG

class PyCalc:
    """PyCalc's controller class."""
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, subExpression):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)

    def _connectSignalsAndSlots(self):
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"=", "C"}:
                button.clicked.connect(
                    partial(self._buildExpression, keySymbol)
                )
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)


def main():
    """main function."""
    pycalcApp = QApplication([])
    pycalcWindow = PyCalcWindow()
    pycalcWindow.show()
    PyCalc(model=evaluateExpression, view=pycalcWindow)
    sys.exit(pycalcApp.exec())

if __name__ == "__main__":
    main()
