import datetime
import pickle
import json
from datetime import *
from PIL import Image
from icalendar import Calendar as ical
from icalendar import Event
from calendar import *
import colorama
from colorama import Fore, Back, Style
from sys import argv

colorama.init()

FILENAME = 'C:/todo.dat'
FILENORM = 'C:/norm.dat'
FILEHIST = 'C:/hist.dat'

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

    def encode(self):
        return dict(summary=self.__summary, start=str(self.__start), delta=str(self.__delta), description=self.__description)

    @staticmethod
    def decode(dict_time_range):
        hours,minutes,seconds = map(int, dict_time_range['delta'].split(':'))
        return Time_range(datetime.strptime(dict_time_range['start'], Task.verify_start_end_format(dict_time_range['start'])),
                                    timedelta(hours=hours, minutes=minutes, seconds=seconds),
                                    dict_time_range['summary'],
                                    dict_time_range['description'])

class Time_line:
    WORK=0
    NON_WORKING=1
    def __init__(self):
        self.__time_line = []

    def generate_work_time(self, time_type=WORK):
        '''Размечает время на линии как свободное в зависимости от time_type. Если WORK то в будни рабочее время с 8 до 17 с
         перерывом на обед с 12 до 13. Если NON_WORKING то в будни с 17 до 23 а в выходные с 8 до 23'''

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
        if time_type == self.WORK:
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
        else:
            for d in cal.itermonthdates(yr, tm):
                if d >= today:
                    if 0 <= d.weekday() <= 4:
                        self.__time_line.append(Time_range(datetime(d.year, d.month, d.day, 17), timedelta(hours=6)))
                    else:
                        self.__time_line.append(Time_range(datetime(d.year, d.month, d.day, 8), timedelta(hours=15)))
            for d in cal.itermonthdates(yr1, tm1):
                if 0 <= d.weekday() <= 4:
                    self.__time_line.append(Time_range(datetime(d.year, d.month, d.day, 17), timedelta(hours=6)))
                else:
                    self.__time_line.append(Time_range(datetime(d.year, d.month, d.day, 8), timedelta(hours=15)))
            for d in cal.itermonthdates(yr2, tm2):
                if 0 <= d.weekday() <= 4:
                    self.__time_line.append(Time_range(datetime(d.year, d.month, d.day, 17), timedelta(hours=6)))
                else:
                    self.__time_line.append(Time_range(datetime(d.year, d.month, d.day, 8), timedelta(hours=15)))
        for d in self.__time_line:
            if self.__time_line.count(d) > 1:
                self.__time_line.remove(d)

    def __str__(self):
        r_s = ''
        for i in self.__time_line:
            r_s += str(i)+'\n'
        return r_s

    def append(self, time_range):
        self.__time_line.append(time_range)

    def get(self):
        return self.__time_line

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

    def get_time_after(self, delta):
        """Возвращает дату и время окончания промежутка времни delta наложенного на рабочее время"""
        for i in self.__time_line:
            if i.summary == '':
                if i.delta > delta:
                    return i.start + delta
                elif i.delta == delta:
                    return i.end
                else:
                    delta -= i.delta

    def add_task(self, task):
        """Добавляет задачу в наиболее раннее свободное время в пересечении множества оставшихся свободных отрезков
         времени и отрезка времени задачи. Жёсткие задачи добавляет точно в срок. Повторяющиеся задачи рассматривает
        как жёсткие. Если задача размещена то возвращает True иначе False"""
        tr = Time_range(task.start, task.delta, task.task, task.comment)
        tr_rp = Time_range(task.start, task.delta, task.task, task.comment)
        lng = len(self.__time_line)
        i = 0
        while i < lng:
            if self.__time_line[i].summary == '':     #Если отрезок времени не занят
                if not task.hard:                         #Если задача не жёсткая
                    if tr.start < self.__time_line[i].start:     #Если задача начинается раньше не занятого отрезка то переносим задачу на начало отрезка
                        tr.start = self.__time_line[i].start
                        if tr.end > task.end:                    #Если срок задачи истёк то не размещаем
                            return False
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
        not_posted = []
        for ts in tasks.get_hard():
            if ts.start < self.__time_line[-1].end:
                if not self.add_task(ts) and ts.repeat_mode == 0:
                    not_posted.append(ts)
        ts_ni = tasks.get_not_important()
        ts_i = tasks.get_important()
        l_ni = len(ts_ni)
        l_i = len(ts_i)
        ni = 0
        i = 0
        stop = True
        while stop:
            if i == l_i or (ni != l_ni and (ts_ni[ni].end < (self.get_time_after(ts_i[i].delta + ts_ni[ni].delta)))):
                if ts_ni[ni].start < self.__time_line[-1].end:
                    if not self.add_task(ts_ni[ni]):
                        not_posted.append(ts_ni[ni])
                ni += 1
            else:
                if ts_i[i].start < self.__time_line[-1].end:
                    if not self.add_task(ts_i[i]):
                        not_posted.append(ts_i[i])
                i += 1
            if i == l_i and ni == l_ni:
                stop = False
        return not_posted

    def paste_time_range(self, list_time_range):
        for i in list_time_range:
            if self.__time_line.count(i) == 0:
                self.__time_line.append(i)

    def copy_day(self, day):
        r_l = []
        for i in self.__time_line:
            if i.start.date() == day:
                r_l.append(i)
        return r_l

    @classmethod
    def cross(cls, time_free, time_task):
        """Возвращает список объектов Time_range заполняющих time_free и остаток от неразмещённой задачи time_task.
        Если time_free и time_task не пересекаются то возвращает пустой список. Если time_task размещена полностью или
        находится ранее time_free то возвращает None."""
        ls = []
        if time_free.summary == '':
            if time_free.start > time_task.start:
                if time_free.end == time_task.end:
                    ls.append(Time_range(time_free.start, time_free.delta, time_task.summary, time_task.description))
                    remainder = None
                elif time_free.start < time_task.end <time_free.end:
                    ls.append(Time_range(time_free.start, time_task.end - time_free.start, time_task.summary, time_task.description))
                    ls.append(Time_range(time_task.end, time_free.end - time_task.end))
                    remainder = None
                elif time_free.start >= time_task.end:
                    remainder = None
                else:
                    ls.append(Time_range(time_free.start, time_free.delta, time_task.summary, time_task.description))
                    remainder = Time_range(time_free.end, time_task.end - time_free.end, time_task.summary,
                                           time_task.description)
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

    def encode(self):
        d = {}
        for num, item in enumerate(self.__time_line):
            d[num] = item.encode()
        return d

    def decode(self, dict_time_line):
        obj_time_line = Time_line()
        for key in dict_time_line:
            d = dict_time_line[key]
            obj_time_line.append(Time_range.decode(dict_time_line[key]))
        return obj_time_line


class Calendar_tasks:
    def __init__(self):
        self.cal = ical()
        self.cal.add('prodid', '-//My calendar product//mxm.dk//')
        self.cal.add('version', '2.0')

    def add_event(self, time_range):
        event = Event()
        event.add('summary', time_range.summary)
        event.add('dtstart', time_range.start)
        event.add('dtend', time_range.end)
        event.add('description', time_range.description)
        self.cal.add_component(event)

    def add_events(self, time_line):
        ltr = time_line.get()
        for i in ltr:
            if i.summary != '':
                self.add_event(i)
        return self.cal.to_ical()

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
    """Класс описания задачи"""

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
                 hard=NO_HARD, progress=0, lables=[], attachment=[]):
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
        self.progress = progress
        self.lables = lables
        self.attachment = attachment
        self.child_tasks = List_tasks()

    def encode(self):
        return dict(task=self.task, start=str(self.start), end=str(self.end), repeat_mode=self.repeat_mode,
                    priority=self.priority, comment=self.comment, duration=self.duration, status=self.status,
                    hard=self.hard, progress=self.progress, child_tasks=self.child_tasks.encode())


    def iterator(self):
        if self.child_tasks.not_empty():
            du = 0.0
            for item in self.child_tasks.iterator():
                du += item.duration
                yield Task(self.task + ' / ' + item.task, item.start, item.end, item.repeat_mode, item.priority,
                           item.comment, item.duration, item.status, item.hard, item.progress, item.lables, item.attachment)
            if self.duration > du:
                yield Task(self.task, self.start, self.end, self.repeat_mode, self.priority, self.comment,
                                self.duration - du, self.status, self.hard, self.progress, self.lables, self.attachment)
        else:
            yield self

    @classmethod
    def verify_task_comment(cls, task_comment):
        if type(task_comment) != str:
            raise TypeError('Должа быть строка')
        return True

    @classmethod
    def verify_start_end_type(cls, start_end):
        if type(start_end) != str and type(start_end) != datetime:
            raise TypeError('Должа быть строка или дата-время')
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
            elif len(start_end) == 19:
                format_start_end = '%Y-%m-%d %H:%M:%S'
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
            pr = Fore.RED
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
        st_ret = pr + str(self.start) + '\t' + str(self.duration) + ' (' + str(self.progress) + '%)' + '\t' + self.task + '\t' + '\n' + str(
            self.duration) + 'ч.' + '\t' + str(self.end) + '\t' + str(self.delta) + '\t'+ self.comment + '\t' + sts + '\t' + hr + '\n' + Style.RESET_ALL + '-' * 150
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
        if type(start) == datetime:
            self.__start = start
        elif self.verify_start_end_type(start):
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
        if type(end) == datetime:
            self.__end = end
        elif self.verify_start_end_type(end):
            fmt = self.verify_start_end_format(end)
            if fmt == '' or fmt == self.MISTAKE:
                self.__end = ''
            else:
                self.__end = datetime.strptime(end, fmt)
                if self.__end <= self.__start:
                    raise Exception('Окончание задачи раньше начала!')

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

class List_tasks:
    def __init__(self):
        """Создаёт список задач"""
        self.tasklist = []

    def encode(self):
        d_l_t = dict()
        for ni, i in enumerate(self.tasklist):
            d_l_t[ni] = i.encode()
        return d_l_t

    def decode(self, d_l_t):
        for key, value in d_l_t.items():
            value_without_child_tasks = {k: v for k, v in value.items() if k != 'child_tasks'}
            task = Task(**value_without_child_tasks)
            if value['child_tasks'] != {}:
                l_t = List_tasks()
                task.child_tasks = l_t.decode(value['child_tasks'])
            self.tasklist.append(task)
        return self

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

    def iterator(self):
        """Возвращает все задачи списка включая подзадачи"""
        if self.not_empty():
            for item in self.tasklist:
                for task in item.iterator():
                    yield task

    def get_hard(self):
        """Возвращает все жёсткие задачи в порядке времени окончания"""
        lst = []
        if self.not_empty():
            for item in self.tasklist:
                if (item.progress < 100) and (item.hard or item.repeat_mode != item.NOREPEAT):
                    lst.append(item)
            lst.sort(key=lambda ts: ts.end)
        return lst

    def get_important(self):
        """Возвращает все важные задачи в порядке времени окончания"""
        lst = []
        if self.not_empty():
            for item in self.tasklist:
                if (item.progress < 100) and not item.hard and item.repeat_mode == item.NOREPEAT and item.priority:
                    lst.append(item)
            lst.sort(key=lambda ts: ts.end)
        return lst

    def get_not_important(self):
        """Возвращает все неважные задачи в порядке времени окончания"""
        lst = []
        if self.not_empty():
            for item in self.tasklist:
                if (item.progress < 100) and not item.hard and item.repeat_mode == item.NOREPEAT and not item.priority:
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

    def __str__(self):
        r_s = ''
        for key, value in self.norm.items():
            r_s += key + " => " + str(value)+'\n'
        return r_s

    def encode(self):
        return self.norm

    def decode(self, norm):
        self.norm = norm

    def add_norm(self, magnitude: str, norm: float):
        """Добавляет единицу измерения и её норму времни"""
        self.norm[magnitude] = norm

    def get_norm(self, magnitude: str):
        """Возвращает норму времни по величине"""
        return self.norm.get(magnitude, 1.0)

class Binary_store:
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

class Json_store:
    def __init__(self, filename, object_store):
        self.filename = filename
        self.object_store = object_store

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.object_store.encode(), file, indent=4, ensure_ascii=False)

    def load(self):
        """Читает данные из файла json"""
        with open(self.filename, 'r', encoding='utf-8') as file:
            dict_obj = json.load(file)
        self.object_store = self.object_store.decode(dict_obj)
        return self.object_store

class cmd:
    def __init__(self, store_task, store_norm, store_hist, time_type):
        """Создаёт объект командной строки"""
        self.current = []
        self.s_t_d = store_task
        self.s_n = store_norm
        self.nm = self.s_n.load()
        self.s_t_d.load()
        self.current_list = self.s_t_d.object_store
        self.current_task = Task()
        self.store_hist = store_hist
        self.time_type = int(time_type)

    def mainloop(self):
        """Главный цикл обработки команд"""
        stop = False
        while not stop:
            prompt = ''                              #создание строки приглашения ко вводу
            self.current_list = self.s_t_d.object_store
            for s_pr in self.current:
                self.current_task = self.current_list.get_task(s_pr)
                self.current_list = self.current_task.child_tasks
                prompt += '/' + self.current_task.task
            p = input(prompt + '>')
            if p == '+':                              #добавить задачу
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
                    pr = self.current_task.LOW
                    du = 0.0
                else:
                    hd = self.current_task.NO_HARD
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
                            if i in '0123456789.':
                                dig += i
                            else:
                                mag += i
                        du = self.nm.get_norm(mag) * float(dig)
                s = input('Дата начала: ')
                e = input('Дата конца: ')
                c = input('Примечание: ')
                self.current_list.add_task(
                    Task(task=n, start=s, end=e, priority=pr, comment=c, duration=du, hard=hd, repeat_mode=rp))
            elif p == 'с':                    #сохранить в файл задачи
                self.s_t_d.save()
            elif p == 'о':                    #прочитать из файла задачи
                self.s_t_d.load()
                self.current_list = self.s_t_d.object_store
            elif p == 'пв':                    #печать задач
                for i, task in enumerate(self.current_list.iterator()):
                        if task.progress < 100:
                            if task.hard:
                                if task.end.date() >= date.today():
                                    print('--', i+1, '--', task)
                            else:
                                print('--', i + 1, '--', task)
            elif p == 'п':                    #печать задач
                for i, task in enumerate(self.current_list.tasklist):
                        if task.progress < 100:
                            if task.child_tasks.not_empty():
                                txt = '...'
                            else:
                                txt = ''
                            if task.hard:
                                if task.end.date() >= date.today():
                                    print('--', i+1, txt, '--', task)
                            else:
                                print('--', i + 1, txt, '--', task)
            elif p == 'вып':                    #печать задач
                if self.current_list.not_empty():
                    for i, task in enumerate(self.current_list.get_tasks()):
                        if task.progress == 100:
                            print('--', i+1, '--', task)
                else:
                    print('Подзадачи отсутствуют')
            elif p == 'в':                    #выход
                self.s_t_d.save()
                stop = True
            elif p.isdigit():                 #выбор задачи по номеру
                p = int(p) - 1
                if p >= 0:
                    if self.current_list.in_range(p):
                        self.current.append(p)
            elif p == '..':                   #возврат на уровень выше
                if len(self.current) > 0:
                    self.current.pop()
            elif p == 'д':                    #вывод задач на день
                tl = Time_line()
                tl.generate_work_time(self.time_type)
                line_sub_tasks = List_tasks()
                for task in self.s_t_d.object_store.iterator():
                    line_sub_tasks.add_task(task)
                np = tl.add_tasks(line_sub_tasks)
                print(tl.day(date.today()))
                if len(np) > 0:
                    print('Не размещены:')
                for t in np:
                    print(t)
            elif p == 'з':                    #вывод задач на завтра
                tl = Time_line()
                tl.generate_work_time(self.time_type)
                line_sub_tasks = List_tasks()
                for task in self.s_t_d.object_store.iterator():
                    line_sub_tasks.add_task(task)
                np = tl.add_tasks(line_sub_tasks)
                print(tl.day(date.today() + timedelta(days=1)))
                if len(np) > 0:
                    print('Не размещены:')
                for t in np:
                    print(t)
            elif p == 'н':                    #вывод задач на неделю
                tl = Time_line()
                tl.generate_work_time(self.time_type)
                line_sub_tasks = List_tasks()
                for task in self.s_t_d.object_store.iterator():
                    line_sub_tasks.add_task(task)
                np = tl.add_tasks(line_sub_tasks)
                print(tl.get_str(date.today(), timedelta(days=7)))
                if len(np) > 0:
                    print('Не размещены:')
                for t in np:
                    print(t)
            elif p == 'м':                    #вывод задач на месяц
                tl = Time_line()
                tl.generate_work_time(self.time_type)
                line_sub_tasks = List_tasks()
                for task in self.s_t_d.object_store.iterator():
                    line_sub_tasks.add_task(task)
                np = tl.add_tasks(line_sub_tasks)
                print(tl.get_str(date.today(), timedelta(days=30)))
                if len(np) > 0:
                    print('Не размещены:')
                for t in np:
                    print(t)
            elif p == 'ст':                   #изменение статуса текущей задачи
                self.current_task.status = int(input('Статус (0 - не начата, 1 - выполняется, 2 - ожидает, 3 - выполнена): '))
            elif p == 'уд':                   #удаление задачи
                nu = int(input('Номер удаляемой задачи: '))-1
                self.current_list.del_task(nu)
            elif p == 'ред':                  #редактирование текста задачи
                self.current_task.task = input('Новый текст задачи: ')
            elif p == 'ком':                  #редактирование комментария к задаче
                print(self.current_task.comment)
                self.current_task.comment = input('Новый комментарий: ')
            elif p == 'ж':                    #изменение жёсткости задачи
                h = input('Жёсткая задача?(+): ')
                if h == '+':
                    self.current_task.hard = self.current_task.HARD
                else:
                    self.current_task.hard = self.current_task.NO_HARD
            elif p == 'важ':                  #изменение приоритета задачи
                if self.current_task.priority:
                    print('+')
                pr = input('Важность (+): ')
                if pr == '':
                    self.current_task.priority = self.current_task.LOW
                else:
                    self.current_task.priority = self.current_task.HIGH
            elif p == 'пр':                    #изменение прогресса выполнения задачи
                pr = int(input('Прогресс: '))
                self.current_task.progress = pr
            elif p == 'нач':                   #изменение начала выполнения задачи
                st = input('Начало: ')
                self.current_task.start = st
            elif p == 'кон':                   #изменение конца выполнения задачи
                en = input('Конец: ')
                self.current_task.end = en
            elif p == 'тр':                    #изменение трудоёмкости
                du = input('Трудоёмкость: ')
                if du == '':
                    du = 0.0
                else:
                    du = float(du)
                self.current_task.duration = du
            elif p == 'пов':                   #изменение режима повторения задачи
                rp = input('Повторение (1 - ежедневно, 2 - еженедельно, 3 - ежемесячно, 4 - ежегодно): ')
                if rp != '':
                    self.current_task.repeat_mode = int(rp)
                else:
                    self.current_task.repeat_mode = 0
            elif p == 'пл':                    #планирование задач по линии времени
                tl = Time_line()
                tl.generate_work_time(self.time_type)
                line_sub_tasks = List_tasks()
                for task in self.s_t_d.object_store.iterator():
                    line_sub_tasks.add_task(task)
                np = tl.add_tasks(line_sub_tasks)
                print(tl)
                if len(np) > 0:
                    print('Не размещены:')
                for t in np:
                    print(t)
            elif p == 'си':                    #сохранить текущий день в историю
                h = tl.copy_day(date.today())
                self.store_hist.load().paste_time_range(h)
                self.store_hist.save()
            elif p == 'пи':                    #печать истории
                print(self.store_hist.load())
            elif p == 'дн':                   #добавить норму
                self.nm = self.s_n.load()
                m = input('Норма: ')
                n = float(input('Значение: '))
                self.nm.add_norm(m, n)
                self.s_n.save()
            elif p == 'пн':                   #печать норм
                print(self.nm)
            elif p == 'кал':                   #вывод запланированных задач в файл календаря
                cl = Calendar_tasks()
                cal_str = cl.add_events(tl)
                with open('my_calendar.ics', 'wb') as file:
                    file.write(cal_str)
            elif p == 'пом':
                print('''+
с   - сохранить главный список задач;
о   - открыть файл и загрузить главный список задач;
пв  - печать всех задач включая подзадачи;
п   - печать текущего списка задач с номерами но без подзадач;
вып - печать выполненных задач;
в   - сохранение и выход;
..  - возврат на уровень выше;
д   - план на сегодняшний день;
з   - план на завтрашний день;
н   - план на неделю;
м   - план на месяц;
ст  - изменение статуса текущей задачи;
уд  - удалить задачу (будет запрошен номер задачи);
ред - редактировать текст задачи;
ком - редактировать комментарий к задаче;
ж   - изменить жёсткость текущей задачи;
важ - изменить важность текущей задачи;
пр  - изменить прогресс текущей задачи;
нач - изменить дату и время начала текущей задачи;
кон - изменить дату и время конца текущей задачи;
тр  - изменить трудоёмкость текущей задачи;
пов - измнить режим повторения текущей задачи;
пл  - планировать все задачи с подзадачами на линии времени;
си  - сохранить задачи текущего дня в историю; 
пи  - печать истории;
дн  - добавить норму времени;
пн  - печать норм времени;
кал - вывод заполненной задачами линии времени в файл календаря.''')
            else:
                print('Недопустимая команда!')

if __name__ == '__main__':
    script, first, second, third, time_type = argv
    s_t = Json_store(first, List_tasks())
    s_n = Json_store(second, Time_norm())
    s_h = Json_store(third, Time_line())
    c = cmd(store_task=s_t, store_norm=s_n, store_hist=s_h, time_type=time_type)
    c.mainloop()
