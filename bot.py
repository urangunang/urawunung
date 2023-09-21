buatlah agar ketika menambahkan bot command akan otomatis memperbarui command pada bot telegram,pada kode dibawah:

import config, sys, os, requests

from plugins import Database
from pyrogram import Client, enums
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats

data = []

class Bot(Client):
    def __init__(self):
        super().__init__(
            'nekomenfessbot',
            api_id=config.api_id,
            api_hash=config.api_hash,
            plugins={
                "root": "plugins"
            },
            bot_token=config.bot_token
        )
    async def start(self):
        await super().start()
        bot_me = await self.get_me()

        db = Database(bot_me.id)
        os.system('cls')
        if not await db.cek_user_didatabase():
            print('[!] Menambahkan data bot ke database...')
            await db.tambah_databot()
        print("[!] Database telah ready")
        print(f"[!] Link Database Kamu : {config.db_url}")
        print("================")

        if config.channel_1:
            try:
                await self.export_chat_invite_link(config.channel_1)
            except:
                print(f'Harap periksa kembali ID [ {config.channel_1} ] pada channel 1')
                print('Pastikan bot telah dimasukan kedalam channel dan menjadi admin')
                print('-> Bot terpaksa dihentikan')
                sys.exit()
        if config.channel_2:
            try:
                await self.export_chat_invite_link(config.channel_1)
            except:
                print(f'Harap periksa kembali ID [ {config.channel_2} ] pada channel 2')
                print('Pastikan bot telah dimasukan kedalam channel dan menjadi admin')
                print('-> Bot terpaksa dihentikan')
                sys.exit()
        if config.channel_log:
            try:
                await self.export_chat_invite_link(config.channel_log)
            except:
                print(f'Harap periksa kembali ID [ {config.channel_log} ] pada channel log')
                print('Pastikan bot telah dimasukan kedalam channel dan menjadi admin')
                print('-> Bot terpaksa dihentikan')
                sys.exit()

        self.username = bot_me.username
        self.id_bot = bot_me.id
        data.append(self.id_bot)
        # Mendapatkan perintah bot yang sudah ada
        existing_commands = await self.get_my_commands()
        
        # Daftar perintah baru yang ingin Anda tambahkan
        new_commands = [
            BotCommand('status', 'Cek Penipu/Bukan'
            BotCommand('status', '🍃 check status'),
            BotCommand('talent', '👙 talent konten / vcs'),
            BotCommand('daddysugar', '👔 daddy sugar trusted'),
            BotCommand('moansgirl', '🧘‍♀️ moans girl'),
            BotCommand('moansboy', '🧘 moans boy'),
            BotCommand('gfrent', '🤵 girl friend rent'),
            BotCommand('bfrent', '🤵 boy friend rent')
        ]

        # Memeriksa perintah baru apa yang belum ada dalam daftar perintah yang sudah ada
        for command in new_commands:
            if command not in existing_commands:
                existing_commands.append(command)

        # Mengatur perintah bot dengan daftar perintah yang sudah diperbarui
        await self.set_my_commands(existing_commands)

        print('BOT TELAH AKTIF')
    
    async def stop(self):
        await super().stop()
        print('BOT BERHASIL DIHENTIKAN')
    
    async def kirim_pesan(self, x: str):
        db = Database(config.id_admin).get_pelanggan()
        pesan = f'<b>TOTAL USER ( {db.total_pelanggan} ) PENGGUNA 📊</b>\n'
        pesan += f'➜ <i>Total user yang mengirim menfess hari ini adalah {x}/{db.total_pelanggan} user</i>\n'
        pesan += '➜ <i>Berhasil direset menjadi 0 menfess</i>'
        url = f'https://api.telegram.org/bot{config.bot_token}'
        a = requests.get(f'{url}/sendMessage?chat_id={config.channel_log}&text={pesan}&parse_mode=HTML').json()
        requests.post(f'{url}/pinChatMessage?chat_id={config.channel_log}&message_id={a["result"]["message_id"]}&parse_mode=HTML')
        requests.post(f'{url}/deleteMessage?chat_id={config.channel_log}&message_id={a["result"]["message_id"] + 1}&parse_mode=HTML')
