import os
import discord
from discord.ext import commands, tasks
import random
import aiohttp

intents = discord.Intents.default()
intents.message_content = True  # 🔑 necesario para que funcione !pregunta
bot = commands.Bot(command_prefix="!", intents=intents)


async def generar_texto_daily():
    api_key = os.getenv("AI_API_KEY")  # tu clave de Hugging Face
    url = "https://router.huggingface.co/models/bigscience/bloom"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": "Genera una pregunta del día en español:"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            data = await resp.json()
            print("Respuesta IA:", data)

    texto = None

    # Caso 1: lista con generated_text
    if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
        texto = data[0]["generated_text"]

    # Caso 2: objeto con generated_text
    elif isinstance(data, dict) and "generated_text" in data:
        texto = data["generated_text"]

    # Caso 3: error
    elif isinstance(data, dict) and "error" in data:
        raise ValueError(f"Error IA: {data['error']}")

    if not texto:
        raise ValueError("Respuesta IA inválida")

    # Limpieza: quitar el prompt inicial si aparece
    texto = texto.replace(
        "Genera una pregunta del día en español:", "").strip()
    return texto


# Lista de preguntas

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
    pregunta_diaria.start()  # Inicia la tarea automática

# Tarea que se ejecuta cada 24 hora


@tasks.loop(hours=24)
async def pregunta_diaria():
    canal = bot.get_channel(1261175263190978610)  # tu canal
    try:
        # Intentar con IA
        pregunta = await generar_texto_daily()
    except Exception as e:
        print(f"Error con IA: {e}")
        # Si falla, usar una pregunta random de la lista
        pregunta = random.choice(preguntas)

    await canal.send(
        f"📢 @everyone Buenos días miembros\nPregunta del día: {pregunta}\nRespondan con @PreguntaDelDiaBot#3980 en general"
    )


@bot.command()
async def pregunta(ctx):
    try:
        pregunta = await generar_texto_daily()
    except Exception:
        pregunta = random.choice(preguntas)

    await ctx.send(
        f"📢 @everyone Buenos días miembros\nPregunta del día: {pregunta}\nRespondan con @PreguntaDelDiaBot#3980 en general"
    )

bot.run(os.getenv("DISCORD_TOKEN"))
