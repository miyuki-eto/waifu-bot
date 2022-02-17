import requests
from xml.etree import ElementTree
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

bot = commands.Bot(command_prefix='!')


def get_post_image(tags):
    tags = tags.replace("!waifu", "").strip().replace(" ", "+")
    url = "https://yande.re/post.xml?limit=1&tags=order%3Arandom+-loli"
    if len(tags) > 0:
        url = url + "+" + tags
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    image_url = ElementTree.fromstring(r.content)[0].attrib['sample_url']
    print(image_url)
    return image_url


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def waifu(ctx):
    print(ctx.message.content)
    await ctx.send(get_post_image(ctx.message.content))

bot.run(TOKEN)
