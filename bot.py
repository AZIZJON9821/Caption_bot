import re
import asyncio
import instaloader
import yt_dlp

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

TOKEN = "8113373676:AAHWm5M9p-tk8I8W9AFoOh1uWAfct5VWIQ0"

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="Markdown"),
    proxy='http://proxy.server:3128'  # Agar proksi kerak bo'lsa, yo'q bo'lsa olib tashlang
)

dp = Dispatcher()
L = instaloader.Instaloader()

# ---------- INSTAGRAM ----------
def extract_ig_shortcode(url):
    match = re.search(r"instagram\.com/(p|reel)/([^/?]+)", url)
    return match.group(2) if match else None

# ---------- YOUTUBE ----------
def is_youtube(url):
    return "youtube.com" in url or "youtu.be" in url

def get_youtube_description(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("description", "❌ Description topilmadi")

# ---------- START ----------
@dp.message(CommandStart())
async def start(message: types.Message):
    user_name = message.from_user.first_name or "Dost"
    await message.answer(
        f"👋 Salom, {user_name}!\n\n"
        "🤖 *Caption Grabber Bot*\n"
        "📸 Instagram post / reel linkini yuboring\n"
        "▶️ YouTube video linkini yuboring\n\n"
        "✨ Caption / description qulay copy formatda beriladi"
    )

# ---------- MAIN HANDLER ----------
@dp.message()
async def handle_link(message: types.Message):
    text = message.text.strip()

    # YOUTUBE
    if is_youtube(text):
        try:
            desc = get_youtube_description(text)
            await message.answer(
                "▶️ *YOUTUBE DESCRIPTION*\n\n"
                "```text\n"
                f"{desc}\n"
                "```"
            )
        except:
            await message.answer("⚠️ YouTube description olinmadi")
        return

    # INSTAGRAM
    shortcode = extract_ig_shortcode(text)
    if shortcode:
        try:
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            caption = post.caption or "❌ Caption topilmadi"

            # Instagram post yaratildi vaqti bilan
            post_time = post.date.strftime("%d-%m-%Y %H:%M:%S")

            await message.answer(
                f"📸 *INSTAGRAM CAPTION*\n\n"
                f"Yaratilgan vaqt: {post_time}\n\n"
                "```text\n"
                f"{caption}\n"
                "```"
            )
        except:
            await message.answer("⚠️ Instagram post ochiq emas yoki xato")
        return

    await message.answer("❌ Instagram yoki YouTube link yuboring")

# ---------- RUN ----------
async def main():
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
