# coding:utf-8

import sys

from PyQt5.QtCore import QDir, QFileInfo, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from language_tool_python import LanguageTool
from loguru import logger
from nltk import WordNetLemmatizer

import Dication
from nlp_check import is_plural_nltk, check_spelling_pair_languagetool


class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = Dication.Ui_dicationDialog()
        self.ui.setupUi(self)

        # player
        self.player = QMediaPlayer(self)
        self.playlist = QMediaPlaylist(self)
        self.player.setPlaylist(self.playlist)
        self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)  # 循环模式
        self.__duration = "%02d:%02d:%02d" % (0, 0, 0)  # 文件总时间长度
        self.__curPos = "%02d:%02d:%02d" % (0, 0, 0)  # 当前播放到位置
        self.ui.label_playProgress.setText(self.__curPos + "/" + self.__duration)

        self.player.stateChanged.connect(self.do_stateChanged)
        self.player.positionChanged.connect(self.do_positionChanged)
        self.player.durationChanged.connect(self.do_durationChanged)
        # self.playlist.currentIndexChanged.connect(self.do_currentChanged)

        self.idx_wl = 0
        self.buffer_file = ''
        self.check_file = ''
        self.input_buffer = []
        self.word_list = []
        self.check_list = []
        self.tool = LanguageTool('en-US')
        self.lemmatizer = WordNetLemmatizer()
        self.ui.label_wordStatus.setText('x: new word\nl: lose\n')

        #  =============自定义槽函数===============================

    def do_stateChanged(self, state):  # 播放器状态变化
        # self.ui.btnPlay.setEnabled(state != QMediaPlayer.PlayingState)
        # self.ui.btnPause.setEnabled(state == QMediaPlayer.PlayingState)
        # self.ui.btnStop.setEnabled(state == QMediaPlayer.PlayingState)
        self.ui.pushButton_play.setText('Play' if state == QMediaPlayer.PlayingState else 'Pause')

    def do_positionChanged(self, position):  # 当前文件播放位置变化，更新进度显示
        if self.ui.sliderPosition.isSliderDown():  # 在拖动滑块调整进度
            return
        self.ui.sliderPosition.setSliderPosition(position)
        self.__curPos = self.time_to_hms(position)
        self.ui.label_playProgress.setText(self.__curPos + "/" + self.__duration)

    def do_durationChanged(self, duration):  # 文件时长变化
        self.ui.sliderPosition.setMaximum(duration)

        self.__duration = self.time_to_hms(duration)
        self.ui.label_playProgress.setText(self.__curPos + "/" + self.__duration)

    @staticmethod
    def time_to_hms(duration):
        mins, secs = divmod(duration / 1000, 60)
        hours, mins = divmod(mins, 60)
        return "%02d:%02d:%02d" % (hours, mins, secs)

    # def do_currentChanged(self, position):  #playlist当前曲目变化
    #     self.ui.listWidget.setCurrentRow(position)
    #     item = self.ui.listWidget.currentItem()  # QListWidgetItem
    #     if (item != None):
    #         self.ui.LabCurMedia.setText(item.text())
    #
    #     #  ==========由connectSlotsByName() 自动连接的槽函数==================
    #     #  播放列表管理
    #
    # @pyqtSlot()  #添加文件
    # def on_btnAdd_clicked(self):
    #     #      curPath=os.getcwd()     #获取系统当前目录
    #     #      curPath=QDir.homePath()
    #     curPath = QDir.currentPath()
    #     dlgTitle = "选择音频文件"
    #     filt = "音频文件(*.mp3 *.wav *.wma);;所有文件(*.*)"
    #     fileList, flt = QFileDialog.getOpenFileNames(self, dlgTitle, curPath, filt)
    #     count = len(fileList)
    #     if count < 1:
    #         return
    #
    #     filename = fileList[0]
    #     fileInfo = QFileInfo(filename)  # 文件信息
    #     QDir.setCurrent(fileInfo.absolutePath())  # 重设当前路径
    #
    #     for i in range(count):
    #         filename = fileList[i]
    #         fileInfo.setFile(filename)
    #         song = QMediaContent(QUrl.fromLocalFile(filename))
    #         self.playlist.addMedia(song)  # 添加播放媒体
    #         #         basename=os.path.basename(filename)    #文件名和后缀
    #         basename = fileInfo.baseName()
    #         self.ui.listWidget.addItem(basename)  # 添加到界面文件列表
    #
    #     if (self.player.state() != QMediaPlayer.PlayingState):
    #         self.playlist.setCurrentIndex(0)
    #         self.player.play()
    #
    # @pyqtSlot()  #移除一个文件
    # def on_btnRemove_clicked(self):
    #     pos = self.ui.listWidget.currentRow()
    #     item = self.ui.listWidget.takeItem(pos)  # python会自动删除
    #
    #     if (self.playlist.currentIndex() == pos):  # 是当前播放的曲目
    #         nextPos = 0
    #         if pos >= 1:
    #             nextPos = pos - 1
    #
    #         self.playlist.removeMedia(pos)  # 从播放列表里移除
    #         if self.ui.listWidget.count() > 0:  # 剩余个数
    #             self.playlist.setCurrentIndex(nextPos)
    #             self.do_currentChanged(nextPos)  # 当前曲目变化
    #         else:
    #             self.player.stop()
    #             self.ui.LabCurMedia.setText("无曲目")
    #     else:
    #         self.playlist.removeMedia(pos)
    #
    # @pyqtSlot()  #清空播放列表
    # def on_btnClear_clicked(self):
    #     self.playlist.clear()  # 清空播放列表
    #     self.ui.listWidget.clear()
    #     self.player.stop()  # 停止播放
    #
    # #   @pyqtSlot()    #双击时切换播放文件
    # def on_listWidget_doubleClicked(self, index):
    #     rowNo = index.row()  # 行号
    #     self.playlist.setCurrentIndex(rowNo)
    #     self.player.play()
    #
    # #  播放控制
    # @pyqtSlot()  #播放
    # def on_btnPlay_clicked(self):
    #     if (self.playlist.currentIndex() < 0):
    #         self.playlist.setCurrentIndex(0)
    #     self.player.play()
    #
    # @pyqtSlot()  #暂停
    # def on_btnPause_clicked(self):
    #     self.player.pause()
    #
    # @pyqtSlot()  #停止
    # def on_btnStop_clicked(self):
    #     self.player.stop()
    #
    # @pyqtSlot()  #上一曲目
    # def on_btnPrevious_clicked(self):
    #     self.playlist.previous()
    #
    # @pyqtSlot()  #下一曲目
    # def on_btnNext_clicked(self):
    #     self.playlist.next()
    #
    # @pyqtSlot()  #静音控制
    # def on_btnSound_clicked(self):
    #     mute = self.player.isMuted()
    #     self.player.setMuted(not mute)
    #     if mute:
    #         self.ui.btnSound.setIcon(QIcon(":/icons/images/volumn.bmp"))
    #     else:
    #         self.ui.btnSound.setIcon(QIcon(":/icons/images/mute.bmp"))
    #
    # @pyqtSlot(int)  #调节音量
    # def on_sliderVolumn_valueChanged(self, value):
    #     self.player.setVolume(value)
    #
    # @pyqtSlot(int)  #文件进度调控
    # def on_sliderPosition_valueChanged(self, value):
    #     self.player.setPosition(value)

    # self.pushButton_openAudio.clicked.connect(dicationDialog.btn_open_audio_clicked)  # type: ignore
    # self.pushButton_pause.clicked.connect(dicationDialog.btn_open_pause_clicked)  # type: ignore
    # self.pushButton_openWordList.clicked.connect(dicationDialog.btn_open_word_list_clicked)  # type: ignore
    # self.pushButton_start.clicked.connect(dicationDialog.btn_open_start_clicked)  # type: ignore
    # self.lineEdit_wordInput.returnPressed.connect(dicationDialog.line_word_input_return_pressed)  # type: ignore
    # self.pushButton_next.clicked.connect(dicationDialog.btn_open_next_clicked)  # type: ignore

    @staticmethod
    def parse_word_list(filename: str) -> list:
        word_list = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                word_list.append(line.strip())
        return word_list

    def btn_open_word_list_clicked(self):

        # default_path = r'G:\BaiduNetdiskDownload\雅思复习计划（趴趴雅思原创）\复习计划配套电子资料\听力\雅思王听力真题语料库  趴趴雅思整理\王陆语料库 剑14 版本 音频'

        # cur_path = default_path
        cur_path = QDir.currentPath()
        dlg_title = "选择词表文件"
        filt = "音频文件(*.txt *.csv);;所有文件(*.*)"
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Optional: To open file in read-only mode
        file_list, flt = QFileDialog.getOpenFileNames(self, dlg_title, cur_path, filt, options=options)
        count = len(file_list)
        if count != 1:
            return

        filename = file_list[0]
        self.buffer_file = filename.replace(".txt", ".answer.txt")
        self.check_file = filename.replace(".txt", ".check.txt")
        self.word_list = self.parse_word_list(filename)
        print(self.word_list)

    def btn_open_audio_clicked(self):
        #      cur_path=os.getcwd()     #获取系统当前目录
        #      cur_path=QDir.homePath()
        default_path = r'G:\BaiduNetdiskDownload\雅思复习计划（趴趴雅思原创）\复习计划配套电子资料\听力\雅思王听力真题语料库  趴趴雅思整理\王陆语料库 剑14 版本 音频'

        cur_path = default_path
        dlg_title = "选择音频文件"
        filt = "音频文件(*.mp3 *.wav *.wma);;所有文件(*.*)"
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Optional: To open file in read-only mode
        file_list, flt = QFileDialog.getOpenFileNames(self, dlg_title, cur_path, filt, options=options)
        count = len(file_list)
        if count != 1:
            return

        filename = file_list[0]
        file_info = QFileInfo(filename)  # 文件信息
        QDir.setCurrent(file_info.absolutePath())  # 重设当前路径

        for i in range(count):
            filename = file_list[i]
            file_info.setFile(filename)
            song = QMediaContent(QUrl.fromLocalFile(filename))
            self.playlist.addMedia(song)  # 添加播放媒体
            #         basename=os.path.basename(filename)    #文件名和后缀
            basename = file_info.baseName()
            self.ui.lineEdit_audioPath.setText(basename)  # 添加到界面文件列表

        if self.player.state() != QMediaPlayer.PlayingState:
            self.playlist.setCurrentIndex(0)
            self.player.play()
            self.ui.pushButton_play.setText("Pause")

    def btn_play_clicked(self):
        if self.playlist.mediaCount() == 0:
            self.show_notification('Error', '未加载音频文件')
            return
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.ui.pushButton_play.setText("Play")
        else:
            self.player.play()
            self.ui.pushButton_play.setText("Pause")

    def calc_check_count(self):
        cat_count = ['_', 0, 0, 0, 0, 0, 0, 0]
        for check in self.check_list:
            cat_count[check] += 1
        return cat_count

    def btn_next_clicked(self):
        if len(self.word_list) == 0:
            self.show_notification('Error', '未加载词表')

        if self.idx_wl > len(self.word_list) :
            self.show_notification('Error', '已经是最后一题了')

        input_word = self.ui.lineEdit_wordInput.text()
        if input_word != "":
            self.input_buffer.append(input_word)
            self.check_list.append(self.eval_input(input_word, self.word_list[self.idx_wl]))
            logger.debug(self.input_buffer)
            # logger.debug(self.check_list)

            self.write_buffer_and_check_to_file()

            self.idx_wl += 1
            self.ui.lineEdit_wordInput.clear()

        if self.idx_wl == len(self.word_list) :
            check_count = self.calc_check_count()
            display_str = f'{self.CHECK_MAP[1]}:\t{check_count[1]}\n{self.CHECK_MAP[2]}:\t{check_count[2]}\n' \
                          f'{self.CHECK_MAP[3]}:\t{check_count[3]}\n{self.CHECK_MAP[4]}:\t{check_count[4]}\n' \
                          f'{self.CHECK_MAP[5]}:\t{check_count[5]}\n{self.CHECK_MAP[6]}:\t{check_count[6]}\n' \
                          f'{self.CHECK_MAP[7]}:\t{check_count[7]}'
            self.ui.label_wordStatus.setText(display_str)

    def write_buffer_and_check_to_file(self):
        with open(self.buffer_file, 'a', encoding='utf-8') as f:
            for word in self.input_buffer[-1:]:
                f.write(word + '\n')
        with open(self.check_file, 'a', encoding='utf-8') as f:
            for check in self.check_list[-1:]:
                f.write(str(self.input_buffer[-1:]) + ', ' + str(check) + ', ' + str(self.CHECK_MAP[check]) + '\n')

    def line_word_input_return_pressed(self):
        self.btn_next_clicked()

    CORRECT = 1
    ERROR_PLURAL = 2
    ERROR_UNKNOWN = 3
    ERROR_LOSE = 4
    ERROR_SPELLING = 5
    ERROR_UPPER_CASE = 6
    ERROR_NEW_WORD = 7

    CHECK_MAP = ['_', 'CORRECT', 'ERROR_PLURAL', 'ERROR_UNKNOWN', 'ERROR_LOSE', 'ERROR_SPELLING',
                 'ERROR_CAPITAL',
                 'ERROR_NEW_WORD']

    def eval_input(self, input, gt):
        if input == 'x':
            return self.ERROR_NEW_WORD
        elif input == 'l':
            return self.ERROR_LOSE
        elif input == gt:
            return self.CORRECT
        elif gt.upper() == input.upper():
            return self.ERROR_UPPER_CASE
        elif is_plural_nltk(self.lemmatizer, input, gt):
            return self.ERROR_PLURAL
        elif check_spelling_pair_languagetool(self.tool, input, gt):
            return self.ERROR_SPELLING
        else:
            return self.ERROR_UNKNOWN

    def show_notification(self, title, message):
        # app = QApplication(sys.argv)

        # 创建一个消息框
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)

        # 显示消息框
        result = msg_box.exec_()
        logger.debug(f'reach the end of word list, result={result}')
        # sys.exit(result)


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())
