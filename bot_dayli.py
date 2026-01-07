import os
import discord
from discord.ext import commands, tasks
import random

intents = discord.Intents.default()
intents.message_content = True  # 🔑 necesario para que funcione !pregunta
bot = commands.Bot(command_prefix="!", intents=intents)


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

# Tarea que se ejecuta cada 24 horas


@tasks.loop(hours=24)
async def pregunta_diaria():
    # Reemplaza con el ID de tu canal
    canal = bot.get_channel(1261175263190978610)
    pregunta = random.choice(preguntas)
    await canal.send(f"📢@everyone Buenos dias miembros Pregunta del día: {pregunta} respondan con @PreguntaDelDiaBot#3980")

# Comando manual por si quieres lanzar una pregunta al instante


@bot.command()
async def pregunta(ctx):
    pregunta = random.choice(preguntas)
    await ctx.send(f"📢@everyone Buenos dias miembros Pregunta del día: {pregunta} respondan con @PreguntaDelDiaBot#3980")

# Reemplaza con el token de tu bot

bot.run(os.getenv("DISCORD_TOKEN"))
