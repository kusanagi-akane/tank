import random

import discord
from discord import app_commands
from discord.ext import commands



TANK_QUOTES: list[str] = [
	"ㄟㄟㄟ許腎虛，要吃甚麼",
	"ㄟㄟㄟ許腎虛，(揮空)",
	"ㄟㄟㄟ許腎虛，你在幹嘛",
	"ㄟㄟㄟ許腎虛，你怎麼穿制服",
	"ㄟㄟㄟ許腎虛，你剛剛去哪了",
]


class 坦克語錄(commands.Cog):
	"""/坦克語錄：隨機回覆一則坦克語錄"""
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	@app_commands.command(name="坦克語錄", description="坦克語錄：隨機一句")
	async def tank(self, interaction: discord.Interaction):
		if not TANK_QUOTES:
			await interaction.response.send_message("目前沒有可用的語錄。", ephemeral=True)
			return
		text = random.choice(TANK_QUOTES)
		if len(text) > 2000:
			await interaction.response.send_message("語錄過長，請調整後再試。", ephemeral=True)
			return
		await interaction.response.send_message(text)


async def setup(bot: commands.Bot):
	await bot.add_cog(坦克語錄(bot))
