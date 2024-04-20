#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import time
import logging

from selenium.webdriver import Chrome, ActionChains, ChromeOptions, ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import WebDriverException, NoSuchElementException, ElementNotInteractableException, TimeoutException

import core.core_utils as utils

class CoreChrome(Chrome):
    def __init__(self,driver_path, chrome_path, user_path):
        
         #日志记录器
        self.logger = logging.getLogger(__name__)

        '''浏览器配置'''
        
        self.chrome_options = ChromeOptions()
        self.chrome_options.binary_location = chrome_path
        self.chrome_options.add_argument(f"--user-data-dir={user_path}") #设置用户数据目录
        self.chrome_options.add_argument('--start-maximized')
        self.chrome_options.add_argument('ignore-certificate-errors') 
        self.chrome_options.add_argument('--disable-infobars')
        self.chrome_options.add_argument('--disable-blink-features') 
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled') 

        self.chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']) 

        prefs = {
                'profile.default_content_settings.popups': 0, #禁用弹出窗口
                'credentials_enable_service' : False, # 屏蔽'保存密码'提示框
                'profile.password_manager_enabled' : False # 屏蔽'保存密码'提示框
            }
        self.chrome_options.add_experimental_option('prefs', prefs)

        self.service = ChromeService(executable_path=driver_path)
        try:
            super(CoreChrome, self).__init__(service=self.service , options=self.chrome_options)
        except Exception as e:
            self.logger.error(f'查看chrome.exe是否存在于当前目录的chrome文件夹当中, {e}')

        self.logger.info('浏览器初始化完成！')
    
    def css_to_element(self,sub_ele, css_selector):
        """
        基于元素查找单个子元素
        css_selector：css选择器字符串
        return:可见返回元素
        """
        try:
            element = sub_ele.find_element(By.CSS_SELECTOR, css_selector)
            return element
        except Exception as e: 
            self.logger.error(f'css_to_element error：{css_selector}, {e}')
            return None
        
    def css_to_elements(self,sub_ele, css_selector):
        """
        基于元素查找多个子元素
        css_selector：css选择器字符串
        return:可见返回元素列表
        """
        try:
            elements = sub_ele.find_elements(By.CSS_SELECTOR, css_selector)
            return elements
        except Exception as e: 
            self.logger.error(f'css_to_elements error：{css_selector}, {e}')
            return None
        
    def start_client(self):
        """Called before starting a new session.

        This method may be overridden to define custom startup behavior.
        """
        # self.navigator_stealth_min()
    
    def navigator_stealth_min(self):
        """
        目前网上的反检测方法几乎都是掩耳盗铃，因为模拟浏览器有几十个特征可以被检测，仅仅隐藏 webdriver 这一个值是没有任何意义的。
        尝试隐藏webdriver特征
        """
        with open('stealth.min.js') as f:
            js = f.read()
            self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
            })

    def navigator_undefined(self):
        """
        chrome在79和79版之后可用
        webdriver.navigator标志=> undefined
        """
        self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                """
            })
    
    def located_css_element(self, css_selector, timeout=15):
        """
        单个元素存在DOM中返回元素，用于获取元素数据
        css_selector：css选择器字符串
        timeout:等待超时默认15秒
        return:可见返回元素
        """
        try:
            errors = [NoSuchElementException, ElementNotInteractableException]
            wait = WebDriverWait(self , timeout=timeout, poll_frequency=1, ignored_exceptions=errors)
            # 循环检查元素是否存在于页面的DOM上。这并不一定意味着元素是可见的。
            element = wait.until(ES.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            return element
        except TimeoutException:
            self.logger.warning(f'visible_css_element Timeout：{css_selector}')
            return None
        except Exception as e: 
            self.logger.error(f'visible_css_element error：{css_selector}, {e}')
            return None
        
    def located_css_elements(self, css_selector, timeout=15):
        """
        多个元素存在DOM中返回元素列表，用于获取元素数据
        css_selector：css选择器字符串
        timeout:等待超时默认15秒
        return:可见返回元素
        """
        try:
            errors = [NoSuchElementException, ElementNotInteractableException]
            wait = WebDriverWait(self , timeout=timeout, poll_frequency=1, ignored_exceptions=errors)
            # 循环检查网页上是否存在至少一个元素。
            elements = wait.until(ES.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))
            return elements
        except TimeoutException:
            self.logger.warning(f'visible_css_elements Timeout：{css_selector}')
            return None
        except Exception as e: 
            self.logger.error(f'visible_css_elements error：{css_selector}, {e}')
            return None

    def visible_css_element(self, css_selector, timeout=15):
        """
        单个元素可见返回元素，用于点击元素
        css_selector：css选择器字符串
        timeout:等待超时默认15秒
        return:可见返回元素
        """
        try:
            errors = [NoSuchElementException, ElementNotInteractableException]
            wait = WebDriverWait(self , timeout=timeout, poll_frequency=1, ignored_exceptions=errors)
            # 循环检查元素是否存在于页面的DOM上并且可见。可见性意味着不仅显示视图，而且视图的高度和宽度都大于0。
            element = wait.until(ES.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
            return element
        except TimeoutException:
            self.logger.warning(f'visible_css_element Timeout：{css_selector}')
            return None
        except Exception as e: 
            self.logger.error(f'visible_css_element error：{css_selector}, {e}')
            return None

    def visible_css_elements(self, css_selector, timeout=15):
        """
        多个元素可见返回元素，用于点击场合
        css_selector：css选择器字符串
        timeout:等待超时默认15秒
        return:可见返回元素
        """
        try:
            errors = [NoSuchElementException, ElementNotInteractableException]
            wait = WebDriverWait(self , timeout=timeout, poll_frequency=1, ignored_exceptions=errors)
            # 循环检查所有元素是否存在于页面的DOM上并且可见。可见性意味着不仅显示视图，而且视图的高度和宽度都大于0。
            elements = wait.until(ES.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector)))
            return elements
        except TimeoutException:
            self.logger.warning(f'visible_css_elements Timeout：{css_selector}')
            return None
        except Exception as e: 
            self.logger.error(f'visible_css_elements error：{css_selector}, {e}')
            return None
    
    def visible_linktext_element(self, link_text, timeout=15):
        """
        单个元素可见返回元素，用于点击元素
        link_text：链接包含的字符串
        timeout:等待超时默认15秒
        return:可见返回元素
        """
        try:
            errors = [NoSuchElementException, ElementNotInteractableException]
            wait = WebDriverWait(self , timeout=timeout, poll_frequency=1, ignored_exceptions=errors)
            # 循环检查元素是否存在于页面的DOM上并且可见。可见性意味着不仅显示视图，而且视图的高度和宽度都大于0。
            element = wait.until(ES.visibility_of_element_located((By.LINK_TEXT, link_text)))
            return element
        except TimeoutException:
            self.logger.warning(f'visible_linktext_element Timeout：{link_text}')
            return None
        except Exception as e: 
            self.logger.error(f'visible_linktext_element error：{link_text}, {e}')
            return None

    def text_css_element(self, text, css_selector, timeout=15):
        """
        单个元素是否存在text返回元素
        text：元素存在的text
        css_selector：节点选择器字符串
        timeout:等待超时默认15秒
        return:存在text返回元素
        """
        try:
            errors = [NoSuchElementException, ElementNotInteractableException]
            wait = WebDriverWait(self , timeout=timeout, poll_frequency=1, ignored_exceptions=errors)
            text_to_be_present = wait.until(ES.text_to_be_present_in_element((By.CSS_SELECTOR, css_selector), text) )
            if text_to_be_present:
                return self.find_element(By.CSS_SELECTOR,css_selector)
            
        except TimeoutException:
            self.logger.warning(f'text_css_element Timeout：{css_selector}')
            return None
        except Exception as e: 
            self.logger.error(f'text_css_element error：{css_selector}, {e}')
            return None
        
    def css_el_input(self, element, value):
        '''
        对元素进行行清空并进行输入
        '''
        element.clear()
        element.send_keys(value) #输入

            
    def move_to_offset(self, x, y):
        """
        从当前光标位置（原点）偏移 x,y
        """
        try:
            ActionChains(self).move_by_offset(x, y).perform() 
            return True  
        except Exception as e: 
            self.logger.error(f'move_to_offset error：{e}')
            return False
        
    def move_to_element(self, element):
        """
        移动到元素中心点
        """
        try:
            ActionChains(self).move_to_element(element).perform() 
            return True  
        except Exception as e: 
            self.logger.error(f'move_to_element error：{e}')
            return False
        
    def check_title_is(self, title_txt, timeout=15):
        """
        检查网页标题是否是指定值，是返回True，否则返回False
        """
        try:
            errors = [NoSuchElementException, ElementNotInteractableException]
            wait = WebDriverWait(self , timeout=timeout, poll_frequency=1, ignored_exceptions=errors)
            ttitle_is = wait.until(ES.title_is(title=title_txt) )
            return ttitle_is  
        except TimeoutException:
            self.logger.warning(f'text_css_element Timeout：{title_txt}')
            return False
        except Exception as e: 
            self.logger.error(f'check_title_is error：{e}')
            return False
        
    def page_down(self,func,goto_selector, wait_selector, css_selector, count):
        for i in range(1, count+1):
            # self.visible_css_elements(wait_selector) 
            page_els = self.visible_css_elements(css_selector)
            # 按顺序筛选出当前要点击的页
            page_el = list(filter(lambda el: el.text==str(i), page_els ) )[0]
            if page_el:
                goto_pags_el = self.visible_css_element(goto_selector) 
                self.element_scroll_center(goto_pags_el)
                self.move_to_element(goto_pags_el)
                page_el.click()
            
            func()
    
    def page_down(self,func,goto_selector, wait_selector, css_selector, count):
        table_html = ''

        for i in range(1, count+1):
            for cs in range(6):
                # 点不到元素报错及表格内容比较，重试最大次数6次
                try:
                    self.visible_css_elements(wait_selector) 
                    page_els = self.visible_css_elements(css_selector)
                    # 按顺序筛选出当前要点击的页
                    page_el = list(filter(lambda el: el.text==str(i), page_els ) )[0]
                    if page_el:
                        goto_pags_el = self.visible_css_element(goto_selector) 
                        self.element_scroll_center(goto_pags_el)
                        self.move_to_element(goto_pags_el)
                        page_el.click()

                        tmp_html = self.get_css_element_outerhtml(wait_selector) 
                        # print(len(table_html),len(tmp_html))
                        if tmp_html != table_html:
                            print(f'点击第{i}页完成！')
                            table_html = tmp_html
                            func(i)
                            break
                        else:
                            time.sleep(1)
                            continue
                except Exception as e:
                    print(e)
                    time.sleep(1)
            
    def settr_column_datas(self,element):
        """
        读取html表格，并将带link的表的某列，替换到无link的表
        """
        df = utils.readhtml_to_df(element, 0, 0 )
        df2 = utils.readhtml_to_df(element, 0, 0, 'body')

        df['题名'] = df2['题名'].values

        return df

    def get_css_element_outerhtml(self,selector):
        """
        获取元素自身html
        """
        element = self.visible_css_element(selector) 
        html =  element.get_attribute('outerHTML') 
        return html


    def element_scroll_center(self,element):
        """
        将元素滚动到视图水平居中位置
        """
        self.execute_script('arguments[0].scrollIntoView({block:"center",inline:"center"});',element)
        
    def check_number_of_windows(self, count, timeout=15):
        """
        检查网页窗口是否是指定值，是返回True，否则返回False
        """
        try:
            errors = [NoSuchElementException, ElementNotInteractableException]
            wait = WebDriverWait(self , timeout=timeout, poll_frequency=1, ignored_exceptions=errors)
            number_of_windows = wait.until(ES.number_of_windows_to_be(count) )
            return number_of_windows  
        except TimeoutException:
            self.logger.warning(f'check_number_of_windows Timeout：{count}')
            return False
        except Exception as e: 
            #self.logger.error(f'check_number_of_windows error：{e}')
            return False
