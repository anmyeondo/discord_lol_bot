import discord
import requests
import json
from urllib import parse
from discord.ext import commands

# get token from riot and discord api
bot_token = "Nzc0NTQ4MzQ5OTY1Njk3MDMz.X6ZYXQ.8USj5wXe6WBOb-scWvIEli5skYM"
riot_key = "RGAPI-e498b380-974d-4355-9809-c2f4c87740b0"

# prefix of command
# ex - !대답
bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("{0.user} 어서오고".format(bot))


@bot.command("대답")
async def ans(ctx):
    await ctx.send("아잇씻팔")


@bot.command(name="인사")
async def hello(ctx, name):
    await ctx.send(f"{name} 어서오고")


@bot.command(name="죽상")
async def say(ctx):
    await ctx.send("고길동 개잦밥새끼가 꼴받게 하잖아")


@bot.command(name="호잇")
async def search(ctx, *, summoner_name):

    # Summoner
    enc_summoner_name = parse.quote(summoner_name)
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{enc_summoner_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": riot_key
    }

    res = requests.get(url=url, headers=headers)
    res_obj = json.loads(res.text)

    name = res_obj["name"]
    level = res_obj["summonerLevel"]
    profile_icon_id = res_obj["profileIconId"]

    profile_icon_name = f"{profile_icon_id}.png"
    profile_icon_file = discord.File(f"profileicon/{profile_icon_name}")

    # Legue
    summoner_id = res_obj["id"]
    url = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"

    res = requests.get(url=url, headers=headers)
    res_obj = json.loads(res.text)

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

    tier_icon_name = f"Emblem_{tier}.png"
    tier_icon_file = discord.File(f"ranked-emblems/{tier_icon_name}")
    # Build embed
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

bot.run(bot_token)
