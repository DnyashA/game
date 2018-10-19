import sys
from PyQt5.QtWidgets import QApplication

from Field import Field

app = QApplication(sys.argv)

if __name__ == '__main__':
    try:
        f = Field(random=sys.argv[1])
    except IndexError:
        f = Field()
    f.show()
    app.exec_()