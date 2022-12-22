import requests
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import ParseMode
from telegram import Bot
import psutil
import telegram
import markdown
import subprocess

updater = Updater("<bot_token>",use_context=True)
bot = Bot("<bot_token>")

# defining some functions which correspond to command typed by user
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Private bot for hecatonchire")

def status(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id == <chat_id>:
        update.message.reply_text("Here is the status of your server, dear.\nComputing...")

        # Getting stats
        cpu_usage :str = str(psutil.cpu_percent(1))
        ram_usage :str = str(psutil.virtual_memory()[2])
        disk_usage :str = str(psutil.disk_usage('/home').percent)
        temp :str = str(psutil.sensors_temperatures()["amdgpu"][0].current)

        caddy :int = subprocess.run(["systemctl", "is-active", "caddy"])
        openvpn :int = subprocess.run(["systemctl", "is-active", "openvpn"])
        sshd :int = subprocess.run(["systemctl", "is-active", "sshd"])

        if caddy.returncode != 0:
            update.message.reply_text("*\[\> CADDY IS NOT RUNNING \!*", parse_mode="MarkdownV2")
        else:
            update.message.reply_text("[+] Caddy should run well.")

        if openvpn.returncode != 0:
            update.message.reply_text("*\[\> OPENVPN IS NOT RUNNING \!*", parse_mode="MarkdownV2")
        else:
            update.message.reply_text("[+] openvpn should run well.")

        if sshd.returncode != 0:
            update.message.reply_text("*\[\> SSHD IS NOT RUNNING \!*", parse_mode="MarkdownV2")
        else:
            update.message.reply_text("[+] sshd should run well.")

        update.message.reply_text("The CPU usage is: " + cpu_usage + "%.\nRAM memory % used: " + ram_usage + "%.\nDisks usage: " + disk_usage + "%.\nTemperature: " + temp + "C.")
    else:
        update.message.reply_text("You're not allowed to access this part.")

def config(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id == 1452859994:

        cpu_count :str = str(psutil.cpu_count())
        cpu_freq :str = str(psutil.cpu_freq().max)
        total_ram :str = str(psutil.virtual_memory().total)

        update.message.reply_text("Running hardware config :\n[+] Core number: " + cpu_count + "\n[+] CPU freq: " + cpu_freq + "MHz\n[+] Total RAM: " + total_ram)
    else:
        update.message.reply_text("You're not allowed to access this part.")

# calling functions when command is passed
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('status', status))
updater.dispatcher.add_handler(CommandHandler('config', config))

# start the bot
updater.start_polling()
