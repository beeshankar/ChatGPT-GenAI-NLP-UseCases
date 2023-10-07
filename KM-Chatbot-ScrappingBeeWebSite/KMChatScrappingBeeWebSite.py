import requests
from bs4 import BeautifulSoup
from scrapingbee import ScrapingBeeClient
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

api_key = 'your-key'  # Replace with your ScrapingBee API key
chatbot = ChatBot('WebScrapingBot')
trainer = ChatterBotCorpusTrainer(chatbot)

def scrape_js_website(url):
    scrapingbee_client = ScrapingBeeClient(api_key)

    # Set up the ScrapingBee API parameters
    params = {
        'extract_rules': {"text": "body"},
    }

    # Send the request to ScrapingBee API
    response = scrapingbee_client.get(url, params)
    print('Response HTTP Status Code:', response.status_code)

    # Extract the text from the main content
    text = response.content.get_text(separator=' ')
    return text

# Example usage
url = "https://support.atlassian.com/confluence-cloud/docs/share-content-externally-with-public-links/"
scraped_text = scrape_js_website(url)

# Train the chatbot using the scraped text
trainer.train('chatterbot.corpus.english')  # Train with English language data
trainer.train(scraped_text)  # Train with the scraped text

# Start a conversation with the chatbot
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    response = chatbot.get_response(user_input)
    print("Bot:", response)
