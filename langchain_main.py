from scrape_lang_GPT import *

# Setup environment variables
from dotenv import load_dotenv

def main():
    # import API key
    load_dotenv()

    # Parse query through google browser
    g_query = "CISSP certification passing rate"

    #TODO: Define the chunk size, etc. here
    #TODO: Iterate it for every url in g_query. If not a webpage, go to next url. Or if cannot find, go to next url. Try catch errors
    #TODO: Clean main() some stuff can be shifted to the functions
    # url you would like to scrape. worked for 4th url [3]
    url = find_urls(g_query)[3]

    # question and system prompt you have for GPT
    question = 'What is the passing rate?'
    system = 'Use the provided articles delimited by triple quotes to answer questions. If the answer cannot be found in the articles, write "I could not find an answer."'
    # system = ''

    # call function to scrape HTML and save as .txt
    scrape_html_only(url)

    # query for GPT
    query = '\n' + system + '\n' + '\n' + '"""' + '\n' + scrape_html_only(url) + '\n' + '"""' + '\n' + '\n' + 'Question: ' + question + '\n'

    # GPT's response
    langchain_response(query)

main()