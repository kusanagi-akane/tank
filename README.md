# 坦克語錄 Discord 機器人

提供斜線指令（已拆分至 `commands/` 套件中的獨立模組）：
- `/say`：讓機器人用「ㄟㄟㄟ許腎虛{你的訊息}」的格式說話。對應 `commands/say.py`。
- `/tank`：坦克語錄，隨機回覆一句預設語錄。對應 `commands/tank.py`。

## 需要的權限與範圍
- OAuth2 Scopes：`applications.commands`, `bot`
- 不需特別開啟 Privileged Intents（此專案未使用成員/訊息內容意圖）

## 安裝與執行（Windows PowerShell）

1) 安裝相依套件

```powershell
pip install -r .\requirements.txt
```

2) 設定環境變數（至少需要 Token）

```powershell
# 必填：Discord Bot Token（從開發者後台取得）
$env:DISCORD_TOKEN = "你的 Bot Token"

# 選填：若提供 GUILD_ID，slash 指令會優先同步到該伺服器，幾乎立即可用
# 未提供時則進行全域同步（約需 1~5 分鐘才會在所有伺服器生效）
# $env:GUILD_ID = "123456789012345678"
```

3) 啟動機器人

```powershell
python .\main.py
```

## 使用方式
- 在已邀請機器人的伺服器：
  - `/say`：欄位「要說的訊息」填入內容後送出，機器人回覆 `ㄟㄟㄟ許腎虛{你的訊息}`。
  - `/tank`：直接送出，機器人隨機回覆一則坦克語錄。

> 注意：Discord 目前規範斜線指令名稱需為英文小寫（a-z、數字、連字號），因此本專案以 `/tank` 代表「/坦克語錄」。

## 專案結構

```
.
├─ main.py               # 啟動、同步 slash 指令；自動載入 commands 套件
└─ commands/
   └─坦克語錄
  ├─ __init__.py
  ├─ say.py             # /say 指令
  └─ tank.py            # /tank 指令 + 語錄清單
  ├─ fun/               # 子資料夾（示例，可自行新增更多）
    └─ echo.py         # commands/fun/echo.py 也會被自動載入
```

## 新增一個指令
1) 在 `commands/` 或其子資料夾新增檔案，例如 `fun/foo.py`。
2) 建立一個 Cog，並在 `async def setup(bot)` 中 `await bot.add_cog(...)`。
3) 使用 `@app_commands.command` 定義指令；建議名稱使用英文小寫。
4) 重新啟動程式即可自動載入新模組（不需改 `main.py`）。

注意事項：
- 以底線 `_` 開頭的模組/套件（例如 `_utils.py`、`_private/`）會被略過。
- 子資料夾需要有 `__init__.py` 才會被辨識為套件並遞迴探索（例如 `commands/坦克語錄/__init__.py`）。
- 你也可以把整個子資料夾做成擴充（在該資料夾的 `__init__.py` 寫 `async def setup`）。若沒有 `setup`，該套件本身不會被載入，但其中的模組仍會被自動載入。

## 常見問題
- 指令沒出現：
  - 第一次全域同步可能會延遲 1~5 分鐘；
  - 若你設定了 `$env:GUILD_ID`，請確認 ID 正確且機器人已加入該伺服器；
  - 檢查 Bot 是否具備 scopes `applications.commands` 與 `bot`；
  - 重新啟動程式會再次嘗試同步。
- 訊息太長：Discord 單一訊息上限約 2000 字元，超過會收到提示。

## 開發說明
- 主要檔案：`main.py`
- 相依：`discord.py` 2.x
- 若要改指令名稱或描述，請調整 `@bot.tree.command` 與 `@app_commands.describe`。
