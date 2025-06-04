from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import random

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Token du bot (fourni par l'utilisateur)
BOT_TOKEN = "8198861847:AAEbdLQVw7QsikLgoxsoGRAJdGIiXGSUlDg"

# Date et heure de l'épreuve de Bac de Français : 13 juin 2025 à 9h (heure de Paris)
BAC_DATETIME = datetime(2025, 6, 13, 9, 0, 0, tzinfo=ZoneInfo("Europe/Paris"))

# Astuces / références courtes pour motiver et rappeler le programme
BAC_TIPS = [
    "La métaphore, c'est comme un airdrop : tu reçois une image sans prévenir, mais elle te donne de la valeur.",
    "L'hyperbole, c'est le pump d'un shitcoin : ça exagère grave pour faire rêver.",
    "La métonymie, c'est comme dire \"le wallet\" pour \"le trader\" : on remplace le contenant par le contenu.",
    "L'oxymore, c'est le \"rug-pull sécurisé\" de la littérature : deux mots opposés dans le même smart contract.",
    "L'allégorie, c'est une roadmap artistique : un récit concret pour parler d'idées abstraites.",
    "Le classicisme, c'est la layer 1 du bon goût : ordre, règles, clarté.",
    "Le romantisme, c'est le bull run des émotions : passion, nature, dépassement.",
    "Le réalisme, c'est l'audit d'un projet DeFi : on regarde la réalité en face, sans embellir.",
    "Le symbolisme, c'est comme les NFT PFP : chaque détail cache un sens plus profond.",
    "Le surréalisme, c'est du yield farming mental : on explore l'irrationnel pour en tirer du sens.",
    "L'introduction, c'est ton whitepaper : elle doit poser le cadre et convaincre vite.",
    "La problématique, c'est le smart contract de ta réflexion : elle structure tout le reste.",
    "Chaque partie, c'est un staking pool : tu y déposes tes arguments et tu récoltes des points.",
    "La transition, c'est ton bridge entre deux blockchains d'idées.",
    "La conclusion, c'est ton claim final : tu retires ton rendement intellectuel.",
    "Lire un texte, c'est comme faire un DYOR (Do Your Own Research) : faut scanner les lignes et pas se faire rug.",
    "Un champ lexical, c'est le tokenomics d'un passage : ça te dit où le texte veut aller.",
    "Le narrateur, c'est le dev anonyme : il peut manipuler sans qu'on le voie.",
    "Le rythme des phrases, c'est la volatilité du marché : parfois calme, parfois frénétique.",
    "Un changement de registre, c'est un flip de narrative : le FUD devient FOMO.",
    "À l'oral, sois comme un bon shiller : clair, fluide, et avec des punchlines.",
    "Si t'es bloqué, fais comme dans un bear market : reste calme et recentre-toi sur les fondamentaux.",
    "Ta voix, c'est ton whitepaper vocal : inspire confiance pour donner envie d'investir dans ton discours.",
    "La question de grammaire, c'est l'analyse technique : faut être rigoureux et précis.",
    "La lecture expressive, c'est ton graphique animé : elle rend la structure visible.",
]


def format_time_delta(delta: timedelta) -> str:
    """Formate un objet timedelta en chaîne lisible indiquant j/h/m/s."""
    total_seconds = int(delta.total_seconds())
    if total_seconds < 0:
        return "L'épreuve a déjà commencé ! 🎉"

    days = total_seconds // 86_400
    hours = (total_seconds % 86_400) // 3_600
    minutes = (total_seconds % 3_600) // 60
    seconds = total_seconds % 60

    parts = []
    if days:
        parts.append(f"{days} jour{'s' if days > 1 else ''}")
    if hours or parts:
        parts.append(f"{hours} heure{'s' if hours > 1 else ''}")
    if minutes or parts:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    parts.append(f"{seconds} seconde{'s' if seconds > 1 else ''}")

    return ", ".join(parts)


async def bac_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Répond au /bac avec le compte à rebours avant l'épreuve."""
    now = datetime.now(ZoneInfo("Europe/Paris"))
    delta = BAC_DATETIME - now
    countdown_text = format_time_delta(delta)
    tip = random.choice(BAC_TIPS)
    await update.message.reply_text(
        (
            f"⏳ Il reste {countdown_text} avant l'épreuve de Bac de Français 📚\n\n"
            f"💡 {tip}\n\n"
            f"Bon courage @mkyDnys !"
        )
    )


async def revise_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Rappelle à l'utilisateur @mkyDnys de réviser."""
    await update.message.reply_text(
        "📚 Hey @mkyDnys, n'oublie pas de réviser pour le Bac de Français ! 💪"
    )


# --- Réponse automatique quand le bot est mentionné ---


async def mention_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Répond lorsqu'on @mentionne le bot dans n'importe quel chat."""
    message = update.message
    if message is None:
        return

    bot_username = (context.bot.username or "").lower()

    # Vérifie si le message contient une mention directe du bot (@BotUsername)
    for entity in message.entities or []:
        if entity.type == "mention":  # type: ignore[attr-defined]
            mentioned_text = message.text[entity.offset : entity.offset + entity.length]
            if mentioned_text.lower() == f"@{bot_username}":
                # Même réponse que la commande /bac
                now = datetime.now(ZoneInfo("Europe/Paris"))
                delta = BAC_DATETIME - now
                countdown_text = format_time_delta(delta)
                tip = random.choice(BAC_TIPS)
                await message.reply_text(
                    (
                        f"⏳ Il reste {countdown_text} avant l'épreuve de Bac de Français 📚\n\n"
                        f"💡 {tip}\n\n"
                        f"Bon courage @mkyDnys !"
                    )
                )
                break


def main() -> None:
    """Lance le bot en mode polling."""
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("bac", bac_command))
    application.add_handler(CommandHandler("revise", revise_command))

    # Handler pour les @mentions
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mention_handler))

    # Démarrage du bot
    print("Bot lancé. Appuyez sur Ctrl+C pour arrêter.")
    application.run_polling()


if __name__ == "__main__":
    main() 
