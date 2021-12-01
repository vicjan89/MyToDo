import datetime
import pickle
from datetime import *

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

class Attachments:
    def __init__(self):
        '''Создание объекта хранения вложений'''
        self.attachments = []

#Константы для класса Task
NOREPEAT = 0
EVERYDAY = 1
EVERYWEEK = 2
EVERYMONTH =3
EVERYYEAR = 4


class Task:
    def __init__(self, t_d='', start='', end='', repeat_mode=NOREPEAT, priority='', comment='', duration='', status='', hard='', lables=[], attachment=[]):
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
        self.child_tasks = List_tasks()
        if hard == '+':
            self.hard = True
        else:
            self.hard = False
        self.progress = 0.0
        self.lables = lables
        self.attachment = attachment

    def add_sub_task(self, task):
        '''Добавляет подзадачу к задаче'''
        self.child_tasks.add_task(task)

#    def get_tasks_range(self, date_start, date_end):
        '''Возвращает список задач, попавших в заданный диапазон дат
        if len(self.child_tasks) > 0:
            list_tasks = []
            for task in self.child_tasks:
                if task.status != 3:
                    if task.start.date() <= date_end and task.end.date() >= date_start:
                        list_tasks.append(task)
                    for sub_task in task.child_tasks:
                        list_tasks.append(sub_task.get_tasks_range(date_start, date_end))
            return list_tasks
'''
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

#    def get_tasks(self):
        '''Возвращает строку задачи и всех вложенных задач. Вложенные задачи имеют номер и отступ
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
        if len(self.child_tasks) != 0:
            for n, i in enumerate(self.child_tasks):
                st_ed = i.get_tasks()
                st_ret += '\n' + '└─' + str(n+1)+ '──' + st_ed[5:]
        st_ret = st_ret.replace('\n', '\n    ')
        return st_ret
'''

class List_tasks:
    def __init__(self):
        '''Создаёт список задач'''
        self.tasklist = []

    def add_task(self, task: Task):
        '''Добавляет задачу в список'''
        self.tasklist.append(task)

    def del_task(self, index: int):
        '''Удаляет задачу из списка по её номеру'''
        self.tasklist.pop(index)

    def get_task(self, index: int):
        '''Возвращает задачу из списка по её индексу'''
        if self.not_empty():
            return self.tasklist[index]

    def get_tasks(self):
        '''Возвращает все задачи списка'''
        if self.not_empty():
            return self.tasklist

    def not_empty(self):
        '''Возвращает True если список непустой'''
        if len(self.tasklist)>0:
            return True
        else:
            return False

    def get_tasks_range(self, start, end):
        '''Возвращает список задач, включая вложенные, попадающих в указанный диапазон дат'''
        if len(self.tasklist) > 0:
            list_tasks = []
            for task in self.tasklist:
                if task.start.date() <= end and task.end.date() >= start:
                    list_tasks.append(task)
                lt = task.child_tasks
                if lt.not_empty():
                    list_tasks += lt.get_tasks_range(start, end)
            return list_tasks

class Store:
    def __init__(self, filename):
        '''Создаёт объект умеющий хранить задачи в бинарном файле с именем filename.'''
        self.filename = filename

    def save_todo(self, task_list: List_tasks):
        '''Сохраняет задачу ч подзадачами в бинарный файл'''
        with open(self.filename, 'wb') as file:
            pickle.dump(task_list, file)

    def load_todo(self):
        '''Читает задачу с подзадачами из бинарного файла'''
        with open(self.filename, 'rb') as file:
            return pickle.load(file)

class cmd:
    def __init__(self, store):
        '''Создаёт объект командной строки'''
        self.current = []
        self.current_task = Task()
        self.s_t_d = store
        self.main_list = List_tasks()
        self.current_list = self.main_list

    def mainloop(self):
        '''Главный цикл обработки команд'''
        stop = False
        while not stop:
            prompt = ''
            for s_pr in self.current:
                self.current_task = self.current_list.get_task(s_pr)
                prompt += '/' + self.current_task.td
            p = input(prompt + '>')
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
                self.current_list.add_task(Task(n, s, e, pr, c, du, st, h))
            elif p == 'с':
                self.s_t_d.save_todo(self.main_list)
            elif p == 'о':
                self.main_list = self.s_t_d.load_todo()
                self.current_list = self.main_list
            elif p == 'п':
                for task in self.current_list.get_tasks():
                    print(task)
            elif p == 'в':
                self.s_t_d.save_todo(self.main_list)
                stop = True
            elif p.isdigit():
                p = int(p) - 1
                if (len(self.current_task.child_tasks) - 1) >= p:
                    self.current.append(p)
            elif p == '..':
                if len(self.current) > 0:
                    self.current.pop()
            elif p == 'д':
                dt = datetime.now()
                for task in self.main_list.get_tasks_range(dt.date(), dt.date()):
                    if task != None:
                        print(task)
            elif p == 'з':
                dt = datetime.now()
                dt = dt.date() + timedelta(1)
                for task in self.main_list.get_tasks_range(dt, dt):
                    if task != None:
                        print(task)
            elif p == 'н':
                dt = datetime.now()
                dt = dt.date()
                for task in self.main_list.get_tasks_range(dt, dt + timedelta(6)):
                    if task != None:
                        print(task)
            elif p == 'м':
                dt = datetime.now()
                dt = dt.date()
                for task in self.main_list.get_tasks_range(dt, dt + timedelta(30)):
                    if task != None:
                        print(task)
            elif p == 'ст':
                self.current_task.change_status(
                    int(input('Статус (0 - не начата, 1 - выполняется, 2 - ожидает, 3 - выполнена): ')))
            else:
                print('Недопустимая команда!')


if __name__ == '__main__':
    s = Store(FILENAME)
    c = cmd(s)
    c.mainloop()


