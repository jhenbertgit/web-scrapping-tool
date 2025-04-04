import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_dynamic_website(url, element_type, element_id, output_dir="output", output_file="scraped_data.txt"):
    """
    Scrapes a website with dynamically loaded content using Selenium and extracts text
    from specific HTML elements, saving the output to a specified directory.

    Args:
        url (str): The URL of the website to scrape.
        element_type (str): The HTML element type to target (e.g., 'p', 'div', 'h1').
        element_id (str): The ID of the HTML element to target.  If None, all elements
                           of element_type are scraped.
        output_dir (str, optional): The directory to save the output file. Defaults to "output".
        output_file (str, optional): The name of the file to save the scraped data.
                                      Defaults to "scraped_data.txt".

    Returns:
        None. Writes the scraped data to the specified output file.
    """
    try:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Configure Chrome options (headless mode)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (recommended for headless)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")  # Set User-Agent

        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=chrome_options)

        # Load the webpage
        driver.get(url)

        # Wait for the content to load (adjust the sleep time as needed)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "element"))  # wait for id="element" to be present
            )
        except:
             print("Timed out waiting for element")


        # Get the rendered HTML source code
        html = driver.page_source

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Find the target elements
        if element_id:
            elements = soup.find_all(element_type, id=element_id)
        else:
            elements = soup.find_all(element_type)

        # Create the full output file path
        output_path = os.path.join(output_dir, output_file)

        # Extract the text and write to a file
        with open(output_path, 'w', encoding='utf-8') as f:
            for element in elements:
                text = element.get_text(strip=True)  # Remove extra whitespace
                if text:  # Only write non-empty text
                    f.write(text + '\n\n')

        print(f"Successfully scraped data from {url} and saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        if 'driver' in locals():
            driver.quit()  # Ensure the driver is closed even if errors occur

# Example usage (replace with your actual URL and element details)
if __name__ == "__main__":
    target_url = "https://example.com"  # Replace with the URL you want to scrape
    target_element_type = "li"  # Replace with the HTML element you want to target (e.g., 'p', 'div')
    target_element_id = None  # Replace with the id of the element if it exists
    output_directory = "output" # Directory where the output file will be saved.

    scrape_dynamic_website(target_url, target_element_type, target_element_id, output_dir=output_directory)