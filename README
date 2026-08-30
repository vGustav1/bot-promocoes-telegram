# 🔥 Bot de Promoções para Telegram

Bot em Python que automatiza a divulgação de ofertas de afiliado em um canal do Telegram. Permite cadastrar ofertas de três formas diferentes (comando único, lote, ou conversa guiada) e as publica automaticamente em rodízio, em um intervalo de tempo configurável.

Projeto criado como exercício prático de Engenharia de Software, aplicando conceitos de consumo de APIs, automação, tratamento de erros e boas práticas de segurança em código.

## 📋 Funcionalidades

- **Três formas de cadastrar uma oferta**: comando direto, lote (várias de uma vez) ou conversa passo a passo guiada pelo bot.
- **Publicação com foto**: cada oferta é postada como imagem com legenda formatada (preço antigo riscado, preço promocional em destaque).
- **Rodízio automático**: as ofertas cadastradas ficam ativas e são publicadas em loop, uma a cada X minutos (configurável), sem repetir a mesma oferta em sequência.
- **Gerenciamento das ofertas ativas**: comandos para listar e remover ofertas do rodízio.
- **Token protegido**: credenciais nunca ficam expostas no código-fonte, usando variáveis de ambiente.

## 🖼️ Exemplo de oferta publicada

```
🔥 OFERTA!

📦 Smartphone Samsung Galaxy A07 4G 256GB
De: R$ 1.427,00 (riscado)
💰 Por: R$ 789,90 (destaque)
🔗 [link de afiliado]
```//
(acompanhado da imagem do produto)

## 🛠️ Tecnologias utilizadas

- **Python 3.10+**
- [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot) — biblioteca para integração com a API do Telegram, incluindo o `JobQueue` para tarefas agendadas.
- [`python-dotenv`](https://github.com/theskumar/python-dotenv) — carregamento seguro de variáveis de ambiente.

## 📦 Pré-requisitos

- Python 3.10 ou superior instalado
- Uma conta no Telegram
- Um bot criado através do [@BotFather](https://t.me/BotFather)
- Um canal do Telegram (público ou privado) onde o bot tenha permissão de administrador para postar mensagens

## 🚀 Instalação e configuração

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/bot-promocoes-telegram.git
cd bot-promocoes-telegram
```

### 2. Crie e ative um ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Abra o arquivo `.env` recém-criado e preencha com seus dados:

```
TELEGRAM_BOT_TOKEN=seu_token_do_botfather_aqui
TELEGRAM_CANAL=@nome_do_seu_canal
INTERVALO_SEGUNDOS=300
```

- `TELEGRAM_BOT_TOKEN`: gerado pelo [@BotFather](https://t.me/BotFather) ao criar seu bot.
- `TELEGRAM_CANAL`: username do seu canal público (com @) ou o ID numérico caso seja privado.
- `INTERVALO_SEGUNDOS`: intervalo entre cada postagem do rodízio, em segundos (300 = 5 minutos).

> ⚠️ **Nunca compartilhe seu arquivo `.env` nem o token do bot.** O `.gitignore` deste projeto já está configurado para impedir que o `.env` seja enviado ao GitHub por engano.

### 5. Adicione o bot como administrador do seu canal

No Telegram, vá em **Configurações do canal → Administradores → Adicionar Admin**, procure seu bot pelo username e garanta que a permissão de "Postar mensagens" está ativada.

### 6. Rode o bot

```bash
python bot.py
```

Se tudo estiver certo, o terminal vai exibir `Bot rodando... (Ctrl+C pra parar)`.

## 💬 Comandos disponíveis

| Comando | Descrição |
|---|---|
| `/start` | Inicia a conversa com o bot |
| `/ajuda` | Lista todos os comandos disponíveis |
| `/novaoferta` | Cadastra uma oferta respondendo perguntas, uma de cada vez |
| `/addoferta` | Cadastra uma oferta em uma única linha |
| `/addofertas` | Cadastra várias ofertas de uma vez (uma por linha) |
| `/listaofertas` | Mostra todas as ofertas atualmente no rodízio |
| `/removeroferta` | Remove uma oferta do rodízio pelo número (veja com `/listaofertas`) |
| `/cancelar` | Cancela um cadastro de oferta em andamento |

### Formato do `/addoferta` e `/addofertas`

Cada oferta segue o formato abaixo, com os campos separados por `|`:

```
Nome do produto | Preço antigo | Preço promocional | Link de afiliado | URL da imagem
```

Exemplo:

```
/addoferta Fone Bluetooth JBL | 149,90 | 99,90 | https://meli.la/xxxxx | https://http2.mlstatic.com/imagem.webp
```

Para várias ofertas de uma vez com `/addofertas`, envie uma por linha:

```
/addofertas
Fone Bluetooth JBL | 149,90 | 99,90 | https://meli.la/xxxxx | https://http2.mlstatic.com/imagem1.webp
Carregador Turbo | 79,90 | 45,00 | https://meli.la/yyyyy | https://http2.mlstatic.com/imagem2.webp
```

> 💡 Não inclua o símbolo `R$` ao digitar os preços — o bot adiciona isso automaticamente na formatação da mensagem.

## 🔄 Como funciona o rodízio

Todas as ofertas cadastradas entram em uma lista ativa e permanecem nela até serem removidas manualmente com `/removeroferta`. A cada intervalo definido em `INTERVALO_SEGUNDOS`, o bot publica a próxima oferta da lista, e ao chegar no final, recomeça do início — criando um ciclo contínuo.

O tempo que uma mesma oferta leva para reaparecer depende da combinação entre o intervalo configurado e a quantidade de ofertas ativas:

```
tempo de retorno = INTERVALO_SEGUNDOS × quantidade de ofertas ativas
```

Por exemplo, com `INTERVALO_SEGUNDOS=300` (5 minutos) e 6 ofertas ativas, cada oferta reaparece a cada 30 minutos.


## 🗺️ Possíveis melhorias futuras

- [ ] Persistência das ofertas em arquivo/banco de dados
- [ ] Interface de administração via botões inline do Telegram, em vez de comandos de texto
- [ ] Suporte a categorias de produto e filtros
- [ ] Métricas de cliques por oferta
- [ ] Deploy automatizado em nuvem

## 📄 Licença

Este projeto é livre para uso e modificação.

---

Desenvolvido como projeto de estudo