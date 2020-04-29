import logging
import csv
import copy
from collections import deque
import sys
import os


class Patient:
    def __init__(self, first_name, last_name, birth_date, phone, document_type, document_id):
        self.logger_e = logging.getLogger("errors")
        self.logger_e.setLevel(logging.ERROR)
        self.formatter = logging.Formatter("%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s")
        self.logger_s = logging.getLogger("success")
        self.logger_s.setLevel(logging.INFO)

        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.phone = phone
        self.document_type = document_type
        self.document_id = document_id

        self.log_good("пациент {0} {1} успешно записан".format(self.last_name, self.document_type))

    first_name = property()

    @first_name.getter
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if hasattr(self, 'first_name') == False:
            if isinstance(first_name, str):
                if first_name.strip().isalpha():
                    self._first_name = first_name.strip().title()
                else:
                    self.log_error("ValueError:Имя должно быть строкой из букв")
                    raise ValueError('Имя должно быть строкой из букв')
            else:
                self.log_error('не правильный тип имени')
                raise TypeError
        else:
            self.log_error("AttributeError:Имя не должно меняться")
            raise AttributeError('Имя не должно меняться')

    last_name = property()

    @last_name.getter
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        if hasattr(self, 'last_name') == False:
            if isinstance(last_name, str):
                if last_name.strip().isalpha():
                    self._last_name = last_name.strip().title()
                else:
                    self.log_error("ValueError:Фамилия должна быть строкой из букв")
                    raise ValueError('Фамилия должна быть строкой из букв')
            else:
                self.log_error('TypeError: фамия должна быть буквами')
                raise TypeError
        else:
            self.log_error("AttributeError:Фамилия не должна меняться")
            raise AttributeError('Фамилия не должна меняться')

    birth_date = property()

    @birth_date.getter
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
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
                    self.log_error("TypeError:Числа даты рождения неверные")
                    raise TypeError('Числа даты рождения неверные')
                if len(birthday_month) == 1:
                    birthday_month = '0' + birthday_month
                if len(birthday_day) == 1:
                    birthday_day = '0' + birthday_day
                birthday = birthday_year + '-' + birthday_month + '-' + birthday_day
                self._birth_date = birthday
                if change:
                    self.log_good("birth_date changed")
            else:
                self.log_error("ValueError:Дата рождения должна быть строкой из разделенных цифр")
                raise ValueError()
        else:
            self.log_error("TypeError birh_date")
            raise TypeError

    phone = property()

    @phone.getter
    def phone(self):
        return self._phone

    @phone.setter
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
                    self.log_good("phone changed")
            else:
                self.log_error("ValueError:Номер телефона должен быть 11 значным числом  или числами в строке")
                raise ValueError()
        else:
            self.log_error("TypeError phone")
            raise TypeError


    document_type = property()

    @document_type.getter
    def document_type(self):
        return self._document_type

    @document_type.setter
    def document_type(self, document_type):
        if isinstance(document_type, str):
            document_type = document_type.strip()
            document_type = document_type.lower()
            change = hasattr(self, 'document_type')
            if document_type == 'паспорт' or document_type == 'водительское удостоверение' or document_type == 'заграничный паспорт':
                self._document_type = document_type
                if change:
                    self.log_good("doc_type changed")
            else:
                self.log_error(
                    "ValueError:Тип документа личности:'паспорт','водительское удостоверение' или 'заграничный паспорт'")
                raise ValueError()
        else:
            self.log_error("TypeError doc_type")
            raise TypeError

    document_id = property()

    @document_id.getter
    def document_id(self):
        return self._document_id

    @document_id.setter
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
                document_id = document_id[:4] + ' ' + document_id[4:]
                self._document_id = document_id
                if change:
                    self.log_good("doc_id changed")
            elif (document_id.isalpha() == False) and (count == 9) and (
                    self._document_type == "заграничный паспорт"):
                document_id = ''.join(i for i in document_id if i.isdigit())
                document_id = document_id[:2] + ' ' + document_id[2:]
                self._document_id = document_id
                if change:
                    self.log_good("doc_id changed")
            elif (document_id.isalpha() == False) and (count == 10) and (
                    self._document_type == 'водительское удостоверение'):
                document_id = ''.join(i for i in document_id if i.isdigit())
                document_id = document_id[:2] + ' ' + document_id[2:4] + ' ' + document_id[4:]
                self._document_id = document_id
                if change:
                    self.log_good("doc_id changed")
            else:
                self.log_error(
                    "ValueError:Номер документа должен быть 10(пасп,вод) или 9(загран) значным числом/числами в строке")
                raise ValueError(
                    'Номер документа должен быть 10(пасп,вод) или 9(загран) значным числом/числами в строке')
        else:
            self.log_error("TypeError doc_id")
            raise TypeError

    @staticmethod
    def create(first_name, last_name, birth_date, phone, document_type, document_id):
        patient = Patient(first_name, last_name, birth_date, phone, document_type, document_id)
        return patient

    def log_error(self, message_e):
        self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
        self.handler_e.setFormatter(self.formatter)
        self.logger_e.addHandler(self.handler_e)
        self.logger_e.error(message_e)
        self.logger_e.removeHandler(self.handler_e)

    def log_good(self, message_g):
        self.handler_s = logging.FileHandler('good_log.txt', 'a', 'utf-8')
        self.handler_s.setFormatter(self.formatter)
        self.logger_s.addHandler(self.handler_s)
        self.logger_s.info(message_g)
        self.logger_s.removeHandler(self.handler_s)

    def save(self):
        try:
            with open('patient.csv', 'a', newline='') as csvfile:
                fieldnames = ['first_name', 'last_name', 'birth_date', 'phone', 'document_type', 'document_id']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(
                    {'first_name': self.first_name, 'last_name': self.last_name, 'birth_date': self.birth_date,
                     'phone': self.phone, 'document_type': self.document_type, 'document_id': self.document_id})
        except OSError:
            self.log_error("Error: Данные не сохранены")
            raise OSError("Error: Данные не сохранены")
        except UnicodeError:
            self.log_error("Error: Данные не сохранены")
            raise UnicodeError("Error: Данные не сохранены")
        except RuntimeError:
            self.log_error("Error: Данные не сохранены")
            raise RuntimeError("Error: Данные не сохранены")
        else:
            self.log_good("Данные сохранены")


class PatientCollection(Patient):
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.num = 0
        self.lim = None

    def __iter__(self):
        return self

    def __next__(self):
        if (self.lim != None and self.num >= self.lim) or os.stat(self.path_to_file).st_size == 0:
            raise StopIteration
        with open(self.path_to_file, newline='') as file:
            self.num += 1
            line = file.readlines()[(self.num - 1):self.num]
            if line == []:
                raise StopIteration
            else:
                letter = line[0]
                letter = letter.split(',')
                patient = Patient(*letter)
                return patient

    def limit(self, n):
        self.lim = n
        return self

