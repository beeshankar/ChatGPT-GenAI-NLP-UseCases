import requests
from bs4 import BeautifulSoup
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Define your Confluence base URL and password
CONFLUENCE_BASE_URL = 'https://your-confluence-instance.com'
PASSWORD = 'your-password'  # Replace with your Confluence password

# Define the username
USERNAME = 'name1@xyz.com'

# Create a session for API requests
session = requests.Session()

# Log in to Confluence
login_url = f'{CONFLUENCE_BASE_URL}/rest/auth/1/session'
login_data = {
    'username': USERNAME,
    'password': PASSWORD
}
login_response = session.post(login_url, json=login_data)

# Add a delay (e.g., 2 seconds) after sending the login request
time.sleep(2)

# Check if login was successful
if login_response.status_code != 200:
    print('Login failed. Check your credentials.')
else:
    print('Login successful.')

    # Fetch a list of all Confluence spaces
    spaces_url = f'{CONFLUENCE_BASE_URL}/rest/api/space'
    spaces_response = session.get(spaces_url)

    if spaces_response.status_code == 200:
        spaces_data = spaces_response.json()

        # Iterate through each space and fetch pages
        for space in spaces_data['results']:
            space_key = space['key']
            space_name = space['name']
            
            # Fetch pages in the current space
            pages_url = f'{CONFLUENCE_BASE_URL}/rest/api/space/{space_key}/content/page'
            pages_response = session.get(pages_url)

            if pages_response.status_code == 200:
                pages_data = pages_response.json()

                # Iterate through pages in the current space
                for page in pages_data['results']:
                    page_title = page['title']
                    page_id = page['id']
                    
                    # Fetch content for the current page
                    page_url = f'{CONFLUENCE_BASE_URL}/content/{page_id}?expand=body.view'
                    page_response = session.get(page_url)

                    if page_response.status_code == 200:
                        page_data = page_response.json()
                        content = page_data['body']['view']['value']

                        # Create a chatbot for this page
                        chatbot = ChatBot(f'KMChatBot - {space_name} - {page_title}')

                        # Create a trainer and train the chatbot with the page content
                        trainer = ChatterBotCorpusTrainer(chatbot)
                        trainer.train([content])

                        # Chat with the chatbot
                        while True:
                            user_input = input(f'You ({space_name} - {page_title}): ')
                            if user_input.lower() == 'exit':
                                break
                            response = chatbot.get_response(user_input)
                            print(f'KMChatBot - {space_name} - {page_title}:', response)
    else:
        print('Failed to fetch the list of Confluence spaces.')

    # Logout (optional)
    logout_url = f'{CONFLUENCE_BASE_URL}/rest/auth/1/session'
    session.delete(logout_url)

    # Close the session
    session.close()
