import pytest
import unittest

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.ui import WebDriverWait as wait
from webdriver_manager.chrome import ChromeDriverManager


class ContactTests(unittest.TestCase):
    driver = None
    options = Options()
    profile_img = 'C:/Users/x3m09/Downloads/DOUZONE/web-automation/assets/contact.jpg'
    card_front = 'C:/Users/x3m09/Downloads/DOUZONE/web-automation/assets/cardfront.png'
    card_back = 'C:/Users/x3m09/Downloads/DOUZONE/web-automation/assets/cardback.jpg'

    _fname = 'John'
    _lname = 'Smith'
    _phone = '010-123-45678'
    _email = 'workmail@company.com'
    _cname = 'Company LTD'
    _org = 'Sales'
    _rank = 'Sales manager'
    _task = 'Selling the product'
    _group = 'new'
    _hp = 'url.com'
    _memo = 'memo'
    _tag = 'sales'
    _workaddr: str
    _homeaddr: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.options.platform_name = 'Windows 11'
        cls.options.add_experimental_option("useAutomationExtension", 'false')
        cls.options.add_experimental_option("excludeSwitches", ['enable-automation'])
        cls.driver.maximize_window()
        cls.driver.get("https://www.wehago.com")

    @pytest.mark.order(1)
    def test_Login(self):
        wait(self.driver, 10).until(cond.presence_of_element_located((By.ID, 'login'))).click()
        self.driver.find_element(By.ID, 'inputId').send_keys('testsw3')
        self.driver.find_element(By.ID, 'inputPw').send_keys('1q2w3e4r')
        self.driver.find_element(By.CLASS_NAME, 'WSC_LUXButton').click()
        try:
            if wait(self.driver, 1).until(cond.presence_of_element_located((By.CLASS_NAME, 'duplicate_login'))):
                self.driver.find_element(By.XPATH,
                                         '//button[contains(@class, "WSC_LUXButton")]//*[contains(., "Confirm")]/..').click()
        except:
            pass

        assert wait(self.driver, 5).until(
            cond.presence_of_element_located((By.CLASS_NAME, 'tit'))).text == 'WEHAGO, All-in-one Enterprise Platform'

    @pytest.mark.order(2)
    def test_Contacs(self):
        wait(self.driver, 10).until(cond.presence_of_element_located((By.ID, 'MAIN-SVC_contacts'))).click()
        assert wait(self.driver, 5).until(cond.presence_of_element_located((
            By.CLASS_NAME, 'sub_header'))).find_element(By.TAG_NAME, 'h1').text == 'contact'

    @pytest.mark.order(3)
    def test_RegisterContact(self):

        # add contact information
        wait(self.driver, 10).until(cond.presence_of_element_located((
            By.XPATH,
            '//button[contains(@class, "LUX_basic_btn Confirm basic2")]//*[contains(., "Register contacts")]/..'))).click()
        wait(self.driver, 10).until(cond.presence_of_element_located((By.XPATH, '*//input[@type="file"]'))).send_keys(
            self.profile_img)
        self.driver.find_element(By.ID, 'enroll_lastName').send_keys(self.__class__._lname)
        self.driver.find_element(By.ID, 'enroll_firstName').send_keys(self.__class__._fname)
        self.driver.find_element(By.ID, 'phoneInputField0').send_keys(self.__class__._phone)
        self.driver.find_element(By.ID, 'selectPhoneObject0').click()
        wait(self.driver, 2).until(cond.presence_of_element_located((By.ID, 'scrollElement'))).find_elements(
            By.CLASS_NAME, 'WSC_LUXTooltip')[1].click()
        self.driver.find_element(By.ID, 'emailInputField0').send_keys(self.__class__._email)
        self.driver.find_element(By.ID, 'selectEmailObject0').click()
        wait(self.driver, 2).until(cond.presence_of_element_located((By.ID, 'scrollElement'))).find_elements(
            By.TAG_NAME, 'a')[1].click()
        self.driver.find_element(By.XPATH,
                                 '//button[contains(@class, "WSC_LUXButton")]//*[contains(., "Select group")]/..').click()
        """
        Unable to click on group element while automating creation of contact! Possible reason: no radio button in DOM, radio button
        was created by canvas.
        """
        self.driver.find_element(By.XPATH, '//*/div/canvas/..').click()
        wait(self.driver, 2).until(cond.element_to_be_clickable((
            By.XPATH, '/html/body/div[3]/div/div/div[4]/button[2]'))).click()

        # add company information
        self.driver.find_element(By.ID, 'enroll_company_name0').send_keys(self.__class__._cname)
        self.driver.find_element(By.ID, 'enroll_full_path0').send_keys(self.__class__._org)
        self.driver.find_element(By.ID, 'enroll_position_name0').send_keys(self.__class__._rank)
        self.driver.find_element(By.ID, 'enroll_task0').send_keys(self.__class__._task)

        # upload business card mock
        self.driver.find_element(By.ID, 'inputFile_front0').send_keys(self.card_front)
        self.driver.find_element(By.ID, 'inputFile_back0').send_keys(self.card_back)

        self.driver.execute_script("window.scrollTo(500,document.body.scrollHeight);")

        # add work address
        self.driver.find_element(By.XPATH,
                                 '//button[contains(@class, "WSC_LUXButton")]//*[contains(., "Search address")]/..').click()

        # switch to the first frame of address searching api
        iframe = wait(self.driver, 5).until(cond.presence_of_element_located((By.TAG_NAME, 'iframe')))
        self.driver.switch_to.frame(iframe)

        # switch to the second frame of address search api
        innerframe = wait(self.driver, 2).until(cond.presence_of_element_located((By.ID, '__daum__viewerFrame_1')))
        self.driver.switch_to.frame(innerframe)
        self.driver.find_element(By.ID, 'region_name').send_keys('seoul')
        self.driver.find_element(By.CLASS_NAME, 'btn_search').click()
        self.driver.implicitly_wait(0.5)
        self.driver.find_elements(By.XPATH,
                                  '//button[contains(@class, "link_post")]//span[contains(@class, "txt_addr")]/..')[
            0].click()
        self.driver.switch_to.default_content()
        self.driver.find_element(By.ID, 'companyAddress2_0').send_keys('101')

        self.__class__._workaddr = self.driver.find_element(By.ID, 'companyAddress1_0').get_attribute('value')

        # add additional info
        self.driver.find_elements(By.XPATH,
                                  '//button[contains(@class, "WSC_LUXButton")]//*[contains(., "Search address")]/..')[
            1].click()

        # switch to the first frame of address searching api
        iframe = wait(self.driver, 5).until(cond.presence_of_element_located((By.TAG_NAME, 'iframe')))
        self.driver.switch_to.frame(iframe)

        # switch to the second frame of address search api
        innerframe = wait(self.driver, 2).until(cond.presence_of_element_located((By.ID, '__daum__viewerFrame_2')))
        self.driver.switch_to.frame(innerframe)
        self.driver.find_element(By.ID, 'region_name').send_keys('seoul')
        self.driver.find_element(By.CLASS_NAME, 'btn_search').click()
        self.driver.implicitly_wait(0.5)
        self.driver.find_elements(By.XPATH,
                                  '//button[contains(@class, "link_post")]//span[contains(@class, "txt_addr")]/..')[
            0].click()
        self.driver.switch_to.default_content()
        self.driver.find_element(By.ID, 'address2_0').send_keys('202')

        self.__class__._homeaddr = self.driver.find_element(By.ID, 'address1_0').get_attribute('value')

        # add homepage
        self.driver.find_element(By.ID, 'enroll_homepage_url').send_keys(self.__class__._hp)

        # add birthday
        self.driver.find_element(By.CLASS_NAME, 'WSC_LUXDatePicker').find_element(By.TAG_NAME, 'button').click()
        self.driver.find_element(By.XPATH,
                                 '//button[contains(@class,"WSC_LUXButton")]//*[contains(.,"Today")]/..').click()

        # add memo
        self.driver.find_element(By.ID, 'memo').send_keys(self.__class__._memo)

        # add tag
        self.driver.find_element(By.CLASS_NAME, 'WSC_LUXTagField ').find_element(By.TAG_NAME, 'input').send_keys(
            self.__class__._tag + ';')

        # register contact
        self.driver.find_element(By.XPATH,
                                 '//button[contains(@class, "WSC_LUXButton")]//*[contains(., "Register")]/..').click()

        contact = wait(self.driver, 10).until(cond.presence_of_element_located((By.ID, 'contactsList'))).find_element(
            By.XPATH, '//span[@class="char"]')

        assert contact.text == self.__class__._lname + self.__class__._fname

    @classmethod
    def tearDownClass(cls) -> None:
        # cls.driver.find_element(By.CLASS_NAME, 'WSC_LUXCheckBox').find_element(By.XPATH, '//input[@type="checkbox"]').click()
        cls.driver.find_element(By.ID, 'checkbox_item0').click()
        wait(cls.driver, 1).until(cond.presence_of_element_located((
            By.XPATH, '//button[contains(@class, "WSC_LUXButton")]//*[contains(., "Delete")]/..'))).click()
        wait(cls.driver, 1).until(cond.presence_of_element_located((
            By.XPATH, '//button[contains(@class, "WSC_LUXButton")]//*[contains(., "Confirm")]/..'))).click()
        # cls.driver.quit()


if __name__ == '__main__':
    pytest.main()
