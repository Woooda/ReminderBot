import time
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Замените 'YOUR_TOKEN' на ваш токен, полученный от BotFather на Telegram
TOKEN = 'YOUR_TOKEN'

def remind_user(update, context):
    # Парсим сообщение от пользователя
    message = update.message.text.split(' ', 1)
    if len(message) != 2:
        update.message.reply_text("Пожалуйста, введите время и сообщение для напоминания в формате /remind HH:MM Напоминание")
        return

    # Получаем время и сообщение
    reminder_time = message[0]
    reminder_text = message[1]

    try:
        # Парсим время из строки в формате HH:MM
        reminder_time_obj = datetime.strptime(reminder_time, "%H:%M")
        current_time = datetime.now()

        # Вычисляем время до напоминания
        delta_time = reminder_time_obj - current_time.replace(second=0, microsecond=0)
        if delta_time.total_seconds() <= 0:
            update.message.reply_text("Время напоминания должно быть в будущем.")
            return

        # Устанавливаем напоминание
        context.job_queue.run_once(send_reminder, delta_time.total_seconds(), context=update.effective_chat.id, text=reminder_text)

        # Отправляем подтверждение
        update.message.reply_text(f"Напоминание установлено на {reminder_time}.")

    except ValueError:
        update.message.reply_text("Неверный формат времени. Пожалуйста, используйте формат HH:MM.")

def send_reminder(context: CallbackContext):
    # Отправляем пользователю напоминание
    context.bot.send_message(chat_id=context.job.context, text=context.job.context['text'])

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Добавление обработчика команды /remind
    remind_handler = CommandHandler('remind', remind_user)
    dispatcher.add_handler(remind_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
