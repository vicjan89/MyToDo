import datetime
import pickle
import pyperclip
from datetime import *
import calendar
import os

FILENAME = 'todo.dat'
INDENT = '    '

class Lables:
    def __init__(self):
        self.lables_list = []

    def add_lable(self, text_lable):
        if text_lable not in self.lables_list:
            self.lables_list.append(text_lable)

    def get(self, list_num):
        ls = []
        ln = len(self.lables_list)
        for l in list_num:
            if l < ln:
                ls.append(self.lables_list[l])
        return ls

class ToDo:
    def __init__(self, t_d, start='', end='', priority='', comment='', duration='', status='', hard='', lables=[], attachment=[]):
        '''Создаёт задачу'''
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
                self.end = self.end.replace(hour=23, minute=59, second=59)
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
        self.progress = 0.0
        self.lables = lables
        self.attachment = attachment

    def add_sub_task(self, todo):
        '''Добавляет подзадачу к задаче'''
        self.child_todo.append(todo)

    def get_tasks_frame(self, date_start, date_end):
        '''Возвращает список задач, попавших в заданный диапазон дат'''
        if len(self.child_todo) > 0:
            list_tasks = []
            for task in self.child_todo:
                if task.status != 3:
                    if task.start.date() <= date_end and task.end.date() >= date_start:
                        list_tasks.append(task)
                    for sub_task in task.child_todo:
                        list_tasks.append(sub_task.get_tasks_frame(date_start, date_end))
            return list_tasks

    def __str__(self):
        '''Возвращает через функции print и str данные задачи без вложений в виде строки'''
        if self.priority:
            prt = 'Важно'
        else:
            prt = ''
        if self.status == 0:
            sts = 'Не начата'
        elif self.status == 1:
            sts = 'Выполняется'
        elif self.status == 2:
            sts = 'Ожидает'
        elif self.status == 3:
            sts = 'Выполнена'
        else:
            sts = 'Неправильный статус'
        st_ret = str(self.start) + '\t' + self.td + '\t' + prt + '\n' + str(self.end) + '\t' + self.comment + '\t' + sts + '\n'+'-'*80
        return st_ret

    def change_status(self, status):
        '''Изменяет статус задачи'''
        if status >= 0 and status <= 3:
            self.status = status
        else:
            print('Неверный статус')

    def get_tasks(self):
        '''Возвращает строку задачи и всех вложенных задач. Вложенные задачи имеют номер и отступ'''
        st_ret = '\n' + self.td
        if self.start != '':
            if self.start.time() != time(0, 0, 0):
                st_ret += ' Начало: ' + str(self.start)
            else:
                st_ret += ' Начало: ' + str(self.start.date())
        if self.end != '':
            if self.end.time() != time(23, 59, 59):
                st_ret += ' Конец: ' + str(self.end)
            else:
                st_ret += ' Конец: ' + str(self.end.date())
        if self.priority:
            st_ret += ' Важно!'
        if self.hard:
            st_ret += ' Жёсткая '
        if self.status == 0:
            st_ret += ' Не начата '
        elif self.status == 1:
            st_ret += ' Выполняется '
        elif self.status == 2:
            st_ret += ' Ожидает '
        elif self.status == 3:
            st_ret += ' Выполнена '
        else:
            st_ret += ' Ошибочный статус '
        if self.comment != '':
            st_ret += ' Примечание: ' + self.comment
        if len(self.child_todo) != 0:
            for n, i in enumerate(self.child_todo):
                st_ed = i.get_tasks()
                st_ret += '\n' + '└─' + str(n+1)+ '──' + st_ed[5:]
        st_ret = st_ret.replace('\n', '\n    ')
        return st_ret


class Store:
    def __init__(self, filename):
        '''Создаёт объект умеющий хранить задачи в бинарном файле с именем filename.'''
        self.filename = filename

    def save_todo(self, todo: ToDo):
        '''Сохраняет задачу ч подзадачами в бинарный файл'''
        with open(self.filename, 'wb') as file:
            pickle.dump(todo, file)

    def load_todo(self):
        '''Читает задачу с подзадачами из бинарного файла'''
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
            print(current_todo.get_tasks())
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
        elif p == 'д':
            dt = datetime.now()
            for task in td.get_tasks_frame(dt.date(), dt.date()):
                if task != None:
                    print(task)
        elif p == 'з':
            dt = datetime.now()
            dt = dt.date() + timedelta(1)
            for task in td.get_tasks_frame(dt, dt):
                if task != None:
                    print(task)
        elif p == 'н':
            dt = datetime.now()
            dt = dt.date()
            for task in td.get_tasks_frame(dt, dt + timedelta(6)):
                if task != None:
                    print(task)
        elif p == 'м':
            dt = datetime.now()
            dt = dt.date()
            for task in td.get_tasks_frame(dt, dt + timedelta(30)):
                if task != None:
                    print(task)
        elif p == 'ст':
            current_todo.change_status(int(input('Статус (0 - не начата, 1 - выполняется, 2 - ожидает, 3 - выполнена): ')))
        else:
            print('Недопустимая команда!')
