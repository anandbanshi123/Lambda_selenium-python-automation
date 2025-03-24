import unittest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.options import Options as IEOptions
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from dotenv import load_dotenv
import warnings

# Load environment variables
load_dotenv()

username = os.getenv("LT_USERNAME")
access_key = os.getenv("LT_ACCESS_KEY")

def suppress_resource_warnings():
    warnings.filterwarnings("ignore", category=ResourceWarning)

class LambdaTest(unittest.TestCase):
    driver = None

    def setUp(self):
        """ Setup different browsers based on a parameter """
        browser = os.getenv("BROWSER", "firefox")  # Default: Chrome

        lt_options = {
            "username": username,
            "accessKey": access_key,
            "platformName": "",
            "browserName": "",
            "browserVersion": "",
            "build": "Cross Browser Test",
            "name": f"Test on {browser}",
        }

        if browser == "chrome":
            lt_options["platformName"] = "Windows 10"
            lt_options["browserName"] = "Chrome"
            lt_options["browserVersion"] = "128.0"
            options = ChromeOptions()

        elif browser == "edge":
            lt_options["platformName"] = "macOS Ventura"
            lt_options["browserName"] = "MicrosoftEdge"
            lt_options["browserVersion"] = "127.0"
            options = EdgeOptions()

        elif browser == "firefox":
            lt_options["platformName"] = "Windows 11"
            lt_options["browserName"] = "Firefox"
            lt_options["browserVersion"] = "130.0"
            options = FirefoxOptions()

        elif browser == "ie":
            lt_options["platformName"] = "Windows 10"
            lt_options["browserName"] = "Internet Explorer"
            lt_options["browserVersion"] = "11.0"
            options = IEOptions()
        else:
            raise ValueError("Unsupported browser specified!")

        options.set_capability("LT:Options", lt_options)

        self.driver = webdriver.Remote(
            command_executor=f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub",
            options=options
        )

    def test_demo_site(self):
        driver = self.driver
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)

        print("Loading URL")
        driver.get("https://lambdatest.github.io/sample-todo-app/")

        driver.find_element(By.NAME, "li1").click()
        driver.find_element(By.NAME, "li2").click()
        print("Clicked on the second element")

        driver.find_element(By.ID, "sampletodotext").send_keys("LambdaTest")
        driver.find_element(By.ID, "addbutton").click()
        print("Added LambdaTest checkbox")

        heading = driver.find_element(By.CSS_SELECTOR, ".container h2")
        assert heading.is_displayed(), "Heading is not displayed"
        print(heading.text)

        driver.execute_script("lambda-status=passed")
        print("Tests ran successfully!")

    def test_scenario1(self):
        driver = self.driver
        driver.implicitly_wait(10)

        try:
            driver.get("https://www.lambdatest.com/selenium-playground")
            
            simple_form_demo = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Simple Form Demo"))
            )
            simple_form_demo.click()

            WebDriverWait(driver, 10).until(lambda d: "Simple Form Demo" in d.current_url)

            message = "Welcome to LambdaTest"
            input_box = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "user-message"))
            )
            input_box.clear()
            input_box.send_keys(message)

            get_value_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.id, "showInput"))
            )
            get_value_button.click()

            displayed_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "message"))
            )
            actual_text = displayed_element.text.strip()

            assert actual_text == message, f"Expected '{message}', but got '{actual_text}'"
            print("Test Passed: The message is correctly displayed.")

        except Exception as e:
            print("Test Failed:", e)

    def test_scenario2(self):
        driver = self.driver
        driver.implicitly_wait(10)

        try:
            driver.get("https://www.lambdatest.com/selenium-playground")

            drag_sliders_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Drag & Drop Sliders"))
            )
            drag_sliders_link.click()
            time.sleep(2)

            slider = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='slider1']/div/input"))
            )

            print("Current slider value:", slider.get_attribute("value"))

            action = ActionChains(driver)
            action.click_and_hold(slider).move_by_offset(95, 0).release().perform()

            # Ensure the value updates
            WebDriverWait(driver, 5).until(lambda d: slider.get_attribute("value") == "95")

            new_value = slider.get_attribute("value")
            print("New slider value:", new_value)

            assert new_value == "95", f"Expected slider value to be 95, but got {new_value}"
            print("Test Passed: Slider value is 95.")

        except Exception as e:
            print("Test Failed:", e)


    def test_scenario3(self):
        driver = self.driver
        driver.implicitly_wait(10)

        try:
            driver.get("https://www.lambdatest.com/selenium-playground")
            
            input_form_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Input Form Submit"))
            )
            input_form_link.click()

            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='seleniumform']/div[6]/button"))
            )
            submit_button.click()

            name_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "name"))
            )
            validation_message = name_field.get_attribute("validationMessage")
            assert validation_message == "Please fill out this field.", (
                f"Expected 'Please fill out this field.' but got '{validation_message}'"
            )

            name_field.send_keys("John Doe")
            email_field = driver.find_element(By.ID, "inputEmail4")
            email_field.send_keys("john.doe@example.com")
      

            country_dropdown = Select(driver.find_element(By.NAME, "country"))
            country_dropdown.select_by_visible_text("United States")

            submit_button.click()

            success_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[contains(text(),'Thanks for contacting us, we will get back to you shortly.')]")
                )
            )
            assert "Thanks for contacting us, we will get back to you shortly." in success_element.text.strip()
            print("Test Passed: Success message validated.")

        except Exception as e:
            print("Test Failed:", e)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
