import sqlite3
import datetime

import config


class Income:
    """
    Income class
    """

    def __init__(self, id, uid, month_day,
                 month_number, year, income, income_description):
        self.id = id
        self.uid = uid
        self.month_day = month_day
        self.month_number = month_number
        self.year = year
        self.income = income
        self.income_description = income_description


class Outcome:
    """
    Outcome class
    """

    def __init__(self, id, uid, month_day,
                 month_number, year, outcome, outcome_description):
        self.id = id
        self.uid = uid
        self.month_day = month_day
        self.month_number = month_number
        self.year = year
        self.outcome = outcome
        self.outcome_description = outcome_description


def add_income(uid, amount, description):
    """
    Add new income
    """
    month_day = int(str(datetime.datetime.now())[8:10])
    month_number = int(str(datetime.datetime.now())[5:7])
    year = int(str(datetime.datetime.now())[0:4])
    with sqlite3.connect(config.db_name) as connection:
        cursor = connection.cursor()
        sql = '''INSERT INTO income (uid, month_day, month_number,
		year, income, income_description) VALUES (?, ?, ?, ?, ?, ?)'''
        cursor.execute(
            sql,
            (uid,
             month_day,
             month_number,
             year,
             amount,
             description))
        connection.commit()


def add_outcome(uid, amount, description):
    """
    Add new outcome
    """
    month_day = int(str(datetime.datetime.now())[8:10])
    month_number = int(str(datetime.datetime.now())[5:7])
    year = int(str(datetime.datetime.now())[0:4])
    with sqlite3.connect(config.db_name) as connection:
        cursor = connection.cursor()
        sql = '''INSERT INTO outcome (uid, month_day, month_number,
		year, outcome, outcome_description) VALUES (?, ?, ?, ?, ?, ?)'''
        cursor.execute(
            sql,
            (uid,
             month_day,
             month_number,
             year,
             amount,
             description))
        connection.commit()


def get_month_income(uid, month_number):
    """
    Get month income value
    """
    year = int(str(datetime.datetime.now())[0:4])
    with sqlite3.connect(config.db_name) as connection:
        cursor = connection.cursor()
        sql = '''SELECT * FROM income WHERE uid=? AND month_number=? AND year=? ORDER BY id'''
        res = cursor.execute(sql, (uid, month_number, year)).fetchall()
        connection.commit()
    incomes = []
    for x in res:
        print(x)
        incomes.append(Income(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
    return incomes


def get_month_outcome(uid, month_number):
    """
    Get month outcome value
    """
    year = int(str(datetime.datetime.now())[0:4])
    with sqlite3.connect(config.db_name) as connection:
        cursor = connection.cursor()
        sql = '''SELECT * FROM outcome WHERE uid=? AND month_number=? AND year=? ORDER BY id'''
        res = cursor.execute(sql, (uid, month_number, year)).fetchall()
        connection.commit()
    outcomes = []
    for x in res:
        print(x)
        outcomes.append(Outcome(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
    return outcomes


def generate_correct_date(x):
    """
    Generate correct date
    :param x: income/outcome instance
    :return: normal date as string
    """
    _date = str(x.year) + '.'
    if len(str(x.month_number)) == 1:
        _date += '0' + str(x.month_number)
    else:
        _date += str(x.month_number)
    _date += '.'
    if len(str(x.month_day)) == 1:
        _date += '0' + str(x.month_day)
    else:
        _date += str(x.month_day)
    return _date


def delete_income(income_id):
    """
    Delete income
    """
    with sqlite3.connect(config.db_name) as connection:
        cursor = connection.cursor()
        sql = '''DELETE FROM income WHERE id=?'''
        cursor.execute(sql, (income_id,))
        connection.commit()


def delete_outcome(outcome_id):
    """
    Delete outcome
    """
    with sqlite3.connect(config.db_name) as connection:
        cursor = connection.cursor()
        sql = '''DELETE FROM outcome WHERE id=?'''
        cursor.execute(sql, (outcome_id,))
        connection.commit()


def delete_old_month_data():
    """
    Delete old month data
    """
    last_month_number = int(str(datetime.datetime.now())[5:7]) - 1
    if last_month_number == 0:
        last_month_number = 12
    with sqlite3.connect(config.db_name) as connection:
        cursor = connection.cursor()
        sql = '''DELETE FROM income WHERE month_number<?'''
        cursor.execute(sql, (last_month_number,))
        sql = '''DELETE FROM outcome WHERE month_number<?'''
        cursor.execute(sql, (last_month_number,))
        connection.commit()
