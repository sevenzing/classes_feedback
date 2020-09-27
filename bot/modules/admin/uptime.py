from aiogram import types
from misc import dp
from subprocess import run, PIPE
import asyncio
import logging

from modules.admin.utils import admin_only_handler, send_message_to_admin
from modules.common.config import exit_codes


@admin_only_handler
async def cmd_uptime(message: types.Message, *args, **kwargs):
    '''
    Send currect uptime
    '''
    uptime = run('uptime', stdout=PIPE).stdout.decode()
    await send_message_to_admin(uptime)

    
