"""
@Author: Petrov Roman
@Date: 2022-08-20
@Description: This script is a test script for selenium automation framework. The script covers most of the
functionalities of 'WEHAGO' application.

Test names describe the functionality covered by test. Next functionalities
were not covered by the script: PREFERENCES -> import\export, link etc... , CONTACT MOVE/COPY. The reason is the
specifics of a blackbox testing.

Tests are ordered and should run in specified order.(pytest-order plugin). All plugins are included into pyproject.toml
file.

Tests store test result data into allure-report folder. This is done by parametrizing the run configuration.
"""

import datetime
import time
import unittest

import allure
import allure_commons.types
import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
    _phone = '01012345678'
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
        cls.options.add_experimental_option("useAutomationExtension", False)
        cls.options.add_experimental_option("excludeSwitches", ['enable-automation'])
        cls.driver.maximize_window()
        cls.driver.get("https://www.wehago.com")
        cls.driver.implicitly_wait(1)

    @pytest.mark.order(1)
    def test_Login(self):
        wait(self.driver, 10).until(cond.presence_of_element_located((By.ID, 'login'))).click()
        self.driver.find_element(By.ID, 'inputId').send_keys('testsw3')
        self.driver.find_element(By.ID, 'inputPw').send_keys('1q2w3e4r')
        self.driver.find_element(By.CLASS_NAME, 'WSC_LUXButton').click()
        try:
            if wait(self.driver, 10).until(cond.presence_of_element_located((By.CLASS_NAME, 'duplicate_login'))):
                self.driver.find_element(By.XPATH,
                                         '//button[contains(@class, "WSC_LUXButton")]//*[contains(., "Confirm")]/..').click()
        except (NoSuchElementException, TimeoutException):
            pass

        assert wait(self.driver, 10).until(
            cond.presence_of_element_located((By.CLASS_NAME, 'tit'))).text == 'WEHAGO, All-in-one Enterprise Platform'

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

    @pytest.mark.order(2)
    def test_Contacs(self):
        wait(self.driver, 10).until(cond.presence_of_element_located((By.ID, 'MAIN-SVC_contacts'))).click()
        assert wait(self.driver, 5).until(cond.presence_of_element_located((
            By.CLASS_NAME, 'sub_header'))).find_element(By.TAG_NAME, 'h1').text == 'contact'

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot2',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

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

        # add group info
        group = self.driver.find_element(By.TAG_NAME, 'canvas')

        time.sleep(0.5)

        action = ActionBuilder(self.driver)
        x = group.location['x'] + 5
        y = group.location['y'] + 5
        action.pointer_action.move_to_location(x=x, y=y).click()
        action.perform()

        time.sleep(0.5)

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot3',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        self.driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[4]/button[2]').click()

        # add company information
        self.driver.find_element(By.ID, 'enroll_company_name0').send_keys(self.__class__._cname)
        self.driver.find_element(By.ID, 'enroll_full_path0').send_keys(self.__class__._org)
        self.driver.find_element(By.ID, 'enroll_position_name0').send_keys(self.__class__._rank)
        self.driver.find_element(By.ID, 'enroll_task0').send_keys(self.__class__._task)

        # upload business card mock
        self.driver.find_element(By.ID, 'inputFile_front0').send_keys(self.card_front)
        self.driver.find_element(By.ID, 'inputFile_back0').send_keys(self.card_back)

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot3.1',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

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
        time.sleep(0.5)
        self.driver.find_element(By.CLASS_NAME, 'btn_search').click()
        time.sleep(0.5)
        self.driver.find_elements(By.XPATH,
                                  '//button[contains(@class, "link_post")]//span[contains(@class, "txt_addr")]/..')[
            0].click()
        self.driver.switch_to.default_content()
        self.driver.find_element(By.ID, 'companyAddress2_0').send_keys('101')

        time.sleep(0.5)
        self.__class__._workaddr = wait(self.driver, 5).until(
            cond.presence_of_element_located((By.ID, 'companyAddress1_0'))).get_property('value')

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot3.2',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

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
        self.driver.find_elements(By.XPATH,
                                  '//button[contains(@class, "link_post")]//span[contains(@class, "txt_addr")]/..')[
            0].click()
        self.driver.switch_to.default_content()
        self.driver.find_element(By.ID, 'address2_0').send_keys('202')

        time.sleep(0.5)
        self.__class__._homeaddr = wait(self.driver, 5).until(
            cond.presence_of_element_located((By.ID, 'address1_0'))).get_property('value')

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

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot3.3',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

    @pytest.mark.order(4)
    def test_AddGroup(self):
        # add group
        self.driver.find_element(By.XPATH, '//button[@class="add_group"]//*[contains(.,"Create group")]/..').click()
        self.driver.find_element(By.ID, 'input_new_group').send_keys('test')
        self.driver.find_element(By.CSS_SELECTOR,
                                 '#my_group_list > div.group_box.group_box_set > div.btn_group_set > button.LUX_basic_btn').click()

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot4',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        # delete group
        self.driver.find_element(By.ID, 'btn_edit1').click()
        self.driver.find_element(By.CSS_SELECTOR,
                                 '#edit_list1 > div > div > div > ul > li:nth-child(2) > button').click()
        self.driver.find_element(By.CSS_SELECTOR, '#confirm').click()

    @pytest.mark.order(5)
    def test_Search(self):
        # add mock contacts
        self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div/div/div/div[1]/div[2]/div[1]/button').click()
        self.driver.find_element(By.ID, 'enroll_lastName').send_keys('mock1')
        self.driver.execute_script("arguments[0].click();", self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[2]/div/button[2]'))

        self.driver.find_element(By.XPATH, '//*[@id="menu_all"]/a').click()

        wait(self.driver, 30).until(cond.presence_of_element_located((
            By.XPATH,
            '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div/div/div/div[1]/div[2]/div[1]/button'))).click()
        wait(self.driver, 10).until(cond.presence_of_element_located((By.ID, 'enroll_lastName'))).send_keys('mock2')
        self.driver.execute_script("arguments[0].click();", self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[2]/div/button[2]'))

        time.sleep(1)

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot5',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        # search for Smith
        self.driver.find_element(By.ID, 'searchContactInfo').send_keys(self.__class__._lname + self.__class__._fname)
        self.driver.find_element(By.ID, 'searchContactInfo').send_keys(Keys.ENTER)

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot5.1',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        self.driver.find_element(By.ID, 'searchContactInfo').send_keys(' ')
        self.driver.find_element(By.ID, 'searchContactInfo').clear()

        # display all contacts
        self.driver.find_element(By.XPATH, '//*[@id="menu_all"]/a').click()

    @pytest.mark.order(6)
    def test_Sort(self):
        wait(self.driver, 10).until(cond.visibility_of_all_elements_located((By.CSS_SELECTOR, '#contactsList > li')))

        # sort by time
        self.driver.find_element(By.XPATH, '//*[@id="contactListMenu"]/div/div[1]/button').click()
        self.driver.find_element(By.ID, 'sort_update').click()

        time.sleep(0.5)

        contacts = self.driver.find_element(By.ID, 'contactsList').find_elements(By.CLASS_NAME, 'char')
        assert contacts[0].text > contacts[1].text

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot6',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        # sort by alphabet
        self.driver.find_element(By.XPATH, '//*[@id="contactListMenu"]/div/div[1]/button').click()
        self.driver.find_element(By.ID, 'sort_ganada').click()

        time.sleep(0.5)

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot6.1',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

    @pytest.mark.order(7)
    def test_Favorites(self):
        # add to fav
        self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.ID, 'LUXBookMark1'))

        self.driver.find_element(By.XPATH, '//*[@id="menu_fav"]/a').click()

        time.sleep(0.5)

        assert self.driver.find_element(By.CSS_SELECTOR, '#menu_fav > a > span').text == '1'

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot7',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        # display all contacts
        self.driver.find_element(By.XPATH, '//*[@id="menu_all"]/a').click()

    @pytest.mark.order(8)
    def test_DeleteContacts(self):
        # check all contacts
        self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.ID, 'checkbox_all'))

        # uncheck main contact
        self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.ID, 'checkbox_item1'))

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot8',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        # delete checked contacs
        self.driver.execute_script("arguments[0].click();", self.driver.find_element(
            By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/div/button[1]'))
        self.driver.find_element(
            By.XPATH,
            '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[3]/div[2]/div/div/div[2]/button[2]').send_keys(
            Keys.SPACE)

        time.sleep(2)

        assert self.driver.find_element(By.XPATH, '//*[@id="menu_all"]/a/span').text == '1'

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot8.1',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

    @pytest.mark.order(9)
    def test_ContactDetail(self):
        contact = self.driver.find_element(By.ID, 'contactsList').find_elements(By.TAG_NAME, 'li')[-1].find_element(
            By.TAG_NAME, 'a')
        contact.click()

        time.sleep(0.5)

        assert self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div/div/div/div[1]/div[3]/div[2]/div[2]/div[1]/div[1]/h2'). \
                   text == self.__class__._lname + self.__class__._fname + ' '
        assert self.driver.find_element(
            By.CSS_SELECTOR, '#tbl_base > table > tbody > tr:nth-child(1) > td > div > a').text == self.__class__._phone
        assert self.driver.find_element(
            By.CSS_SELECTOR, '#tbl_base > table > tbody > tr:nth-child(2) > td > div').text == self.__class__._email

        assert self.driver.find_element(
            By.CSS_SELECTOR, '#tbl_company0 > table > tbody > tr:nth-child(1) > td > div').text == self.__class__._cname
        assert self.driver.find_element(
            By.CSS_SELECTOR, '#tbl_company0 > table > tbody > tr:nth-child(2) > td > div').text == self.__class__._org
        assert self.driver.find_element(
            By.CSS_SELECTOR, '#tbl_company0 > table > tbody > tr:nth-child(3) > td > div').text == self.__class__._rank
        assert self.driver.find_element(
            By.CSS_SELECTOR, '#tbl_company0 > table > tbody > tr:nth-child(4) > td > div').text == self.__class__._task

        assert self.driver.find_element(By.ID, 'namecardFront_0')
        assert self.driver.find_element(By.ID, 'namecardBack_0')

        assert self.driver.find_element(
            By.CSS_SELECTOR,
            '#tbl_company0 > table > tbody > tr:nth-child(6) > td > div').text == f'{self.__class__._workaddr} 101'

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot9',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        assert self.driver.find_element(
            By.CSS_SELECTOR,
            '#tbl_addition > table > tbody > tr:nth-child(1) > td > div').text == f'{self.__class__._homeaddr} 202'
        assert self.driver.find_element(
            By.CSS_SELECTOR,
            '#tbl_addition > table > tbody > tr:nth-child(2) > td > div > a').text == f'http://{self.__class__._hp}'
        assert self.driver.find_element(
            By.CSS_SELECTOR, '#detail_birth_date').text == datetime.date.today().strftime(
            '%Y. %m. %d. (Solar calendar)')
        assert self.driver.find_element(
            By.CSS_SELECTOR,
            '#tbl_addition > table > tbody > tr:nth-child(4) > td > div > p').text == self.__class__._memo
        assert self.driver.find_element(
            By.CSS_SELECTOR,
            '#tbl_addition > table > tbody > tr:nth-child(5) > td > div > div > span').text == self.__class__._tag

    @pytest.mark.order(10)
    def test_ActivityRecord(self):
        self.driver.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/ul/li[2]/a').click()

        assert wait(self.driver, 10).until(cond.presence_of_element_located((By.CLASS_NAME, 'log_list')))

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot10',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        # back to all contacts
        self.driver.find_element(By.XPATH, '//*[@id="menu_all"]/a').click()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.execute_script("arguments[0].click();", cls.driver.find_element(By.ID, 'checkbox_all'))
        cls.driver.execute_script("arguments[0].click();", cls.driver.find_element(By.XPATH,
                                                                                   '//*[@id="app"]/div/div[2]/div[2]/div[1]/div/button[1]'))
        cls.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div/div/div/div[3]/div[2]/div/div/div[2]/button[2]').send_keys(
            Keys.SPACE)

        # empty trash
        cls.driver.find_element(By.XPATH,
                                '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/ul/li[3]/button').click()
        cls.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div/div/div/div[3]/div[2]/div/div/div[2]/button[2]').send_keys(
            Keys.SPACE)

        # quit driver
        cls.driver.quit()


if __name__ == '__main__':
    pytest.main()