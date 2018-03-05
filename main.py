#!/usr/bin/env python3

import time
import sqlite3

import telebot
from telebot import types

import util
import config


bot = telebot.TeleBot(config.BOT_TOKEN)
READY_TO_INCOME = {}
READY_TO_OUTCOME = {}


with sqlite3.connect(config.db_name) as connection:
	cursor = connection.cursor()
	# Income maney table
	sql = '''CREATE TABLE IF NOT EXISTS income (
		id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		uid INTEGER NOT NULL,
		month_day INTEGER NOT NULL,
		month_number INTEGER NOT NULL,
		income INTEGER NOT NULL,
		income_description TEXT)'''
	cursor.execute(sql)
	# Outcome money table
	sql = '''CREATE TABLE IF NOT EXISTS outcome (
		id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		uid INTEGER NOT NULL,
		month_day INTEGER NOT NULL,
		month_number INTEGER NOT NULL,
		outcome INTEGER NOT NULL,
		outcome_description TEXT)'''
	cursor.execute(sql)
	connection.commit()


@bot.message_handler(commands=['start'])
def start_command_handler(message):
	cid = message.chat.id
	uid = message.from_user.id
	markup = types.ReplyKeyboardMarkup(
		one_time_keyboard=False, resize_keyboard=True, row_width=1)
	for command_arr in config.main_markup:
		markup.row(*command_arr)
	return bot.send_message(cid, config.main_text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text_content_handler(message):
	cid = message.chat.id
	uid = message.from_user.id

	# Handle other buttons
	if message.text == '⬅️ Отмена':
		if uid in READY_TO_INCOME:
			del READY_TO_INCOME[uid]
		if uid in READY_TO_OUTCOME:
			del READY_TO_OUTCOME[uid]
		markup = types.ReplyKeyboardMarkup(
			one_time_keyboard=False, resize_keyboard=True, row_width=1)
		for command_arr in config.main_markup:
			markup.row(*command_arr)
		return bot.send_message(cid, config.main_text, reply_markup=markup)
	elif message.text == '⏩ Пропустить этот шаг':
		if uid in READY_TO_INCOME:
			util.add_income(uid, READY_TO_INCOME[uid]['amount'], '')
			del READY_TO_INCOME[uid]
			text = '✅ Доход добавлен!'
			markup = types.ReplyKeyboardMarkup(
				one_time_keyboard=False, resize_keyboard=True, row_width=1)
			for command_arr in config.main_markup:
				markup.row(*command_arr)
			return bot.send_message(cid, text, reply_markup=markup)
		elif uid in READY_TO_OUTCOME:
			util.add_outcome(uid, READY_TO_OUTCOME[uid]['amount'], '')
			del READY_TO_OUTCOME[uid]
			text = '✅ Расход добавлен!'
			markup = types.ReplyKeyboardMarkup(
				one_time_keyboard=False, resize_keyboard=True, row_width=1)
			for command_arr in config.main_markup:
				markup.row(*command_arr)
			return bot.send_message(cid, text, reply_markup=markup)

	if uid in READY_TO_INCOME:
		if 'amount' not in READY_TO_INCOME[uid]:
			try:
				amount = int(message.text)
			except Exception as e:
				err_text = '⛔️ Введите число! ⛔️'
				return bot.send_message(cid, err_text)
			READY_TO_INCOME[uid]['amount'] = amount
			text = 'Введите описание дохода, если нужно.'
			markup = types.ReplyKeyboardMarkup(
				one_time_keyboard=False, resize_keyboard=True, row_width=1)
			markup.row('⏩ Пропустить этот шаг')
			markup.row('⬅️ Отмена')
			return bot.send_message(cid, text, reply_markup=markup)
		if 'description' not in READY_TO_INCOME[uid]:
			util.add_income(uid, READY_TO_INCOME[uid]['amount'], message.text)
			del READY_TO_INCOME[uid]
			text = '✅ Доход добавлен!'
			markup = types.ReplyKeyboardMarkup(
				one_time_keyboard=False, resize_keyboard=True, row_width=1)
			for command_arr in config.main_markup:
				markup.row(*command_arr)
			return bot.send_message(cid, text, reply_markup=markup)

	if uid in READY_TO_OUTCOME:
		if 'amount' not in READY_TO_OUTCOME[uid]:
			try:
				amount = int(message.text)
			except Exception as e:
				err_text = '⛔️ Введите число! ⛔️'
				return bot.send_message(cid, err_text)
			READY_TO_OUTCOME[uid]['amount'] = amount
			text = 'Введите описание расхода, если нужно.'
			markup = types.ReplyKeyboardMarkup(
				one_time_keyboard=False, resize_keyboard=True, row_width=1)
			markup.row('⏩ Пропустить этот шаг')
			markup.row('⬅️ Отмена')
			return bot.send_message(cid, text, reply_markup=markup)
		if 'description' not in READY_TO_OUTCOME[uid]:
			util.add_outcome(uid, READY_TO_OUTCOME[uid]['amount'], message.text)
			del READY_TO_OUTCOME[uid]
			text = '✅ Расход добавлен!'
			markup = types.ReplyKeyboardMarkup(
				one_time_keyboard=False, resize_keyboard=True, row_width=1)
			for command_arr in config.main_markup:
				markup.row(*command_arr)
			return bot.send_message(cid, text, reply_markup=markup)

	# Handle main menu buttons
	if message.text == '➕ Доход':
		text = 'Введите сумму дохода в рублях (Число)'
		READY_TO_INCOME[uid] = {}
		markup = types.ReplyKeyboardMarkup(
			one_time_keyboard=False, resize_keyboard=True, row_width=1)
		markup.row('⬅️ Отмена')
		return bot.send_message(cid, text, reply_markup=markup)
	elif message.text == '➖ Расход':
		text = 'Введите сумму расхода в рублях (Число)'
		READY_TO_OUTCOME[uid] = {}
		markup = types.ReplyKeyboardMarkup(
			one_time_keyboard=False, resize_keyboard=True, row_width=1)
		markup.row('⬅️ Отмена')
		return bot.send_message(cid, text, reply_markup=markup)
	elif message.text == '📈 Статистика':
		text = 'В разработке'
		return bot.send_message(cid, text)
	elif message.text == 'ℹ️ О боте':
		return bot.send_message(cid, config.about_bot)
	elif message.text == 'ℹ️ О разработчике':
		return bot.send_message(cid, config.about_developer)


def main():
	# TODO: while loop
	# TODO: autopep8 lint
	bot.polling(none_stop=True)


if __name__ == '__main__':
	main()
