import base64
import json
import os

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the Chrome Options
options = webdriver.ChromeOptions()
print_options = {
    "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }
    ],
    "selectedDestinationId": "Save as PDF",
    "version": 2,
    "mediaSize": {
        "height_microns": 297000,
        "name": "ISO_A4",
        "width_microns": 210000,
        "custom_display_name": "A4",
    },
    "isCssBackgroundEnabled": True,
    "isHeaderFooterEnabled": False,
}

# Add the arguments to the Chrome Options
options.add_experimental_option(
    "prefs",
    {
        "printing.print_preview_sticky_settings.appState": json.dumps(print_options),
    },
)
options.add_argument("--headless=new")
options.add_argument("--kiosk-printing")

# Load the Chrome Driver
driver = webdriver.Chrome(options=options)
driver.get("https://devayaan.me/resume")

# Wait for the page to load
wait = WebDriverWait(driver, timeout=10)
wait.until(lambda _: driver.find_element(By.XPATH, "//main/div[1]/span").is_displayed())

# Wait more for the page load completely
sleep(0.5)

# Scroll to the bottom of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Print the page to PDF
os.mkdir(os.path.join(os.getcwd(), "resume-dist"))
with open(os.path.join(os.getcwd(), "resume-dist", "resume.pdf"), "wb") as file:
    file.write(
        base64.b64decode(
            driver.execute_cdp_cmd("Page.printToPDF", print_options)["data"]
        )
    )
