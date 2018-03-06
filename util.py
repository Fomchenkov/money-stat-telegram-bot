import sqlite3
import datetime

import config


class Income:
	"""
	Income class
	"""

	def __init__(self, id, uid, month_day, 
		month_number, income, income_description):
		self.id = id
		self.uid = uid
		self.month_day = month_day
		self.month_number = month_number
		self.income = income
		self.income_description = income_description


class Outcome:
	"""
	Outcome class
	"""

	def __init__(self, id, uid, month_day, 
		month_number, outcome, outcome_description):
		self.id = id
		self.uid = uid
		self.month_day = month_day
		self.month_number = month_number
		self.outcome = outcome
		self.outcome_description= outcome_description


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


def get_month_income(uid, month_number):
	"""
	Get month income value
	"""
	with sqlite3.connect(config.db_name) as connection:
		cursor = connection.cursor()
		sql = '''SELECT * FROM income WHERE uid=? AND month_number=? ORDER BY id'''
		res = cursor.execute(sql, (uid, month_number)).fetchall()
		connection.commit()
	incomes = []
	for x in res:
		print(x)
		incomes.append(Income(x[0], x[1], x[2], x[3], x[4], x[5]))
	return incomes


def get_month_outcome(uid, month_number):
	"""
	Get month outcome value
	"""
	with sqlite3.connect(config.db_name) as connection:
		cursor = connection.cursor()
		sql = '''SELECT * FROM outcome WHERE uid=? AND month_number=? ORDER BY id'''
		res = cursor.execute(sql, (uid, month_number)).fetchall()
		connection.commit()
	outcomes = []
	for x in res:
		print(x)
		outcomes.append(Outcome(x[0], x[1], x[2], x[3], x[4], x[5]))
	return outcomes


def generate_correct_date(x):
	"""
	Generate correct date
	:param x: income/outcome instance
	:return: normal date as string
	"""
	_date = ''
	if len(str(x.month_number)) == 1:
		_date = '0' + str(x.month_number)
	else:
		_date = str(x.month_number)
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
