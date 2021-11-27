import pickle
import pyperclip
from datetime import *

FILENAME = 'todo.dat'
INDENT = '    '

class ToDo:
    def __init__(self, t_d, start='', end='', priority='', comment='', duration='', status='', hard=''):
        self.td = t_d
        if start != '':
            if len(start) == 8:
                self.start = datetime.strptime(start, '%d/%m/%y')
            else:
                self.start = datetime.strptime(start, '%d/%m/%y %H-%M')
        else:
            self.start = start
        if end != '':
            if len(end) == 8:
                self.end = datetime.strptime(end, '%d/%m/%y')
            else:
                self.end = datetime.strptime(end, '%d/%m/%y %H-%M')
        else:
            self.end = end
        if priority == '+':
            self.priority = True
        else:
            self.priority = False
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
        self.child_todo = []
        if hard == '+':
            self.hard = True
        else:
            self.hard = False

    def add_sub_task(self, todo):
        self.child_todo.append(todo)

    def __str__(self):
        st_ret = '\n' + self.td
        if self.start != '':
            st_ret += ' Начало: ' + str(self.start)
        if self.end != '':
            st_ret += ' Конец: ' + str(self.end)
        if self.priority:
            st_ret += ' Важно!'
        if self.hard:
            st_ret += ' Жёсткая '
        if self.comment != '':
            st_ret += ' Примечание: ' + self.comment
        if len(self.child_todo) != 0:
            for n, i in enumerate(self.child_todo):
                st_ed = str(i)
                st_ret += '\n' + '└─' + str(n+1)+ '──' + st_ed[5:]
        st_ret = st_ret.replace('\n', '\n    ')
        return st_ret


class Store:
    def __init__(self, filename):
        self.filename = filename

    def save_todo(self, todo: ToDo):
        with open(self.filename, 'wb') as file:
            pickle.dump(todo, file)

    def load_todo(self):
        with open(self.filename, 'rb') as file:
            return pickle.load(file)

if __name__ == '__main__':
    s_t_d = Store(FILENAME)
    td = ToDo('Януш')
    current = []
    while True:
        current_todo = td
        prompt = td.td
        for s_pr in current:
            current_todo = current_todo.child_todo[s_pr]
            prompt += '/'+current_todo.td
        p = input(prompt+'>')
        if p == '+':
            n = input('Введите задачу: ')
            h = input('Жёсткая задача?(+): ')
            if h == '+':
                st = ''
                pr = ''
                du = ''
            else:
                st = input('Статус (0 - не начата, 1 - выполняется, 2 - ожидает, 3 - выполнена): ')
                pr = input('Важное?(+)')
                du = input('Трудоёмкость: ')
            s = input('Дата начала: ')
            e = input('Дата конца: ')
            c = input('Примечание: ')

            new_task = ToDo(n, s, e, pr, c, du, st, h)
            current_todo.add_sub_task(new_task)
        elif p == 'с':
            s_t_d.save_todo(td)
        elif p == 'о':
            td = s_t_d.load_todo()
        elif p == 'п':
            print(current_todo)
        elif p == 'в':
            s_t_d.save_todo(td)
            break
        elif p.isdigit():
            p = int(p)-1
            if (len(current_todo.child_todo)-1) >= p:
                current.append(p)
        elif p == '..':
            if len(current) > 0:
                current.pop()
        else:
            print('Недопустимая команда!')
