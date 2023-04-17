# Cross-Platform Message Mirroring for Discord and Telegram
The project is a cross-platform messaging solution that allows users to mirror Telegram messages to Discord. It enables seamless communication across multiple channels, and allowing filtering of messages by keyword. The project includes features such as message mirroring, real-time updates, and easy setup and configuration. The goal of the project is to provide a simple and efficient way for users to communicate and share information across different platforms, without having to switch between them.

## Prerequisites
- Telegram Auth Token for the source channels
- Webhooks for the destination servers
- aiohttp==3.8.3
- nextcord==2.1.0
- nextcord_ext_menus==1.5.4
- python-dotenv==0.20.0
- requests==2.28.1
- Telethon==1.26.0


## Installation
```git install https://github.com/LudoviKush/Telegram-To-Discord/new/main```

## Usage
- cd into the directory
- Setup the Webhooks in the .env (Default are WEBHOOK_1 and WEBHOOK_2
- Setup the Telegram Authtoken and the appid in the .env
- node install
- node main.js
