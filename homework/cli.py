import click
import sqlite3
from patient import Patient, PatientCollection
db_path = r'patients.db'


@click.group()
def cli():
    '''
    Реализация следующего интерфейса командной строки (через click):
    cd homework

    Добавление нового пользователя в БД:
    cli.py create Имя Фамилия --birth-date 1990-01-01 --phone +7-916-000-00-00 --document-type паспорт --document-number 0000 000000
    Вывод на экран первых 10 пользователей:
    python cli.py show
    Вывод на экран произвольного количества пользователей:
    python cli.py show 8
    Вывод на экран количества сохраненных пользователей:
    python cli.py count
    '''
    pass


@click.command()
@click.argument('first_name')
@click.argument('last_name')
@click.option('--birth-date')
@click.option('--phone')
@click.option('--document-type')
@click.option('--document-number', nargs=2)
def create(first_name, last_name, birth_date, phone, document_type, document_number):
    patient = Patient(first_name, last_name, birth_date, phone, document_type, document_id)
    patient.save()
    click.echo('the patient add')


@click.command()
@click.argument('amount', default=10)
def show(amount):
    collection = PatientCollection(db_path)
    for patient in collection.limit(amount):
        print(patient.first_name, patient.last_name, patient.birth_date, patient.phone, patient.document_type, patient.document_id)


@click.command()
def count():
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    counter = curs.execute("""SELECT COUNT(*) 
                            FROM patients;""").fetchone()
    counter = list(counter)[0] #преобразуем в обычную цифру
    curs.close()
    click.echo(counter)


cli.add_command(create)
cli.add_command(show)
cli.add_command(count)

if __name__ == '__main__':
    cli()