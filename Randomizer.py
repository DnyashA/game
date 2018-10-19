import random

class Randomizer:
    def __init__(self):
        self.pieces = ['r', 'g', 'b'] * 5
        self.template = []


    def generateField(self):
        for i in range(4):
            self.pieces.append('o')
        #Заполнение четных рядов исключая возможность попадания в них блокирующих плиток
        for i in range(5):
            self.template.append([])
            for j in range(5):
                self.template[i].append(0)
        random.shuffle(self.pieces)
        for i in range(5):
            for j in range(0, 6, 2):
                self.template[i][j] = self.pieces.pop()
        #Нечетные ряды с блокирующими плитками
        for i in range(6):
            self.pieces.append('x')
        random.shuffle(self.pieces)
        for i in range(5):
            for j in range(1, 5, 2):
                self.template[i][j] = self.pieces.pop()

        self.deadlockCheck()
    #Решение проблемы со стеной, перекрывающей поле
    def deadlockSolve(self, column):
        piece = random.randint(0, 4)
        for i in range(5):
            #1 ^ 2 = 3, 3 ^ 2 = 1 : выбираем разрешенную для блоков колонку(блоки либо в 1 либо в 3 колонке)
            if self.template[i][column ^ 2] != 'x':
                self.template[piece][column] = self.template[i][column ^ 2]
                self.template[i][column ^ 2] = 'x'
                break

    def deadlockCheck(self):
        if [i[1] for i in self.template] == ['x'] * 5:
            self.deadlockSolve(1)
        if [i[3] for i in self.template] == ['x'] * 5:
            self.deadlockSolve(3)