import os
import shutil
import Subtitle_Rename_Design
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox


class SubtitleNames(QWidget):
    def __init__(self):
        super().__init__()
        self.win = Subtitle_Rename_Design.Ui_winSubtitleRename()
        self.win.setupUi(self)
        self.win.toolPath.clicked.connect(self.fetch_path)
        self.win.btnRenameSub.clicked.connect(self.rename_sub)
        self.win.btnRenameEpisodes.clicked.connect(self.rename_episodes)
        self.win.btnDelete.clicked.connect(self.delete)

    def fetch_path(self):
        options = QFileDialog.Options()
        path = QFileDialog.getExistingDirectory(caption="Select the directory to season",
                                                   directory="",
                                                   options=options)
        self.win.entPath.setText(path)

    def rename_sub(self):
        p = self.win.entPath.text().replace("\\", "/")
        path = f'{p}\Subs'
        episodes = self.win.entEpisodes.toPlainText().split(", ")
        for idx, folder in enumerate(os.listdir(path)):
            os.chdir(f"{path}/{folder}")

            name = os.listdir(f'{path}/{folder}')
            os.rename(name[0], f'{idx+1} - {episodes[idx]}.srt')

            shutil.move(f"{path}/{folder}/{idx+1} - {episodes[idx]}.srt", path)
        os.chdir("C:/D")
        QMessageBox.information(self, "Done", "Successful!")

    def rename_episodes(self):
        path = self.win.entPath.text().replace("\\", "/")
        os.chdir(path)
        episodes = self.win.entEpisodes.toPlainText().split(", ")
        for idx, episode in enumerate(os.listdir("./")):
            if ".mp4" in episode:
                os.rename(episode, f'{idx + 1} - {episodes[idx].replace(":", " -")}.mp4')
            if ".mkv" in episode:
                os.rename(episode, f'{idx + 1} - {episodes[idx].replace(":", " -")}.mkv')
        QMessageBox.information(self, "Done", "Successful!")

    def delete(self):
        p = self.win.entPath.text().replace("\\", "/")
        path = f'{p}\Subs'
        for folder in os.listdir(path):
            if ".srt" not in folder:
                new_path = os.path.join(path, folder)
                shutil.rmtree(new_path)


app = QApplication([])
win = SubtitleNames()
win.show()
app.exec_()
