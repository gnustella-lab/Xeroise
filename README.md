# 🤖 Xeroise - Discord AI Selfbot

Xeroise é um selfbot de Discord escrito em Python usando a biblioteca `discord.py-self`. Ela responde automaticamente quando alguém menciona a palavra-gatilho (o nome "Xeroise") ou responde a ela, e sustenta conversas usando modelos de IA via Groq ou OpenAI. Funciona numa conta real do Discord, então outras pessoas conseguem conversar com ela em DMs, servidores e group chats sem precisar convidar um bot, parecendo uma pessoa de verdade.

A personalidade padrão da Xeroise é uma garota de 18 anos entusiasta de tecnologia, que conversa de forma casual e natural (em português) típica de um servidor do Discord. A personalidade vive em `config/instructions.txt` e pode ser editada livremente.

> ⚠️ **Aviso de TOS:** usar isso numa conta de usuário real viola os [Termos de Serviço do Discord](https://discord.com/terms) e pode levar a ban da conta em casos raros. Use por sua conta e risco, de preferência numa conta que não se importe em perder.
>
> Eu não me responsabilizo por nenhuma ação tomada contra a sua conta pelo uso deste código aberto, nem por como os usuários o utilizam.

---

## ✨ O que a Xeroise faz

- **Selfbot no Discord:** roda numa conta real, sem precisar convidar bot pra lugar nenhum.
- **Persona configurável:** edite `config/instructions.txt` para a IA agir do jeito que quiser. A persona padrão é a Xeroise (18 anos, nerd de tech, fala PT-BR casual).
- **Sem emojis (por padrão):** a persona proíbe emojis e, pra garantir, o código remove qualquer emoji da resposta no pós-processamento (`utils/sanitize.py`). O modelo não consegue desobedecer.
- **Limite de tokens:** `config.yaml` tem `max_tokens` (padrão 400) que limita o tamanho de cada resposta e o uso da API.
- **Reconhecimento de menção e de gatilho:** responde quando mencionada, quando respondem a ela, ou quando a palavra-gatilho aparece.
- **Conversa contínua:** se `hold_conversation` estiver ligado, ela continua o papo mesmo sem gatilho, dentro de um timeout.
- **Digitação realista:** com `realistic_typing`, ela "digita" por um tempo antes de enviar, parecendo uma pessoa de verdade.
- **Reconhecimento de imagem:** consegue "ver" imagens anexadas e responder dentro da persona.
- **Respostas por canal:** use `~toggleactive` para escolher em quais canais ela responde.
- **Anti-spam:** tem proteção embutida contra abuso por flood.
- **Comando de psicanálise:** `~analyse` analisa o histórico de um usuário e "perfila" a personalidade (só pra diversão).
- **Credenciais seguras:** tokens e chaves de API ficam em `config/.env` (que não é versionado).

---

## 🤖 Comandos

Todos os comandos usam o prefixo `~` (configurável em `config.yaml`). Apenas o `owner_id` pode usar a maioria deles.

| Comando | Descrição |
| --- | --- |
| `~pause` | Pausa/despausa as respostas de IA da Xeroise |
| `~analyse [user]` | Analisa o histórico de mensagens de um usuário e dá um perfil "psicológico" (diversão) |
| `~wipe` | Limpa o histórico de mensagens da Xeroise (memória) |
| `~ping` | Mostra a latência do bot |
| `~toggleactive [channel]` | Ativa/desativa o canal atual (ou um ID/canal mencionado) na lista de canais ativos |
| `~toggledm` | Liga/desliga respostas em DMs |
| `~togglegc` | Liga/desliga respostas em group chats |
| `~ignore [user]` | Ignora ou libera um usuário |
| `~reload` | Recarrega todos os cogs e as instruções da persona |
| `~prompt [texto / clear]` | Visualiza, define ou limpa o prompt/instruções da IA |
| `~restart` | Reinicia o bot inteiro |
| `~shutdown` | Encerra o bot |

> Se `help_command_enabled` estiver `true` no `config.yaml`, qualquer um pode usar `~help` para ver a lista. Por padrão está desligado.

---

## 🛠️ Configuração

Tudo fica na pasta `config/`:

- **`config/.env`** - credenciais (não versionado):
  - `DISCORD_TOKEN` - token da sua conta do Discord
  - `GROQ_API_KEY` - chave da Groq (grátis). Se presente, é usada por padrão.
  - `OPENAI_API_KEY` - chave da OpenAI (opcional). Se presente e a da Groq ausente, usa OpenAI.
- **`config/config.yaml`** - ajustes do bot (modelo, trigger, canais, limites etc.)
- **`config/instructions.txt`** - a personalidade da IA (system prompt)

### Principais campos de `config.yaml`

```yaml
bot:
  owner_id: 123456789012345678   # seu ID de usuário (não o da conta do bot)
  prefix: "~"                    # prefixo dos comandos
  trigger: "Xeroise"             # palavra-gatilho que faz a Xeroise responder
  groq_model: "llama-3.3-70b-versatile"   # modelo usado se GROQ_API_KEY estiver setada
  openai_model: "gpt-4o"         # modelo usado se OPENAI_API_KEY estiver setada
  allow_dm: false                # responde em DMs?
  allow_gc: true                 # responde em group chats?
  realistic_typing: false        # "digita" antes de enviar?
  batch_messages: true           # aguarda mensagens em lote antes de responder
  batch_wait_time: 10.0          # segundos aguardando mensagens em lote
  hold_conversation: true        # continua o papo sem gatilho?
  anti_age_ban: true             # filtra números abaixo de 13 (medida anti-ban)
  help_command_enabled: false    # ~help disponível para todos?
  disable_mentions: true         # bloqueia menções @everyone/@here
  reply_ping: true               # dá ping ao responder?
  max_tokens: 400                # limite de tokens por resposta (custo/tamanho)
```

---

## ⭐ Como rodar

### 1. Clone o repositório

```bash
git clone https://github.com/gnustella-lab/Xeroise.git
cd Xeroise
```

### 2. Crie o ambiente e instale as dependências

Recomendado usar [uv](https://docs.astral.sh/uv/) (mais rápido e não precisa de sudo):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv bot-env
source bot-env/bin/activate
uv pip install -r requirements.txt
```

Ou, com o `venv` padrão do Python (precisa do pacote `python3-venv` instalado):

```bash
python3 -m venv bot-env
source bot-env/bin/activate
pip install -r requirements.txt
```

### 3. Preencha as credenciais

Copie o exemplo e edite com seus dados:

```bash
cp config/example.env config/.env
```

Abra `config/.env` e coloque:
- `DISCORD_TOKEN` - veja abaixo como pegar
- `GROQ_API_KEY` - pegue em https://console.groq.com/keys (grátis)

### 4. Ajuste o `config.yaml`

Edite `config/config.yaml` e defina pelo menos:
- `owner_id` - o seu ID de usuário do Discord
- `trigger` - a palavra que faz a Xeroise responder (padrão: `Xeroise`)

Na primeira execução, se faltar algum arquivo de config, um assistente interativo (`utils/setup.py`) pergunta tudo no terminal e cria os arquivos pra você.

### 5. Pegue seu token do Discord

- Entre no [Discord](https://discord.com) na conta que vai usar.
- Pressione `Ctrl + Shift + I` (Windows/Linux) ou `Cmd + Opt + I` (Mac).
- Vá na aba **Network**.
- Envie qualquer mensagem ou troque de servidor.
- Procure por uma requisição com nome `messages?limit=50`, `science` ou `preview` e clique nela.
- Role até achar **Authorization** em **Request Headers**; o valor é o seu token.

> Nunca compartilhe esse token. Ele dá acesso total à sua conta.

### 6. Rode a Xeroise

```bash
python3 main.py
```

Ela abre o console mostrando o login. Para que ela responda num servidor, use `~toggleactive` no canal desejado (sendo o owner). Em DMs/group chats, depende de `allow_dm`/`allow_gc` no `config.yaml`.

---

## 💭 Mudando a personalidade

Edite `config/instructions.txt` com o sistema de instruções que quiser e use `~reload` (ou reinicie o bot) para aplicar. A persona padrão é a Xeroise, mas nada te obriga a manter assim.

---

## 📂 Estrutura do projeto

```
Xeroise/
├── main.py                 # entrypoint, eventos do Discord e fila de mensagens
├── requirements.txt        # dependências
├── config/
│   ├── config.yaml         # ajustes do bot
│   ├── example.env         # modelo de credenciais
│   └── instructions.txt    # personalidade da IA (system prompt)
├── cogs/
│   ├── management.py        # comandos de dono (pause, toggle, ignore, etc.)
│   ├── error_handler.py     # tratamento de erros de comando
│   └── general.py           # comandos gerais (ping, help, analyse)
└── utils/
    ├── ai.py                # chamadas à API Groq/OpenAI (com max_tokens)
    ├── db.py                # banco SQLite de canais/usuários ignorados
    ├── helpers.py           # utilidades de caminho/config
    ├── sanitize.py          # remoção de emojis no pós-processamento
    ├── split_response.py    # quebra respostas longas em chunks
    ├── error_notifications.py # log de erros via webhook
    └── setup.py             # assistente de configuração interativo
```

---

## 🤝 Contribuindo

PRs são bem-vindos. O repositório original é o [Discord-AI-Selfbot](https://github.com/Najmul190/Discord-AI-Selfbot) do Najmul190, do qual este projeto deriva.

> Lembre-se: selfbots ficam numa área cinzenta dos Termos de Serviço do Discord. Use com responsabilidade.
