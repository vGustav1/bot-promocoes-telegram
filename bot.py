import os
import json
import asyncio
from datetime import datetime, timezone
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CANAL = os.getenv("TELEGRAM_CANAL")
INTERVALO_SEGUNDOS = int(os.getenv("INTERVALO_SEGUNDOS", "300"))
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # seu ID pessoal, pra receber os alertas
DIAS_ALERTA = int(os.getenv("DIAS_ALERTA", "3"))  # a partir de quantos dias avisar

if not TOKEN or not CANAL:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN e TELEGRAM_CANAL precisam estar definidos no arquivo .env"
    )

ARQUIVO_OFERTAS = "ofertas.json"
ARQUIVO_ESTADO = "estado.json"

NOME, PRECO_ANTIGO, PRECO_PROMO, LINK, IMAGEM = range(5)

# ---------- Persistência: carregar e salvar em arquivo ----------

def carregar_ofertas():
    if os.path.exists(ARQUIVO_OFERTAS):
        with open(ARQUIVO_OFERTAS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_ofertas():
    with open(ARQUIVO_OFERTAS, "w", encoding="utf-8") as f:
        json.dump(ofertas_ativas, f, ensure_ascii=False, indent=2)

def carregar_indice():
    if os.path.exists(ARQUIVO_ESTADO):
        with open(ARQUIVO_ESTADO, "r", encoding="utf-8") as f:
            return json.load(f).get("indice_atual", 0)
    return 0

def salvar_indice():
    with open(ARQUIVO_ESTADO, "w", encoding="utf-8") as f:
        json.dump({"indice_atual": indice_atual}, f)

ofertas_ativas = carregar_ofertas()
indice_atual = carregar_indice()

# ---------- Comandos básicos ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        "Olá! Eu sou o bot de promoções. Use /ajuda pra ver os comandos.\n\n"
        f"Seu chat_id é: {chat_id}\n"
        "(guarde esse número — ele é usado no .env como ADMIN_CHAT_ID pra você receber alertas)"
    )

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponíveis:\n"
        "/start - inicia o bot e mostra seu chat_id\n"
        "/ajuda - mostra essa mensagem\n"
        "/novaoferta - cadastra uma oferta passo a passo\n"
        "/addoferta - cadastra uma oferta em uma linha só\n"
        "/addofertas - cadastra várias ofertas de uma vez\n"
        "/listaofertas - mostra as ofertas ativas no rodízio\n"
        "/removeroferta - remove uma oferta do rodízio pelo número\n"
        "/cancelar - cancela o cadastro em andamento"
    )

async def listar_ofertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ofertas_ativas:
        await update.message.reply_text("Nenhuma oferta ativa no momento.")
        return
    texto = "Ofertas ativas no rodízio:\n\n"
    for i, oferta in enumerate(ofertas_ativas):
        dias = calcular_dias_ativa(oferta)
        texto += f"{i + 1}. {oferta['nome']} (há {dias} dia(s))\n"
    await update.message.reply_text(texto)

async def remover_oferta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global indice_atual
    try:
        numero = int(context.args[0])
        removida = ofertas_ativas.pop(numero - 1)
        if indice_atual >= len(ofertas_ativas) and len(ofertas_ativas) > 0:
            indice_atual = 0
        salvar_ofertas()
        salvar_indice()
        await update.message.reply_text(f"Removida: {removida['nome']}")
    except (IndexError, ValueError):
        await update.message.reply_text("Use: /removeroferta NUMERO (veja os números com /listaofertas)")

def montar_legenda(nome, preco_antigo, preco_promo, link):
    return (
        f"🔥 OFERTA!\n\n"
        f"📦 {nome}\n"
        f"<s>De: R$ {preco_antigo}</s>\n"
        f"💰 <b>Por: R$ {preco_promo}</b>\n"
        f"🔗 {link}"
    )

def data_hoje():
    return datetime.now(timezone.utc).isoformat()

def calcular_dias_ativa(oferta):
    data_cadastro_str = oferta.get("data_cadastro")
    if not data_cadastro_str:
        return "?"
    data_cadastro = datetime.fromisoformat(data_cadastro_str)
    diferenca = datetime.now(timezone.utc) - data_cadastro
    return diferenca.days

# ---------- /addoferta (uma linha só) ----------

async def addoferta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = " ".join(context.args)
    try:
        nome, preco_antigo, preco_promo, link, imagem = texto.split("|")
        ofertas_ativas.append({
            "nome": nome.strip(),
            "preco_antigo": preco_antigo.strip(),
            "preco_promo": preco_promo.strip(),
            "link": link.strip(),
            "imagem": imagem.strip(),
            "data_cadastro": data_hoje(),
        })
        salvar_ofertas()
    except ValueError:
        await update.message.reply_text(
            "Formato errado! Use:\n/addoferta Nome | Preço antigo | Preço promo | Link | URL da imagem"
        )
        return
    await update.message.reply_text(f"Oferta adicionada ao rodízio! ({len(ofertas_ativas)} ativas)")

# ---------- /addofertas (várias de uma vez) ----------

async def addofertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_completo = update.message.text.replace("/addofertas", "").strip()
    linhas = texto_completo.split("\n")
    adicionadas = 0
    erros = []

    for i, linha in enumerate(linhas, start=1):
        linha = linha.strip()
        if not linha:
            continue
        try:
            nome, preco_antigo, preco_promo, link, imagem = linha.split("|")
            ofertas_ativas.append({
                "nome": nome.strip(),
                "preco_antigo": preco_antigo.strip(),
                "preco_promo": preco_promo.strip(),
                "link": link.strip(),
                "imagem": imagem.strip(),
                "data_cadastro": data_hoje(),
            })
            adicionadas += 1
        except ValueError:
            erros.append(f"Linha {i}: formato inválido")

    if adicionadas > 0:
        salvar_ofertas()

    if erros:
        await update.message.reply_text("Alguns erros encontrados:\n" + "\n".join(erros))
    await update.message.reply_text(
        f"{adicionadas} oferta(s) adicionada(s)! ({len(ofertas_ativas)} ativas no total)"
    )

# ---------- /novaoferta (passo a passo, via conversa) ----------

async def novaoferta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Vamos criar uma nova oferta!\n\nQual o nome do produto?")
    return NOME

async def receber_nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["nome"] = update.message.text
    await update.message.reply_text("Qual o preço antigo? (só número, ex: 149,90)")
    return PRECO_ANTIGO

async def receber_preco_antigo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["preco_antigo"] = update.message.text
    await update.message.reply_text("Qual o preço promocional?")
    return PRECO_PROMO

async def receber_preco_promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["preco_promo"] = update.message.text
    await update.message.reply_text("Qual o link de afiliado?")
    return LINK

async def receber_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["link"] = update.message.text
    await update.message.reply_text("Qual a URL da imagem?")
    return IMAGEM

async def receber_imagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["imagem"] = update.message.text
    ofertas_ativas.append({
        "nome": context.user_data["nome"],
        "preco_antigo": context.user_data["preco_antigo"],
        "preco_promo": context.user_data["preco_promo"],
        "link": context.user_data["link"],
        "imagem": context.user_data["imagem"],
        "data_cadastro": data_hoje(),
    })
    salvar_ofertas()
    await update.message.reply_text(f"Oferta adicionada ao rodízio! ({len(ofertas_ativas)} ativas)")
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cadastro de oferta cancelado.")
    return ConversationHandler.END

# ---------- Job automático: roda em loop pelas ofertas ativas ----------

async def postar_proxima(context: ContextTypes.DEFAULT_TYPE):
    global indice_atual

    if not ofertas_ativas:
        return

    if indice_atual >= len(ofertas_ativas):
        indice_atual = 0

    oferta = ofertas_ativas[indice_atual]
    legenda = montar_legenda(
        oferta["nome"], oferta["preco_antigo"], oferta["preco_promo"], oferta["link"]
    )

    try:
        await context.bot.send_photo(
            chat_id=CANAL,
            photo=oferta["imagem"],
            caption=legenda,
            parse_mode="HTML"
        )
    except Exception as erro:
        print(f"[ERRO] Falha ao postar oferta '{oferta['nome']}' no canal: {erro}")
        # mesmo com erro, avança o índice para não travar sempre na mesma oferta quebrada

    indice_atual = (indice_atual + 1) % len(ofertas_ativas)
    salvar_indice()

# ---------- Job automático: alerta diário de ofertas antigas ----------

async def verificar_ofertas_antigas(context: ContextTypes.DEFAULT_TYPE):
    if not ADMIN_CHAT_ID:
        return  # sem chat_id configurado, não tem pra quem avisar

    antigas = []
    for i, oferta in enumerate(ofertas_ativas):
        dias = calcular_dias_ativa(oferta)
        if isinstance(dias, int) and dias >= DIAS_ALERTA:
            antigas.append((i + 1, oferta["nome"], dias))

    if not antigas:
        return

    texto = (
        f"⚠️ Estas ofertas estão ativas há {DIAS_ALERTA}+ dias.\n"
        f"Confira se ainda são válidas (estoque, preço, promoção ativa):\n\n"
    )
    for numero, nome, dias in antigas:
        texto += f"{numero}. {nome} — há {dias} dia(s)\n"
    texto += "\nUse /removeroferta NUMERO para tirar do rodízio quem já não vale mais."

    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=texto)
    except Exception as erro:
        print(f"[ERRO] Falha ao enviar alerta de ofertas antigas para ADMIN_CHAT_ID: {erro}")
        print("Verifique se ADMIN_CHAT_ID no .env/Variables está com o chat_id correto (obtido via /start).")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(CommandHandler("listaofertas", listar_ofertas))
    app.add_handler(CommandHandler("removeroferta", remover_oferta))
    app.add_handler(CommandHandler("addoferta", addoferta))
    app.add_handler(CommandHandler("addofertas", addofertas))

    conversa_oferta = ConversationHandler(
        entry_points=[CommandHandler("novaoferta", novaoferta)],
        states={
            NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_nome)],
            PRECO_ANTIGO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_preco_antigo)],
            PRECO_PROMO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_preco_promo)],
            LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_link)],
            IMAGEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_imagem)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )
    app.add_handler(conversa_oferta)

    app.job_queue.run_repeating(postar_proxima, interval=INTERVALO_SEGUNDOS, first=10)
    app.job_queue.run_repeating(verificar_ofertas_antigas, interval=86400, first=30)  # a cada 24h

    print(f"Bot rodando com {len(ofertas_ativas)} oferta(s) carregada(s)... (Ctrl+C pra parar)")
    app.run_polling()

if __name__ == "__main__":
    main()