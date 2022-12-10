from aiogram import types



#Menu
#-------------------------------------------------------------#
menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(types.KeyboardButton('✉️ Discord Сервер'))
menu.add(types.KeyboardButton('🔐 ВК Группа'))
#-------------------------------------------------------------#

#Admin
#-------------------------------------------------------------#
apanel = types.InlineKeyboardMarkup(row_width=3)
apanel.add(
    types.InlineKeyboardButton(text='Статистика', callback_data='stats'),
	types.InlineKeyboardButton(text='Рассылка', callback_data='rass')
    )
#-------------------------------------------------------------#

#Back/Cancel
#-------------------------------------------------------------#
back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back.add(
    types.KeyboardButton('Отмена')
)
#-------------------------------------------------------------#