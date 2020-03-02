import discord
from discord.ext import commands
import asyncio,time,random,logging,json

TOKEN = "TOKEN"

logging.basicConfig(level=logging.INFO)
game = discord.Game("Starting Up!")
bot = commands.Bot(command_prefix="typ",description="Pokémon Type Advantages!",activity=game)

@bot.event
async def on_ready():
    game = discord.Game("Pokémon Shield")
    await bot.change_presence(activity=game)
    logging.info("BOT IS UP")

async def checkTypes(ctx,type1,type2):
    f = open("typeAdvantages.json")
    typeAdvantages = json.load(f)
    if type1 not in typeAdvantages.keys(): # CHECKING IF ARGUMENTS ARE A POKEMON TYPE
        await ctx.send(f"{type1} is not a type!")
        return
    if type2 != None and type2 not in typeAdvantages.keys():
        await ctx.send(f"{type2} is not a type!")
        return
    if type2 == None:
        type2 = "None"
    # CREATING A DICTIONARY OF HOW EFFECTIVE STUFF IS AGAINST THIS
    types = {"normal": 1,"fighting": 1,"flying": 1,"poison": 1,"ground": 1,"rock": 1,"bug": 1,"ghost": 1, "steel": 1,"fire": 1,"water": 1,"grass": 1,"electric": 1,"psychic": 1,"ice": 1,"dragon": 1,"dark": 1,"fairy": 1}
    for pkmntype in typeAdvantages[type1].keys(): # MULTIPLYING BY TYPE ONE EFFECTIVENESS
        typeValue = types[pkmntype] * typeAdvantages[type1][pkmntype]
        types[pkmntype] = typeValue
    if type2 != "None":
        for pkmntype in typeAdvantages[type2].keys(): # MULTIPLYING BY TYPE TWO EFFECTIVENESS
            typeValue = types[pkmntype] * typeAdvantages[type2][pkmntype]
            if typeValue % 1 == 0:
                typeValue = int(typeValue)
            types[pkmntype] = typeValue
    fourTimes = []
    twoTimes = []
    oneTimes = []
    halfTimes = []
    quarterTimes = []
    zeroTimes = []
    for key in types.keys():
        value = types[key]
        if value == 4:
            fourTimes.append(key.capitalize())
        elif value == 2:
            twoTimes.append(key.capitalize())
        elif value == 1:
            oneTimes.append(key.capitalize())
        elif value == 0.5:
            halfTimes.append(key.capitalize())
        elif value == 0.25:
            quarterTimes.append(key.capitalize())
        else:
            zeroTimes.append(key.capitalize())
    f.flush()
    return fourTimes,twoTimes,oneTimes,halfTimes,quarterTimes,zeroTimes,type2

@bot.command(name="e")
async def typeCommand(ctx,type1,type2=None):
    fourTimes,twoTimes,oneTimes,halfTimes,quarterTimes,zeroTimes,type2 = await checkTypes(ctx,type1,type2)
    embed = discord.Embed(colour=discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255)))
    embed.set_author(name=f"{type1.capitalize()} - {type2.capitalize()}".replace(" - None",""), icon_url="https://cdn2.iconfinder.com/data/icons/pokemon-filledoutline/64/pokeball-people-pokemon-nintendo-video-game-gaming-gartoon-ball-512.png")
    embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
    if len(fourTimes) > 0:
        embed.add_field(inline=False,name="4x from", value=" ᛫ ".join(fourTimes))
    if len(twoTimes) > 0:
        embed.add_field(inline=False,name="2x from", value=" ᛫ ".join(twoTimes))
    if len(oneTimes) > 0:
        embed.add_field(inline=False,name="1x from", value=" ᛫ ".join(oneTimes))
    if len(halfTimes) > 0:
        embed.add_field(inline=False,name="½x from", value=" ᛫ ".join(halfTimes))
    if len(quarterTimes) > 0:
        embed.add_field(inline=False,name="¼x from", value=" ᛫ ".join(quarterTimes))
    if len(zeroTimes) > 0:
        embed.add_field(inline=False,name="0x from", value=" ᛫ ".join(zeroTimes))
    await ctx.send(embed = embed)

@bot.command(name="ePokemon",aliases=["epokemon","ep","eP","epoke","ePoke"])
async def pokemon(ctx,pokemon):
    pokemon = pokemon[0:1].upper() + pokemon[1::]
    f = open("pokemon.json")
    pokemons = json.load(f)
    if pokemon in pokemons.keys():
        type1 = pokemons[pokemon][0]
        if len(pokemons[pokemon]) > 1:
            type2 = pokemons[pokemon][1]
        else:
            type2 = None
    else:
        await ctx.send(f"{pokemon} is not a pokemon!")
        return
    fourTimes,twoTimes,oneTimes,halfTimes,quarterTimes,zeroTimes,type2 = await checkTypes(ctx,type1,type2)
    embed = discord.Embed(colour=discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255)))
    embed.set_author(name=f"{pokemon} ᛫ {type1.capitalize()} - {type2.capitalize()}".replace(" - None",""), icon_url="https://cdn2.iconfinder.com/data/icons/pokemon-filledoutline/64/pokeball-people-pokemon-nintendo-video-game-gaming-gartoon-ball-512.png")
    embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
    if pokemon == "Zamazenta" or pokemon == "Zacian":
        swordorshield = "Sword" if pokemon == "Zacian" else "Shield"
        embed.description = f"This Pokémon has multiple forms, if it is the other form use `Crowned{swordorshield}{pokemon}` as the Pokémon name instead!"
    if len(fourTimes) > 0:
        embed.add_field(inline=False,name="4x from", value=" ᛫ ".join(fourTimes))
    if len(twoTimes) > 0:
        embed.add_field(inline=False,name="2x from", value=" ᛫ ".join(twoTimes))
    if len(oneTimes) > 0:
        embed.add_field(inline=False,name="1x from", value=" ᛫ ".join(oneTimes))
    if len(halfTimes) > 0:
        embed.add_field(inline=False,name="½x from", value=" ᛫ ".join(halfTimes))
    if len(quarterTimes) > 0:
        embed.add_field(inline=False,name="¼x from", value=" ᛫ ".join(quarterTimes))
    if len(zeroTimes) > 0:
        embed.add_field(inline=False,name="0x from", value=" ᛫ ".join(zeroTimes))
    await ctx.send(embed = embed)
    f.flush()

bot.run(TOKEN)