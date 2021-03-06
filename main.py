#!/usr/bin/env python3

import time
import sqlite3
import datetime

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
		year INTEGER NOT NULL,
		income INTEGER NOT NULL,
		income_description TEXT)'''
    cursor.execute(sql)
    # Outcome money table
    sql = '''CREATE TABLE IF NOT EXISTS outcome (
		id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		uid INTEGER NOT NULL,
		month_day INTEGER NOT NULL,
		month_number INTEGER NOT NULL,
		year INTEGER NOT NULL,
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


@bot.message_handler(commands=['help'])
def help_command_handler(message):
    return bot.send_message(message.chat.id, config.help_message)


# Clear old month data
@bot.message_handler(commands=['clear'])
def clear_command_handler(message):
    cid = message.chat.id
    uid = message.from_user.id

    if uid in config.admins:
        util.delete_old_month_data()
        text = 'Устаревшие данные успешно очищены.'
        return bot.send_message(cid, text)
    else:
        text = 'Доступ запрещен.'
        return bot.send_message(cid, text)


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
            util.add_outcome(
                uid,
                READY_TO_OUTCOME[uid]['amount'],
                message.text)
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
        month_number = int(str(datetime.datetime.now())[5:7])
        month_income = 0
        month_income_arr = util.get_month_income(uid, month_number)
        for x in month_income_arr:
            month_income += x.income
        month_outcome = 0
        month_outcome_arr = util.get_month_outcome(uid, month_number)
        for x in month_outcome_arr:
            month_outcome += x.outcome
        statistic = month_income - month_outcome
        text = 'Статистика за {!s}\n\n➕ Доход: {!s}p\n➖ Расход: {!s}p\n💵 Прибыль: {!s}p'.format(
            config.months_values[month_number], month_income, month_outcome, statistic)
        keyboard = types.InlineKeyboardMarkup()
        income_btn = types.InlineKeyboardButton(
            text='Смотреть доходы', callback_data='current_incomes')
        outcome_btn = types.InlineKeyboardButton(
            text='Смотреть расходы', callback_data='current_outcomes')
        keyboard.add(income_btn, outcome_btn)
        keyboard.add(
            types.InlineKeyboardButton(
                text='⏮ Прошлый месяц',
                callback_data='lastmonth'))
        return bot.send_message(cid, text, reply_markup=keyboard)
    elif message.text == 'ℹ️ О боте':
        return bot.send_message(cid, config.about_bot)
    elif message.text == 'ℹ️ О разработчике':
        return bot.send_message(cid, config.about_developer)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    uid = call.from_user.id
    cid = call.message.chat.id
    month_number = int(str(datetime.datetime.now())[5:7])

    bot.send_chat_action(cid, 'typing')

    if call.data == 'current_incomes':
        incomes = util.get_month_income(uid, month_number)
        if len(incomes) == 0:
            text = 'Нет доходов.'
            return bot.send_message(cid, text)
        for x in incomes:
            _date = util.generate_correct_date(x)
            text = '*Доход*\n\nСумма: {}\nОписание: {!s}\nДата: {!s}'.format(
                x.income, x.income_description, _date)
            keyboard = types.InlineKeyboardMarkup()
            income_btn = types.InlineKeyboardButton(
                text='❌ Удалить', callback_data='deleteincome_{!s}'.format(x.id))
            keyboard.add(income_btn)
            bot.send_message(
                cid,
                text,
                parse_mode='markdown',
                reply_markup=keyboard)
    elif call.data == 'current_outcomes':
        outcomes = util.get_month_outcome(uid, month_number)
        if len(outcomes) == 0:
            text = 'Нет расходов.'
            return bot.send_message(cid, text)
        for x in outcomes:
            _date = util.generate_correct_date(x)
            text = '*Расход*\n\nСумма: {}\nОписание: {!s}\nДата: {!s}'.format(
                x.outcome, x.outcome_description, _date)
            keyboard = types.InlineKeyboardMarkup()
            income_btn = types.InlineKeyboardButton(
                text='❌ Удалить', callback_data='deleteoutcome_{!s}'.format(x.id))
            keyboard.add(income_btn)
            bot.send_message(
                cid,
                text,
                parse_mode='markdown',
                reply_markup=keyboard)
    elif call.data == 'lastmonth':
        month_number = int(str(datetime.datetime.now())[5:7]) - 1
        month_income = 0
        month_income_arr = util.get_month_income(uid, month_number)
        for x in month_income_arr:
            month_income += x.income
        month_outcome = 0
        month_outcome_arr = util.get_month_outcome(uid, month_number)
        for x in month_outcome_arr:
            month_outcome += x.outcome
        statistic = month_income - month_outcome
        text = 'Статистика за {!s}\n\n➕ Доход: {!s}p\n➖ Расход: {!s}p\n💵 Прибыль: {!s}p'.format(
            config.months_values[month_number], month_income, month_outcome, statistic)
        keyboard = types.InlineKeyboardMarkup()
        income_btn = types.InlineKeyboardButton(
            text='Смотреть доходы', callback_data='last_incomes')
        outcome_btn = types.InlineKeyboardButton(
            text='Смотреть расходы', callback_data='last_outcomes')
        keyboard.add(income_btn, outcome_btn)
        return bot.send_message(cid, text, reply_markup=keyboard)
    elif call.data == 'last_incomes':
        month_number -= 1
        if month_number == 0:
            month_number = 12
        incomes = util.get_month_income(uid, month_number)
        if len(incomes) == 0:
            text = 'Нет доходов.'
            return bot.send_message(cid, text)
        for x in incomes:
            _date = util.generate_correct_date(x)
            text = '*Доход*\n\nСумма: {}\nОписание: {!s}\nДата: {!s}'.format(
                x.income, x.income_description, _date)
            keyboard = types.InlineKeyboardMarkup()
            income_btn = types.InlineKeyboardButton(
                text='❌ Удалить', callback_data='deleteincome_{!s}'.format(x.id))
            keyboard.add(income_btn)
            bot.send_message(
                cid,
                text,
                parse_mode='markdown',
                reply_markup=keyboard)
    elif call.data == 'last_outcomes':
        month_number -= 1
        if month_number == 0:
            month_number = 12
        outcomes = util.get_month_outcome(uid, month_number)
        if len(outcomes) == 0:
            text = 'Нет расходов.'
            return bot.send_message(cid, text)
        for x in outcomes:
            _date = util.generate_correct_date(x)
            text = '*Расход*\n\nСумма: {}\nОписание: {!s}\nДата: {!s}'.format(
                x.outcome, x.outcome_description, _date)
            keyboard = types.InlineKeyboardMarkup()
            income_btn = types.InlineKeyboardButton(
                text='❌ Удалить', callback_data='deleteoutcome_{!s}'.format(x.id))
            keyboard.add(income_btn)
            bot.send_message(
                cid,
                text,
                parse_mode='markdown',
                reply_markup=keyboard)
    elif call.data.startswith('deleteincome'):
        income_id = int(call.data.split('_')[1])
        print(income_id)
        util.delete_income(income_id)
        bot.delete_message(cid, call.message.message_id)
        try:
            bot.answer_callback_query(callback_query_id=call.id, text='Готово')
        except Exception as e:
            print(e)
    elif call.data.startswith('deleteoutcome'):
        outcome_id = int(call.data.split('_')[1])
        print(outcome_id)
        util.delete_outcome(outcome_id)
        bot.delete_message(cid, call.message.message_id)
        try:
            bot.answer_callback_query(callback_query_id=call.id, text='Готово')
        except Exception as e:
            print(e)


def main():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(30)


if __name__ == '__main__':
    main()
