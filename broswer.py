import pytest
import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
import warnings
from urllib3.exceptions import NotOpenSSLWarning # type: ignore
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

# Import options for various browsers.
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@pytest.fixture(scope='class')
def without_login(request, pytestconfig):
    driver = None
    try:
        # Retrieve browser and OS parameters from the command line
        browser = pytestconfig.getoption('browser')
        os_platform = pytestconfig.getoption('os')
        
        if browser == 'chrome':
            options = ChromeOptions()
            options.browser_version = "132"
            options.platform_name = os_platform  # Use provided OS
            lt_options = {
                "username": "anand_jha1",
                "accessKey": "mH6NxUju1aFk7S58ve32Y0ALwi3eiu8nHDkDKJFEO7ht6n4MTl",
                "project": "Untitled",
                "w3c": True,
                "plugin": "python-python"
            }
            options.set_capability('LT:Options', lt_options)
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(options=options)
        
        elif browser == 'edge':
            options = EdgeOptions()
            options.browser_version = "132"
            options.platform_name = os_platform  # Use provided OS
            lt_options = {
                "username": "anand_jha1",
                "accessKey": "mH6NxUju1aFk7S58ve32Y0ALwi3eiu8nHDkDKJFEO7ht6n4MTl",
                "project": "Untitled",
                "w3c": True,
                "plugin": "python-python"
            }
            options.set_capability('LT:Options', lt_options)
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Edge(options=options)
        
        elif browser == 'safari':
            options = SafariOptions()
            options.browser_version = "18"
            options.platform_name = os_platform  # Use provided OS
            lt_options = {
                "username": "anand_jha1",
                "accessKey": "mH6NxUju1aFk7S58ve32Y0ALwi3eiu8nHDkDKJFEO7ht6n4MTl",
                "project": "Untitled",
                "w3c": True,
                "plugin": "python-python"
            }
            options.set_capability('LT:Options', lt_options)
            driver = webdriver.Safari(options=options)
        
        elif browser == 'firefoz':
            options = FirefoxOptions()
            options.browser_version = "130"
            options.platform_name = os_platform  # Use provided OS
            lt_options = {
                "username": "anand_jha1",
                "accessKey": "mH6NxUju1aFk7S58ve32Y0ALwi3eiu8nHDkDKJFEO7ht6n4MTl",
                "project": "Untitled",
                "w3c": True,
                "plugin": "python-python"
            }
            options.set_capability('LT:Options', lt_options)
            driver = webdriver.Firefox(options=options)
        
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        # Set window size and log it
        driver.set_window_size(1792, 1023)
        logger.info("Window size: %s", driver.get_window_size())
        
        # Open the URL
        driver.get("https://www.lambdatest.com/selenium-playground")
        logger.debug('Inside UI portal without login')
        
        # Attach driver to the test class for use in tests
        request.cls.driver = driver
        
        yield driver
    
    except Exception as e:
        logger.error(e)
        if driver:
            screenshot_name = f"{request.node.name}.png"
            driver.save_screenshot(screenshot_name)
        assert False, str(e)
    
    finally:
        if driver:
            driver.quit()

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--os", action="store", default="Windows 10")
