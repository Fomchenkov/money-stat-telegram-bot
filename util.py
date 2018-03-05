import sqlite3
import datetime

import config


def add_income(uid, amount, description):
    """
    Add new income
    """
    month_day = int(str(datetime.datetime.now())[8:10])
    month_number = int(str(datetime.datetime.now())[5:7])
    with sqlite3.connect(config.db_name) as connection:
        cursor = connection.cursor()
        sql = '''INSERT INTO income (uid, month_day, month_number, 
        income, income_description) VALUES (?, ?, ?, ?, ?)'''
        cursor.execute(sql, (uid, month_day, month_number, amount, description))
        connection.commit()


def add_outcome(uid, amount, description):
    """
    Add new outcome
    """
    month_day = int(str(datetime.datetime.now())[8:10])
    month_number = int(str(datetime.datetime.now())[5:7])
    with sqlite3.connect(config.db_name) as connection:
        cursor = connection.cursor()
        sql = '''INSERT INTO outcome (uid, month_day, month_number, 
        outcome, outcome_description) VALUES (?, ?, ?, ?, ?)'''
        cursor.execute(sql, (uid, month_day, month_number, amount, description))
        connection.commit()
