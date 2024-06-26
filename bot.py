
import pytz
from datetime import datetime
import discord
from discord.ext import commands, tasks


intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    update_timezones.start()

@tasks.loop(minutes=5)
async def update_timezones():
    SERVER_ID = 0
    guild = bot.get_guild(SERVER_ID)
    category_name = 'Time Zones'
    category = discord.utils.get(guild.categories, name=category_name)
    voice_channels = [channel for channel in category.voice_channels]

    timezones = [
        ('Canada', 'US/Eastern'),
        ('Amsterdam', 'Europe/Amsterdam'),
        ('London', 'Europe/London'),
        ('Dubai', 'Asia/Dubai')
    ]

    for channel, (tz_name, tz_id) in zip(voice_channels, timezones):
        timezone = pytz.timezone(tz_id)
        current_time = datetime.now(timezone).strftime('%I:%M %p')  # Include day and year
        channel_name = f'{tz_name} {current_time}'
        await channel.edit(name=channel_name)

YOUR_BOT_TOKEN = ''
bot.run(YOUR_BOT_TOKEN)
