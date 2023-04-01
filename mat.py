import telebot
import wolframalpha
import matplotlib.pyplot as plt
from io import BytesIO

bot = telebot.TeleBot('6037310007:AAEHoYIYUWK9Q-Ppt8SHtrrwEAed1ccdFA0')
app_id = '3559KX-23WV87W7T7'
client = wolframalpha.Client(app_id)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Здравствуйте, я решу ваши математические задачи. Используйте команду /instruction, чтобы просмотреть инструкции.")


@bot.message_handler(commands=['instruction'])
def send_instructions(message):
    instructions = "Инструкция:\n\n1. Запустите бота, отправив команду /start.\n2. Отправьте боту математическое выражение, которое вы хотите решить.\n3. Бот будет использовать базу данных создателя для решения выражения и отправит решение обратно вам.\n\nЕсли бот не сможет решить выражение, он отправит сообщение: 'Создатель меня этому еще не научил.'\n Если пример решается в несколько действий то полученный ответ необходимо повторно отправить боту. Удачи!"
    bot.reply_to(message, instructions)


@bot.message_handler(func=lambda message: True)
def solve_expression(message):
    try:
        res = client.query(message.text)

        chart_pod = next((pod for pod in res.pods if pod.get('@id') == 'Plot'), None)
        if chart_pod:
            chart_data = chart_pod.subpods[0].img
            chart = BytesIO(chart_data)
            fig = plt.imread(chart)

            bot.send_photo(message.chat.id, fig)

        result = next(res.results).text
        bot.reply_to(message, f"Решение: {result}")
    except:
        bot.reply_to(message, "Создатель меня этому еще не научил.")


bot.polling()
