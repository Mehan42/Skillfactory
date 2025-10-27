from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_forgot_password_element():
    """Find the forgot password element using the cached driver"""
    options = Options()
    options.add_argument("--start-maximized")
    
    # Use the cached driver directly
    service = Service("/home/uss/.wdm/drivers/geckodriver/linux64/v0.36.0/geckodriver")
    driver = webdriver.Firefox(service=service, options=options)
    
    try:
        logger.info("Opening Rostelecom passport page...")
        driver.get("https://b2c.passport.rt.ru/")
        
        # Wait for page to load
        time.sleep(5)
        
        # First, let's try the original ID we identified
        try:
            forgot_element = driver.find_element(By.ID, "forgot_password")
            print(f"FOUND by ID 'forgot_password': {forgot_element.tag_name} | {forgot_element.text}")
        except:
            print("Element not found by ID 'forgot_password'")
        
        # Now try a broader search for text containing "Забыл" (Forgot)
        xpath_patterns = [
            "//a[contains(text(), 'Забыл')]",
            "//span[contains(text(), 'Забыл')]",
            "//div[contains(text(), 'Забыл')]",
            "//button[contains(text(), 'Забыл')]",
            "//a[contains(text(), 'Forgot')]",
            "//span[contains(text(), 'Forgot')]",
            "//div[contains(text(), 'Forgot')]",
            "//button[contains(text(), 'Forgot')]"
        ]
        
        print("\nTrying XPath patterns:")
        for i, xpath in enumerate(xpath_patterns):
            try:
                elements = driver.find_elements(By.XPATH, xpath)
                if elements:
                    print(f"\nPattern {i+1} '{xpath}' found {len(elements)} element(s):")
                    for j, elem in enumerate(elements):
                        print(f"  {j+1}. Tag: {elem.tag_name}, Text: '{elem.text}', ID: {elem.get_attribute('id')}, Class: {elem.get_attribute('class')}, Href: {elem.get_attribute('href')}")
            except Exception as e:
                print(f"Pattern {i+1} '{xpath}' failed: {str(e)}")
        
        # Find all links on the page
        all_links = driver.find_elements(By.TAG_NAME, "a")
        print(f"\nFound {len(all_links)} links on the page")
        forgot_like_links = [link for link in all_links if "забыл" in link.text.lower() or "forgot" in link.text.lower()]
        
        if forgot_like_links:
            print(f"\nFound {len(forgot_like_links)} links with 'forgot' in text:")
            for i, link in enumerate(forgot_like_links):
                print(f"  {i+1}. Text: '{link.text}', ID: {link.get_attribute('id')}, HREF: {link.get_attribute('href')}, Class: {link.get_attribute('class')}")
        else:
            print("\nNo links with 'forgot' in text found.")
            # Show first 10 links to see what's available
            print("\nFirst 10 links on the page:")
            for i, link in enumerate(all_links[:10]):
                print(f"  {i+1}. Text: '{link.text}', ID: {link.get_attribute('id')}, HREF: {link.get_attribute('href')}")
        
        # Find all clickable elements that might be the forgot password
        clickable_elements = driver.find_elements(By.XPATH, "//a | //button | //span | //div")
        clickables_with_forgot = []
        
        for element in clickable_elements:
            text = element.text.lower()
            if "забыл" in text or "forgot" in text or "парол" in text.lower():
                clickables_with_forgot.append(element)
        
        print(f"\nFound {len(clickables_with_forgot)} clickable elements with 'forgot', 'password', or 'parol' in text:")
        for i, elem in enumerate(clickables_with_forgot):
            print(f"  {i+1}. Tag: {elem.tag_name}, Text: '{elem.text}', ID: {elem.get_attribute('id')}, Class: {elem.get_attribute('class')}")
        
        # Try to find by class names that might contain "forgot"
        class_patterns = ["*forgot*", "*password*", "*pass*"]
        for pattern in class_patterns:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, f"[class*='{pattern.replace('*', '')}']")
                if elements:
                    print(f"\nElements with '{pattern}' in class name: {len(elements)}")
                    for i, elem in enumerate(elements):
                        print(f"  {i+1}. Tag: {elem.tag_name}, Text: '{elem.text}', ID: {elem.get_attribute('id')}, Class: {elem.get_attribute('class')}")
            except:
                pass
        
    except Exception as e:
        logger.error(f"Error during inspection: {str(e)}")
    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    find_forgot_password_element()