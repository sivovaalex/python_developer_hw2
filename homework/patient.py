import logging
import csv
import os
import sqlite3
import os.path

logger_e = logging.getLogger("errors")
logger_e.setLevel(logging.ERROR)
formatter = logging.Formatter("%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s")
logger_s = logging.getLogger("success")
logger_s.setLevel(logging.INFO)


def my_logging_decorator(fn):
    def log_error(mes):
        handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
        handler_e.setFormatter(formatter)
        logger_e.addHandler(handler_e)
        logger_e.error(mes)
        logger_e.removeHandler(handler_e)

    def log_good(mes):
        handler_s = logging.FileHandler('good_log.txt', 'a', 'utf-8')
        handler_s.setFormatter(formatter)
        logger_s.addHandler(handler_s)
        logger_s.info(mes)
        logger_s.removeHandler(handler_s)

    def wrapper(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except AttributeError:
            log_error("AttributeError:Имя и фамилия не должны меняться")
            raise AttributeError('Имя и фамилия не должны меняться')
        except TypeError:
            log_error("TypeError: не правильный тип ввода")
            raise TypeError('не правильный тип ввода')
        except ValueError:
            log_error("ValueError:неправильное значение ввода")
            raise ValueError('неправильное значение ввода')
        except OSError:
            log_error("Ошибка системы: Данные не сохранены")
            raise OSError("Ошибка системы: Данные не сохранены")
        except UnicodeError:
            log_error("Ошибка кодировки: Данные не сохранены")
            raise UnicodeError("Ошибка кодировки: Данные не сохранены")
        except RuntimeError:
            log_error("RuntimeError: Данные не сохранены")
            raise RuntimeError("RuntimeError: Данные не сохранены")
        except sqlite3.OperationalError:
            log_error('sqlite3.OperationalError')
            raise sqlite3.OperationalError()
        except sqlite3.IntegrityError:
            log_error('sqlite3.IntegrityError: уже есть такой номер документа')
            raise sqlite3.IntegrityError('sqlite3.IntegrityError: уже есть такой номер документа')
        except FileExistsError:
            log_error('Данные не сохранены')
            raise FileExistsError
        except FileNotFoundError:
            log_error('файл не найден: Данные не сохранены')
            raise FileNotFoundError
        except IsADirectoryError:
            log_error('Ошибка директории: Данные не сохранены')
            raise IsADirectoryError
        except PermissionError:
            log_error('Данные не сохранены')
            raise PermissionError
        else:
            if fn.__name__ == 'save':
                log_good("Данные сохранены")
            elif fn.__name__ == '__init__':
                log_good("Данные записаны")
    return wrapper


class Patient:
    @my_logging_decorator
    def __init__(self, first_name, last_name, birth_date, phone, document_type, document_id):
        self.formatter = logging.Formatter("%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s")
        self.logger_s = logging.getLogger("success")
        self.logger_s.setLevel(logging.INFO)
        self.db_path = r'patients.db'
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS patients
                          (first_name varchar(20) not null, 
                          last_name varchar(20) not null, 
                          birth_date varchar(10) not null, 
                          phone varchar(11) not null, 
                          document_type varchar(20) not null, 
                          document_id varchar(10) not null UNIQUE
                          );""")
        c.close()

        if first_name and last_name and birth_date and phone and document_type and document_id:
            self.first_name = first_name
            self.last_name = last_name
            self.birth_date = birth_date
            self.phone = phone
            self.document_type = document_type
            self.document_id = document_id

    first_name = property()

    @first_name.getter
    def first_name(self):
        return self._first_name

    @first_name.setter
    @my_logging_decorator
    def first_name(self, first_name):
        if hasattr(self, 'first_name') == False:
            if isinstance(first_name, str):
                if first_name.strip().isalpha():
                    self._first_name = first_name.strip().title()
                else:
                    raise ValueError('Имя должно быть строкой из букв')
            else:
                raise TypeError()
        else:
            raise AttributeError('Имя не должно меняться')

    last_name = property()

    @last_name.getter
    def last_name(self):
        return self._last_name

    @last_name.setter
    @my_logging_decorator
    def last_name(self, last_name):
        if hasattr(self, 'last_name') == False:
            if isinstance(last_name, str):
                if last_name.strip().isalpha():
                    self._last_name = last_name.strip().title()
                else:
                    raise ValueError('Фамилия должна быть строкой из букв')
            else:
                raise TypeError()
        else:
            raise AttributeError('Фамилия не должна меняться')

    birth_date = property()

    @birth_date.getter
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    @my_logging_decorator
    def birth_date(self, birth_date):
        if isinstance(birth_date, str):
            birth_date = birth_date.strip()
            count = 0
            change = hasattr(self, 'birth_date') #пытаемся ли менять уже существующее знаяение
            for i in birth_date:
                if i.isdigit():
                    count += 1
            if (count >= 5 and count <= 8):
                for i in birth_date:
                    if i.isdigit():
                        count += 1
                if '-' in birth_date:
                    birthday_list = birth_date.split('-')
                elif '/' in birth_date:
                    birthday_list = birth_date.split('/')
                elif '.' in birth_date:
                    birthday_list = birth_date.split('.')
                elif ',' in birth_date:
                    birthday_list = birth_date.split(',')
                elif ' ' in birth_date:
                    birthday_list = birth_date.split()
                if (len(birthday_list[0]) == 4) and (int(birthday_list[0]) >= 1870 and int(birthday_list[0]) <= 2020) \
                        and (len(birthday_list[1]) == 1 or len(birthday_list[1]) == 2) and (
                        int(birthday_list[1]) >= 1 and int(birthday_list[1]) <= 12) \
                        and (len(birthday_list[2]) == 1 or len(birthday_list[2]) == 2) and (
                        int(birthday_list[2]) >= 1 and int(birthday_list[2]) <= 31):
                    birthday_year = birthday_list[0]
                    birthday_month = birthday_list[1]
                    birthday_day = birthday_list[2]
                elif (len(birthday_list[2]) == 4) and (int(birthday_list[2]) >= 1870 and int(birthday_list[2]) <= 2020) \
                        and (len(birthday_list[1]) == 1 or len(birthday_list[1]) == 2) and (
                        int(birthday_list[1]) >= 1 and int(birthday_list[1]) <= 12) \
                        and (len(birthday_list[0]) == 1 or len(birthday_list[0]) == 2) and (
                        int(birthday_list[0]) >= 1 and int(birthday_list[0]) <= 31):
                    birthday_year = birthday_list[2]
                    birthday_month = birthday_list[1]
                    birthday_day = birthday_list[0]
                else:
                    raise TypeError('Числа даты рождения неверные')
                if len(birthday_month) == 1:
                    birthday_month = '0' + birthday_month
                if len(birthday_day) == 1:
                    birthday_day = '0' + birthday_day
                birthday = birthday_year + '-' + birthday_month + '-' + birthday_day
                self._birth_date = birthday
                if change:
                    self.log_good('changed')
            else:
                raise ValueError()
        else:
            raise TypeError()

    phone = property()

    @phone.getter
    def phone(self):
        return self._phone

    @phone.setter
    @my_logging_decorator
    def phone(self, phone):
        if isinstance(phone, str):
            phone = phone.strip()
            count = 0
            change = hasattr(self, 'phone')
            for i in phone:
                if i.isdigit():
                    count += 1
            if count == 11:
                phone = ''.join(i for i in phone if i.isdigit())
                phone = '7' + phone[1:]
                self._phone = phone
                if change:
                    self.log_good('changed')
            else:
                raise ValueError()
        else:
            raise TypeError()


    document_type = property()

    @document_type.getter
    def document_type(self):
        return self._document_type

    @document_type.setter
    @my_logging_decorator
    def document_type(self, document_type):
        if isinstance(document_type, str):
            document_type = document_type.strip()
            document_type = document_type.lower()
            change = hasattr(self, 'document_type')
            if document_type == 'паспорт' or document_type == 'водительское удостоверение' or document_type == 'заграничный паспорт':
                self._document_type = document_type
                if change:
                    self.log_good('changed')
            else:
                raise ValueError()
        else:
            raise TypeError()

    document_id = property()

    @document_id.getter
    def document_id(self):
        return self._document_id

    @document_id.setter
    @my_logging_decorator
    def document_id(self, document_id):
        if isinstance(document_id, str):
            document_id = document_id.strip()
            count = 0
            change = hasattr(self, 'document_id')
            for i in document_id:
                if i.isdigit():
                    count += 1
            if (document_id.isalpha() == False) and (count == 10) and (
                    self._document_type == "паспорт"):
                document_id = ''.join(i for i in document_id if i.isdigit())
                self._document_id = document_id
                if change:
                    self.log_good('changed')
            elif (document_id.isalpha() == False) and (count == 9) and (
                    self._document_type == "заграничный паспорт"):
                document_id = ''.join(i for i in document_id if i.isdigit())
                self._document_id = document_id
                if change:
                    self.log_good('changed')
            elif (document_id.isalpha() == False) and (count == 10) and (
                    self._document_type == 'водительское удостоверение'):
                document_id = ''.join(i for i in document_id if i.isdigit())
                self._document_id = document_id
                if change:
                    self.log_good('changed')
            else:
                raise ValueError(
                    'Номер документа должен быть 10(пасп,вод) или 9(загран) значным числом/числами в строке')
        else:
            raise TypeError()

    @staticmethod
    def create(first_name, last_name, birth_date, phone, document_type, document_id):
        patient = Patient(first_name, last_name, birth_date, phone, document_type, document_id)
        return patient

    @my_logging_decorator
    def save(self):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""INSERT INTO patients (first_name, last_name, birth_date, phone, document_type, document_id)
                              VALUES ('{}', '{}', '{}', '{}', '{}', '{}');""".format(
                self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id
            ))
            conn.commit()
            c.close()
        except OSError:
            raise OSError("Ошибка системы: Данные не сохранены")
        except UnicodeError:
            raise UnicodeError("Ошибка кодировки: Данные не сохранены")
        except RuntimeError:
            raise RuntimeError("RuntimeError: Данные не сохранены")
        except sqlite3.OperationalError:
            raise sqlite3.OperationalError()
        except sqlite3.IntegrityError:
            raise sqlite3.IntegrityError('sqlite3.IntegrityError: уже есть такой номер документа')
        except FileExistsError:
            raise FileExistsError
        except FileNotFoundError:
            raise FileNotFoundError
        except IsADirectoryError:
            raise IsADirectoryError
        except PermissionError:
            raise PermissionError


    def log_good(self, message_g):
        self.handler_s = logging.FileHandler('good_log.txt', 'a', 'utf-8')
        self.handler_s.setFormatter(self.formatter)
        self.logger_s.addHandler(self.handler_s)
        self.logger_s.info(message_g)
        self.logger_s.removeHandler(self.handler_s)


class PatientCollection(Patient):
    def __init__(self, path_to_file):
        self.db_path = path_to_file
        self.num = 0
        self.lim = None
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

    def __iter__(self):
        return self

    def __next__(self):
        if (self.lim != None and self.num >= self.lim) or os.stat(self.db_path).st_size == 0:
            self.c.close()
            raise StopIteration
        self.num += 1
        line = self.c.execute("""SELECT first_name, last_name, birth_date, phone, document_type, document_id 
                        FROM patients
                        WHERE rowid = {};""".format(self.num))
        line = list(line)
        if line == []:
            self.c.close()
            raise StopIteration
        else:
            letter = list(line[0])
            patient = Patient(*letter)
            return patient

    def limit(self, n):
        self.lim = n
        return self





'''collection = PatientCollection("patient.csv")
for patient in collection:
    print(patient.first_name)'''
a = Patient('nnhhf', 'nhnhj', "1978-01-21", "7-916-000-00-00", 'паспорт', '1008 000009')
print(a.__dict__)
a.document_id='1330 083499'
a.save()

print(a.__dict__)
#print(a.first_name)
def select(verbose=True):
    sql = "SELECT * FROM patients"
    recs = c.execute(sql)
    if verbose:
        for row in recs:
            print(row)
db_path = r'patients.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
select()
c.close()
'''collection = PatientCollection("patients.db")
i = 0
for patient in collection.limit(4):
    i += 1
    print(i, patient.document_id)'''

'''import sqlite3

conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""CREATE TABLE IF NOT EXISTS patients
                  (first_name varchar(20) not null, 
                  last_name varchar(20) not null, 
                  birth_date varchar(10) not null, 
                  phone varchar(11) not null, 
                  document_type varchar(20) not null, 
                  document_id varchar(12) not null,
                  PRIMARY KEY (first_name, last_name));
               """)'''

