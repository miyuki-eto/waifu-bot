import requests
from xml.etree import ElementTree
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

bot = commands.Bot(command_prefix='!')


def get_post_image(tags):
    # check for qty field, if absent default to 1
    if 'qty:' in tags:
        qty = int(tags.split('qty:')[-1])
        tags = tags.split('qty:')[0]
    else:
        qty = 1
    qty = 10 if qty > 10 else qty

    # remove function name from command
    tags = tags.replace("!waifu", "").strip().replace(" ", "+")

    # construct api url
    url = "https://yande.re/post.xml?limit=" + str(qty) + "&tags=order%3Arandom+-loli"
    if len(tags) > 0:
        url = url + "+" + tags

    # make api call
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    # create array of image urls else return no results string
    results = ElementTree.fromstring(r.content)
    images = []
    if len(results) > 0:
        for x in results:
            images.append(x.attrib['sample_url'])
    else:
        images = 'no results'
    print(images)
    return images


def get_tags(tags):
    # remove function names from command
    tags1 = tags.replace("!tag", "").replace("!waifu", "").strip().split(' ')[0]

    # construct api url
    url = "https://yande.re/tag.xml?limit=10&order=count&name=" + tags1

    # make api call
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    # append tag details to output string
    results = ElementTree.fromstring(r.content)
    output = ""
    for x in results:
        new_result = '{} - qty: {}'.format(x.attrib['name'], x.attrib['count'])
        output = output + new_result + '\n'

    return output


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def waifu(ctx):
    # check for images
    result = get_post_image(ctx.message.content)

    # if no image results do a tag search and display results
    if result == 'no results':
        embed = discord.Embed(title='waifu not found :(')
        value = get_tags(ctx.message.content)
        if len(value) > 0:
            embed.add_field(name="try these tags instead", value=value, inline=False)
            await ctx.send(embed=embed)
        else:
            embed.add_field(name="no similar tags", value='-', inline=False)
            await ctx.send(embed=embed)

    # for each image result post image to channel
    else:
        for x in result:
            await ctx.send(x)


@bot.command()
async def tag(ctx):
    # run tag search and embed results
    embed = discord.Embed()
    value = get_tags(ctx.message.content)
    if len(value) > 0:
        embed.add_field(name="tag search", value=value, inline=False)
        await ctx.send(embed=embed)
    else:
        embed.add_field(name="no similar tags", value='-', inline=False)
        await ctx.send(embed=embed)


bot.run(TOKEN)
