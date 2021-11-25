import pickle
import pyperclip
from datetime import *

FILENAME = 'todo.dat'


class ToDo:
    def __init__(self, t_d, start='', end='', priority='', comment='', duration='', status='', child_todo=[]):
        self.td = t_d
        if start != '':
            self.start = datetime.strptime(start, '%d/%m/%y %H-%M')
        else:
            self.start = start
        if end != '':
            self.end = datetime.strptime(end, '%d/%m/%y %H-%M')
        else:
            self.end = end
        if priority == '+':
            self.priority = True
        else:
            self.priority = False
        self.parent_td = parent_td
        self.comment = comment
        if duration == '':
            self.duration = 0.0
        elif duration[-1] == 'с':
            self.duration = int(duration[:-1])*2/60
        else:
            self.duration = float(duration)
        if status == '':
            self.status = 0
        else:
            self.status = int(status)
        self.child_todo = child_todo

    def __str__(self):
        if self.priority:
            sp = ' Важно!'
        else:
            sp = ' '
        return self.td + '\n' + 'Начало: ' + str(self.start) + ' Конец: ' + str(
            self.end) + sp + '\n' + 'Примечание: ' + self.comment


class Store:
    def __init__(self, filename):
        self.filename = filename
        self.list_todo = []

    def save_todo(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.list_todo, file)

    def load_todo(self):
        with open(self.filename, 'rb') as file:
            self.list_todo = pickle.load(file)

    def add_todo(self, t_d: ToDo):
        self.list_todo.append(t_d)

    def view(self, num):
        print(self.list_todo[num])

    def __str__(self):
        string_to_print = ''
        for nu, i in enumerate(self.list_todo):
            string_to_print += '----' + str(nu) + '----' + '\n' + str(i) + '\n' * 2
        return string_to_print


if __name__ == '__main__':
    s_t_d = Store(FILENAME)
    prompt = 'todo>'
    current_todo = s_t_d
    while True:
        p = input(prompt)
        if p == '+':
            n = input('Введите задачу: ')
            s = input('Дата начала: ')
            e = input('Дата конца: ')
            pr = input('Важное?(+)')
            c = input('Примечание: ')
            du = input('Трудоёмкость: ')
            st = input('Статус (0 - не начата, 1 - выполняется, 2 - ожидает, 3 - выполнена): ')
            td = ToDo(n, s, e, pr, c, du, st)
            s_t_d.add_todo(td)
            print('Добавлено', td)
        elif p == 'с':
            s_t_d.save_todo()
        elif p == 'о':
            s_t_d.load_todo()
        elif p == 'п':
            print(s_t_d)
        elif p == 'в':
            s_t_d.save_todo()
            break
        elif p.isdigit():
            print(s_t_d.view(int(p)))
            prompt = 'todo/'+p+'>'
        else:
            print('Недопустимая команда!')
