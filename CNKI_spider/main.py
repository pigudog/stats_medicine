# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

'''
安装第三方模块
pip install pandas
pip install openpyxl
pip install selenium

'''

import os
import time

from selenium.webdriver.remote.webelement import WebElement
import core.core_utils as utils
from core.core_chrome import CoreChrome


class Main(CoreChrome):

    def __init__(self):
        BASEDIR = os.getcwd() #当前工作路径
        CHROME_PATH = os.path.join(BASEDIR, 'chrome\\chrome.exe')
        CHROME_DRIVER_PATH = os.path.join(BASEDIR, 'chrome\\chromedriver.exe')
        USER_PATH = os.path.join(BASEDIR, 'chrome\\userdata')
        super(Main, self).__init__(CHROME_DRIVER_PATH, CHROME_PATH, USER_PATH)
        
    def run(self):
        utils.create_dir('file')
        utils.clear_dir('file')
        # 先打开网页噻
        self.get('https://www.cnki.net/')

        # 点击高级检索
        high_search_ele: WebElement = self.visible_css_element('#highSearch') 
        if high_search_ele:
            high_search_url = high_search_ele.get_attribute('href')
            self.get(high_search_url)
        
        #题名:(糖尿病视网膜病变)
        self.retrieval_first_line_input('篇名', '糖尿病视网膜病变')

        gradetxt_dd_eles: WebElement = self.visible_css_elements('#gradetxt dd') # 定位搜索主div dd
        # and 主题:(发病机制 or 病机) 
        self.retrieval_line_input(gradetxt_dd_eles[1], 'AND', '主题', '发病机制')
        self.retrieval_line_input(gradetxt_dd_eles[2], 'OR', '主题', '病机')

        #and 题名:(现状 or 进展 or 综述 or 概况 or 概述))
        # ele = self.add_retrieval_line()
        # self.retrieval_line_input(ele, 'AND', '篇名', '现状')
        # ele = self.add_retrieval_line()
        # self.retrieval_line_input(ele, 'OR', '篇名', '进展')
        # ele = self.add_retrieval_line()
        # self.retrieval_line_input(ele, 'OR', '篇名', '综述')
        # ele = self.add_retrieval_line()
        # self.retrieval_line_input(ele, 'OR', '篇名', '概况')
        # ele = self.add_retrieval_line()
        # self.retrieval_line_input(ele, 'OR', '篇名', '概述')

        #and 出版时间:[2018-01-01 TO *}
        datebox0_ele: WebElement = self.visible_css_element('#datebox0') # 发表时间
        self.execute_script('arguments[0].removeAttribute("readonly")',datebox0_ele)
        datebox0_ele.send_keys('2018-01-01')

        self.visible_css_element('.btn-search').click() #检索
        self.execute_script('window.scrollTo(0,document.body.scrollHeight)')

        self.execute_script("document.documentElement.scrollTop=10000")

        # 指定页数翻页保存表格
        # 处理函数
        # css
        # 页数
        page_count = self.compute_page_count()
        if page_count > 1 :
            self.page_down(self.write_table,'.pages', '.result-table-list td', '.pages div.pagesnums a', page_count)
        else:
            self.write_table()

    def compute_page_count(self):
        '''计算总页数以实现翻页'''
        are_page_count_el = self.visible_css_element('#perPageDiv span')
        text = are_page_count_el.text
        are_page_count = utils.extracting_numbers(text)

        result_count_el = self.visible_css_element('.pagerTitleCell em')
        text = result_count_el.text
        result_count = utils.extracting_numbers(text)

        page_count = utils.round_up(result_count/are_page_count)
        return page_count

    def write_table(self,page_index):
        '''获取到表格后的操作函数，可在这修改成其它形式'''
        table_ele: WebElement = self.visible_css_element('.result-table-list') # 发表时间
        df = self.settr_column_datas(table_ele)
        file = f'file\\{page_index}_{utils.timestamp()}.xlsx'
        df.to_excel(file)

    def add_retrieval_line(self):
        '''添加一行新的检索条件，并返回元素Element'''
        add_line_ele: WebElement = self.visible_css_element('#gradetxt dt a') # 点击第一行左边下拉框
        add_line_ele.click()
        gradetxt_dd_eles: WebElement = self.visible_css_elements('#gradetxt dd') # 定位搜索主div dd
        print(len(gradetxt_dd_eles))
        return gradetxt_dd_eles[-1]

    def retrieval_first_line_input(self, category, text):
        '''填写首行检索条件'''
        sort_ele: WebElement = self.visible_css_element('#gradetxt .nological+div .sort.reopt span') # 点击第一行左边下拉框
        sort_ele.click()
        self.visible_linktext_element(category).click() # 选择下拉框选项
        self.move_to_offset(50,50) # 移动一下鼠标
        gradetxt_1 = self.visible_css_element('#gradetxt .nological+div div~input') 
        self.css_el_input(gradetxt_1, text)

    def retrieval_line_input(self, main_ele, logic, category, text):
        '''填写一行检索条件'''
        logical_ele: WebElement = self.css_to_element(main_ele,'.logical')  # 点击第三行左边第一个下拉框
        logical_ele.click()
        self.visible_linktext_element(logic).click() # 选择下拉框选项
        logical_ele: WebElement = self.css_to_element(main_ele,'.reopt') # 点击第三行左边第二个下拉框
        logical_ele.click()
        self.visible_linktext_element(category).click() # 选择下拉框选项
        gradetxt = self.css_to_element(main_ele,'.input-box div~input') # 输入， 添加检索栏gradetxt-（2）递增
        self.css_el_input(gradetxt, text)


if __name__ == '__main__':

    main = Main()
    main.run()

    # 合并所有表格
    # total = utils.merge_excel_to_dir('file')
    # total.to_excel('res.xlsx')