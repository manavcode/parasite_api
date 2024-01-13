from bs4 import BeautifulSoup
import requests

def read_file():
    with open("sample.html", "r", encoding="utf-8") as file:
        data = file.read()

    return data

def extract_interactive_elements(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # remove unwanted elements like images
    for element in soup(['img', 'svg']):  
        element.decompose()

    # interactive elements like buttons and forms
    interactive_elements = soup.find_all(['button'])  

    # Combine 
    combined_output = ' '.join(str(element) for element in interactive_elements)

    return combined_output


def parse_gpt_response(response):
    soup = BeautifulSoup(response, 'html.parser')

    all_tags = soup.find_all()

    # tags and attributes
    tag_info_list = []
    for tag in all_tags:
        tag_info = {
            "tag_name": tag.name,
            "attributes": tag.attrs
        }
        tag_info_list.append(tag_info)

    
    return tag_info_list

def get_html(url):
    try:
        # Make a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Parse the HTML content
        html_content = response.content

        return html_content

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None