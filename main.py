import os
import logging
import importlib
import pkgutil

import discord
from discord.ext import commands


logging.basicConfig(
	level=logging.INFO,
	format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
)


INTENTS = discord.Intents.default()


def _get_dev_guild():
	guild_id = os.getenv("GUILD_ID")
	if guild_id:
		try:
			return discord.Object(id=int(guild_id))
		except ValueError:
			logging.warning("環境變數 GUILD_ID 不是有效的整數，將改為全域同步指令。")
	return None


DEV_GUILD = _get_dev_guild()


class TankQuotesBot(commands.Bot):
	def __init__(self) -> None:
		super().__init__(command_prefix="!", intents=INTENTS, help_command=None,
						 activity=discord.Game(name="坦克語錄"))

	async def setup_hook(self):
		await self._load_all_extensions()
		if DEV_GUILD is not None:
			self.tree.copy_global_to(guild=DEV_GUILD)
			await self.tree.sync(guild=DEV_GUILD)
			logging.info("已同步指令至指定伺服器 (guild=%s)", DEV_GUILD.id)
		else:
			await self.tree.sync()
			logging.info("已全域同步指令（可能需要數分鐘在所有伺服器上生效）")

	async def on_ready(self):
		logging.info("已登入為 %s (id=%s)", self.user, self.user.id if self.user else "?")

	async def _load_all_extensions(self):
		try:
			pkg = importlib.import_module("commands")
		except Exception as e:
			logging.warning("找不到 commands 套件或載入失敗：%s", e)
			return

		count = 0
		for module_finder, name, is_pkg in pkgutil.walk_packages(pkg.__path__, prefix="commands."):
			base = name.rsplit(".", 1)[-1]
			if base.startswith("_"):
				continue
			if is_pkg:
				continue
			try:
				await self.load_extension(name)
				logging.info("已載入指令模組：%s", name)
				count += 1
			except Exception as e:
				logging.debug("略過或載入失敗：%s（原因：%s）", name, e)

		if count:
			logging.info("共載入 %d 個指令模組（包含子資料夾）", count)
		else:
			logging.warning("未在 commands/ 下找到可載入的指令模組。")


bot = TankQuotesBot()


def main() -> int:
	token = os.getenv("DISCORD_TOKEN")
	if not token:
		logging.error(
			"未找到環境變數 DISCORD_TOKEN。"
		)
		return 1

	try:
		bot.run(token)
	except KeyboardInterrupt:
		logging.info("收到中斷訊號，正在關閉…")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())