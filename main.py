import logging
import sqlite3
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = "YOUR_TOKEN_HERE"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def init_db():
    conn = sqlite3.connect('filestore.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content (
            unique_id TEXT PRIMARY KEY,
            type TEXT,
            data TEXT,
            caption TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_content(unique_id, c_type, data, caption=None):
    conn = sqlite3.connect('filestore.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO content (unique_id, type, data, caption) VALUES (?, ?, ?, ?)', 
                   (unique_id, c_type, data, caption))
    conn.commit()
    conn.close()

def get_content(unique_id):
    conn = sqlite3.connect('filestore.db')
    cursor = conn.cursor()
    cursor.execute('SELECT type, data, caption FROM content WHERE unique_id = ?', (unique_id,))
    result = cursor.fetchone()
    conn.close()
    return result

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args and len(args) > 0:
        unique_id = args[0]
        content = get_content(unique_id)
        
        if content:
            c_type, data, caption = content
            chat_id = update.effective_chat.id
            
            if c_type == 'text':
                await context.bot.send_message(chat_id=chat_id, text=data)
            elif c_type == 'photo':
                await context.bot.send_photo(chat_id=chat_id, photo=data, caption=caption)
            elif c_type == 'video':
                await context.bot.send_video(chat_id=chat_id, video=data, caption=caption)
            elif c_type == 'audio':
                await context.bot.send_audio(chat_id=chat_id, audio=data, caption=caption)
            elif c_type == 'voice':
                await context.bot.send_voice(chat_id=chat_id, voice=data, caption=caption)
            elif c_type == 'document':
                await context.bot.send_document(chat_id=chat_id, document=data, caption=caption)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Content not found.")
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Send me any file, text, or media, and I will generate a shareable link for it."
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    unique_id = str(uuid.uuid4())[:8]
    bot_username = context.bot.username
    
    c_type = None
    data = None
    caption = msg.caption if msg.caption else None

    if msg.text:
        c_type = 'text'
        data = msg.text
    elif msg.photo:
        c_type = 'photo'
        data = msg.photo[-1].file_id
    elif msg.video:
        c_type = 'video'
        data = msg.video.file_id
    elif msg.audio:
        c_type = 'audio'
        data = msg.audio.file_id
    elif msg.voice:
        c_type = 'voice'
        data = msg.voice.file_id
    elif msg.document:
        c_type = 'document'
        data = msg.document.file_id
    
    if c_type and data:
        save_content(unique_id, c_type, data, caption)
        link = f"https://t.me/{bot_username}?start={unique_id}"
        await msg.reply_text(f"Stored! Share this link:\n{link}")
    else:
        await msg.reply_text("Unsupported content type.")

if __name__ == '__main__':
    init_db()
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.ALL & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    print("Bot is running...")
    application.run_polling()
