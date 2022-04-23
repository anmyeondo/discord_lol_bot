import discord
from discord.ext import commands
import json
import io
import random
from Riot import Riot

bot = commands.Bot(command_prefix="#")

@bot.event
async def on_ready():
    print(f"{bot.user}")

@bot.command(name="인사")
async def hello(ctx, name):
    await ctx.send(f"{name} 어서오고")

@bot.command(name="솔랭")
async def search(ctx, summoner_name):
    # Get summoner info
    user_profile = riot.get_user_profile(summoner_name)
    if type(user_profile) == int:
        await ctx.send(f"{summoner_name}란 사람은 없는데요?")
        return

    # Get profile icon image from cdn
    profile_id = user_profile["profileIconId"]
    profile_icon_stream = riot.get_user_profile_icon_cdn(profile_id)
    if type(profile_icon_stream) == int:
        await ctx.send("문제가 발생했어요 ...")
        return

    # Get User's match data
    summoner_id = user_profile["id"]
    user_match_log = riot.get_user_match_log(summoner_id)
    if type(user_match_log) == int:
        await ctx.send("문제가 발생했어요 ...")
        return
    
    # Data processing
    for obj in res_obj:
        if obj["queueType"] == "RANKED_SOLO_5x5":
            tier = obj["tier"]
            rank = obj["rank"]
            league_points = obj["leaguePoints"]
            wins = obj["wins"]
            losses = obj["losses"]
            winrate = wins / (wins + losses) * 100

            if "miniSeries" in obj:
                progress = obj["miniSeries"]["progress"]
                progress_desc = f"\n승급전: "
                for prog in progress:
                    if prog == "W":
                        progress_desc += "O"
                    elif prog == "L":
                        progress_desc += "X"
                    else:
                        progress_desc += "-"
            else:
                progress_desc = ""

    # Set icon image file
    profile_icon_name = "profile.png"
    profile_icon_file = discord.File(io.BytesIO(profile_icon_stream), filename=profile_icon_name)
    
    tier_icon_name = f"Emblem_{tier}.png"
    tier_icon_file = discord.File(f"ranked-emblems/{tier_icon_name}")
    
    # Build Embed Interface
    embed = discord.Embed(
        title=f"{tier} {rank} - {league_points}점",
        description=f"{wins+losses}전 {wins}승 {losses}패 {winrate:.2f}%{progress_desc}"
    )
    embed.set_author(
        name=f"{summoner_name} (Lv.{level})",
        icon_url=f"attachment://{profile_icon_name}"
    )
    embed.set_thumbnail(
        url=f"attachment://{tier_icon_name}"
    )
    
    await ctx.send(files=[profile_icon_file, tier_icon_file], embed=embed)

@bot.command(name="야옹")
async def meow(ctx):
    rand = random.randrange(1, 16)
    image = discord.File(f"cat/{rand}.png", filename="image.png")
    embed = discord.Embed()
    embed.set_image(
        url=f"attachment://image.png"
    )

    await ctx.send(files=[image], embed=embed)

if __name__ == '__main__':
    with open('config.json') as f:
        data = json.load(f)
    
    riot = Riot(data['riot_key'])
    bot.run(data['bot_token'])