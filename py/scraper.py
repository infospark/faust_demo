import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# download chromedriver from here https://chromedriver.chromium.org/downloads
# needs to match the installed version of Chrome on your machine (e.g. 98.0.4758.102)


# Scrapes a singleton URL and returns the source
def get_page_source(web_driver, url):
    web_driver.get(url)
    source = web_driver.page_source
    return source


# What should this return ? Either side effect on the web_driver or an exception?
def login_with_google(web_driver, url, username, password):
    web_driver.get(url)

    # Find and click for Continue With Google Button
    continue_with_google_button = find_continue_with_google_button(web_driver)
    continue_with_google_button.click()

    # Clicking this button should open a new window
    # Wait for two windows to be available
    WebDriverWait(web_driver, 10).until(EC.number_of_windows_to_be(2))
    homepage_handle = web_driver.current_window_handle
    window_handles = web_driver.window_handles

    # Switch to the new (google sign in) Window
    found_sign_in_with_google_window = False

    for window_handle in window_handles:
        if window_handle != homepage_handle:
            web_driver.switch_to.window(window_handle)
            assert("Sign in with Google" in web_driver.page_source,
                   "Attempting to sign into Google - window does not contain expected text")
            found_sign_in_with_google_window = True

    if not found_sign_in_with_google_window:
        raise Exception(f"Sign In With Google window did not appear")

    # Find the username input box and type in username
    username_input_boxes = web_driver.find_elements_by_css_selector("[aria-label='Email or phone']")
    assert(len(username_input_boxes) == 1,
           "Found zero or more than one username input boxes on Sign in with Google page")
    username_input_boxes[0].send_keys(username)

    # Find the next button and click it
    buttons = web_driver.find_elements(By.XPATH, '//button')
    found_next_button = False
    for b in buttons:
        if "Next" in b.text:
            b.click()
            found_next_button = True
            break

    if not found_next_button:
        raise Exception("Unable to find a Next button on the Sign in with Google page (username stage)")

    # Just wait ten seconds here - the password box is enabled via animation and selenium seems to be thrown by this
    time.sleep(10)
    #WebDriverWait(web_driver, 10).until(EC.visibility_of_element_located((By.ID, 'password')))

    # This needs to assert visibility not just check for presence in the source
    #   if "Couldn't find your Google Account" in web_driver.page_source:
    #       raise Exception(f"Got 'Couldnt find your Google Account' error when attempting to login in with {username}")

    # Find the password input box and type in the password
    password_input_boxes = web_driver.find_elements_by_css_selector("[aria-label='Enter your password']")
    assert (len(password_input_boxes) == 1, "Found zero or more than one password input boxes on Sign in with Google page")
    password_input_boxes[0].send_keys(password)

    # Click Next again
    found_next_button = False
    buttons = web_driver.find_elements(By.XPATH, '//button')
    for b in buttons:
        if "Next" in b.text:
            b.click()
            found_next_button = True
            break

    if not found_next_button:
        raise Exception("Unable to find a Next button on the Sign in with Google page (password stage)")

    # This needs to assert visibility not just check for presence in the source
    #if "Wrong Password" in web_driver.page_source:
    #    raise Exception(f"Got 'Wrong Password' error for Sign in with Google page with username {username}")

    # Ensure we're back on the homepage
    web_driver.switch_to.window(homepage_handle)

    # All being well the Google Window will close itself and we'll be back at the home page
    WebDriverWait(web_driver, 10).until(EC.number_of_windows_to_be(1))

    return web_driver.page_source


# Finds most likely candidate for a next button and returns it
def find_continue_with_google_button(web_driver):
    buttons = web_driver.find_elements(By.CLASS_NAME, 'google')
    for b in buttons:
        if b.accessible_name == 'Continue with Google':
            return b
    else:
        return None


# Finds most likely candidate for a next button and returns it
def find_next_button(web_driver):
    buttons = web_driver.find_elements(By.XPATH, '//button')
    for b in buttons:
        if b.get_attribute('aria-label') is not None and 'Next' in b.get_attribute('aria-label') \
                and b.get_attribute('data-direction') is not None and 'next' in b.get_attribute('data-direction'):
            return b
    return None


# Scrapes a page - looks for the Next button and keeps returning pages until the
# Next button is disabled
def scrape_paginated_url(web_driver, url):
    more_to_scrape = True
    web_driver.get(url)
    while more_to_scrape:
        yield web_driver.page_source
        next_button = find_next_button(web_driver)
        if next_button is None:
            more_to_scrape = False
        else:
            ActionChains(web_driver).move_to_element(next_button).perform()
            time.sleep(2);
            #next_button.click()
            web_driver.execute_script("arguments[0].click();", next_button)


