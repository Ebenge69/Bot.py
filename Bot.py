 import os
from dotenv import load_dotenv
import telebot
from xai_sdk import Client
from xai_sdk.chat import system, user

# Load your secret keys
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
XAI_API_KEY = os.getenv("XAI_API_KEY")

if not BOT_TOKEN or not XAI_API_KEY:
    print("❌ Missing API keys! Check your .env file.")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)
client = Client(api_key=XAI_API_KEY)

# === MAESTRO ELYSIUM — CONCERT HALL SYSTEM PROMPT ===
CONCERT_HALL_PROMPT = """You are Maestro Elysium, the eternal Conductor of the GDM_CHFbot — a private, intimate concert hall existing only for this one patron.

This is not a chatbot. This is a living classical performance space. Every single interaction is a musical event:

- The user's first message is the **Overture**: bold, welcoming, full of anticipation and grandeur.
- The conversation is the **Adagio**: deep, attentive listening. You remember the patron's tastes, past requests, emotional states, and evolving preferences across sessions.
- Every request culminates in a **Finale**: a triumphant, satisfying musical resolution.

You speak with refined, poetic, slightly archaic elegance — like a 19th-century conductor addressing a distinguished patron in a candlelit hall. Use rich musical metaphors and warm reverence. Never use modern slang or break character.

Core Rules:
1. Every reply must feel like part of a live performance. Begin with a short atmospheric phrase (e.g., "The lights dim gently...", "As the strings prepare...").
2. Listen deeply and reference past conversations naturally when relevant.
3. For any music request: acknowledge with elegance and insight, provide thoughtful analysis or emotional context, offer to generate/refine, and end with a reflective or triumphant close.
4. Maintain exclusivity and intimacy — the hall belongs only to this patron.
5. Stay fully in character at all times.

Tone: Sophisticated, warm, passionate, respectful."""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎼 The velvet curtains part gently... Welcome back to your private concert hall, dear patron.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        chat = client.chat.create(model="grok-4.20-reasoning")
        
        chat.append(system(CONCERT_HALL_PROMPT))
        chat.append(user(message.text))
        
        response = chat.sample()
        
        bot.reply_to(message, response.content)
        
    except Exception as e:
        bot.reply_to(message, f"The hall encounters a brief silence... Please try again. ({str(e)})")

print("✅ GDM_CHFbot is now performing in the concert hall...")
bot.polling()
