## Scrap Data from Amazon
Extract Product information from Amazon. 

GitHub Repo: [https://github.com/sannjayy/python_amazon_scraper](https://github.com/sannjayy/python_amazon_scraper)
### Installaion
Do the following in your virtualenv:

`pip install python_amazon_scraper`

**Import:**
```
from python_amazon_scraper import ExtractAmazon
```
---
**Minimal Code Example:**
```
from python_amazon_scraper import ExtractAmazon
url = 'AMAZON PRODUCT URL'
product = ExtractAmazon(url)

print("Product Title = ", product.get_title())
print("Product Price = ", product.get_price())
print("Availability = ", product.is_available())
print("Has Deal = ", product.has_deal())

print("Product Images = ", product.get_images())
```

---

**DEMO OUTPUT:**


```
Product Title = Apple iPhone 12 (64GB) - Purple
Product Price = Not Available
Availability = False
Has Deal = False

Product Images = ['https://m.media-amazon.com/images/I/31jQ91XUDhS._SY445_SX342_QL70_FMwebp_.jpg']
```

---

[![](https://img.shields.io/github/followers/sannjayy?style=social)](https://github.com/sannjayy)  
Developed by *Sanjay Sikdar*.   
- 📫 me@sanjaysikdar.dev



