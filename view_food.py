from telegram import Update, InputMediaPhoto
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = "8902552924:AAHHQdwJ9Qds5thma5YSzBAiqDa--lOr5js"

# =========================
# MENU
# =========================
foods = {

    "Food": {
        "name": "🍛 មុខម្ហូប (Food)",
        "images": [
            "images/foods/food1.jpg",
            "images/foods/food2.jpg", 
            "images/foods/food3.jpg", 
        ]
    },

    "Drink": {
        "name": "🥤 ភេសជ្ជៈ (Drink)",
        "images": [
            "images/drinks/drink1.jpg",
             
        ]
    },

    "Beer": {
        "name": "🍺 ស្រាបៀរ (Beer)",
        "images": [
            "images/beers/beer1.jpg",
            "images/beers/beer2.jpg",
            "images/beers/beer3.jpg",
             
        ]
    },

}


# =========================
# START COMMAND
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🍴 សូមស្វាគមន៍មកកាន់ Food Shop\n\n"
        "📋 ម៉ឺនុយរបស់យើង"
    )

    for category in foods.values():

        media = []
        opened_files = []

        for index, image_path in enumerate(category["images"]):

            photo = open(image_path, "rb")
            opened_files.append(photo)

            media.append(
                InputMediaPhoto(
                    media=photo,
                    caption=category["name"] if index == 0 else ""
                )
            )

        # Send album
        await update.message.reply_media_group(media=media)

        # Close files
        for file in opened_files:
            file.close()


# =========================
# MAIN
# =========================
def main():

    app = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))

    print("🍴 Food Shop Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()