from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import csv
import time
import random
from urllib.parse import urljoin
import sys
import os

class OLXSeleniumScraper:
    def __init__(self, headless=True):
        self.base_url = "https://www.olx.in"
        self.search_url = "https://www.olx.in/items/q-car-cover"
        self.headless = headless
        self.driver = None
        self.wait = None
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Disable images to speed up loading
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            # Try to initialize the driver
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.wait = WebDriverWait(self.driver, 10)
            print("Chrome WebDriver initialized successfully")
            
        except WebDriverException as e:
            print(f"Error initializing Chrome WebDriver: {e}")
            print("\nTroubleshooting steps:")
            print("1. Make sure Chrome browser is installed")
            print("2. Install ChromeDriver: pip install chromedriver-autoinstaller")
            print("3. Or download ChromeDriver from: https://chromedriver.chromium.org/")
            sys.exit(1)
    
    def get_page(self, url, retries=3):
        """Navigate to page with retry mechanism"""
        for attempt in range(retries):
            try:
                print(f"Loading: {url} (Attempt {attempt + 1})")
                self.driver.get(url)
                
                # Wait for page to load
                time.sleep(random.uniform(3, 5))
                
                # Check if page loaded properly
                if "olx.in" in self.driver.current_url.lower():
                    print("Page loaded successfully")
                    return True
                else:
                    print("Page might not have loaded correctly")
                    
            except Exception as e:
                print(f"Error loading {url}: {e}")
                if attempt < retries - 1:
                    time.sleep(random.uniform(5, 8))
                else:
                    return False
        return False
    
    def wait_for_listings(self):
        """Wait for listings to load on the page"""
        try:
            # Wait for at least one listing to be present
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li[data-aut-id='itemBox3'], [data-aut-id='itemBox']"))
            )
            return True
        except TimeoutException:
            print("Timeout waiting for listings to load")
            return False
    def handle_popups(self):
        """Handle common popups that might appear"""
        try:
            # Wait a bit for popups to appear
            time.sleep(2.5)
            
            # Try to close location popup
            location_buttons = [
                "[data-aut-id='btnLocationAllow']",
                "[data-aut-id='btnLocationDeny']",
                "button[data-aut-id='btnLocationAllow']",
                "button[data-aut-id='btnLocationDeny']"
            ]
            
            for selector in location_buttons:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        elements[0].click()
                        print("Closed location popup")
                        time.sleep(1)
                        break
                except:
                    continue
                    
            close_selectors = [
                ".close",
                ".modal-close", 
                "[aria-label='Close']",
                "button[aria-label='Close']",
                ".rui-vV2ld",
                "[data-aut-id='close']"
            ]
            
            for selector in close_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            element.click()
                            time.sleep(1)
                            break
                except:
                    continue
                    
        except Exception as e:
            print(f"Note: Could not handle popups: {e}")
    
    def scroll_page(self):
        """Scroll page to load more content"""
        try:
            # Scroll down slowly to load dynamic content
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        except Exception as e:
            print(f"Error scrolling page: {e}")
    
    def parse_listing(self, listing_element):
        """Parse individual listing element"""
        try:
            listing_data = {}
            
            # Title - updated selectors based on OLX structure
            title_selectors = [
                "[data-aut-id='itemTitle']",
                "span[data-aut-id='itemTitle']",
                ".rui-2Pidb span",
                "._1TqQb ._18Mg3",
                "._18Mg3"
            ]
            
            title_text = "N/A"
            for selector in title_selectors:
                try:
                    title_elem = listing_element.find_element(By.CSS_SELECTOR, selector)
                    title_text = title_elem.text.strip()
                    if title_text:
                        break
                except:
                    continue
            listing_data['title'] = title_text
            
            # Price - updated selectors based on OLX structure
            price_selectors = [
                "[data-aut-id='itemPrice']",
                "span[data-aut-id='itemPrice']",
                ".rui-ANaKy span",
                "._2oe2Z ._2pwN6",
                "._2pwN6"
            ]
            
            price_text = "N/A"
            for selector in price_selectors:
                try:
                    price_elem = listing_element.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_elem.text.strip()
                    if price_text and "₹" in price_text:
                        break
                except:
                    continue
            listing_data['price'] = price_text
            
            # Location - try multiple selectors
            location_selectors = [
                "[data-aut-id='item-location']",
                ".rui-1BHbr span",
                "span[color='#7F7F7F']"
            ]
            
            location_text = "N/A"
            for selector in location_selectors:
                try:
                    location_elem = listing_element.find_element(By.CSS_SELECTOR, selector)
                    location_text = location_elem.text.strip()
                    if location_text and any(char.isalpha() for char in location_text):
                        break
                except:
                    continue
            listing_data['location'] = location_text
            
            # Date - try multiple selectors
            date_selectors = [
                "[data-aut-id='item-date']",
                ".rui-1BHbr span:last-child",
                "span[color='#7F7F7F']:last-child"
            ]
            
            date_text = "N/A"
            for selector in date_selectors:
                try:
                    date_elem = listing_element.find_element(By.CSS_SELECTOR, selector)
                    date_text = date_elem.text.strip()
                    if date_text and ("day" in date_text.lower() or "hour" in date_text.lower() or "minute" in date_text.lower()):
                        break
                except:
                    continue
            listing_data['date'] = date_text
            
            # Link
            try:
                link_elem = listing_element.find_element(By.CSS_SELECTOR, "a")
                href = link_elem.get_attribute('href')
                if href:
                    listing_data['link'] = href if href.startswith('http') else urljoin(self.base_url, href)
                else:
                    listing_data['link'] = 'N/A'
            except:
                listing_data['link'] = 'N/A'
            
            # Image URL
            try:
                img_elem = listing_element.find_element(By.CSS_SELECTOR, "img")
                img_src = img_elem.get_attribute('src')
                listing_data['image_url'] = img_src if img_src else 'N/A'
            except:
                listing_data['image_url'] = 'N/A'
            
            if listing_data['title'] != 'N/A' or listing_data['price'] != 'N/A':
                return listing_data
            else:
                return None
                
        except Exception as e:
            print(f"Error parsing listing: {e}")
            return None
    
    def scrape_listings(self, max_pages=3):
        """Scrape car cover listings from OLX"""
        all_listings = []
        
        for page in range(1, max_pages + 1):
            if page == 1:
                url = self.search_url
            else:
                url = f"{self.search_url}?page={page}"
            
            print(f"\n--- Scraping page {page} ---")
            
            if not self.get_page(url):
                print(f"Failed to load page {page}")
                continue
            
            # Handle popups
            self.handle_popups()
            
            # Wait for listings to load
            if not self.wait_for_listings():
                print(f"No listings loaded on page {page}")
                continue
            
            # Scroll to load content
            self.scroll_page()
            
            # Find listing containers - updated based on actual OLX structure
            listing_selectors = [
                "li[data-aut-id='itemBox3']",
                "[data-aut-id='itemBox3']",
                "li[data-aut-id='itemBox']",
                "[data-aut-id='itemBox']",
                "li._1DNjT",
                "._1DNjT"
            ]
            
            listings = []
            for selector in listing_selectors:
                try:
                    listings = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if listings:
                        print(f"Found {len(listings)} listings using selector: {selector}")
                        break
                except Exception as e:
                    print(f"Selector {selector} failed: {e}")
                    continue
            
            if not listings:
                print(f"No listings found on page {page}")
                # Save page source for debugging
                with open(f"debug_page_{page}.html", "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                print(f"Page source saved to debug_page_{page}.html for inspection")
                continue
            
            print(f"Processing {len(listings)} listings...")
            
            for i, listing in enumerate(listings):
                try:
                    parsed_listing = self.parse_listing(listing)
                    if parsed_listing:
                        all_listings.append(parsed_listing)
                        print(f"  Parsed listing {i+1}: {parsed_listing['title'][:50]}...")
                except Exception as e:
                    print(f"  Error processing listing {i+1}: {e}")
                    continue
            
            # Random delay between pages
            if page < max_pages:
                delay = random.uniform(5, 8)
                print(f"Waiting {delay:.1f} seconds before next page...")
                time.sleep(delay)
        
        return all_listings
    
    def save_to_csv(self, listings, filename='olx_car_covers.csv'):
        """Save listings to CSV file"""
        if not listings:
            print("No listings to save")
            return
            
        fieldnames = ['title', 'price', 'location', 'date', 'link', 'image_url']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(listings)
        
        print(f"Saved {len(listings)} listings to {filename}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("Browser closed")

def main():
    scraper = None
    
    try:
        print("=== OLX Car Cover Scraper with Selenium ===")
        print("Initializing browser...")
        
        scraper = OLXSeleniumScraper(headless=True)
        
        print("Starting scraping process...")
        listings = scraper.scrape_listings(max_pages=3)
        
        if listings:
            print(f"\n=== SCRAPING COMPLETED ===")
            print(f"Total listings found: {len(listings)}")
            
            # Save to CSV
            scraper.save_to_csv(listings)
            
            # Print summary
            print("\n=== SUMMARY ===")
            print("Preview of scraped listings:")
            for i, listing in enumerate(listings[:5], 1):
                print(f"\n{i}. {listing['title']}")
                print(f"   Price: {listing['price']}")
                print(f"   Location: {listing['location']}")
                print(f"   Date: {listing['date']}")
                
            if len(listings) > 5:
                print(f"\n... and {len(listings) - 5} more listings")
        else:
            print("\nNo listings found. This might be due to:")
            print("1. OLX changing their website structure")
            print("2. Anti-bot measures")
            print("3. Network issues")
            print("4. Search query returning no results")
            
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()