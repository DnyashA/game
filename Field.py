import math
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QPainter, QPolygonF
from PyQt5.QtCore import Qt, QPointF

from Randomizer import Randomizer


class Field(QWidget):
    def __init__(self, random=False):
        super().__init__()

        self.setWindowTitle('Prototype')

        self.piece_size = 40
        self.resize(self.piece_size * 5, self.piece_size * 6)
        self.random = random

        #Открытые клетки будут иметь код "о"
        self.open_piece = 'o'
        #Закрытые "х"
        self.block_piece = 'x'

        self.randomizer = Randomizer()
        self.field = None
        self.current_piece = None

        self.fit()

    def fit(self):
        if self.random:
            self.randomizer.generateField()
            self.field = self.randomizer.template
        else:
            #Каждая плитка имеет код цвета(RGB)
            self.field = [['r', 'x', 'b', 'x', 'r'],
                            ['g', 'o', 'b', 'o', 'r'],
                            ['b', 'x', 'g', 'x', 'g'],
                            ['r', 'o', 'r', 'o', 'b'],
                            ['g', 'x', 'g', 'x', 'b']]

#Выбор перемещаемой плитки осуществляется нажатием ЛКМ на нее
    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        pos = e.pos()
        x, y = pos.y() // self.piece_size, pos.x() // self.piece_size
        self.current_piece = [x, y]
        #Выбор плиток только на поле
        if self.current_piece[0] > 4 or self.current_piece[1] > 4:
            self.current_piece = None
        self.repaint()

    #Движение осуществляется с помощью стандартных стрелок и WASD
    def keyPressEvent(self, e):
        if self.current_piece is None:
            return

        x, y = self.current_piece

        #Получение кода плитки и ее координат
        def get_piece_id(x, y):
            try:
                return self.field[x][y], x, y
            except IndexError:
                return None

        #Проверяем соседей на предмет их существования и открытости
        def checkNeighbor(dir):
            if dir == 'up':
                if get_piece_id(x - 1, y) is not None and get_piece_id(x - 1, y)[0] == self.open_piece:
                    return True, get_piece_id(x - 1, y)
                else:
                    return False, None

            if dir == 'dn':
                if get_piece_id(x + 1, y) is not None and get_piece_id(x + 1, y)[0] == self.open_piece:
                    return True, get_piece_id(x + 1, y)
                else:
                    return False, None

            if dir == 'rt':
                if get_piece_id(x, y + 1) is not None and get_piece_id(x, y + 1)[0] == self.open_piece:
                    return True, get_piece_id(x, y + 1)
                else:
                    return False, None

            if dir == 'lt':
                if get_piece_id(x, y - 1) is not None and get_piece_id(x, y - 1)[0] == self.open_piece:
                    return True, get_piece_id(x, y - 1)
                else:
                    return False, None

        def swapPieces(neigbor):
            piece = get_piece_id(x, y)[0]
            empty_piece, x1, y1 = neigbor
            self.field[x][y] = empty_piece
            self.field[x1][y1] = piece
            #Обновляем положение выбранной плитки для того, чтобы не нужно было выбирать ее снова после одного хода
            self.current_piece = [x1, y1]
            self.repaint()

        try:
            #Свободные и блокирующие плитки премещать нельзя
            if get_piece_id(x, y)[0] == self.block_piece or get_piece_id(x, y)[0] == self.open_piece:
                return
            #Двигаем в направлении, зависящем от нажатой клавиши
            if e.key() in (Qt.Key_Up, Qt.Key_W):
                if checkNeighbor('up')[0]:
                    swapPieces(checkNeighbor('up')[1])
            if e.key() in (Qt.Key_Down, Qt.Key_S):
                if checkNeighbor('dn')[0]:
                    swapPieces(checkNeighbor('dn')[1])
            if e.key() in (Qt.Key_Left, Qt.Key_A):
                if checkNeighbor('lt')[0]:
                    swapPieces(checkNeighbor('lt')[1])
            if e.key() in (Qt.Key_Right, Qt.Key_D):
                if checkNeighbor('rt')[0]:
                    swapPieces(checkNeighbor('rt')[1])

            #Победа
            if [i[0] for i in self.field] == ['r'] * 5 \
                    and [i[2] for i in self.field] == ['g'] * 5 \
                    and [i[4] for i in self.field] == ['b'] * 5:
                QMessageBox.information(self, 'GZ!', 'U WON')
                self.close()
        except IndexError:
            pass

    #Упрощение конструкции выбора пэинтером цвета плитки в зависимости от ее кода
    def pickColor(self, piece_id):
        if piece_id == 'o':
            return Qt.white
        elif piece_id == 'x':
            return Qt.black
        elif piece_id == 'r':
            return Qt.red
        elif piece_id == 'g':
            return Qt.green
        elif piece_id == 'b':
            return Qt.blue

    def drawPoly(self, n, r, s, pos):
        polygon = QPolygonF()
        w = 360 / n
        for i in range(n):
            t = w * i + s
            x = r * math.cos(math.radians(t))
            y = r * math.sin(math.radians(t))
            polygon.append(QPointF(pos[0] + x, pos[1] + y))
        return polygon

    #Отрисовка поля
    def paintEvent(self, e):
        super().paintEvent(e)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(Qt.black)

        painter.setBrush(Qt.red)
        painter.drawPolygon(self.drawPoly(3, 20, 30, [20, 220]))
        painter.setBrush(Qt.green)
        painter.drawPolygon(self.drawPoly(3, 20, 30, [100, 220]))
        painter.setBrush(Qt.blue)
        painter.drawPolygon(self.drawPoly(3, 20, 30, [180, 220]))

        for i, row in enumerate(self.field):
            y = i * self.piece_size
            for j, piece in enumerate(row):
                x = j * self.piece_size
                painter.setBrush(self.pickColor(piece))
                painter.drawRect(x, y, self.piece_size, self.piece_size)
