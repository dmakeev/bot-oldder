"""PROсрочка bot - main entry point."""
import logging
from telegram.ext import ApplicationBuilder
from .config import BOT_TOKEN
from .handlers import setup_handlers
from .services.date_calc import DateCalculator
from .services.calendar import CalendarService

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def main():
    """Initialize and start the bot."""
    # Create application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Set up date calculator and calendar service
    date_calc = DateCalculator()
    calendar = CalendarService()

    # Set up handlers
    setup_handlers(app, date_calc, calendar)

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
