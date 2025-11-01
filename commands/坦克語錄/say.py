import discord
from discord import app_commands
from discord.ext import commands


class 坦克說(commands.Cog):
	"""/坦克說：把訊息包成『ㄟㄟㄟ許腎虛...』後送出"""
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	@app_commands.command(name="坦克說", description="把你的訊息用『ㄟㄟㄟ許腎虛...』格式說出來")
	@app_commands.describe(message="要說的訊息")
	async def say(self, interaction: discord.Interaction, message: str):
		text = f"ㄟㄟㄟ許腎虛{message}嘿嘿嘿嘿嘿"
		if len(text) > 2000:
			await interaction.response.send_message("訊息太長，請縮短後再試。", ephemeral=True)
			return
		await interaction.response.send_message(text)


async def setup(bot: commands.Bot):
	await bot.add_cog(坦克說(bot))
