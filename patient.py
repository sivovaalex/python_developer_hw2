import logging
import csv
import copy
from collections import deque
import sys
import os

class Patient:
    def __init__(self, name, second_name, birthday_in, phone_in, type_doc, number_doc_in):
        self.logger_e = logging.getLogger("errors")
        self.logger_e.setLevel(logging.ERROR)
        self.formatter = logging.Formatter("%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s")



        # получим логгер для нашего приложения либо создадим новый, если он еще не создан (паттерн Синглтон)
        self.logger_s = logging.getLogger("success")
        self.logger_s.setLevel(logging.INFO)

        self.k = 0
        self.k_first = 0
        self.k_last = 0
        self.k_birth_date = 0
        self.k_phone = 0
        self.k_document_type = 0
        self.k_document_id = 0

        self.first_name = name
        self.last_name = second_name
        self.birth_date = birthday_in
        self.phone = phone_in
        self.document_type = type_doc
        self.document_id = number_doc_in

        self.handler_s = logging.FileHandler('good_log.txt', 'a', 'utf-8')
        self.handler_s.setFormatter(self.formatter)
        self.logger_s.addHandler(self.handler_s)
        self.logger_s.info("пациент {0} {1} успешно записан".format(self.last_name,self.document_type))
        self.logger_s.removeHandler(self.handler_s)

    first_name = property()

    @first_name.getter
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, name):
            if self.k_first == 0:
                try:
                    name = name + ''
                except TypeError as e:
                    self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
                    self.handler_e.setFormatter(self.formatter)
                    self.logger_e.addHandler(self.handler_e)
                    #self.handler_s.close()
                    #self.handler_e.close()
                    self.logger_e.error('не правильный тип имени')
                    self.logger_e.removeHandler(self.handler_e)
                    raise e
                else:
                    if name.strip().isalpha():
                        self._first_name = name.strip().title()
                        self.k_first += 1
                        self.k += 1
                    else:
                        self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
                        self.handler_e.setFormatter(self.formatter)
                        self.logger_e.addHandler(self.handler_e)
                        self.logger_e.error("ValueError:Имя должно быть строкой из букв")
                        self.logger_e.removeHandler(self.handler_e)
                        raise ValueError('Имя должно быть строкой из букв')
            else:
                self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
                self.handler_e.setFormatter(self.formatter)
                self.logger_e.addHandler(self.handler_e)
                self.logger_e.error("AttributeError:Имя не должно меняться")
                self.logger_e.removeHandler(self.handler_e)
                raise AttributeError()

    last_name = property()

    @last_name.getter
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, second_name):
        if self.k_last == 0:
            try:
                second_name = second_name + ''
            except TypeError as e:
                self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
                self.handler_e.setFormatter(self.formatter)
                self.logger_e.addHandler(self.handler_e)
                self.logger_e.error(e)
                self.logger_e.removeHandler(self.handler_e)
                raise e
            else:
                if second_name.strip().isalpha():
                    self._last_name = second_name.strip().title()
                    self.k_last += 1
                    self.k += 1
                else:
                    self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
                    self.handler_e.setFormatter(self.formatter)
                    self.logger_e.addHandler(self.handler_e)
                    self.logger_e.exception("ValueError:Фамилия должна быть строкой из букв")
                    self.logger_e.removeHandler(self.handler_e)
                    raise ValueError('Фамилия должна быть строкой из букв')
        else:
            self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
            self.handler_e.setFormatter(self.formatter)
            self.logger_e.addHandler(self.handler_e)
            self.logger_e.error("AttributeError:Фамилия не должна меняться")
            self.logger_e.removeHandler(self.handler_e)
            raise AttributeError('Фамилия не должна меняться')

    birth_date = property()

    @birth_date.getter
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, birthday_in):
        try:
            birthday_in += ''
        except TypeError as e:
            self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
            self.handler_e.setFormatter(self.formatter)
            self.logger_e.addHandler(self.handler_e)
            self.logger_e.error(e)
            self.logger_e.removeHandler(self.handler_e)
            raise e

        else:
            birthday_in = birthday_in.strip()
            count = 0
            if type(birthday_in) == str:
                for i in birthday_in:
                    if i.isdigit():
                        count += 1
            if type(birthday_in) == str and (count >= 5 and count <= 8):
                birthday_str = birthday_in
                for i in birthday_in:
                    if i.isdigit():
                        count += 1
                if '-' in birthday_in:
                    birthday_list = birthday_str.split('-')
                elif '/' in birthday_in:
                    birthday_list = birthday_str.split('/')
                elif '.' in birthday_in:
                    birthday_list = birthday_str.split('.')
                elif ',' in birthday_in:
                    birthday_list = birthday_str.split(',')
                elif ' ' in birthday_in:
                    birthday_list = birthday_str.split()
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
                    self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
                    self.handler_e.setFormatter(self.formatter)
                    self.logger_e.addHandler(self.handler_e)
                    self.logger_e.error("TypeError:Числа даты рождения неверные")
                    self.logger_e.removeHandler(self.handler_e)
                    raise TypeError('Числа даты рождения неверные')
                if len(birthday_month) == 1:
                    birthday_month = '0' + birthday_month
                if len(birthday_day) == 1:
                    birthday_day = '0' + birthday_day
                birthday = birthday_year + '-' + birthday_month + '-' + birthday_day
                self._birth_date = birthday
                self.k += 1
                if self.k > 6:
                    self.handler_s = logging.FileHandler('good_log.txt', 'a', 'utf-8')
                    self.handler_s.setFormatter(self.formatter)
                    self.logger_s.addHandler(self.handler_s)
                    self.logger_s.info("changed")
                    self.logger_s.removeHandler(self.handler_s)

                self.k_birth_date += 1
            else:
                self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
                self.handler_e.setFormatter(self.formatter)
                self.logger_e.addHandler(self.handler_e)
                self.logger_e.error("ValueError:Дата рождения должна быть строкой из разделенных цифр")
                self.logger_e.removeHandler(self.handler_e)
                raise ValueError()

    phone = property()

    @phone.getter
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone_in):
        try:
            phone_in = phone_in + ''
        except TypeError as e:
            self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
            self.handler_e.setFormatter(self.formatter)
            self.logger_e.addHandler(self.handler_e)
            self.logger_e.error(e)
            self.logger_e.removeHandler(self.handler_e)
            raise e
        else:
            phone_str = phone_in
            phone_str = phone_str.strip()
            count = 0
            for i in phone_str:
                if i.isdigit():
                    count += 1
            if count == 11:
                phone = ''.join(i for i in phone_str if i.isdigit())
                phone = '7' + phone[1:]
                self._phone = phone
                self.k += 1
                if self.k > 6:
                    self.handler_s = logging.FileHandler('good_log.txt', 'a', 'utf-8')
                    self.handler_s.setFormatter(self.formatter)
                    self.logger_s.addHandler(self.handler_s)
                    self.logger_s.info("changed")
                    self.logger_s.removeHandler(self.handler_s)
                self.k_phone += 1
            else:
                self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
                self.handler_e.setFormatter(self.formatter)
                self.logger_e.addHandler(self.handler_e)
                self.logger_e.error("ValueError:Номер телефона должен быть 11 значным числом  или числами в строке")
                self.logger_e.removeHandler(self.handler_e)
                raise ValueError()

    document_type = property()

    @document_type.getter
    def document_type(self):
        return self._document_type

    @document_type.setter
    def document_type(self, type_doc):
        try:
            type_doc = type_doc + ''
        except TypeError as e:
            self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
            self.handler_e.setFormatter(self.formatter)
            self.logger_e.addHandler(self.handler_e)
            self.logger_e.error(e)
            self.logger_e.removeHandler(self.handler_e)
            raise e
        else:
            type_doc = type_doc.strip()
            type_doc = type_doc.lower()
            if type_doc == 'паспорт' or type_doc == 'водительское удостоверение' or type_doc == 'заграничный паспорт':
                self._document_type = type_doc
                self.k += 1
                if self.k > 6:
                    self.handler_s = logging.FileHandler('good_log.txt', 'a', 'utf-8')
                    self.handler_s.setFormatter(self.formatter)
                    self.logger_s.addHandler(self.handler_s)
                    self.logger_s.info("changed")
                    self.logger_s.removeHandler(self.handler_s)
                self.k_document_type += 1
            else:
                self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
                self.handler_e.setFormatter(self.formatter)
                self.logger_e.addHandler(self.handler_e)
                self.logger_e.error(
                    "ValueError:Тип документа личности:'паспорт','водительское удостоверение' или 'заграничный паспорт'")
                self.logger_e.removeHandler(self.handler_e)
                raise ValueError()

    document_id = property()

    @document_id.getter
    def document_id(self):
        return self._document_id

    @document_id.setter
    def document_id(self, number_doc_in):
        try:
            number_doc_in += ''
        except TypeError as e:
            self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
            self.handler_e.setFormatter(self.formatter)
            self.logger_e.addHandler(self.handler_e)
            self.logger_e.error(e)
            self.logger_e.removeHandler(self.handler_e)
            raise e
        else:
            number_doc_in = number_doc_in.strip()
            count = 0
            number_str = str(number_doc_in)
            for i in number_doc_in:
                if i.isdigit():
                    count += 1
            if (number_doc_in.isalpha() == False) and (count == 10) and (
                    self._document_type == "паспорт"):
                number = ''.join(i for i in number_str if i.isdigit())
                number_doc = number[:4] + ' ' + number[4:]
                self._document_id = number_doc
                self.k += 1
                if self.k > 6:
                    self.handler_s = logging.FileHandler('good_log.txt', 'a', 'utf-8')
                    self.handler_s.setFormatter(self.formatter)
                    self.logger_s.addHandler(self.handler_s)
                    self.logger_s.info("changed")
                    self.logger_s.removeHandler(self.handler_s)
                self.k_document_id += 1
            elif (number_doc_in.isalpha() == False) and (count == 9) and (
                    self._document_type == "заграничный паспорт"):
                number = ''.join(i for i in number_str if i.isdigit())
                number_doc = number[:2] + ' ' + number[2:]
                self._document_id = number_doc
                self.k += 1
                if self.k > 6:
                    self.handler_s = logging.FileHandler('good_log.txt', 'a', 'utf-8')
                    self.handler_s.setFormatter(self.formatter)
                    self.logger_s.addHandler(self.handler_s)
                    self.logger_s.info("changed")
                    self.logger_s.removeHandler(self.handler_s)
                self.k_document_id += 1
            elif (number_doc_in.isalpha() == False) and (count == 10) and (self._document_type == 'водительское удостоверение'):
                number = ''.join(i for i in number_str if i.isdigit())
                number_doc = number[:2]+' '+number[2:4]+' '+number[4:]
                self._document_id = number_doc
                self.k += 1
                if self.k > 6:
                    self.handler_s = logging.FileHandler('good_log.txt', 'a', 'utf-8')
                    self.handler_s.setFormatter(self.formatter)
                    self.logger_s.addHandler(self.handler_s)
                    self.logger_s.info("changed")
                    self.logger_s.removeHandler(self.handler_s)
                self.k_document_id += 1
            else:
                self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
                self.handler_e.setFormatter(self.formatter)
                self.logger_e.addHandler(self.handler_e)
                self.logger_e.error(
                    "ValueError:Номер документа должен быть 10(пасп,вод) или 9(загран) значным числом/числами в строке")
                self.logger_e.removeHandler(self.handler_e)
                raise ValueError('Номер документа должен быть 10(пасп,вод) или 9(загран) значным числом/числами в строке')

    @classmethod
    def create(cls, name, second_name, birthday_in, phone_in, type_doc, number_doc_in):
        super(Patient, cls).__init__(name, second_name, birthday_in, phone_in, type_doc, number_doc_in)
        cls.cr = Patient(name, second_name, birthday_in, phone_in, type_doc, number_doc_in)
        return cls.cr

    def save(self):
        try:
            with open('patient.csv', 'a', newline='') as csvfile:
                fieldnames = ['first_name', 'last_name', 'birth_date', 'phone', 'document_type', 'document_id']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(
                    {'first_name': self.first_name, 'last_name': self.last_name, 'birth_date': self.birth_date,
                     'phone': self.phone, 'document_type': self.document_type, 'document_id': self.document_id})
        except Exception as e:
            self.handler_e = logging.FileHandler('error_log.txt', 'a', 'utf-8')
            self.handler_e.setFormatter(self.formatter)
            self.logger_e.addHandler(self.handler_e)
            self.logger_e.error("Error: Данные не сохранены")
            self.logger_e.removeHandler(self.handler_e)
            raise e
        else:
            self.handler_s = logging.FileHandler('good_log.txt', 'a', 'utf-8')
            self.handler_s.setFormatter(self.formatter)
            self.logger_s.addHandler(self.handler_s)
            self.logger_s.info("Данные сохранены")
            self.logger_s.removeHandler(self.handler_s)
            self.k_first = 0
            self.k_last = 0


class PatientCollection(Patient):
    def __init__(self, path_to_file):

        self.path_to_file = path_to_file
        self.lim = None
        self.num = 0
        self.count_line = 0
        self.col = []
        self.File = open(self.path_to_file, newline='')
        self.reader = csv.reader(self.File)
        self.d1 = deque(self.File)

        for letter in self.d1:
            self.count_line += 1
            letter = letter.split(',')
            a = Patient(letter[0], letter[1], letter[2], letter[3], letter[4], letter[5])
            self.col.append(a)
        self.d = deque(self.col)
        self.len = self.count_line
        print(self.len)
        self.File.close()


    def __iter__(self):
        return self

    def __next__(self):
        self.File_1 = open(self.path_to_file, newline='')
        self.len = len(self.File_1.readlines())
        self.File_1.close()
        if self.lim == None:
            self.lim = self.len
        if self.num >= self.lim or os.stat(self.path_to_file).st_size == 0:
            raise StopIteration
        else:
            self.num += 1
            self.File = open(self.path_to_file, newline='')
            line = self.File.readlines()[(self.num - 1):self.num]
            letter = line[0]
            letter = letter.split(',')
            a = Patient(letter[0], letter[1], letter[2], letter[3], letter[4], letter[5])
            self.col.append(a)
            self.d = deque(self.col)
            self.File.close()
            return self.d.pop()

    def limit(self, n):
        self.lim = n
        return self.__iter__()
