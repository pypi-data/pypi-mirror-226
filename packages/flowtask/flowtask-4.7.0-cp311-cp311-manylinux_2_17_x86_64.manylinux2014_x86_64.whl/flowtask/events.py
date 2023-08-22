# -*- coding: utf-8 -*-
"""FlowTask Task Events.

Event System for Flowtask tasks.
"""
import asyncio
import traceback
from datetime import datetime
import socket
from typing import Any, Union
from collections.abc import Callable, Awaitable
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from asyncdb import AsyncDB
# logging system
from navconfig.logging import logging
## Notify System
from notify import Notify
from notify.providers.email import Email
from notify.providers.slack import Slack
from notify.models import Actor, Chat, Channel
from flowtask.conf import (
    SEND_NOTIFICATIONS,
    EVENT_CHAT_ID,
    EVENT_CHAT_BOT,
    NOTIFY_ON_ERROR,
    NOTIFY_ON_SUCCESS,
    NOTIFY_ON_FAILURE,
    NOTIFY_ON_WARNING,
    DEFAULT_RECIPIENT,
    EMAIL_USERNAME,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_HOST,
    ENVIRONMENT,
    TASK_EXEC_BACKEND,
    TASK_EXEC_CREDENTIALS,
    TASK_EVENT_TABLE,
    INFLUX_DATABASE,
    TASK_EXEC_TABLE,
    USE_TASK_EVENT,
    SLACK_DEFAULT_CHANNEL,
    SLACK_DEFAULT_CHANNEL_NAME
)
from flowtask.utils.functions import check_empty


def getNotify(notify, **kwargs):
    if notify == 'telegram':
        # defining the Default chat object:
        recipient = Chat(**{"chat_id": EVENT_CHAT_ID, "chat_name": "Navigator"})
        # send notifications to Telegram bot
        args = {
            "bot_token": EVENT_CHAT_BOT,
            **kwargs
        }
        ntf = Notify('telegram', **args)
    elif notify == 'slack':
        recipient = Channel(
            channel_id=SLACK_DEFAULT_CHANNEL,
            channel_name=SLACK_DEFAULT_CHANNEL_NAME
        )
        ntf = Slack()
    elif notify == 'email':
        account = {
            "host": EMAIL_HOST,
            "port": EMAIL_PORT,
            "username": EMAIL_USERNAME,
            "password": EMAIL_PASSWORD,
            **kwargs
        }
        recipient = Actor(**DEFAULT_RECIPIENT)
        ntf = Email(debug=True, **account)
    else:
        recipient = Actor(**DEFAULT_RECIPIENT)
        ntf = Notify(notify, **kwargs)
    return [ntf, recipient]


async def notifyOnSuccess(
    message: str = '',
    result: Any = None,
    event_loop: asyncio.AbstractEventLoop = None,
    **kwargs
):
    """
    notifyOnSuccess.

    Processing event when a task finished correctly
    """
    ntf, recipients = getNotify(NOTIFY_ON_SUCCESS)
    if not check_empty(result):
        message = f'✅ ::{ENVIRONMENT} -  {message!s}'
    else:
        message = f'⚠️ ::{ENVIRONMENT} -  {message!s}, Empty Result.'
    # start sending notifications
    if SEND_NOTIFICATIONS is True:
        args = {
            "recipient": [recipients],
            "message": message
        }
        if ntf.provider_type == 'email':
            args['subject'] = message
        elif ntf.provider == 'telegram':
            args["disable_notification"] = True
        else:
            args['subject'] = message
        async with ntf as t:
            result = await t.send(**args)
    return result


async def notifyEvent(
    message: str = '',
    result: Any = None,
    error: str = None,
    cls: Callable = None,
    trace: str = None,
    task: Callable = None,
    event_loop: asyncio.AbstractEventLoop = None,
    **kwargs
):
    """
    notifyEvent.

    Processing events and send notification to users.
    """
    program = task.getProgram()
    task = task.taskname

    if message is not None and result is not None:
        # success event:
        ntf, recipients = getNotify(NOTIFY_ON_SUCCESS)
        message = f'✅ ::{ENVIRONMENT} -  {message!s}'
    elif trace is not None:
        ntf, recipients = getNotify(NOTIFY_ON_FAILURE)
        message = f'🛑 ::{ENVIRONMENT} -  {error!s}'
    elif message == '':
        program = None
        task = None
        component = None
        if not error:
            error = str(cls)
        if 'component' in kwargs:
            component = kwargs['component']
            del kwargs['component']
        if program and task and component:
            message = f'🛑 ::{ENVIRONMENT} -  Task {program}.{task}, Error on {component}: {error!s}'
        elif program and task:
            message = f'🛑 ::{ENVIRONMENT} -  Error on {program}.{task}: {error!s}'
        elif task:
            message = f'🛑 ::{ENVIRONMENT} -  Error on {task}, raised {cls.__class__!s}: {error!s}'
        else:
            message = f'⚠️ ::{ENVIRONMENT} -  Task Error: {error!s}'
        ntf, recipients = getNotify(NOTIFY_ON_ERROR, **kwargs)
    else:
        # is a warning
        ntf, recipients = getNotify(NOTIFY_ON_WARNING, **kwargs)
        msg = result if result is not None else message
        message = f'⚠️ ::{ENVIRONMENT} -  {msg!s}'
    # start sending notifications
    if SEND_NOTIFICATIONS is True:
        args = {
            "recipient": [recipients],
            "message": message,
        }
        if ntf.provider_type == 'email':
            args['subject'] = message
        if ntf.provider == 'telegram':
            args["disable_notification"] = True
        print('ARGS: ', args)
        async with ntf as t:
            result = await t.send(**args)
        return result


async def notifyFailure(
    error: str = '',
    cls: Callable = None,
    task: Callable = None,
    event_loop: asyncio.AbstractEventLoop = None,
    **kwargs
):
    """
    notifyFailure.

    Processing events and send notification to users.
    """
    trace = ''
    if 'stacktrace' in kwargs:
        trace = kwargs['stacktrace']
    program = task.getProgram()
    task = task.taskname
    if cls is not None:
        if hasattr(cls, 'message'):
            msg = cls.message
        else:
            msg = str(cls)
    else:
        msg = error
    if program and task:
        message = f'🛑 ::{ENVIRONMENT} -  Task {program}.{task}, {msg!s}'
    else:
        message = f'🛑 ::{ENVIRONMENT} -  {msg!s}'
    if trace:
        message = message + f'\n `*{trace}*`'
    ntf, recipients = getNotify(NOTIFY_ON_FAILURE, **kwargs)
    if SEND_NOTIFICATIONS is True:
        args = {
            "recipient": [recipients],
            "message": message,
        }
        async with ntf as t:
            result = await t.send(**args)
        return result


async def notifyWarning(
    cls: Callable = None,
    task: Callable = None,
    event_loop: asyncio.AbstractEventLoop = None,
    **kwargs
):
    """
    notifyWarning.

    Processing events and send notification to users.
    """
    program = task.getProgram()
    task = task.taskname
    component = None
    status = None
    if 'status' in kwargs:
        status = kwargs['status']
        del kwargs['status']
    if 'component' in kwargs:
        component = kwargs['component']
        del kwargs['component']
    if 'message' in kwargs:
        msg = kwargs['message']
        del kwargs['message']
    else:
        msg = None
    if program and task and component:
        message = f'⚠️ ::{ENVIRONMENT} - *{program}.{task}*: Warning {component}->{str(msg)!s}: {status}'
    elif program and task:
        message = f'⚠️ ::{ENVIRONMENT} - *{program}.{task}*: {str(msg)!s}: {status}'
    else:
        message = f'⚠️ ::{ENVIRONMENT} - {str(msg)!s}: {status}'
    # telegram, chat = getNotify('telegram')
    ntf, recipients = getNotify(NOTIFY_ON_WARNING, **kwargs)
    result = None
    if SEND_NOTIFICATIONS is True:
        args = {
            "recipient": [recipients],
            "message": message,
        }
        if ntf.provider_type == 'email':
            args['subject'] = message
        if ntf.provider == 'telegram':
            args["disable_notification"] = True
        async with ntf as conn:
            result = await conn.send(**args)
    return result
