from huggingface_hub import InferenceClient
import os
import discord
from discord.ext import commands, tasks
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def generar_texto_daily():
    api_key = os.getenv("AI_API_KEY")
    if not api_key:
        print("⚠️ No se encontró la API Key")
        return random.choice(preguntas)

    client = InferenceClient(model="google/flan-t5-base", token=api_key)

    try:
        response = client.text_generation(
            "Genera una pregunta del día en español:",
            max_new_tokens=50
        )
        print("Respuesta IA:", response)

        # Validar que sea un string y no esté vacío
        if isinstance(response, str) and response.strip():
            return response.strip()
        else:
            print("⚠️ El modelo devolvió vacío")
            return random.choice(preguntas)
    except Exception as e:
        print("⚠️ Error con IA:", repr(e))
        return random.choice(preguntas)


preguntas = [
    "¿Cuál es tu comida favorita? 🍕",
    "¿Qué juego estás jugando últimamente? 🎮",
    "¿Playa o montaña? 🏖️⛰️",
    "Si pudieras tener un superpoder, ¿cuál sería? ✨",
    "¿Cuál es tu película favorita? 🎬",
    "¿Qué canción no puedes dejar de escuchar? 🎶",
    "¿Prefieres café o té? ☕🍵",
    "¿Cuál fue el último libro que leíste? 📚",
    "¿Qué animal te gustaría tener como mascota? 🐾",
    "¿Cuál es tu estación del año favorita? 🌸☀️🍂❄️"
]


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    pregunta_diaria.start()


@tasks.loop(hours=24)
async def pregunta_diaria():
    canal = bot.get_channel(1261175263190978610)
    try:
        pregunta = generar_texto_daily()
    except Exception as e:
        print(f"Error con IA: {e}")
        pregunta = random.choice(preguntas)

    await canal.send(
        f"📢 @everyone Buenos días miembros\nPregunta del día: {pregunta}\nRespondan con @PreguntaDelDiaBot#3980 en general"
    )


@bot.command()
async def pregunta(ctx):
    try:
        pregunta = generar_texto_daily()  # 👈 ya no lleva await
    except Exception:
        pregunta = random.choice(preguntas)

    await ctx.send(
        f"📢 @everyone Buenos días miembros\nPregunta del día: {pregunta}\nRespondan con @PreguntaDelDiaBot#3980 en general"
    )

bot.run(os.getenv("DISCORD_TOKEN"))
