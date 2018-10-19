Поле для игры представляет собой матрицу 5х5, где каждый элемент представляет собой код плитки. 
Плитки могут иметь следующие коды: r - красная, g - зеленая, b - синяя, x - блок, o - путь.
Выбор плитки осуществляется нажатием на нее левой кнопкой мыши, перемещение с помощью стрелок на клавиатуре или WASD.
Условием победы является выстроение в столбец(над треугольником соответствующего цвета) плиток одного цвета для каждого цвета.

В классе Field реализованны методы генерации поля, выбора плитки, ее перемещения и отрисовки самого поля.
В классе Randomizer реализованна генерация случайной разметки для поля. А также, методы разрешения ситуации, когда завершение
игры невозможно по причине наличия блокирующей все поле стены блоков.

Возможность передвижения плитки осуществлялась посредством проверки кода соседней в направлении движения плитки. В случае если
был получен код "о"(открытый путь) плитки меняются местами.

Для реализации графического интерфейса была использована библиотека PyQt(наличие ее на машине для запуска не требуется).
По умолчанию игра запускается с пресетовым полем. Для запуска игры с рандомным полем необходимо запустить ее с параметром "True".
Либо через ярлык game_random.
Исполняемые файлы находятся в папке bin в корне.
Тестирование проводилось на базе ОС Windows 10