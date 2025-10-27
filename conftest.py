import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="firefox",
        help="Browser to run tests in (chrome, firefox, edge)"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )

@pytest.fixture
def driver(request):
    """Фикстура для инициализации веб-драйвера с поддержкой браузера Mozilla Firefox"""
    browser_name = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")
    
    if browser_name == "firefox":
        # Настройка опций для браузера Firefox
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        
        # Опции запуска Firefox
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument("--start-maximized")
        options.add_argument("--no-first-run")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-features=Translate")
        
        # Используем закэшированный драйвер, так как GitHub API имеет ограничения
        geckodriver_path = "/home/uss/.wdm/drivers/geckodriver/linux64/v0.36.0/geckodriver"
        service = Service(geckodriver_path)
        driver = webdriver.Firefox(service=service, options=options)
        driver.maximize_window()
        logger.info(f"Firefox browser initialized with headless={headless}")
        
        yield driver
        driver.quit()
        logger.info("Firefox browser closed")
    else:
        pytest.skip(f"Browser {browser_name} is not supported in this configuration")