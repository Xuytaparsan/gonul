#Buralara əl dəymə...
#Deploy butonuna bas deploy elə.
#Rəsmi Kanal t.me/Botsinator 

import os, youtube_dl, requests, time
from config import Config
from youtube_search import YoutubeSearch
from pyrogram.handlers import MessageHandler
from pyrogram import Client, filters
import yt_dlp
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)


#config#

bot = Client(
    'FidowMusicBot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

#start mesajı

@bot.on_message(filters.command(['start']))
def start(client, message):
    demon = f'👋 **Salam** {message.from_user.mention}\n\n**ℹ️ Mən musiqi yükləmə botuyam, istədiyiniz musiqini yükləyə bilərəm**\n\n** ✅ Yardım üçün** /help **əmrindən** istifadə edin
    message.reply_text(
        text=demon, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [[
                    InlineKeyboardButton('❤Sahib❤', url='https://t.me/HuseynH'),
                  ],[
                    InlineKeyboardButton('Playlist 🎵', url=f'https://t.me/{Config.PLAYLIST_NAME}')
                ]
            ]
        )
    )
    
#alive mesaji#

@bot.on_message(filters.command("alive") & filters.user(Config.BOT_OWNER))
async def live(client: Client, message: Message):
    livemsg = await message.reply_text('`Bəli Mən Qoz Kimi İşləyirəm 😎`')
    
#musiqi əmri#

@bot.on_message(filters.command("bul") & ~filters.edited)
def bul(_, message):
    query = " ".join(message.command[1:])
    m = message.reply("<b> Axtarılır ... 🔍</b>")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        m.edit("<b>😭Mahnını Tapa Bilmədim.</b>")
        print(str(e))
        return
    m.edit("<b>📥 Yükləmə başladı...</b>")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"**🎶 Endirildi. Xoş dinləmələr [MusicAz](https://t.me/MusicAzPlaylist) 🎶.**"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("📤 Yüklənir..")
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name, performer="MusicAzPlaylist")
        m.delete()
        bot.send_audio(chat_id=Config.PLAYLIST_ID, audio=audio_file, caption=rep, performer="@FidowMusicBot", parse_mode='md', title=title, duration=dur, thumb=thumb_name)
    except Exception as e:
        m.edit("<b>❌ Xəta  Zəhmət Olmasa Sahibimə Bildirin .</b>")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
