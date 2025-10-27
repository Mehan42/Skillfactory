from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def inspect_page_elements():
    """Inspect the page to find correct selectors for Rostelecom elements"""
    options = Options()
    options.add_argument("--start-maximized")
    
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    
    try:
        logger.info("Opening Rostelecom passport page...")
        driver.get("https://b2c.passport.rt.ru/")
        
        # Wait for page to load
        time.sleep(10)
        
        # Take screenshot of the initial page
        driver.save_screenshot("screenshots/inspection_page_full.png")
        logger.info("Screenshot saved as inspection_page_full.png")
        
        print("=== Page Title ===")
        print(driver.title)
        
        print("\n=== Page URL ===")
        print(driver.current_url)
        
        # Get page source to analyze
        page_source = driver.page_source
        print(f"\nPage source length: {len(page_source)}")
        
        # Look for common element identifiers
        common_selectors = [
            {"name": "phone tab", "selectors": ["t-btn-tab-phone", "phone-tab", "tab-phone", "btn-phone"]},
            {"name": "email tab", "selectors": ["t-btn-tab-mail", "email-tab", "tab-mail", "btn-mail"]},
            {"name": "login tab", "selectors": ["t-btn-tab-login", "login-tab", "tab-login", "btn-login"]},
            {"name": "LS tab", "selectors": ["t-btn-tab-ls", "ls-tab", "tab-ls", "btn-ls"]},
            {"name": "forgot password", "selectors": ["forgot-password", "forgot", "password-forgot"]},
            {"name": "register", "selectors": ["kc-register", "register", "sign-up"]},
            {"name": "username input", "selectors": ["username", "login", "email", "phone"]},
            {"name": "password input", "selectors": ["password", "pass"]},
            {"name": "login button", "selectors": ["kc-login", "login", "submit"]}
        ]
        
        print("\n=== Searching for elements ===")
        for element in common_selectors:
            print(f"\n{element['name'].upper()}:")
            for selector in element['selectors']:
                # Try by ID
                try:
                    elem = driver.find_element(By.ID, selector)
                    print(f"  - ID '{selector}': FOUND - {elem.tag_name} | {elem.text if elem.text else 'No text'}")
                except:
                    pass
                
                # Try by class name
                try:
                    elem = driver.find_elements(By.CLASS_NAME, selector)
                    if elem:
                        print(f"  - Class '{selector}': FOUND {len(elem)} elements")
                        for e in elem[:2]:  # Show first 2 elements
                            print(f"    - {e.tag_name} | {e.text if e.text else 'No text'}")
                except:
                    pass
                
                # Try by data-testid or other attributes
                try:
                    elem = driver.find_elements(By.CSS_SELECTOR, f"[data-testid*='{selector}'], [data-test-id*='{selector}']")
                    if elem:
                        print(f"  - Data attribute with '{selector}': FOUND {len(elem)} elements")
                except:
                    pass
        
        # Try XPath approach for common patterns
        print("\n=== XPath searches ===")
        xpaths = [
            "//div[contains(@id, 'tab') and contains(@class, 'btn')]",
            "//button[contains(@id, 'tab') or contains(@class, 'tab')]",
            "//span[contains(text(), 'Телефон') or contains(text(), 'Phone')]",
            "//span[contains(text(), 'Почта') or contains(text(), 'Mail')]",
            "//span[contains(text(), 'Логин') or contains(text(), 'Login')]",
            "//span[contains(text(), 'Лицевой') or contains(text(), 'LS')]",
            "//a[contains(text(), 'Забыл') or contains(text(), 'Forgot')]",
            "//a[contains(text(), 'Зарегистрирова') or contains(text(), 'Register')]"
        ]
        
        for xpath in xpaths:
            try:
                elements = driver.find_elements(By.XPATH, xpath)
                if elements:
                    print(f"XPath '{xpath}': FOUND {len(elements)} elements")
                    for element in elements[:3]:  # Show first 3 elements
                        print(f"  - Tag: {element.tag_name}, Text: '{element.text}', ID: {element.get_attribute('id')}, Class: {element.get_attribute('class')}")
            except Exception as e:
                print(f"XPath '{xpath}': ERROR - {str(e)}")
                
    except Exception as e:
        logger.error(f"Error during inspection: {str(e)}")
        driver.save_screenshot("screenshots/inspection_error.png")
    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    inspect_page_elements()