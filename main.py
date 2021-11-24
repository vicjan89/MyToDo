import pickle

FILENAME = 'todo.dat'


class ToDo:
    def __init__(self, t_d, start='', end='', priority=False, parent_td=0):
        self.td = t_d
        self.start = start
        self.end = end
        self.priority = priority
        self.parent_td = parent_td


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

    def list_todo(self):
        print(self.list_todo)


if __name__ == '__main__':
    s_t_d = Store(FILENAME)
    while True:
        p = input('>')
        if p == '+':
            n = input('Введите задачу: ')
            s = input('Дата начала: ')
            e = input('Дата конца: ')
            pr = input('Важное?(+)')
            if pr == '+':
                pr = True
            else:
                pr = False
            td = ToDo(n, s, e, pr)
            s_t_d.add_todo(td)
        elif p == 'с':
            s_t_d.save_todo()
        elif p == 'о':
            s_t_d.load_todo()
        else:
            print('Недопустимая команда!')
