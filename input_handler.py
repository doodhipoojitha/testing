'''
@author: Yaswanth Kumar
'''
import os
import time
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
#from Packages.settings import LOGGER
import logging


def check_errors(driver):
    """function start"""
    print('checking error')
    error_box_xpath = "//div[@id='errorReportModal']"
    close_button_xpath = "//button[@name='confirm' and text()='Close'] "
    message_field_xpath = "//div[@class = 'modal-content errorReportModalContent']/p/" \
                          "span[text()='Message:']/.."
    load_xpath = "//span[@class='loading']"
    logout_button_xpath = "//button[text()='Logout']"
    while is_xpath_displayed(driver, load_xpath, 1):
        print('Loading')
    print('after loading')
    if is_xpath_displayed(driver, error_box_xpath, 2):
        error_message = read_text(driver, message_field_xpath)
        if error_message:
            mouse_click(driver, close_button_xpath)
            raise Exception(error_message)

    if wait_till_clickable(driver, logout_button_xpath, 1):
        mouse_click(driver, logout_button_xpath)
        time.sleep(2)
        raise Exception('Session timed out')


def press_down(driver):
    """function start"""
    actions = ActionChains(driver)
    actions.send_keys(Keys.DOWN).perform()


def get_attribute(driver, xpath, name):
    """function start"""
    try:
        control_click = driver.find_element('xpath',xpath)
        time.sleep(1)
        return control_click.get_attribute(name)
    except Exception as timeout:
        logging.info('%s - %s - %s', "Unable to find the Xpath getAttributess ", xpath, timeout)


def is_clickable(driver, xpath, timeout):
    """function start"""
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element = driver.find_element('xpath',xpath)
        element.click()
        return True
    except Exception as eeee:
        logging.info('Exception   - %s - Xpath : %s',
                    "is_clickable".ljust(30), xpath)
        logging.exception(eeee)
        return False


def switch_iframe(driver, xpath):
    """function start"""
    try:
        iframe = driver.find_element_by_xpath(xpath)
        driver.switch_to.frame(iframe)
    except Exception as e:
        logging.info('%s - %s - %s', "Unable to find the Xpath in switchIframe ",xpath,e)


def choose_drop_down_click(driver, controlxpath, drop_down_xpath, value, tries=30):
    """function start"""
    while tries > 0:
        tries -= 1
        print(tries)
        try:
            print('in drop down')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                            controlxpath)))
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, controlxpath)))
            control_click = driver.find_element('xpath',controlxpath)
            control_click.click()
            print('clicked')
            time.sleep(1)
            control_click.clear()
            control_click.send_keys(value)
            if not is_xpath_displayed(driver, drop_down_xpath, 3):
                print('not found')
                continue
            time.sleep(1)
            drop_down_element = driver.find_element_by_xpath(drop_down_xpath)
            drop_down_element_list = drop_down_element.find_elements_by_tag_name("div")
            for row in drop_down_element_list:
                print(row.text)
                if row.text.upper() == value.upper():
                    time.sleep(1)
                    row.click()
                    return
            print(' not clicked')
            control_click.send_keys(Keys.ARROW_DOWN)
            control_click.send_keys(Keys.ENTER)
            return
        except Exception as timout:
            print(timout)
            check_error(driver)
            if tries == 0:
                logging.info('%s - %s - %s', "Unable to find the Xpath mouseClick", controlxpath,
                            timout)
                raise


def choose_drop_down_enter(driver, xpath, drop_down_xpath, value, tries=30):
    """function start"""
    while tries > 0:
        tries -= 1
        print("in loop", tries)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element = driver.find_element('xpath',xpath)
            print('in drop down')
            element.click()
            print('clicked')
            time.sleep(0.5)
            element.clear()
            element.send_keys(value)
            time.sleep(0.5)
            if not element.get_attribute('value').lower() == value.lower():
                continue
            if not is_xpath_displayed(driver, drop_down_xpath, 3):
                print('not found')
                continue
            time.sleep(1)
            element.send_keys(Keys.ARROW_DOWN)
            element.send_keys(Keys.ENTER)
            return
        except Exception as timout:
            print(timout)
            check_error(driver)
            if tries == 0:
                logging.info('%s - %s - %s', "Unable to find the Xpath mouseClick", xpath, timout)
                raise


def clear(driver, xpath):
    """function start"""
    try:
        control_click = driver.find_element_by_xpath(xpath)
        control_click.clear()
    except Exception as timout:
        logging.info('%s - %s - %s', "Unable to find the Xpath clear ", xpath, timout)


def send_key_no_check(driver, xpath, value):
    """function start"""
    try:
        control_click = driver.find_element_by_xpath(xpath)
        control_click.send_keys(value)
    except Exception as timout:
        logging.info('%s - %s - %s', "Unable to find the Xpath Send Keys ", xpath, timout)


def send_key(driver, xpath, value, no_of_tries=30):
    """function start"""
    while True:
        try:
            print('in try')
            no_of_tries -= 1
            element = driver.find_element_by_xpath(xpath)
            element.clear()
            element.send_keys(value)

            if value.lower() == element.get_attribute('value').lower():
                logging.info('Successfull - %s - Xpath : %s',
                            "send_key".ljust(30), xpath)
                return

            if no_of_tries == 0:
                logging.info('Tries Exceeded - %s - Xpath : %s',
                            "send_key".ljust(30), xpath)
                raise Exception('Entering Value failed. Value : ' + value)

        except Exception as eeee:
            print(eeee)
            check_error(driver)
            if no_of_tries == 0:
                logging.info('Exception - %s - Xpath : %s',
                            "send_key".ljust(30), xpath)
                logging.exception(eeee)
                raise


def send_key_with_special_check(driver, xpath, value, no_of_tries=30):
    """function start"""
    while True:
        try:
            print('in try')
            no_of_tries -= 1
            element = driver.find_element_by_xpath(xpath)
            element.clear()
            element.send_keys(value)

            if re.sub('[^a-zA-Z0-9]', "",
                      value.lower()) == re.sub('[^a-zA-Z0-9]',
                                               "", element.get_attribute('value').lower()):
                logging.info('Successfull - %s - Xpath : %s',
                            "send_key".ljust(30), xpath)
                return

            if no_of_tries == 0:
                logging.info('Tries Exceeded - %s - Xpath : %s',
                            "send_key".ljust(30), xpath)
                raise Exception('Entering Value failed. Value : ' + value)

        except Exception as eeee:
            print(eeee)
            check_error(driver)
            if no_of_tries == 0:
                logging.info('Exception - %s - Xpath : %s',
                            "send_key".ljust(30), xpath)
                logging.exception(eeee)
                raise

def send(driver, xpath, value, no_of_tries=30):
    """function start"""
    while True:
        try:
            print('in try')
            no_of_tries -= 1
            element = driver.find_element('xpath',xpath) #changedd
            element.send_keys(value)
            return

            # if no_of_tries == 0:
            #     LOGGER.info('Tries Exceeded - %s - Xpath : %s',
            #                 "send_key".ljust(30), xpath)
            #     raise Exception('Entering Value failed. Value : ' + value)

        except Exception as eeee:
            print(eeee)
            check_error(driver)
            if no_of_tries == 0:
                logging.info('Exception - %s - Xpath : %s',
                            "send_key".ljust(30), xpath)
                logging.exception(eeee)
                raise

def select_all_send_key(driver, xpath, value, no_of_tries=10):
    """function start"""
    while True:
        try:
            print('in try')
            no_of_tries -= 1
            element = driver.find_element_by_xpath(xpath)
            element.click()
            element.send_keys(Keys.CONTROL + "A")
            element.send_keys(Keys.BACK_SPACE)
            element.send_keys(value)

            if value.lower() == element.get_attribute('value').lower():
                logging.info('Successfull - %s - Xpath : %s',
                            "send_key".ljust(30), xpath)
                return

            if no_of_tries == 0:
                logging.info('Tries Exceeded - %s - Xpath : %s',
                            "send_key".ljust(30), xpath)
                raise Exception('Entering Value failed. Value : ' + value)

        except Exception as eeee:
            print(eeee)
            check_error(driver)
            if no_of_tries == 0:
                logging.info('Exception - %s - Xpath : %s',
                            "send_key".ljust(30), xpath)
                logging.exception(eeee)
                raise


def mouse_click(driver, xpath, tries=30):
    """function start"""
    while tries > 0:
        tries -= 1
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element = driver.find_element('xpath', xpath)
            element.click()


            logging.info('Successfull - %s - Xpath : %s',
                        "mouse_click".ljust(30), xpath)
            return
        except Exception:
            check_error(driver)
            if tries == 0:
                logging.info('Exception - %s - Xpath : %s',
                             "mouse_click".ljust(30), xpath)
                raise


# =============================================================================
# Mouse click and send value to the field with given xpath
# checks whether the right value is entered in the field
# if not then the field is cleared and value is re entered
# =============================================================================
def mouse_click_send_keys(driver, xpath, value, no_of_tries=30):
    """function start"""
    while True:
        try:
            no_of_tries -= 1
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element = driver.find_element('xpath',xpath)
            element.click()
            element.clear()
            time.sleep(0.5)
            element.send_keys(value)

            if value.lower() == element.get_attribute('value').lower():
                logging.info('Successfull - %s - Xpath : %s',
                            "mouse_click_send_keys".ljust(30), xpath)
                return

            if no_of_tries == 0:
                logging.info('Tries Exceeded - %s - Xpath : %s',
                            "mouse_click_send_keys".ljust(30), xpath)
                raise Exception('Entering Value failed. Value : ' + value)

        except Exception as eeee:
            check_error(driver)
            if no_of_tries == 0:
                logging.info('Exception - %s - Xpath : %s',
                            "mouse_click_send_keys", xpath)
                logging.exception(eeee)
                raise



def mouse_click_send_keyand_tab(driver, controlxpath, value):
    """function start"""
    try:
        time.sleep(0.5)
        control_click = driver.find_element_by_xpath(controlxpath)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, controlxpath)))
        control_click.click()
        control_click.clear()
        time.sleep(1)
        control_click.send_keys(value)
        control_click.send_keys(Keys.TAB)
    except Exception as timout:
        logging.info('%s - %s - %s', "Unable to find the Xpath mouseClickSendKeyandTab",
                    controlxpath, timout)



def scroll(driver, offset):
    """function start"""
    driver.execute_script("window.scrollBy(0,"+ str(offset)+");")

def scroll_to_element(driver, xpath):
    """function start"""
    try:
        element = driver.find_element('xpath', xpath)
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
    except Exception as timeout:
        logging.info('%s - %s - %s', "Unable to find the Xpath in scroll to element ", xpath, timeout)

def scroll_to_view(driver, xpath):
    """function start"""
    try:
        element = driver.find_element_by_xpath(xpath)
        driver.execute_script("arguments[0].scrollIntoView();", element)
    except Exception as timout:
        logging.info('%s - %s - %s', "Unable to find the Xpath in scroll to element ", xpath, timout)


def click(driver, xpath):
   try:
       element = driver.find_element('xpath',xpath)
       actions = ActionChains(driver)
       WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
       actions.click(element).perform()
   except Exception as timout:
       actions.click(element).perform()
       logging.info('%s - %s - %s', "Unable to find the Xpath in Click ", xpath, timout)

#def sendKeyActionChain(driver, value):
#    try:
#        actions = ActionChains(driver)
#        actions.send_keys(value).perform()
#    except Exception as timout:
#        LOGGER.info('%s - %s - %s', "Unable to sendkeys using action chains ",timout)

#def doubleClick(driver, xpath):
#    try:
#        element = driver.find_element_by_xpath(xpath)
#        actions = ActionChains(driver)
#        actions.double_click(element).perform()
#    except Exception as timout:
#        LOGGER.info('%s - %s - %s', "Unable to find the Xpath in Click ", xpath, timout)

#def scrollToElementandClick(driver, xpath):
#    try:
#        element = driver.find_element_by_xpath(xpath)
#        actions = ActionChains(driver)
#        actions.move_to_element(element).perform()
#        waitTillClickable(driver, xpath)
#        actions.click(element).perform()
#    except Exception as timout:
#        LOGGER.info('%s - %s - %s', "Unable to find the Xpath in scrollToElementandClick ",
#        xpath, timout)

# '''
# Reads the inner text of the xpath given
# '''
def read_text(driver, xpath):
    """function start"""
    try:
        element = driver.find_element_by_xpath(xpath)
        return element.text
    except Exception as timout:
        logging.info('%s - %s - %s', "Unable to find the Xpath in readText ", xpath, timout)


# '''
# ---------------------------------------------------------------------------
# Important methods to wait until loading done
# ---------------------------------------------------------------------------
# '''

# =============================================================================
# Waits for timeout sec for the element with the xpath to be displayed
# =============================================================================
def processing_check_wait(driver, xpath, timeout):
    """function start"""
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        logging.info('Successfull - %s - Xpath : %s',
                    "processing_check_wait".ljust(30), xpath)
        return True
    except Exception as eeee:
        logging.info('Exception   - %s - Xpath : %s',
                    "processing_check_wait".ljust(30), xpath)
        logging.exception(eeee)
        return False

# '''
# --------------------------------------------------------
# Waits till the element with the xpath is clickable
# if element is not clickable after 10s returns false
# --------------------------------------------------------
# '''
def wait_till_clickable(driver, xpath, timeout):
    """function start"""
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
#        WebDriverWait(driver, timeout).until(EC.stalenessOf((By.XPATH, xpath)))
        return True
    except Exception as timout:
        logging.info('%s - %s - %s', "Unable to find the Xpath in wait till clickable to element ",
                    xpath, timout)
        return False

# '''
# -----------------------------------------
# Checks whether the xpath is displayed.
# If xpath is displayed returns true.
# -----------------------------------------
# '''
def is_xpath_displayed(driver, element_xpath, timeout):
    """function start"""
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,
                                                                             element_xpath)))
        logging.info('%s - %s', "Content Displayed  ", element_xpath)
        return True
    except Exception as eeee:
        logging.info('%s - %s - %s', "Unable to find the Xpath in is xpath displayed ",
                    element_xpath, eeee)
        return False

def mouse_hover(driver, xpath, no_of_tries=30):
    """function start"""
    while True:
        try:
            no_of_tries -= 1
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element = driver.find_element('xpath',xpath)
            hov = ActionChains(driver).move_to_element(element)
            hov.perform()
            return
        except Exception as e:
            logging.exception(e)
            raise

def wait_till_download(path_to_downloads, timeout=30):
    """function start"""
    try:
        seconds = 0
        dl_wait = True
        #file_count_old = len(glob.glob(path_to_downloads+"/*.*"))
        while dl_wait and (seconds < timeout):
            time.sleep(1)
            #file_count_new = len(glob.glob(path_to_downloads+"/*.*"))
            dl_wait = False
            #if file_count_new == file_count_old:
                #dl_wait = True
            for fname in os.listdir(path_to_downloads):
                if fname.endswith('.crdownload'):
                    dl_wait = True
                    break
            seconds += 1
        return True
    except Exception:
        logging.info("Unable to wait for download ")
        return False

