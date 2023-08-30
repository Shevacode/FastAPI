import asyncio
import telebot
import openai

# Замените на свои API-ключи
telegram_api_token = '6323568006:AAGZw8fd7AY_x9mY_Lb5U7fOm4OEbty7m3k'
openai_api_key = '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'

# Числовой идентификатор вашего телеграм канала
channel_id = -1001936584652


# Инициализируем бота и GPT-4.0
bot = telebot.TeleBot(telegram_api_token)
openai.api_key = openai_api_key

# Змінні для зберігання параметра коментування
waiting_for_parameter = False
current_comment_parameter = "коментувати"  # За замовчуванням

@bot.message_handler(commands=['set_parameter'])
def set_parameter(message):
    global waiting_for_parameter
    waiting_for_parameter = True
    bot.send_message(message.chat.id, "Введіть новий параметр коментування у наступному повідомленні.")

@bot.message_handler(content_types=['text', 'photo', 'video', 'audio', 'document', 'sticker', 'voice', 'video_note', 'location', 'contact', 'poll'])
def handle_new_message(message):
    global current_comment_parameter, waiting_for_parameter
    if waiting_for_parameter:
        current_comment_parameter = message.text
        bot.send_message(message.chat.id, f"Параметр коментування встановлено на: {current_comment_parameter}")
        waiting_for_parameter = False
        return

    news_text = message.text if message.text else ""

    if message.caption:
        news_text += " " + message.caption

    if news_text:
        comment = generate_comment_with_parameter(news_text)
        final_comment = f"<b>⬆️🤖 Думка штучного інтелекту:</b>\n\n{comment}"
        bot.send_message(channel_id, final_comment, parse_mode='HTML')

def generate_comment_with_parameter(news_text):
    prompt = f"Як {current_comment_parameter}:\n{news_text}\nКоментар:"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    comment = response.choices[0].message['content'].strip()
    return comment

if __name__ == "__main__":
    bot.polling()
