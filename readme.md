# Simple Slack Q&A Chatbot

## Overview

This project implements a basic Q&A chatbot integrated with Slack. The chatbot uses a predefined set of questions and answers to respond to user queries. It's designed as a minimal viable product (MVP) to quickly deploy and gather user feedback before implementing more advanced features.

## Features

- Simple keyword-based matching for user queries
- Integration with Slack for direct messages and mentions
- Easy-to-update Q&A database using a JSON file
- Basic error handling and logging

## Prerequisites

- Python 3.7+
- A Slack workspace with permissions to add apps and bots
- Slack App with bot token and app-level token

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/simple-slack-qa-chatbot.git
   cd simple-slack-qa-chatbot
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install slack_bolt python-dotenv
   ```

4. Create a `.env` file in the project root with your Slack tokens:
   ```
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_APP_TOKEN=xapp-your-app-token
   ```

5. Update the `qa_data.json` file with your own Q&A pairs.

## Usage

1. Start the bot:
   ```
   python slack_bot.py
   ```

2. In Slack, invite the bot to a channel or start a direct message conversation.

3. Ask questions and receive answers based on the predefined Q&A data.

## Project Structure

- `slack_bot.py`: Main script for Slack integration
- `simple_chatbot.py`: Implementation of the SimpleChatbot class
- `qa_data.json`: JSON file containing predefined Q&A pairs
- `.env`: Environment file for storing Slack tokens (not tracked in git)

## Customization

To add or modify Q&A pairs, edit the `qa_data.json` file. The format is:

```json
{
  "questions": [
    {
      "question": "Your question here?",
      "answer": "Your answer here."
    },
    ...
  ]
}
```

## Future Improvements

- Implement more advanced natural language processing
- Integrate with external data sources
- Add a knowledge graph for more context-aware responses
- Implement RAG (Retrieval-Augmented Generation) for dynamic response generation
- Add user feedback mechanisms
- Implement analytics and performance tracking

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.