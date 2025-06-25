
# 🚗 OLX Car Cover Scraper (Selenium)

A Python-based web scraper that extracts listings of **car covers** from [OLX India](https://www.olx.in) using **Selenium WebDriver**. The scraper collects titles, prices, locations, dates, product links, and image URLs, and stores them in a CSV file.

---

## 📌 Features

- Headless and GUI browser support
- Handles popups and anti-bot measures
- Uses multiple CSS selectors for resilience against layout changes
- Scrolls and waits for dynamic content to load
- Parses multiple pages (pagination supported)
- Saves structured data in CSV format
- Logs detailed scraping progress and results

---

## 🛠️ Requirements

- Python 3.7+
- Google Chrome browser
- ChromeDriver (auto-installed or manually)

### Python Packages

Install dependencies using:

```bash
pip install -r requirements.txt
```

**requirements.txt**
```
selenium
```

> Optionally, use `chromedriver-autoinstaller` to auto-manage the ChromeDriver version:
```bash
pip install chromedriver-autoinstaller
```

---

## 🚀 Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/olx-car-cover-scraper.git
   cd olx-car-cover-scraper
   ```

2. Run the scraper:
   ```bash
   python scraper.py
   ```

   > To **see the browser UI**, open `scraper.py` and set:
   ```python
   scraper = OLXSeleniumScraper(headless=False)
   ```

3. Output file:
   - Scraped data is saved to `olx_car_covers.csv`
   - Debug HTML pages are saved as `debug_page_1.html`, etc. (if listings fail to load)

---

## 📁 Output Format (`olx_car_covers.csv`)

| Title | Price | Location | Date | Link | Image URL |
|-------|-------|----------|------|------|------------|
| "Premium Car Cover" | ₹499 | Delhi | 2 days ago | https://olx.in/... | https://img.olx.in/... |

---

## 🧠 Troubleshooting

- ❌ **No listings found?**
  - Website structure may have changed — inspect element and update selectors
  - Try setting `headless=False` to visually debug
  - OLX may be blocking scrapers — consider rotating IPs or using proxies

- ❌ **WebDriver errors?**
  - Make sure ChromeDriver matches your Chrome version
  - Download from: [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Navneet Tewatia**  
[LinkedIn](https://www.linkedin.com/in/navneettewatia/) | [GitHub](https://github.com/navneet-97)

---

## 🙌 Contributions

Feel free to fork and submit PRs or raise issues if you’d like to improve the scraper. Open to suggestions and collaborations!"# OLX-Car-Cover-Scraper" 
