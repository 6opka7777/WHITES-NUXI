
##############################
#          WHITE'S           #
#        ----------          #
#           NUXI             #
##############################

print("NUXI loading...")
print("Done...")

# Берём библиотеку discord.py; YoutubeDL.py; Youtube_DL.py; yt_dlp.py
#!!!Предварительно в cmd:
# pip install discord.py
# pip install YoutubeDL.py
# pip install Youtube_DL
# pip install yt_dlp
# pip install PyNaCl


import discord
from discord.ext import commands

import  ffmpeg
import yt_dlp
from discord.ext import commands
from discord import utils
from youtube_dl import YoutubeDL
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
    #Замените 'O:/WHITES STUDIOS/BACKUP 16.03.2024/ffmpeg/bin/ffmpeg.exe'  на путь до ffmpeg.exe
    'executable': 'O:/WHITES STUDIOS/BACKUP 16.03.2024/ffmpeg/bin/ffmpeg.exe'
}


intents = discord.Intents.all()
intents = discord.Intents.default()
intents.messages = True  # Включаем интент для сообщений
intents.message_content = True  # Включаем привилегированный интент для содержимого сообщений

bot = commands.Bot(command_prefix='/', intents=intents)

#========================================================

# Выводим сообщение в консоль, что бот успешно запущен

@bot.event
async def on_ready():
    # Вывод сообщения в консоль
    print(f'Бот активен как: {bot.user}') 
    # Установка статуса не активен
    await bot.change_presence(status=discord.Status.idle)

#========================================================

#Cообщение при заходе на сервер

@bot.event
async def on_guild_join(guild):
    # Ищем канал для отправки приветственного сообщения
    # Это может быть первый доступный текстовый канал или канал по умолчанию
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                "Привет, я NUXI.\n"
                "Чат бот созданный @6opka_off.\n"
                "Командой разработчиков: WHITES DEV COMMAND.\n"
                "\n(Возможно скоро в меня добавят нейросеть)"
            )
            break  # Прерываем цикл после отправки сообщения

#========================================================

# Модерация контента

# Список плохих слов для модерации, приведенных к нижнему регистру
bad_words = ['блять', 'хуй', 'пизда', 'гандон', 'шлюха', 'тварь', 'ебанат', 'сдохни', 'умри', 'сучка', 'ебанашка', 'обезьяна тупая', 'пидорас', 'педик', 'Пидор', 'Даун' , 'Дибил', 'Дебил', 'Хуеглот', 'Хуеплет', 'долбоёб', 'Далбаёб', 'Любитель толстых членов', 'Гей', 'Лесбиянка', 'Лесби', 'мать', 'Шахава', 'Лох', 'fuck', 'dick', 'cunt', 'scumbag', 'whore', 'creature', 'fucker', 'die', 'die', 'bitch', 'fucker', 'stupid monkey', 'faggot', 'Faggot', 'Faggot', 'Down', 'Dibil', 'Moron', 'Cocksucker', 'Cocksucker', 'Dolboy', 'Dalbaeb', 'Lover of Thick dicks', 'Gay', 'Lesbian', 'Lesbian', 'Mother', 'Shahava', 'Sucker', 'Негр', 'Негройд', 'Обезьяна', 'Бибизяна', 'Бибизьяна', 'Negr', 'Negroid', 'Собака женского пола', 'Сука', 'ёбанная', 'ебанная', 'ебанный', 'ёбанный', 'епарный', 'ёпарный', 'Пизду', 'Ебать', 'даун', 'Мерзавец', 'Nigers']

# Событие, которое срабатывает при получении нового сообщения
@bot.event
async def on_message(message):
    # Проверяем, не является ли автор сообщения самим ботом
    if message.author == bot.user:
        return

    # Проверяем, имеет ли автор сообщения административную роль
    # Замените Admin_role на админ роли пример: admin_roles = [1160134448369631261, 1160134448369631260, 1160134448369631259, 1160134448369631258]
    admin_roles = [Admin_role]  # ID административных ролей
    if any(role.id in admin_roles for role in message.author.roles):
        # Если пользователь имеет административную роль, не проверяем сообщение на плохие слова
        pass
    else:
        # Проверяем наличие плохих слов в сообщении для остальных пользователей
        if any(bad_word.lower() in message.content.lower() for bad_word in bad_words):
            # Отправляем предупреждение пользователю
            warning_msg = await message.channel.send(f'{message.author.mention}, кажется ты плохо себя ведешь!')
            # Удаляем сообщение пользователя
            await message.delete()
            # Опционально: удалить предупреждение после некоторого времени
            await warning_msg.delete(delay=10)  # Удалить предупреждение через 10 секунд
    
    # Обрабатываем команды бота
    await bot.process_commands(message)

#========================================================

#МУЗЫКА


 #------------------------------
 #   Напишем логистику
queues = {}  # ID сервера : [список URL треков]

def check_queue(ctx):
    if queues[ctx.guild.id]:
        play_next(ctx)

async def play_next(ctx):
    server_id = ctx.guild.id
    if queues[server_id]:
        next_url = queues[server_id].pop(0)
        await play_music(ctx, next_url)

async def play_music(ctx, url):
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    link = info['url']
    source = discord.FFmpegPCMAudio(source=link, **FFMPEG_OPTIONS)
    ctx.voice_client.play(source, after=lambda x=None: check_queue(ctx))

def queue_add(ctx, url):
    server_id = ctx.guild.id
    if server_id in queues:
        queues[server_id].append(url)
    else:
        queues[server_id] = [url]

 #------------------------------
  # Напишем команды /play_n | /skip_n | /stop_n
@bot.command()
async def play_n(ctx, *, url):
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    queue_add(ctx, url)
    if not ctx.voice_client.is_playing():
        await play_next(ctx)

@bot.command()
async def skip_n(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await play_next(ctx)

@bot.command()
async def stop_n(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
    queues[ctx.guild.id] = []

@bot.event
async def on_message(message):
    await bot.process_commands(message)

#========================================================

# Запускаем бота
    
bot.run('******')
