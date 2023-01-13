import os
FIOI_LOGIN = os.environ["FIOI_LOGIN"]
FIOI_PASS = os.environ["FIOI_PASS"]

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time


opt = webdriver.FirefoxOptions()
opt.headless = True
driver = webdriver.Firefox(options=opt)

driver.get("https://concours.algorea.org")

wait = WebDriverWait(driver, 30)
driver.implicitly_wait(30)

# Store the ID of the original window
original_window = driver.current_window_handle

# Check we don't have other windows open already
assert len(driver.window_handles) == 1

# Click the link which opens in a new window
span_connect = driver.find_element(By.CSS_SELECTOR, '[ng-i18next="login_connect"]')
assert span_connect.text == "Se connecter"
span_connect.click()

# Wait for the new window or tab
wait.until(EC.number_of_windows_to_be(2))

# Loop through until we find a new window handle
for window_handle in driver.window_handles:
    if window_handle != original_window:
        driver.switch_to.window(window_handle)
        break

# Wait for the new tab to finish loading content
wait.until(EC.title_is("Login module"))

login_from = driver.find_element(By.TAG_NAME, "form")
id_box = login_from.find_element(By.ID, "identity")
assert id_box.tag_name == "input"
id_box.send_keys(FIOI_LOGIN)
login_from.submit()

pw_box = driver.find_element(By.ID, "password")
login_form = driver.find_element(By.TAG_NAME, "form")
assert pw_box.tag_name == "input"
pw_box.send_keys(FIOI_PASS)
login_form.submit()

wait.until(EC.number_of_windows_to_be(1))

driver.switch_to.window(original_window)
# driver.find_element(By.CLASS_NAME, "menu-item-login").click()

# driver.find_element(By.CSS_SELECTOR, '[ng-i18next="[title];groupRequests_title_my_groups"]').click()

# links = driver.find_element(By.CSS_SELECTOR, '[ng-show="myGroupAdmin.children.length"]').find_elements(By.TAG_NAME, 'a')
# next(filter(lambda l: l.text == "Sélection olympiades 2023 phase 2", links)).click()

wait.until(EC.presence_of_element_located([By.CLASS_NAME, "menu-item-login"]))
driver.get("https://concours.algorea.org/groupAdmin/70330347151610819/")

driver.find_element(By.CSS_SELECTOR, '[ng-i18next="[title];progress"]').click()
driver.find_element(By.CSS_SELECTOR, """[uib-btn-radio="'collective'"]""").click()

div_parcours_select = driver.find_element(By.CLASS_NAME, "parcours-select").find_elements(By.TAG_NAME, "select")
assert len(div_parcours_select) == 2
Select(div_parcours_select[0]).select_by_visible_text("Sélection olympiades 2023")

wait.until(EC.presence_of_element_located([By.CSS_SELECTOR, '[uib-tooltip="Épreuve de sélection 1"]']))
Select(div_parcours_select[1]).select_by_visible_text("Épreuve de sélection 1")

wait.until(EC.presence_of_element_located([By.CSS_SELECTOR, '[uib-tooltip="Épreuve de sélection 1"]']))
to_screen = driver.find_element(By.CSS_SELECTOR, """[ng-if="formValues.progressionType == 'collective'"]""").find_element(By.CLASS_NAME, "table-wrapper")
to_screen.screenshot("test.png")

try:
    time.sleep(20)
except:
    pass
driver.quit()
