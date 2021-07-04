from selenium import webdriver
import time
import sys
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QLineEdit,QGridLayout,QTextBrowser,QMessageBox
from PyQt5.QtGui import QPixmap


class GUI(QWidget):

    def __init__(self):
        super(GUI,self).__init__()
        self.setWindowTitle('阿浩的电影下载器v1.0')
        self.resize(600,480)
        self.setup_ui()
        self.create_button()
        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(10)
        grid.addWidget(self.label,0,0)
        grid.addWidget(self.searchtext,0,1)
        grid.addWidget(self.Area_label,0,2)
        grid.addWidget(self.image_label,1,0,2,0)
        grid.addWidget(self.index_label,3,0)
        grid.addWidget(self.index_text,3,1)
        grid.addWidget(self.author_label,4,0,2,0)
        grid.addWidget(self.search,5,0)
        grid.addWidget(self.download,5,1)
        grid.addWidget(self.watch,5,2)
        grid.addWidget(self.quit,5,3)
        grid.addWidget(self.message_area,1,2,4,2)

    def setup_ui(self):
        self.author_label = QLabel("@author:zzh@wust  email:zhouzhehao0620@qq.com")
        image = QPixmap('./1.jpg')
        self.image_label = QLabel()
        self.image_label.setMaximumSize(320,290)
        self.image_label.setPixmap(image)
        self.label = QLabel("Enter Movie(then click search)")
        # 输入框
        self.searchtext = QLineEdit()
        # 显示框
        self.message_area = QTextBrowser()
        self.index_label = QLabel("Enter the Index")
        self.Area_label = QLabel("          Searching Result:")
        # 输入序号框
        self.index_text = QLineEdit()


    def create_button(self):
        # 创建搜索按钮
        self.search = QPushButton("Search")
        # 按下 获取搜索信息 
        self.search.clicked.connect(self.getinfo1)
        self.download = QPushButton("Download")
        self.download.clicked.connect(self.Download)
        self.watch = QPushButton("Watch on Line")
        self.watch.clicked.connect(self.WatchOnLine)
        self.quit = QPushButton('Quit')
        self.quit.clicked.connect(self.close)

    def getinfo1(self):
        video_name = self.searchtext.text()
        # 执行driver爬虫
        self.driver(video_name)

    def Download(self):
        # self.index = self.index_text.text()
        # self.index = self.index_text.text()
        # self.text = self.real_url[int(self.index)]
        # driver = webdriver.Chrome(executable_path='./chromedriver.exe')
        # driver.get(self.text)
        msg_box = QMessageBox.information(self,"Sorry","暂时只支持在线观看")


    def WatchOnLine(self):
        self.index = self.index_text.text()
        self.text = self.real_url[int(self.index)]
        msg_box = QMessageBox.information(self,"Movie's URL Here",self.text)

    def driver(self,video_name):
        self.real_url = []
        name_list = []
        detail_list = []
        people = []
        
        from selenium.webdriver.chrome.options import Options
        
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # 加载驱动
        driver = webdriver.Chrome(executable_path='./chromedriver.exe')
        # 获取网址
        driver.get('http://www.feijisu6.com/')

        #模仿用户输入关键字
        driver.find_element_by_xpath('//*[@id="kw"]').send_keys(video_name)

        #模仿用户点击按钮
        driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/form/div[2]/label').click()

        # 爬链接
        for link in driver.find_elements_by_xpath('//*[@id="result"]/li/h2/a'):
            self.real_url.append(link.get_attribute('href'))
        # 所有结果
        for name in driver.find_elements_by_xpath('//*[@id="result"]/li/h2/a'):
            name_list.append(name.text)
        # 详情
        for detail in driver.find_elements_by_xpath('//*[@id="result"]/li/span'):
            detail_list.append(detail.text)
        # 演员表
        for person in driver.find_elements_by_xpath('//*[@id="result"]/li/p'):
            people.append(person.text)
        for i in range(len(self.real_url)):
            self.message_area.append((f"index:{i}"))
            self.message_area.append((name_list[i]))
            self.message_area.append((detail_list[i]))
            self.message_area.append((people[i]))
            self.message_area.append("")
        
        driver.quit()

# def driver_real():
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    w = GUI()
    w.show()
    sys.exit(app.exec_())