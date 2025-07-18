import logging
from math import log

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import textwrap
from birdeye_entry import exec_main
import asyncio

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def is_valid_solana_address(address):
    """
    Validates a Solana wallet address.

    Args:
        address (str): The wallet address to validate.

    Returns:
        bool: True if the address is valid, False otherwise.
    """
    # Check if the address is 44 characters long and Base58 compliant
    base58_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    if len(address) == 44 and all(char in base58_chars for char in address):
        return True
    return False


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        textwrap.dedent(
            rf"""
        Hi {user.mention_html()}!
        
        Send Me a Solana Address to get the details of the token.
        """
        ),
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    address = update.message.text
    user = update.effective_user

    logger.info(f"User {user.name} has sent {address}")

    if not is_valid_solana_address(address):
        logger.error(f"{address} Invalid CA")
        await update.message.reply_text("Invalid CA")
        return

    return_string = await exec_main(address)

    if return_string:  # Check if the result contains

        await context.bot.send_photo(
            photo=return_string["icon"],
            chat_id=update.effective_chat.id,
            caption=return_string["text"],
            parse_mode="Markdown",
        )

        logger.info(f"{address} OK")

    else:
        logger.error(f"{address} ERROR")
        await update.message.reply_text("ERROR")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token("NONE")
        .build()
    )

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
