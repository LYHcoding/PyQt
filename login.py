from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import sql
from PySide2.QtCore import Qt, Signal, QObject, Slot, QPoint
from PySide2.QtGui import QMouseEvent, Qt, QCursor
import sys
import echarts
import echartstest
# from threading import Thread  # 导入thread,PySide2 不支持 python 的多线程类 threading
from time import process_time


# 主界面
class mainwindow:
    count = 0
    click_id = 0

    # 初始菜单界面
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('main.ui')
        self.ui.mdi = QMdiArea()
        self.ui.setCentralWidget(self.ui.mdi)
        self.ui.action.triggered.connect(self.windowaction)
        self.ui.action_11.triggered.connect(self.windowaction)
        self.ui.action_9.triggered.connect(self.windowaction1)
        self.ui.action_12.triggered.connect(self.windowaction2)
        # self.ui.action.triggered.connect(self.new_winAction)
        # self.ui.action_11.triggered.connect(self.new_winAction)
        # self.ui.action_9.triggered.connect(self.new_winAction1)
        # self.ui.action_12.triggered.connect(self.new_winAction2)

    # # -------创建新线程函数
    # def new_winAction(self):
    #     thread = Thread(target=self.windowaction)   # 不含参数
    #     thread.start()  # 开启新线程
    #
    # def new_winAction1(self):
    #     thread = Thread(target=self.windowaction1)   # 不含参数
    #     thread.start()  # 开启新线程
    #
    # def new_winAction2(self):
    #     thread = Thread(target=self.windowaction2)   # 不含参数
    #     thread.start()  # 开启新线程

    # 打印被双击选中的列表单元格行数,根据其进行可视化展示
    def double_value(self, sub):
        # row = sub.row()
        # mainwindow.click_id = sql.selectid(row, 0)
        self.windowaction2()

    # 打印被单击选中的列表单元格行数
    def click_value(self, sub):
        row = sub.row()
        column = sub.column()
        # print("double row:", row, "\ndouble column:", column)
        mainwindow.click_id = sql.selectid(row, 0)
        select_value = sql.selectid(row, column)
        print(mainwindow.click_id, select_value)

    # 添加数据列表子窗口
    def windowaction(self):
        print('Triggered列表子窗口')
        t_start = process_time()
        # 子窗口增加一个
        mainwindow.count = mainwindow.count+1
        # 实例化多文档界面对象
        sub = QMdiSubWindow()
        # 向sub内添加内部控件
        sub.setWidget(QTextEdit())

        sub = QUiLoader().load('tablemsg.ui')
        # 设置新建子窗口的标题
        sub.setWindowTitle('项目数据列表--'+str(mainwindow.count))

        self.dataprint(sub)
        # 表格的双击事件捕获
        sub.tableWidget.doubleClicked.connect(self.double_value)
        # 表格的单击事件捕获
        sub.tableWidget.clicked.connect(self.click_value)
        # 将子窗口添加到Mdi区域
        self.ui.mdi.addSubWindow(sub)
        # 子窗口显示
        sub.show()
        t_stop = process_time()
        print("Elapsed time during the whole program in seconds:", t_stop - t_start)


    # 数据传输到列表子窗口
    def dataprint(self, sub):
        all_data = []
        all_data = sql.alldata()
        # print(all_data, type(all_data))
        i = 0
        # 更新的方法是,设置行数为 0
        sub.tableWidget.setRowCount(0)
        for the_data in all_data:
            # print(the_data)
            # 插入行
            sub.tableWidget.insertRow(i)
            project_id = QTableWidgetItem(str(the_data[0]))
            project_id.setTextAlignment(Qt.AlignCenter)
            sub.tableWidget.setItem(i, 0, project_id)

            variety = QTableWidgetItem(the_data[1])
            variety.setTextAlignment(Qt.AlignCenter)
            sub.tableWidget.setItem(i, 1, variety)
            project_name = QTableWidgetItem(the_data[2])
            sub.tableWidget.setItem(i, 2, project_name)
            tank_no = QTableWidgetItem(the_data[3])
            tank_no.setTextAlignment(Qt.AlignCenter)
            sub.tableWidget.setItem(i, 3, tank_no)
            start_time = QTableWidgetItem(str(the_data[4]))
            sub.tableWidget.setItem(i, 4, start_time)
            project_process = QTableWidgetItem(str(the_data[5]))
            project_process.setTextAlignment(Qt.AlignCenter)
            sub.tableWidget.setItem(i, 5, project_process)
            i += 1

            # 禁止编辑
            sub.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            # 整行选择
            sub.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

            # 调整列和行的大小
            sub.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            # sub.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            # 设置水平竖直表头是否显示
            # sub.tableWidget.horizontalHeader().setVisible(False)
            # sub.tableWidget.verticalHeader().setVisible(False)
            sub.tableWidget.resizeColumnsToContents()  # 根据内容调整列宽
            sub.tableWidget.resizeRowsToContents()

    # 安排子窗口在Mdi区域级联显示,即重叠
    def windowaction1(self):
        print('Triggered重叠')
        # cascadeSubWindows()：
        self.ui.mdi.cascadeSubWindows()
        # if q.text() == '平铺':
        #     # tileSubWindow():安排子窗口在Mdi区域平铺显示
        #     self.mdi.tileSubWindow()

    # 添加数据可视化子窗口
    def windowaction2(self):
        print('Triggered可视化子窗口, 选中批次：', mainwindow.click_id)
        t_start = process_time()
        # 子窗口增加一个
        mainwindow.count = mainwindow.count+1
        # 实例化多文档界面对象
        sub = QMdiSubWindow()
        # 向sub内添加内部控件
        sub.setWidget(QTextEdit())
        # 设置新建子窗口的标题
        # sub.setWindowTitle("可视化折线显示"+str(mainwindow.count))
        sub = QUiLoader().load('echarts.ui')

        # 设置浏览器网页为pyecharts图
        bro = QWebEngineView()
        bro.setHtml(echarts.drawallline(mainwindow.click_id))
        # bro.setHtml(echartstest.drawallline(mainwindow.click_id))
        # bro.setHtml(echarts.drawonline(mainwindow.click_id))
        sub.scrollArea.setWidget(bro)

        # ectitle = sql.selproname(mainwindow.click_id)
        ectitle = sql.selproname(mainwindow.click_id) + "（第 " + str(mainwindow.click_id) + " 批）"

        self.linedataprint(sub)

        sub.setWindowTitle(ectitle)
        # # 将子窗口添加到Mdi区域
        self.ui.mdi.addSubWindow(sub)
        # 子窗口显示
        sub.show()
        t_stop = process_time()
        print("Elapsed time during the whole program in seconds:", t_stop - t_start)

    # 折线相关数据传输到列表子窗口
    def linedataprint(self, sub):
        sel_linedata = sql.sellinedata(mainwindow.click_id)
        # print(type(sel_linedata), sel_linedata)
        i = 0
        # 更新的方法是,设置行数为 0
        sub.tableWidget.setRowCount(0)
        for the_data in sel_linedata:
            # print(the_data)
            # 插入行
            sub.tableWidget.insertRow(i)
            offline_color = QTableWidgetItem(the_data[0])
            sub.tableWidget.setItem(i, 0, offline_color)
            offline_name = QTableWidgetItem(the_data[1])
            offline_name.setTextAlignment(Qt.AlignCenter)
            sub.tableWidget.setItem(i, 1, offline_name)
            project_id = QTableWidgetItem(the_data[2])
            project_id.setTextAlignment(Qt.AlignCenter)
            sub.tableWidget.setItem(i, 3, project_id)
            state = QTableWidgetItem(the_data[3])
            state.setTextAlignment(Qt.AlignCenter)
            sub.tableWidget.setItem(i, 4, state)
            project_name = QTableWidgetItem(the_data[4])
            sub.tableWidget.setItem(i, 5, project_name)
            i += 1

            # 禁止编辑
            sub.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            # 整行选择
            sub.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

            sub.tableWidget.resizeColumnsToContents()  # 根据内容调整列宽
            sub.tableWidget.resizeRowsToContents()


# 登陆界面
class Stats_Login:
    def __init__(self):
        self.Lui = QUiLoader().load('login.ui')
        self.Lui.psdLE.setEchoMode(QLineEdit.Password)  # 设置输入密码框
        self.Lui.CloseButton.clicked.connect(self.handleClose)
        self.Lui.ResetButton.clicked.connect(self.handleReset)
        self.Lui.PushButton.clicked.connect(self.handlePush)
        self.Lui.userLE.returnPressed.connect(self.handlePush)
        self.Lui.psdLE.returnPressed.connect(self.handlePush)

    def handleClose(self):
        print("Close")
        self.Lui.close()

    def handleReset(self):
        print("Reset")
        self.Lui.userLE.clear()
        self.Lui.psdLE.clear()

    def handlePush(self):
        print("Push")
        username = self.Lui.userLE.text()
        password = self.Lui.psdLE.text()
        outp = sql.userlog(username, password)
        if outp:
            # 实例化另外一个窗口
            self.mainwindow = mainwindow()
            # 显示新窗口
            self.mainwindow.ui.show()
            # 关闭自己
            self.Lui.close()
        else:
            self.msg()

    def msg(self):
        reply = QMessageBox.warning(self.Lui, "登录异常", "登录信息错误，登录失败", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            print('YES')
            self.handleReset()
        else:
            print('NO')
            self.handleClose()


if __name__ == '__main__':
    app = QApplication([])
    # 登录界面
    stats_login = Stats_Login()
    stats_login.Lui.show()
    # 表格数据界面
    # tabledata = mainwindow()
    # tabledata.ui.show()
    app.exec_()




