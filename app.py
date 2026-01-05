import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("My First App")

label = QLabel("Click the button")
button = QPushButton("Click me")

def on_button_clicked():
    label.setText("Button was clicked!")

button.clicked.connect(on_button_clicked)

layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)
window.setLayout(layout)

window.show()
app.exec()
