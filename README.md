# TeleChatbot

TeleChatbot is a sophisticated Telegram chatbot designed to provide support and respond intelligently to inquiries regarding the Winter Seminar Series (WSS), an event hosted by Sharif University of Technology. The chatbot, named **Mahdi**, utilizes advanced natural language processing (NLP) powered by OpenAI's GPT-3.5 Turbo and document retrieval capabilities through FAISS and LangChain.

## Key Features

- **Telegram Integration**: Seamless interaction through Telegram, powered by pyTelegramBotAPI.
- **Intelligent Responses**: Employs OpenAI's GPT-3.5 Turbo via LangChain to deliver context-aware, accurate answers.
- **Context Management**: Maintains conversational state, enabling coherent dialogue.
- **Efficient Retrieval**: Uses FAISS vector stores for quick retrieval of relevant event details.
- **Rate Limiting**: Controls request frequency to enhance user experience and system stability.
- **Robust Error Handling**: Clear instructions for unsupported interactions.

## Project Structure

```
telechatbot/
├── bot.py                # Telegram bot initialization and message handling
├── chat.py               # Conversation handling, LangChain integration
├── rate_limiter.py       # Request frequency management
├── vectorize.py          # Dataset preprocessing into FAISS vector store
├── requirements.txt      # Python dependencies
└── datasets/
    ├── Q&A.txt           # Question-answer dataset
    └── WSS.txt           # Winter Seminar Series event information
```

## Installation

Follow these steps to set up TeleChatbot:

### Step 1: Clone the repository

```bash
git clone https://github.com/mahdif355/telechatbot.git
cd telechatbot
```

### Step 2: Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Prepare the datasets and vector store

```bash
python vectorize.py
```

## Configuration

Create a `.env` file in your project root and add:

```dotenv
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

Replace placeholders with your actual tokens from [Telegram Bot API](https://core.telegram.org/bots#3-how-do-i-create-a-bot) and [OpenAI](https://platform.openai.com).

## Usage

Launch the bot:

```bash
python bot.py
```

Interact with Mahdi on Telegram using the chatbot of @Mahdi_SMF_bot, you will see
- `/start`: Start interaction.
- `/ask`: Prompt Mahdi for event-related inquiries.

Mahdi will guide users through private chat interactions, enforcing rate limits and supporting clear, structured conversations.

## 🎬 Demo

## Demo

![Demo](./demo/demo.gif)


## Contributing

Your contributions are welcome! Please:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to your branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

TeleChatbot is open-source software licensed under the [MIT License](LICENSE).

## Contact

- **GitHub Issues**: [mahdif355/telechatbot](https://github.com/mahdif355/telechatbot/issues)
- **Email**: mahdifazeli94@gmail.com

---

**Disclaimer**: Responses from TeleChatbot depend on the accuracy and completeness of provided datasets and configured OpenAI models. Always confirm critical information with official event sources.

