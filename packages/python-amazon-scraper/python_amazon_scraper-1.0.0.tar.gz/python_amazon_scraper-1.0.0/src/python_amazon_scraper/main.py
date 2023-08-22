import requests
from bs4 import BeautifulSoup as bs

headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

class ExtractAmazon:
    def __init__(self, url):
        url = url
        page = requests.get(url, headers=headers)
        soup = bs(page.content, "lxml")
        self.soup = soup

    # Function to extract Product Title
    def get_title(self):
        try:
            title = self.soup.find("span", attrs={"id":'productTitle'})
            title_string = title.string.strip()

        except AttributeError:
            title_string = ""	
            
        return title_string

    # Function to extract Product Price
    def get_price(self):
        try:
            price = self.soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

        except AttributeError:          
            try:
                price_tag = self.soup.select_one("#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-whole")
                price = price_tag.string.strip()
            except Exception:
                price =''	

        return price

    # Function to extract Product Rating
    def get_rating(self):
        try:
            rating = self.soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
        except AttributeError:
            try:
                rating = self.soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
            except Exception:
                rating = ""	

        return rating

    # Function to extract Number of User Reviews
    def get_review_count(self):
        try:
            review_count = self.soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
            
        except AttributeError:
            review_count = ""	

        return review_count

    # Function to extract Availability Status
    def is_available(self):
        try:
            available = self.soup.find("div", attrs={'id':'availability'})
            available = available.find("span").string.strip()
            return available == 'In stock'

        except AttributeError:
            return False	
        
    # Function to extract images 
    def get_images(self):
        try:
            images = self.soup.find("div", attrs={'id':'imgTagWrapperId'}).find('img')
            image_src = images['src']
            # FIXME: FETCH ALL IMAGES
            return [image_src]
        except AttributeError as e:
            return False
    
    # Function to extract deal badge
    def has_deal(self, get_regular_price=False):
        try:
            deal_span = self.soup.select_one('#dealBadgeSupportingText')
            # inner_span = deal_span.find('span')
            if get_regular_price:
                try:
                    regular_price = self.soup.select_one('#corePrice_feature_div > div > div > span.a-price.a-text-normal.aok-align-center.reinventPriceAccordionT2 > span:nth-child(2) > span.a-price-whole')   
                    return regular_price.contents[0]
                
                except Exception:
                    return bool(deal_span)
                
            return bool(deal_span)
        
        except AttributeError:
            return False
