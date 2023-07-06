import csv
import requests
from bs4 import BeautifulSoup

# Function for scrapping additional information from a product URL
def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize variables
    description = ''
    asin = ''
    product_description = ''
    manufacturer = ''

    # Find and extract the desired information
    description_element = soup.find('div', {'id': 'productDescription'})
    if description_element:
        description = description_element.text.strip()
        asin_element = soup.find('th', string='ASIN')
        if asin_element:
            asin = asin_element.find_next('td').text.strip()
        product_description_element = description_element.find_next('p')
        if product_description_element:
            product_description = product_description_element.text.strip()
        manufacturer_element = soup.find('th', string='Manufacturer')
        if manufacturer_element:
            manufacturer = manufacturer_element.find_next('td').text.strip()

    return description, asin, product_description, manufacturer

# Function to scrape product information from a given URL
def scrape_product_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    scraped_data = []
    for product in products:
        product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
        product_name = product.find('span', {'class': 'a-size-medium'}).text.strip()
        product_price = product.find('span', {'class': 'a-price-whole'}).text.strip()
        rating = product.find('span', {'class': 'a-icon-alt'}).text.strip()
        review_count = product.find('span', {'class': 'a-size-base'}).text.strip()

        # Scrapping additional information from the product URL
        description, asin, product_description, manufacturer = scrape_product_details(product_url)

        scraped_data.append([product_url, product_name, product_price, rating, review_count, description, asin, product_description, manufacturer])

    return scraped_data

# Main function
def main():
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'
    num_pages = 20

    all_data = []
    for page in range(1, num_pages + 1):
        url = base_url.format(page)
        print('Scraping page:', page)
        data = scrape_product_info(url)
        all_data.extend(data)

    # Save data to CSV file
    header = ['URL', 'Product Name', 'Product Price', 'Rating', 'Review Count', 'Description', 'ASIN', 'Product Description', 'Manufacturer']
    with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(all_data)

    print('Scraped data saved to scraped_data.csv')


if __name__ == '__main__':
    main()
