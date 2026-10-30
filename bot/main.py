"""PROсрочка bot - main entry point."""
import logging
from datetime import datetime, time, timedelta

import pytz
from telegram.ext import ApplicationBuilder, CommandHandler, JobQueue

from .config import ADMIN_USER_ID, BOT_TOKEN
from .handlers import setup_handlers
from .handlers.access import handle_start_with_access, setup_access_handlers
from .handlers.reference import reference_search
from .services.access import AccessService
from .services.calendar import CalendarService
from .services.date_calc import DateCalculator
from .services.reminders import ReminderService
from .utils.formatting import format_today_summary
from .utils.rate_limiter import RateLimiter

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Moscow timezone
MSK = pytz.timezone("Europe/Moscow")

# Rate limiter: 10 requests per minute per user
rate_limiter = RateLimiter(max_requests=10, window_seconds=60)


async def send_daily_reminder(context):
    """Send daily morning reminder at 09:09 MSK."""
    logger.info("Sending daily reminder...")

    # Get today's reminders
    service = ReminderService()
    now = datetime.now(MSK)
    reminders = await service.get_today_reminders(now)

    # Format and send message
    if reminders:
        # Convert raw tuples to dicts for formatting
        reminder_dicts = []
        for r in reminders:
            reminder_dicts.append({
                'action': r[4],  # event type
                'deadline': r[2]  # scheduled_at
            })
        text = format_today_summary(reminder_dicts)
    else:
        text = "🌞 Доброе утро! На сегодня напоминаний нет."

    await context.bot.send_message(chat_id=ADMIN_USER_ID, text=text)
    logger.info("Daily reminder sent to %s", ADMIN_USER_ID)


async def create_application():
    """Create and configure the bot application."""
    # Create JobQueue
    job_queue = JobQueue()

    # Create application
    app = ApplicationBuilder().token(BOT_TOKEN).job_queue(job_queue).build()

    # Set up date calculator and calendar service
    date_calc = DateCalculator()
    calendar = CalendarService()

    # Set up access control service
    access = AccessService()
    await access.init_db()

    # Set up handlers
    setup_handlers(app, date_calc, calendar)

    # Register reference search command
    app.add_handler(CommandHandler("ref", reference_search))

    # Register access control handlers
    setup_access_handlers(app)

    # Override /start with access-controlled version
    app.add_handler(CommandHandler("start", handle_start_with_access))

    # Set up daily reminder job (09:09 MSK)
    # Calculate next run time
    now_msk = MSK.localize(datetime.now().replace(tzinfo=None))
    today_time = time(9, 9)
    target = MSK.localize(datetime.combine(now_msk.date(), today_time))
    if target <= now_msk:
        target += timedelta(days=1)
    first_run = target - now_msk
    if first_run.total_seconds() < 0:
        first_run += timedelta(days=1)

    app.job_queue.run_repeating(
        send_daily_reminder,
        interval=timedelta(days=1).total_seconds(),
        first=first_run.total_seconds(),
        name="daily_reminder"
    )

    return app


async def main():
    """Initialize and start the bot."""
    app = await create_application()

    # Start the bot
    logger.info("Starting PROсрочка bot...")
    await app.initialize()
    await app.start()
    logger.info("Bot started successfully!")

    # Run until interrupted
    try:
        await app.updater.idle()
    except KeyboardInterrupt:
        logger.info("Stopping bot...")
    finally:
        await app.shutdown()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
