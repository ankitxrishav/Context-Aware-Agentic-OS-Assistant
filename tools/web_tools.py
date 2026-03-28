import re
from typing import Dict, Any, List

def scrape_website(url: str, selector: str = "body") -> str:
    """Navigates to a URL using a headless browser and extracts text from a CSS selector."""
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
        
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            # We launch headless Chromium
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            if selector and selector != "body":
                try:
                    page.wait_for_selector(selector, timeout=5000)
                except:
                    # If selector times out, fall back gracefully
                    pass
                
            elements = page.locator(selector).all_inner_texts()
            browser.close()
            
            if not elements:
                return f"No text found on '{url}' for selector '{selector}'."
                
            text_content = "\n".join(elements)
            # Remove excessive whitespace to save LLM context
            text_content = re.sub(r'\n\s*\n', '\n', text_content).strip()
            return f"🌐 Screen-Scraped DOM Data from {url} [Selector: {selector}]:\n{text_content[:2000]}..."
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

web_tools_schema = [
    {
        "name": "scrape_website",
        "description": "Navigates to a website using a headless Playwright browser to fetch live data (e.g., weather, public numbers, articles). Note: Cannot bypass CAPTCHAs or heavy Authentication walls without explicit cookies.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL of the website to scrape (e.g., 'https://en.wikipedia.org/wiki/India')."},
                "selector": {"type": "string", "description": "The CSS selector to target specific text (e.g., 'h1', '.main-content', '#attendance'). Defaults to 'body' if left empty."}
            },
            "required": ["url"]
        }
    }
]
