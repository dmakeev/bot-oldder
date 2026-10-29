"""Reference search handlers."""
from telegram import Update
from telegram.ext import ContextTypes

from bot.services import reference as ref_service


async def reference_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search the reference book."""
    query = ' '.join(context.args)

    if not query:
        await update.message.reply_text(
            "📖 Поиск по справочнику\n\n"
            "Введите ключевые слова для поиска:\n"
            "/ref <ключевые слова>"
        )
        return

    results = ref_service.search(query)

    if not results:
        await update.message.reply_text(
            "🔍 Ничего не найдено по запросу: " + query
        )
        return

    # Build response
    text = f"📖 Найдено {len(results)} результатов:\n\n"
    for i, item in enumerate(results[:5]):  # Limit to 5 results
        text += f"_{item['id']}. {item['action']}_\n"
        text += f"⏰ {item['deadline']} от {item['from']}\n"
        text += f"📜 {item['law']}\n\n"

    if len(results) > 5:
        text += f"и ещё {len(results) - 5}..."

    await update.message.reply_text(text)