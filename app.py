import os
from dotenv import load_dotenv

from flask import Flask
from telegram import (
    Update,
    InputMediaPhoto,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)


load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")


# =========================
# Flask (Render health check)
# =========================

web = Flask(__name__)


@web.route("/")
def home():
    return "Telegram Food Bot Running"


# =========================
# Food Menu Data
# =========================

foods = {

    "pizza": {
        "name": "🍕 Pizza",
        "price": "$5.00",
        "image": "https://i.imgur.com/3ZQ3ZQ3.jpeg"
    },

    "burger": {
        "name": "🍔 Burger",
        "price": "$3.50",
        "image": "https://i.imgur.com/5bK9y5V.jpeg"
    },

    "coffee": {
        "name": "☕ Coffee",
        "price": "$2.00",
        "image": "https://i.imgur.com/6X9X9X9.jpeg"
    }

}


# =========================
# /start command
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [
            InlineKeyboardButton(
                "🍕 Pizza",
                callback_data="pizza"
            )
        ],

        [
            InlineKeyboardButton(
                "🍔 Burger",
                callback_data="burger"
            )
        ],

        [
            InlineKeyboardButton(
                "☕ Coffee",
                callback_data="coffee"
            )
        ]

    ]


    reply = InlineKeyboardMarkup(keyboard)


    await update.message.reply_text(
        """
Welcome to Seko Food 🍽️

Please select your food:
        """,
        reply_markup=reply
    )



# =========================
# Button Click
# =========================

async def menu_click(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    food_id = query.data


    food = foods[food_id]


    keyboard = [

        [
            InlineKeyboardButton(
                "🛒 Order Now",
                callback_data=f"order_{food_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅ Back",
                callback_data="back"
            )
        ]

    ]


    await query.message.reply_photo(

        photo=food["image"],

        caption=f"""
{food['name']}

💵 Price: {food['price']}

Thank you ❤️
        """,

        reply_markup=InlineKeyboardMarkup(keyboard)

    )



# =========================
# Order
# =========================

async def order(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    food_id = query.data.replace(
        "order_",
        ""
    )


    food = foods[food_id]


    await query.message.reply_text(

        f"""
✅ Order Received

Food:
{food['name']}

Price:
{food['price']}

Please contact admin for payment.

📞 012345678
        """

    )



# =========================
# Back Menu
# =========================

async def back(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    await start(update, context)



# =========================
# Telegram Bot Setup
# =========================


def run_bot():

    application = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )


    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            menu_click,
            pattern="^(pizza|burger|coffee)$"
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            order,
            pattern="^order_"
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            back,
            pattern="^back$"
        )
    )


    print("Telegram Bot Started")


    application.run_polling()



# =========================
# Run
# =========================

if __name__ == "__main__":

    import threading


    threading.Thread(
        target=lambda:
        web.run(
            host="0.0.0.0",
            port=10000
        )
    ).start()


    run_bot()
