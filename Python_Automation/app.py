import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
import time

## Change the default behavior of Chrome driver
options = webdriver.ChromeOptions()
## This Option take our chrome profile as default when selenium running
## you can check here for detail chrome://version/
options.add_argument(r"--user-data-dir=C:/Users/Jon Prasetio Bawues/AppData/Local/Google/Chrome/User Data")
options.add_argument(r"--profile-directory=Profile 1")
## this option is to prevent chrome from closing immediately after the script is run
options.add_experimental_option("detach", True)
## surpress the warning/message when running the script
options.add_argument("--log-level=1")

# Service is equal to the path of the Chromedriver.exe
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

## Load Excel data
data = pd.read_excel('Automated_Bank_Testing.xlsx')
descriptions = data['DESCRIPTION'].to_list()
real_category = data['Real Category'].to_list()
real_vendor = data['Real Vendor'].to_list()

## Go to login page of QuickBooks
driver.get("https://accounts.intuit.com/app/sign-in?app_group=QBO&asset_alias=Intuit.accounting.core.qbowebapp&locale=en-ROW&state=%7B%22queryParams%22%3A%7B%22locale%22%3A%22en-ROW%22%7D%7D&app_environment=prod")

## Click the sign-in button
try:
    sign_in_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[1]/section/div[1]/ul/li[1]/div[2]/button')))
    sign_in_button.click()
except TimeoutException:
    pass

## Click the continue button on the password section
try:
    password_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "iux-password-confirmation-password")))
    WebDriverWait(driver, 30).until(lambda driver: password_element.get_attribute('value') != '')
    continue_password_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/form/button[2]')))
    continue_password_button.click()
except TimeoutException:
    pass

## Click the SmartAI button
try:
    smart_ai_test = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="account-list-container"]/div[1]/div/section/div[2]/li[2]/button')))
    smart_ai_test.click()
except TimeoutException:
    pass

## Click the transaction menu
try:
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@id='Navigation']/div[3]/div[4]/a/span")))
    transaction = driver.find_element(By.XPATH, "//*[@id='Navigation']/div[3]/div[4]/a/span")
    transaction.click()
except TimeoutException:
    pass

## Wait for the page to load and get the number of pages
WebDriverWait(driver, 120).until(
    EC.visibility_of_element_located((By.XPATH, "//button[contains(@aria-label,'Current Page')]/following-sibling::button[last()]/preceding-sibling::button[1]")))
pages = int(driver.find_element(By.XPATH, "//button[contains(@aria-label,'Current Page')]/following-sibling::button[last()]/preceding-sibling::button[1]").text)

## Function to handle matching and updating records
def match_and_edit_record(description, vendor, category):
    for page in range(1, pages + 1):
        try:
            xpath_text = f"(//div//table[@class='idsTable--quickbooksTheme idsTable__columnGroup'])[2]//tr//td[4][.='{description}']"
            ## Refresh elements for each iteration to avoid stale element exception
            table_rows = driver.find_elements(By.XPATH, xpath_text)
            for row in table_rows:
                try:
                    WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, "empty-grid")))
                    ## check box element
                    check_box = row.find_element(By.XPATH, "./preceding-sibling::td[3]//input")

                    ## click check box
                    driver.execute_script("arguments[0].scrollIntoView(true);", check_box)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(check_box))
                    check_box.click()

                    ## edit button
                    element = WebDriverWait(driver, 60).until(
                        EC.visibility_of_element_located((By.XPATH, '//div[@class="batch-action-banner pre-redesign"]//div[3]//button')))
                    ## click the edit button
                    element.click()

                    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='ModalDialog--wrapper']")))
                    ## fill the supplier dropdown
                    if isinstance(vendor, str):
                        supplier_customer = WebDriverWait(driver, 60).until(
                            EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Select payee"]')))
                        driver.execute_script("arguments[0].click()", supplier_customer)
                        
                        ## Scroll into view to ensure dropdown is visible
                        driver.execute_script("arguments[0].scrollIntoView(true);", supplier_customer)
                        print(f"Clicked on supplier_customer input for vendor '{vendor}'")

                        supplier_dropdown = WebDriverWait(driver, 60).until(
                            EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(),'{vendor}')]")))
                        driver.execute_script("arguments[0].click()", supplier_dropdown)
                        print(f"Selected vendor '{vendor}' from dropdown")
                    ## fill the account dropdown
                    if isinstance(category, str):
                        account = WebDriverWait(driver, 60).until(
                            EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Select an account"]')))
                        driver.execute_script("arguments[0].click()", account)
                        
                        driver.execute_script("arguments[0].scrollIntoView(true);", account)
                        print(f"Clicked on account input for category '{category}'")

                        account_dropdown = WebDriverWait(driver, 60).until(
                            EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(),'{category}')]")))
                        driver.execute_script("arguments[0].click()", account_dropdown)
                        print(f"Selected category '{category}' from dropdown")
                    ## after dropdown is filled, click apply and accept
                    apply_and_accept = WebDriverWait(driver, 60).until(
                        EC.visibility_of_element_located((By.XPATH, "//button[@class='idsTSButton idsF Button-button-c9b894e Button-quickbooks-2bdac97 Button-light-175522d Button-size-medium-7aafb41 Button-purpose-standard-3ffd7f8 Button-priority-primary-96b464c Modal-styledButton-3ec75cd Modal-primary-d9b05dd']")))
                    driver.execute_script("arguments[0].click()", apply_and_accept)
                    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "data-in-overlay")))
                    ## back to the first page
                    first_page = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'1')]")))
                    first_page.click()
                    return True
                ## catching the exception, if occured
                except (StaleElementReferenceException, TimeoutException, ElementClickInterceptedException) as e:
                    print(f"Exception occurred: {e}. Retrying...")
                    continue
        ## if no matching record in current page, pass and search for the next page
        except NoSuchElementException:
            pass

        ## Click the next page button
        next_page = driver.find_element(By.XPATH, "//button[contains(@aria-label,'Current Page')]/following-sibling::button[1]")
        driver.execute_script("arguments[0].click()", next_page)
        time.sleep(5)
    
    return False

## Loop through the Excel data
for i in range(len(descriptions)):
    description = descriptions[i]
    vendor = real_vendor[i]
    category = real_category[i]
    if not match_and_edit_record(description, vendor, category):
        print(f"Record with description '{description}' not found.")

