# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:35:48 2020

@author: Cao
"""

# -*- coding:utf-8 -*-
from PIL import Image
from time import sleep
from selenium import webdriver
import cv2 as cv
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('w3c', False)
caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {'performance': 'ALL'}
class SliderVerificationCode(object):
    def __init__(self):  # 初始化一些信息
        self.left = 70  # 定义一个左边的起点 缺口一般离图片左侧有一定的距离 有一个滑块
        self.url = 'https://m.iqiyi.com/user.html?ivk_sa=bdw_1074#baseLogin'
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)  # 设置等待时间20秒
        self.phone = "19906979970"
        self.passwd = "password"
 
    def input_name_password(self):  # 输入账号密码
        self.driver.get(self.url)
        self.driver.maximize_window()
        input_name = self.driver.find_element_by_id('phoneNumber')
        input_pwd = self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/form/section/div[1]/div[2]/div[3]/input")
        input_name.send_keys(self.phone)
        input_pwd.send_keys(self.passwd)
        sleep(3)
    
    def click_login_button(self):  # 点击登录按钮,出现验证码图片
        # 点击登录
        self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/form/section/div[1]/div[4]/a').click()
        
        sleep(3)
    
    def get_geetest_image(self):  # 获取验证码图片
        gapimg = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'jigsaw-bg')))
        sleep(2)
        gapimg.screenshot(r'./captcha1.png')
        image = Image.open('captcha1.png')
        region = image.crop([70,30,290,170])
        region.save('captcha.png')
    
    def get_pos(self):
        image = cv.imread('captcha.png', 0)
        blurred = cv.GaussianBlur(image, (3, 3), 0)
        canny = cv.Canny(blurred, 0, 500)
        contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for i, contour in enumerate(contours):
            if 800 < cv.contourArea(contour) < 2500 and 120 < cv.arcLength(contour, True):
                x, y, w, h = cv.boundingRect(contour)
                return x+self.left
        return 150
    
    def get_move_track(self, gap):
        track = []  # 移动轨迹
        current = 0  # 当前位移
        # 减速阈值
        mid = gap * 4 / 5  # 前4/5段加速 后1/5段减速
        t = 0.2  # 计算间隔
        v = 0  # 初速度
        while current < gap:
            if current < mid:
                a = 5  # 加速度为+5
            else:
                a = -5  # 加速度为-5
            v0 = v  # 初速度v0
            v = v0 + a * t  # 当前速度
            move = v0 * t + 1 / 2 * a * t * t  # 移动距离
            current += move  # 当前位移
            track.append(round(move))  # 加入轨迹
        return track
    
    def move_slider(self, gap):
        print("开始滑动")
        slider = self.wait.until(EC.presence_of_element_located((By.ID, 'test')))
        while 1:
            action = ActionChains(self.driver)
            action.click_and_hold(slider).perform()
            action.reset_actions()# 清除之前的action
            track = self.get_move_track(gap)
            for x in track:  # 只有水平方向有运动 按轨迹移动
                ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
                sleep(0.2)
            sleep(1)
            ActionChains(self.driver).release().perform()  # 松开鼠标
            sleep(5)
            
            try:
                alert = self.driver.find_element_by_id('test')
            except Exception as e:
                print ('get alert error: %s' % e)
                alert = ''
            if alert:
                print (u'滑块位移需要调整: %d'%gap)
                if gap > 240:
                    gap = 145
                gap += 15
                sleep(5)
            else:
                print ('滑块验证通过')
                break
 
    def main(self):
        self.input_name_password()
        self.click_login_button()
        self.get_geetest_image()
        gap = self.get_pos()
        print(gap)
        self.move_slider(gap)

if __name__ == "__main__":
    springAutumn = SliderVerificationCode()
    springAutumn.main()