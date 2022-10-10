import asyncio
import logging
from datetime import datetime

import aioredis

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler_di import ContextSchedulerDecorator

from tgbot.config import load_config, Config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot_template.tgbot.handlers.anketa import register_test
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot_template.tgbot.handlers.channel import register_channel
from tgbot_template.tgbot.handlers.prolong import register_prolong
from tgbot_template.tgbot.middlewares.scheduler import SchedulerMiddleware

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config, scheduler):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(SchedulerMiddleware(scheduler))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_channel(dp)
    register_test(dp)
    register_prolong(dp)

    register_echo(dp)


# async def send_message_to_admin(bot: Bot, config: Config):
#     for admin_id in config.tg_bot.admin_ids:
#         await bot.send_message(text="Сообщение по выбранной дате", chat_id=admin_id)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    # Чтобы работал Redis brew services start/stop/restart redis

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    job_stores = {
        "default": RedisJobStore(
            jobs_key="dispatched_trips_jobs", run_times_key="dispatched_trips_running",
            # параметры host и port необязательны, для примера показано как передавать параметры подключения
            host="localhost", port=6379
        )
    }

    # Оборачиваем AsyncIOScheduler специальным классом
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(jobstores=job_stores))
    #
    # # Добавляем зависимости таска в некий контекст
    # scheduler.ctx.add_instance(bot, declared_class=Bot)
    # scheduler.ctx.add_instance(config, declared_class=Config)
    #
    # # Добавляем задачи на выполнение
    # # scheduler.add_job(send_message_to_admin, "interval", seconds=5)
    # scheduler.add_job(send_message_to_admin, 'date', run_date=datetime(2022, 10, 7, 15, 25, 5))
    bot['config'] = config

    register_all_middlewares(dp, config, scheduler)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        scheduler.start()  # запускаем шедулер
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
        scheduler.remove_all_jobs()
        scheduler.shutdown()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
