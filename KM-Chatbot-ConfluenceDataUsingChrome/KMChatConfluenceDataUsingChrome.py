from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
#from chatterbot import ChatBot
#from chatterbot.trainers import ChatterBotCorpusTrainer

# Define your Confluence page title and the URL of the page
confluence_page_title = 'Your Page Title'
#confluence_page_url = 'https://your-confluence-instance.com/display/spacekey/Page+Title'
confluence_page_url = "https://xxxx"




# Create a Chrome WebDriver instance using webdriver_manager
driver = webdriver.Chrome(ChromeDriverManager().install())



# Navigate to the Confluence page URL
driver.get(confluence_page_url)

# Wait for the page to load (you may need to adjust the wait time)
driver.implicitly_wait(10)

# Get the page content using BeautifulSoup
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Extract relevant content from the Confluence page
# You may need to customize this based on your Confluence page structure
content = soup.find('div', class_='your-content-class').get_text()

# Create a chatbot
# chatbot = ChatBot('KMChatBot')

# Create a trainer and train the chatbot
# trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot with the Confluence content
# trainer.train([content])

# Chat with the chatbot
while True:
    user_input = input('You: ')
    if user_input.lower() == 'exit':
        break
  #   response = chatbot.get_response(user_input)
    print('KMChatBot:', content)

# Close the Chrome WebDriver instance
driver.quit()
