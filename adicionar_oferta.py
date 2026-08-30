import requests

TOKEN = "8775146830:AAHGlfBCoRwmHBQxRFJiCejTePH8dHimEzk"
CANAL = "@cafe_ofertas"

def enviar_oferta(nome, preco_antigo, preco_promo, link, imagem):
    legenda = (
        f"🔥 OFERTA!\n\n"
        f"📦 {nome}\n"
        f"<s>De: R$ {preco_antigo}</s>\n"
        f"💰 <b>Por: R$ {preco_promo}</b>\n"
        f"🔗 {link}"
    )

    url = f"https://api.telegram.org/bot{8775146830:AAHGlfBCoRwmHBQxRFJiCejTePH8dHimEzk}/sendPhoto"
    dados = {
        "chat_id": CANAL,
        "photo": imagem,
        "caption": legenda,
        "parse_mode": "HTML"
    }
    resposta = requests.post(url, data=dados)
    return resposta.json()

def main():
    print("=== Nova oferta ===")
    nome = input("Nome do produto: ")
    preco_antigo = input("Preço antigo (só número, ex: 149,90): ")
    preco_promo = input("Preço promocional (só número): ")
    link = input("Link de afiliado: ")
    imagem = input("URL da imagem: ")

    resultado = enviar_oferta(nome, preco_antigo, preco_promo, link, imagem)

    if resultado.get("ok"):
        print("\n✅ Oferta postada com sucesso!")
    else:
        print("\n❌ Erro ao postar:", resultado)

if __name__ == "__main__":
    main()