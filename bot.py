import telebot
from telebot import types
bot = telebot.TeleBot("7806377242:AAHhyhyWlOPJspmbn1eh4rA8eKSinf710js")
user_data = {}
@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {"income": 0, "expenses": []}
    bot.reply_to(message, "Welcome to the Smart Budget Tracker Bot! Use /addincome to add income, /addexpense to add expenses, and /report to generate a report.")
@bot.message_handler(commands=['addincome'])
def add_income(message):
    msg = bot.reply_to(message, "Enter your income amount:")
    bot.register_next_step_handler(msg, process_income)

def process_income(message):
    try:
        income = float(message.text)
        user_data[message.chat.id]["income"] = income
        bot.reply_to(message, f"Income of ${income} added successfully!")
    except ValueError:
        bot.reply_to(message, "Invalid input. Please enter a number.")

# Command to add expenses
@bot.message_handler(commands=['addexpense'])
def add_expense(message):
    msg = bot.reply_to(message, "Enter your expense amount:")
    bot.register_next_step_handler(msg, process_expense)

def process_expense(message):
    try:
        expense = float(message.text)
        user_data[message.chat.id]["expenses"].append(expense)
        bot.reply_to(message, f"Expense of ${expense} added successfully!")
    except ValueError:
        bot.reply_to(message, "Invalid input. Please enter a number.")

@bot.message_handler(commands=['report'])
def generate_report(message):
    income = user_data[message.chat.id]["income"]
    expenses = sum(user_data[message.chat.id]["expenses"])
    remaining_budget = income - expenses
    report = f"Income: ${income}\nTotal Expenses: ${expenses}\nRemaining Budget: ${remaining_budget}"
    bot.reply_to(message, report)
@bot.message_handler(commands=['help'])
def help(message):
    help_text = """
    Available commands:
    /start - Start the bot and get instructions.
    /addincome - Add your income.
    /addexpense - Add your expenses.
    /report - Generate a financial report.
    /help - Show this help message.
    """
    bot.reply_to(message, help_text)

bot.polling()