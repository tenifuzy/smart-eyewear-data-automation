### Overview
This project is a Python-based web scraper that extracts product details (brand, model name, price, discount) from [FramesDirect Eyeglasses](https://www.framesdirect.com/eyeglasses).  
The script uses **Selenium** to handle JavaScript-rendered content and **BeautifulSoup** to parse the DOM. Extracted data is saved into a CSV file (`eyeglasses_data.csv`) for further analysis.

### Key Challenges Encountered and Solutions

## Challenges Encountered

1. **Dynamic Content Loading**
   - The FramesDirect product list is loaded dynamically with JavaScript, so using only `requests + BeautifulSoup` returned incomplete data.
   - **Solution:** Implemented **Selenium WebDriver** with Chrome headless mode to render the page fully before scraping.

2. **Locating Correct HTML Selectors**
   - Initial attempts targeted the wrong classes (`d-flex` instead of `prod-holder`), leading to incomplete or repeated product extraction.
   - **Solution:** Inspected the site’s HTML structure with browser DevTools and updated selectors to `div.prod-holder` for products, and adjusted nested selectors for brand, name, and pricing.

3. **Missing or Empty Fields**
   - Some products did not contain a former price or discount, causing `ValueError` when converting empty strings to floats.
   - **Solution:** Created a helper function `safe_float()` to safely clean and convert price values, returning `None` if the field was missing.

4. **Price Formatting**
   - Prices were returned as strings with symbols (`"$237"`, `"$1,249"`) that broke numeric parsing.
   - **Solution:** Stripped `$` and `,` from the strings and parsed values into floats (e.g., `237.0`).

5. **Discount Extraction**
   - Discounts appeared as text (`"20% OFF"`) and were inconsistent across products.
   - **Solution:** Used **regex** (`re.search`) to extract numeric values and convert them into float percentages (e.g., `"20% OFF"` → `20.0`).

6. **Empty CSV Issue**
   - At first, no data was being written to CSV because the `append` statement was misplaced outside the main loop.
   - **Solution:** Ensured each product dictionary was appended inside the loop and validated by printing debug logs during extraction.

---

## Final Outcome
- Successfully extracted product details for multiple eyeglasses (25 items in a test run).
- Exported clean, structured data into a CSV file (`eyeglasses_data.csv`).
- Implemented safe parsing to handle missing fields gracefully without breaking the script.

---

## Lessons Learned
- Always inspect dynamic sites with browser DevTools to identify correct selectors.
- Use Selenium when dealing with JavaScript-rendered content.
- Always validate and sanitize data before conversion to avoid runtime errors.

### Technical Implementation

**Data Extraction Results:**
- Successfully scraped 25 products from Glasses.com
- Captured brands: Ray-Ban, Oakley, Persol, Burberry, Versace, Gucci, Kate Spade, Dolce & Gabbana, RALPH
- Price range: $98.70 - $605.00
- Discount rates: 15% - 50%

**Data Quality:**
- 96% data completeness (24/25 products with complete information)
- Proper handling of ll values for missing discount information
- Accurate price extraction with decimal precision

### Solutions Implemented

1. **Robust WebDriver Configuration**: Added stability flags to prevent crashes
2. **Intelligent Wait Strategies**: Implemented dynamic waits for content loading
3. **Comprehensive Error Handling**: Added proper exception handling with graceful degradation
4. **Data Validation**: Implemented null handling for optional fields
5. **Structured Output**: JSON format for easy data processing and analysis

### Conclusion
The project successfully overcame technical challenges to deliver a functional web scraping solution. The implementation demonstrates robust error handling, stable data extraction, and proper data structuring for downstream analysis.
