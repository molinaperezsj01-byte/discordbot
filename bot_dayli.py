import os
import discord
from discord.ext import commands, tasks
import random
import cohere

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Inicializar Cohere
co = cohere.Client(os.getenv("COHERE_API_KEY"))

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


def generar_texto_daily():
    try:
        response = co.generate(
            model="command",  # ✅ modelo correcto
            prompt="Genera una pregunta del día en español:",
            max_tokens=50
        )
        texto = response.generations[0].text.strip()
        print("Respuesta IA:", texto)
        return texto if texto else random.choice(preguntas)
    except Exception as e:
        print("⚠️ Error con Cohere:", repr(e))
        return random.choice(preguntas)


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    pregunta_diaria.start()


@tasks.loop(hours=24)
async def pregunta_diaria():
    canal = bot.get_channel(1261175263190978610)
    pregunta = generar_texto_daily()
    await canal.send(
        f"📢 @everyone Buenos días miembros\nPregunta del día: {pregunta}\nRespondan con @PreguntaDelDiaBot#3980 en general"
    )


@bot.command()
async def pregunta(ctx):
    pregunta = generar_texto_daily()
    await ctx.send(
        f"📢 @everyone Buenos días miembros\nPregunta del día: {pregunta}\nRespondan con @PreguntaDelDiaBot#3980 en general"
    )

bot.run(os.getenv("DISCORD_TOKEN"))
