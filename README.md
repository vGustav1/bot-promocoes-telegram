# Bot de Promoções para Telegram

Bot em Python que automatiza a publicação de ofertas de afiliado em um canal do Telegram, com rodízio contínuo e persistência de dados.

## Funcionalidades

- Cadastro de ofertas por comando único, em lote ou via conversa guiada
- Publicação com imagem, preço riscado e destaque para o valor promocional
- Rodízio automático: ofertas ativas são republicadas em loop, em intervalo configurável
- Persistência em arquivo — o estado sobrevive a reinícios do bot
- Alerta diário (privado) para ofertas ativas há muito tempo, evitando divulgar promoções expiradas
- Token e credenciais protegidos via variáveis de ambiente

## Tecnologias

- Python 3.10+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (incluindo `JobQueue`)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

## Pré-requisitos

- Python 3.10+
- Bot criado via [@BotFather](https://t.me/BotFather)
- Canal do Telegram com o bot adicionado como administrador

## Instalação

```bash
git clone https://github.com/SEU_USUARIO/bot-promocoes-telegram.git
cd bot-promocoes-telegram
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/macOS

pip install -r requirements.txt
cp .env.example .env
```

Preencha o `.env`:
