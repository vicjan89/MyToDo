import datetime
import pickle
from datetime import *
from PIL import Image
#from icalendar import Calendar, Event
from calendar import *

FILENAME = 'todo.dat'
FILENORM = 'norm.dat'
INDENT = '    '

class Time_range:
    def __init__(self, start, delta, summary='', description = ''):
        self.__summary = summary
        self.__start = start
        self.__delta = delta
        self.__description = description

    def __eq__(self, other):
        if other != None:
            if self.__summary == other.__summary and self.__start == other.__start and (
                self.__delta == other.__delta) and self.__description == other.__description:
                return True
            else:
                return False
        else:
            return False

    @property
    def summary(self):
        return self.__summary

    @summary.setter
    def summary(self, summary):
        if type(summary) == str:
            self.__summary = summary
        else:
            raise TypeError('summary должно быть строкой')

    @property
    def delta(self):
        return self.__delta

    @delta.setter
    def delta(self, delta):
        self.__delta = delta

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, start):
        self.__start = start

    @property
    def end(self):
        return self.__start + self.__delta

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        if type(description) == str:
            self.__description = description
        else:
            raise TypeError('description должно быть строкой')

    def __str__(self):
        return str(self.__start) + ' ' + str(self.__start + self.__delta) + ' ' + self .__summary + ' ' + self.__description

class Time_line:
    def __init__(self):
        self.__time_line = []

    def generate_work_time(self):
        today = date.today()
        cal = Calendar()
        yr = today.year
        yr1 = yr
        yr2 = yr
        tm = today.month
        tm1 = tm +1
        if tm1 > 12:
            tm1 = tm1 - 12
            yr1 += 1
        tm2 = tm + 2
        if tm2 > 12:
            tm2 = tm2 - 12
            yr2 += 1
        for d in cal.itermonthdates(yr, tm):
            if d >= today:
                if 0 <= d.weekday() <= 4:
                    self.__time_line.append(Time_range(datetime(d.year, d.month, d.day, 8), timedelta(hours=4)))
                    self.__time_line.append(Time_range(datetime(d.year, d.month, d.day, 13), timedelta(hours=4)))
        for d in cal.itermonthdates(yr1, tm1):
            if 0 <= d.weekday() <= 4:
                self.__time_line.append(Time_range(datetime(d.year, d.month, d.day, 8), timedelta(hours=4)))
                self.__time_line.append(Time_range(datetime(d.year, d.month, d.day, 13), timedelta(hours=4)))
        for d in cal.itermonthdates(yr2, tm2):
            if 0 <= d.weekday() <= 4:
                self.__time_line.append(Time_range(datetime(d.year, d.month, d.day, 8), timedelta(hours=4)))
                self.__time_line.append(Time_range(datetime(d.year, d.month, d.day, 13), timedelta(hours=4)))
        for d in self.__time_line:
            if self.__time_line.count(d) > 1:
                self.__time_line.remove(d)

    def __str__(self):
        r_s = ''
        for i in self.__time_line:
            r_s += str(i)+'\n'
        return r_s

    def get_str(self, day, delta):
        r_s = ''
        for i in self.__time_line:
            if i.start.date() >= day and i.end.date() <= (day + delta):
                r_s += str(i) + '\n'
        return r_s

    def day(self, day):
        r_s = ''
        for i in self.__time_line:
            if i.start.date() == day:
                r_s += str(i) + '\n'
        return r_s

    def add_task(self, task):
        """Добавляет задачу в наиболее раннее свободное время. Если срок задачи ранее свободного времени то вставляет
        задачу в середину со сдвигом остальных. Жёсткие задачи добавляет точно в срок."""
        tr = Time_range(task.start, task.delta, task.task, task.comment)
        tr_rp = Time_range(task.start, task.delta, task.task, task.comment)
        lng = len(self.__time_line)
        i = 0
        while i < lng:
            if self.__time_line[i].summary == '':
                if not task.hard:
                    tr.start = self.__time_line[i].start
                cr, tr = self.cross(self.__time_line[i], tr)
                if len(cr) != 0:
                    self.__time_line.pop(i)
                    for tri in cr:
                        self.__time_line.insert(i, tri)
                        i += 1
                else:
                    i += 1
                if tr == None:
                    if task.repeat_mode == 1:
                        tr_rp.start = tr_rp.start + timedelta(days=1.0)
                        tr = Time_range(tr_rp.start, tr_rp.delta, tr_rp.summary, tr_rp.description)
                        i = 0
                    elif task.repeat_mode == 2:
                        tr_rp.start = tr_rp.start + timedelta(weeks=1.0)
                        tr = Time_range(tr_rp.start, tr_rp.delta, tr_rp.summary, tr_rp.description)
                        i = 0
                    else:
                        return True
            else:
                i += 1
            lng = len(self.__time_line)
        return False

    def add_tasks(self, tasks):
        pass

    @classmethod
    def cross(cls, time_free, time_task):
        """Возвращает список объектов Time_range заполняющих time_free и остаток от неразмещённой задачи time_task.
        Если time_free и time_task не пересекаются то возвращает пустой список. Если time_task размещена полностью или
        находится ранее time_free то возвращает None."""
        ls = []
        if time_free.summary == '':
            if time_free.start >= time_task.end:
                    remainder = None
            if time_free.start > time_task.start:
                if time_free.end == time_task.end:
                    ls.append(Time_range(time_free.start, time_free.delta, time_task.summary, time_task.description))
                    remainder = None
                elif time_free.start < time_task.end <time_free.end:
                    ls.append(Time_range(time_free.start, time_task.end - time_free.start, time_task.summary, time_task.description))
                    ls.append(Time_range(time_task.end, time_free.end - time_task.end))
                    remainder = None
            if time_free.start == time_task.start:
                if time_task.end == time_free.end:
                    ls.append(time_task)
                    remainder = None
                elif time_task.end > time_free.end:
                    remainder = Time_range(time_free.end, time_task.end - time_free.end, time_task.summary, time_task.description)
                    ls.append(Time_range(time_task.start, time_free.delta, time_task.summary, time_task.description))
                else:
                    remainder = None
                    ls.append(time_task)
                    ls.append(Time_range(time_task.end, time_free.end - time_task.end))
            if time_free.start < time_task.start:
                if time_task.end == time_free.end:
                    ls.append(Time_range(time_free.start, time_free.delta - time_task.delta))
                    ls.append(time_task)
                    remainder = None
                elif time_task.end < time_free.end:
                    ls.append(Time_range(time_free.start, time_task.start - time_free.start))
                    ls.append(time_task)
                    ls.append(Time_range(time_task.end, time_free.end - time_task.end))
                    remainder = None
            if (time_task.end > time_free.end) and (time_free.start < time_task.start < time_free.end):
                    ls.append(Time_range(time_free.start, time_task.start - time_free.start))
                    ls.append(Time_range(time_task.start, time_free.end -time_task.start, time_task.summary, time_task.description))
                    remainder = Time_range(time_free.end, time_task.end - time_free.end, time_task.summary, time_task.description)
            if time_free.end <= time_task.start:
                    remainder = time_task
        else:
            remainder = time_task
        return ls, remainder


'''
class Calendar_tasks:
    def __init__(self):
        self.cal = Calendar()
        self.cal.add('prodid', '-//My calendar product//mxm.dk//')
        self.cal.add('version', '2.0')

    def add_event(self, task):
        event = Event()
        event.add('summary', task.task)
        event.add('dtstart', task.start)
        event.add('dtend', task.end)
        self.cal.add_component(event)
'''

class Lables:
    def __init__(self):
        self.lables_list = []

    def add_lable(self, text_lable):
        if text_lable not in self.lables_list:
            self.lables_list.append(text_lable)

    def get(self, list_num):
        ls = []
        ln = len(self.lables_list)
        for li in list_num:
            if li < ln:
                ls.append(self.lables_list[li])
        return ls


class Attachments:
    def __init__(self):
        """Создание объекта хранения вложений"""
        self.attachments = []

    def show_attach(self):
        size = (300, 300)
        img = Image.open(r"C:\Users\Виктор\Pictures\soul-knight-unreleased--ico.jpg")
        img.thumbnail(size)
        img.show()


class Task:
    "Класс описания задачи"

    # Константы для класса Task
    NOREPEAT = 0
    EVERYDAY = 1
    EVERYWEEK = 2
    EVERYMONTH = 3
    EVERYYEAR = 4
    HIGH = True
    LOW = False
    HARD = True
    NO_HARD = False
    MISTAKE = 'mistake'

    def __init__(self, task='', start='', end='', repeat_mode=NOREPEAT, priority=LOW, comment='', duration=0.0, status=0,
                 hard=NO_HARD, lables=[], attachment=[]):
        """Создаёт задачу"""
        self.task = task
        self.start = start
        self.end = end
        self.repeat_mode = repeat_mode
        self.priority = priority
        self.comment = comment
        self.duration = duration
        self.status = status
        self.hard = hard
        self.progress = 0
        self.lables = lables
        self.attachment = attachment
        self.child_tasks = List_tasks()

    @classmethod
    def verify_task_comment(cls, task_comment):
        if type(task_comment) != str:
            raise TypeError('Должа быть строка')
        return True

    @classmethod
    def verify_start_end_type(cls, start_end):
        if type(start_end) != str:
            raise TypeError('Должа быть строка')
        return True

    @classmethod
    def verify_start_end_format(cls, start_end):
        if start_end != '':
            if len(start_end) == 8 and start_end[2] == '/' and start_end[5] == '/':
                format_start_end = '%d/%m/%y'
            elif len(start_end) == 10 and start_end[2] == '/' and start_end[5] == '/':
                format_start_end = '%d/%m/%Y'
            elif len(start_end) == 14 and start_end[2] == '/' and start_end[5] == '/' and start_end[8] == ' ' and start_end[11] == '-':
                format_start_end = '%d/%m/%y %H-%M'
            elif len(start_end) == 16 and start_end[2] == '/' and start_end[5] == '/' and start_end[10] == ' ' and start_end[13] == '-':
                format_start_end = '%d/%m/%Y %H-%M'
            else:
                format_start_end = cls.MISTAKE
        else:
            format_start_end = ''
        return format_start_end

    @classmethod
    def verify_status(cls, status):
        if type(status) != int:
            raise TypeError('Должно быть целое число')
        if 0 <= status <= 3:
            return True
        else:
            return False

    @classmethod
    def verify_duration(cls, duration):
        if type(duration) != float:
            raise TypeError('Должно быть вещественное число')
        if duration < 0:
            return False
        else:
            return True

    def add_sub_task(self, task):
        """Добавляет подзадачу к задаче"""
        self.child_tasks.add_task(task)

    def __str__(self):
        """Возвращает через функции print и str данные задачи без вложений в виде строки"""
        if self.priority:
            pr = 'Важно!'
        else:
            pr = ''
        if self.hard:
            hr = 'Жёсткая!'
        else:
            hr = ''
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
        st_ret = str(self.start) + '\t' + str(self.duration) + ' (' + str(self.progress) + '%)' + '\t' + self.task + '\t' + pr + '\n' + str(
            self.duration) + 'ч.' + '\t' + str(self.end) + '\t' + str(self.delta) + '\t'+ self.comment + '\t' + sts + '\t' + hr + '\n' + '-' * 100
        return st_ret

    @property
    def task(self):
        '''Возвращает наименование задачи'''
        return self.__task

    @task.setter
    def task(self, task):
        """Изменяет наименование задачи"""
        if self.verify_task_comment(task):
            self.__task = task

    @property
    def start(self):
        '''Возвращает дату и время начала задачи'''
        return self.__start

    @start.setter
    def start(self, start):
        """Изменяет дату и время начала задачи"""
        if self.verify_start_end_type(start):
            fmt = self.verify_start_end_format(start)
            if fmt == '' or fmt == self.MISTAKE:
                self.__start = ''
            else:
                self.__start = datetime.strptime(start, fmt)

    @property
    def end(self):
        '''Возвращает дату и время окончания задачи'''
        return self.__end

    @end.setter
    def end(self, end):
        """Изменяет дату и время окончания задачи"""
        if self.verify_start_end_type(end):
            fmt = self.verify_start_end_format(end)
            if fmt == '' or fmt == self.MISTAKE:
                self.__end = ''
            else:
                self.__end = datetime.strptime(end, fmt)
                #self.__end = self.__end.replace(hour=23, minute=59, second=59)

    @property
    def delta(self):
        """Возвращает оставшуюся несделанную длительность задачи."""
        if self.hard:
            return self.end - self.start
        else:
            return timedelta(hours=self.duration * (100 - self.progress) / 100)

    @property
    def repeat_mode(self):
        '''Возвращает режим повторения задачи'''
        return self.__repeat_mode

    @repeat_mode.setter
    def repeat_mode(self, repeat_mode):
        """Изменяет режим повторения задачи"""
        if 0 <= repeat_mode <= 4:
            self.__repeat_mode = repeat_mode

    @property
    def priority(self):
        '''Возвращает важность задачи'''
        return self.__priority

    @priority.setter
    def priority(self, priority):
        """Изменяет важность задачи"""
        if type(priority) == bool:
            self.__priority = priority
        else:
            raise TypeError('Важность должна быть логического типа')

    @property
    def comment(self):
        '''Возвращает комментарий к задаче'''
        return self.__comment

    @comment.setter
    def comment(self, comment):
        """Изменяет комментарий к задаче"""
        if self.verify_task_comment(comment):
            self.__comment = comment

    @property
    def duration(self):
        '''Возвращает трудозатраты задачи в часах'''
        return self.__duration

    @duration.setter
    def duration(self, duration):
        """Изменяет трудозатраты задачи в часах"""
        if self.verify_duration(duration):
            self.__duration = duration

    @property
    def duration_hours(self):
        """Возвращает число целых часов трудозатрат"""
        return int((self.__duration - int(self.__duration)) * 60)

    @property
    def duration_minutes(self):
        """Возвращает число целых часов трудозатрат"""
        return int(self.__duration)

    @property
    def status(self):
        '''Возвращает статус задачи'''
        return self.__status

    @status.setter
    def status(self, status):
        """Изменяет статус задачи"""
        if self.verify_status(status):
            self.__status = status

    @property
    def hard(self):
        '''Возвращает жёсткость задачи'''
        return self.__hard

    @hard.setter
    def hard(self, hard):
        """Изменяет жёсткость задачи"""
        if type(hard) == bool:
            self.__hard = hard
        else:
            raise TypeError('Жёсткость должна быть логического типа')

    @property
    def progress(self):
        '''Возвращает прогресс задачи'''
        return self.__progress

    @progress.setter
    def progress(self, progress):
        """Изменяет прогресс задачи"""
        if type(progress) != int:
            raise TypeError('Прогресс должен быть целым числом')
        elif progress < 0:
            self.__progress = 0
        elif progress >100:
            self.__progress = 100
        else:
            self.__progress = progress

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
        """Создаёт список задач"""
        self.tasklist = []

    def add_task(self, task: Task):
        """Добавляет задачу в список"""
        self.tasklist.append(task)

    def del_task(self, index: int):
        """Удаляет задачу из списка по её номеру"""
        self.tasklist.pop(index)

    def get_task(self, index: int):
        """Возвращает задачу из списка по её индексу"""
        if len(self.tasklist) >= index:
            return self.tasklist[index]

    def get_sub_list(self, index: int):
        """Возвращает список подзадач задачи с индексом index"""
        tsk = self.get_task(index)
        return tsk.tasklist

    def get_tasks(self):
        """Возвращает все задачи списка"""
        if self.not_empty():
            return self.tasklist

    def get_hard(self):
        """Возвращает все жёсткие задачи в порядке времени окончания"""
        lst = []
        if self.not_empty():
            for item in self.tasklist:
                if item.hard or item.repeat_mode != item.NOREPEAT:
                    lst.append(item)
            lst.sort(key=lambda ts: ts.end)
        return lst

    def get_important(self):
        """Возвращает все важные задачи в порядке времени окончания"""
        lst = []
        if self.not_empty():
            for item in self.tasklist:
                if not item.hard and item.repeat_mode == item.NOREPEAT and item.priority:
                    lst.append(item)
            lst.sort(key=lambda ts: ts.end)
        return lst

    def get_not_important(self):
        """Возвращает все неважные задачи в порядке времени окончания"""
        lst = []
        if self.not_empty():
            for item in self.tasklist:
                if not item.hard and item.repeat_mode == item.NOREPEAT and not item.priority:
                    lst.append(item)
            lst.sort(key=lambda ts: ts.end)
        return lst

    def not_empty(self):
        """Возвращает True если список непустой"""
        if len(self.tasklist) > 0:
            return True
        else:
            return False

    def in_range(self, index):
        """Возвращает True если элемент с номером index есть в списке"""
        if len(self.tasklist) > index:
            return True
        else:
            return False

    def get_tasks_range(self, start='', end='', status=10):
        """Возвращает список задач, включая вложенные, попадающих в указанный диапазон дат"""
        if len(self.tasklist) > 0:
            list_tasks = []
            for task in self.tasklist:
                if task.start == '' and task.end.date() >= start or task.start.date() <= end and task.end == '' or task.start.date() <= end and task.end.date() >= start:
                    list_tasks.append(task)
                lt = task.child_tasks
                if lt.not_empty():
                    list_tasks += lt.get_tasks_range(start, end, status)
            return list_tasks

    def sort_by_end(self):
        """Сортирует задачи по возрастанию срока окончания."""
        self.tasklist.sort(key=lambda tl: tl.end)


class Time_norm:
    def __init__(self):
        """Создаёт объект хранения норм времни"""
        self.norm = {}

    def add_norm(self, magnitude: str, norm: float):
        """Добавляет единицу измерения и её норму времни"""
        self.norm[magnitude] = norm

    def get_norm(self, magnitude: str):
        """Возвращает норму времни по величине"""
        if magnitude in self.norm:
            return self.norm(magnitude)
        else:
            return 1.0


class Store:
    def __init__(self, filename):
        """Создаёт объект умеющий хранить объекты в бинарном файле с именем filename."""
        self.filename = filename

    def save(self, object_store):
        """Сохраняет объект в бинарный файл"""
        with open(self.filename, 'wb') as file:
            pickle.dump(object_store, file)

    def load(self):
        """Читает задачу с подзадачами из бинарного файла"""
        with open(self.filename, 'rb') as file:
            return pickle.load(file)


class cmd:
    def __init__(self, store_task, store_norm, norm):
        """Создаёт объект командной строки"""
        self.current = []
        self.current_task = Task()
        self.s_t_d = store_task
        self.s_n = store_norm
        self.nm = norm
        self.main_list = self.s_t_d.load()
        self.current_list = self.main_list

    def mainloop(self):
        """Главный цикл обработки команд"""
        stop = False
        while not stop:
            prompt = ''
            self.current_list = self.main_list
            for s_pr in self.current:
                self.current_task = self.current_list.get_task(s_pr)
                self.current_list = self.current_task.child_tasks
                prompt += '/' + self.current_task.task
            p = input(prompt + '>')
            if p == '+':
                n = input('Введите задачу: ')
                rp = input('Повторение (1 - ежедневно, 2 - еженедельно, 3 - ежемесячно, 4 - ежегодно): ')
                if rp != '':
                    rp = int(rp)
                    h = '+'
                else:
                    rp = 0
                    h = input('Жёсткая задача?(+): ')
                if h == '+':
                    hd = self.current_task.HARD
                    st = 0
                    pr = self.current_task.LOW
                    du = 0.0
                else:
                    hd = self.current_task.NO_HARD
                    st = input('Статус (0 - не начата, 1 - выполняется, 2 - ожидает, 3 - выполнена): ')
                    if st != '':
                        st = int(st)
                    else:
                        st = 0
                    if input('Важное?(+)') == '+':
                        pr = self.current_task.HIGH
                    else:
                        pr = self.current_task.LOW
                    du = input('Трудоёмкость: ')
                    if du == '':
                        du = 0.0
                    else:
                        dig = ''
                        mag = ''
                        for i in du:
                            if i.isdigit() or '.':
                                dig += i
                            else:
                                mag += i
                        du = self.nm.get_norm(mag) * float(dig)
                s = input('Дата начала: ')
                e = input('Дата конца: ')
                c = input('Примечание: ')
                self.current_list.add_task(
                    Task(task=n, start=s, end=e, priority=pr, comment=c, duration=du, status=st, hard=hd, repeat_mode=rp))
            elif p == 'с':
                self.s_t_d.save(self.main_list)
            elif p == 'о':
                self.main_list = self.s_t_d.load()
                self.current_list = self.main_list
            elif p == 'п':
                if self.current_list.not_empty():
                    for i, task in enumerate(self.current_list.get_tasks()):
                        if task.progress < 100:
                            print('--', i+1, '--', task)
                else:
                    print('Подзадачи отсутствуют')
            elif p == 'в':
                self.s_t_d.save(self.main_list)
                stop = True
            elif p.isdigit():
                p = int(p) - 1
                if p >= 0:
                    if self.current_list.in_range(p):
                        self.current.append(p)
            elif p == '..':
                if len(self.current) > 0:
                    self.current.pop()
            elif p == 'сп':
                pass
            elif p == 'д':
                tl = Time_line()
                tl.generate_work_time()
                for ts in self.current_list.get_hard():
                    tl.add_task(ts)
                for ts in self.current_list.get_important():
                    if ts.progress < 100:
                        tl.add_task(ts)
                for ts in self.current_list.get_not_important():
                    if ts.progress < 100:
                        tl.add_task(ts)
                print(tl.day(date.today()))
            elif p == 'з':
                tl = Time_line()
                tl.generate_work_time()
                for ts in self.current_list.get_hard():
                    tl.add_task(ts)
                for ts in self.current_list.get_important():
                    if ts.progress < 100:
                        tl.add_task(ts)
                for ts in self.current_list.get_not_important():
                    if ts.progress < 100:
                        tl.add_task(ts)
                print(tl.day(date.today() + timedelta(days=1)))
            elif p == 'н':
                tl = Time_line()
                tl.generate_work_time()
                for ts in self.current_list.get_hard():
                    tl.add_task(ts)
                for ts in self.current_list.get_important():
                    if ts.progress < 100:
                        tl.add_task(ts)
                for ts in self.current_list.get_not_important():
                    if ts.progress < 100:
                        tl.add_task(ts)
                print(tl.get_str(date.today(), timedelta(days=7)))
            elif p == 'м':
                dt = datetime.now()
                dt = dt.date()
                for task in self.main_list.get_tasks_range(dt, dt + timedelta(30)):
                    if task != None:
                        print(task)
            elif p == 'ст':
                self.current_task.status = int(input('Статус (0 - не начата, 1 - выполняется, 2 - ожидает, 3 - выполнена): '))
            elif p == 'уд':
                nu = int(input('Номер удаляемой задачи: '))-1
                self.current_list.del_task(nu)
            elif p == 'пр':
                pr = int(input('Прогресс: '))
                self.current_task.progress = pr
            elif p == 'нач':
                st = input('Начало: ')
                self.current_task.start = st
            elif p == 'кон':
                en = input('Конец: ')
                self.current_task.end = en
            elif p == 'пл':
                tl = Time_line()
                tl.generate_work_time()
                for ts in self.current_list.get_hard():
                    tl.add_task(ts)
                for ts in self.current_list.get_important():
                    if ts.progress < 100:
                        tl.add_task(ts)
                for ts in self.current_list.get_not_important():
                    if ts.progress < 100:
                        tl.add_task(ts)
                print(tl)
            else:
                print('Недопустимая команда!')


if __name__ == '__main__':
    s_t = Store(FILENAME)
    s_n = Store(FILENORM)
    n = Time_norm()
    tl = Time_line()
    c = cmd(store_task=s_t, store_norm=s_n, norm=n)
    c.mainloop()
