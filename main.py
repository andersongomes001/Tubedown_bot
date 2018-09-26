from __future__ import unicode_literals
import youtube_dl,os,time,telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

#youtube_dl.utils.DownloadError: ERROR: ffprobe or avprobe not found. Please install one.
#SOLUCAO
#sudo apt-get install ffmpeg

PATH = "./"
TOKEN = "SEUTOKEN"

bot = telepot.Bot(TOKEN)

def dow(chat_id,url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '{}%(title)s.%(ext)s'.format(PATH),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #ydl.download([url])
        result = ydl.extract_info("{}".format(url))
        filename = "{}{}.{}".format(PATH,result.get("title", None), "mp3")
        tamanho  = os.path.getsize("{}".format(filename))/(1024*1024.0)
        if tamanho <= 20:
            with open(filename, 'rb')  as f:
                bot.sendDocument(chat_id, f)
        else:
            bot.sendMessage(chat_id, "Arquivo Muito grande")


def handle(msg):
    url = None
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        command = msg['text']
        if "youtu.be" in str(command) or "youtube" in  str(command):
            url = str(command)
            bot.sendMessage(chat_id, "baixando Audio")
            dow(chat_id,url)

MessageLoop(bot, handle).run_as_thread()
print('boot ON')
while 1:
    time.sleep(10)