from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from Subtitle_Adjuster_Design import Ui_winSubtitleAdjuster


class Adjuster:
    def __init__(self, file_name):
        self.file_name = file_name
        with open(f"{file_name}.srt", "r") as file:
            self.lines = file.readlines()

    def add_sub_h(self, h, how_much, sign):
        if sign == "+":
            return h + how_much
        return h - how_much

    def add_sub_m(self, m, how_much, sign):
        if sign == "+":
            return [m + how_much, False] if m + how_much < 60 else [m + how_much - 60, True]
        return [m - how_much, False] if m - how_much >= 0 else [60 + m - how_much, True]

    def add_sub_s(self, s, how_much, sign):
        if sign == "+":
            return [s + how_much, False] if s + how_much < 60 else [s + how_much - 60, True]
        return [s - how_much, False] if s - how_much >= 0 else [60 + s - how_much, True]

    def add_sub_ms(self, ms, how_much, sign):
        if sign == "+":
            return [ms + how_much, False] if ms + how_much < 1000 else [ms + how_much - 1000, True]
        return [ms - how_much, False] if ms - how_much >= 0 else [1000 + ms - how_much, True]

    def add_sub(self, how_much, what, sign):
        new_lines = []
        for line in self.lines:
            if "-->" in line:
                from_h = line[:2]
                from_m = line[3:5]
                from_s = line[6:8]
                from_ms = line[9:12]
                to_h = line[17:19]
                to_m = line[20:22]
                to_s = line[23:25]
                to_ms = line[26:29]
                s_too_from = False
                s_too_to = False
                m_too_from = False
                m_too_to = False
                h_too_from = False
                h_too_to = False

                if what == "ms":
                    from_ms, s_too_from = self.add_sub_ms(int(line[9:12]), how_much, sign)
                    to_ms, s_too_to = self.add_sub_ms(int(line[26:29]), how_much, sign)
                elif what == "s":
                    from_s, m_too_from = self.add_sub_s(int(line[6:8]), how_much, sign)
                    to_s, m_too_to = self.add_sub_s(int(line[23:25]), how_much, sign)
                elif what == "m":
                    from_m, h_too_from = self.add_sub_m(int(line[3:5]), how_much, sign)
                    to_m, h_too_to = self.add_sub_m(int(line[20:22]), how_much, sign)
                elif what == "h":
                    from_h = self.add_sub_h(int(line[:2]), how_much, sign)
                    to_h = self.add_sub_h(int(line[17:19]), how_much, sign)

                if s_too_from:
                    from_s, m_too_from = self.add_sub_s(int(line[6:8]), 1, sign)
                if s_too_to:
                    to_s, m_too_to = self.add_sub_s(int(line[23:25]), 1, sign)

                if m_too_from:
                    from_m, h_too_from = self.add_sub_m(int(line[3:5]), 1, sign)
                if m_too_to:
                    to_m, h_too_to = self.add_sub_m(int(line[20:22]), 1, sign)

                if h_too_from:
                    from_h = self.add_sub_h(int(line[:2]), 1, sign)
                if h_too_to:
                    to_h = self.add_sub_h(int(line[17:19]), 1, sign)

                if len(str(from_h)) == 1:
                    from_h = f"0{from_h}"

                if len(str(from_m)) == 1:
                    from_m = f"0{from_m}"

                if len(str(from_s)) == 1:
                    from_s = f"0{from_s}"

                if len(str(from_ms)) == 1:
                    from_ms = f"00{from_ms}"
                elif len(str(from_ms)) == 2:
                    from_ms = f"0{from_ms}"

                if len(str(to_h)) == 1:
                    to_h = f"0{to_h}"

                if len(str(to_m)) == 1:
                    to_m = f"0{to_m}"

                if len(str(to_s)) == 1:
                    to_s = f"0{to_s}"

                if len(str(to_ms)) == 1:
                    to_ms = f"00{to_ms}"
                elif len(str(to_ms)) == 2:
                    to_ms = f"0{to_ms}"

                new_line = f"{from_h}:{from_m}:{from_s},{from_ms} --> {to_h}:{to_m}:{to_s},{to_ms}\n"
                new_lines.append(new_line)
            else:
                new_lines.append(line)

        with open(f"{self.file_name}_edited.srt", "w") as new_file:
            for i in new_lines:
                new_file.write(i)


class Win(QWidget):
    def __init__(self):
        super().__init__()
        self.win = Ui_winSubtitleAdjuster()
        self.win.setupUi(self)
        self.win.btnAdjust.clicked.connect(self.adjust)
        self.win.cbWhat.currentTextChanged.connect(self.how_many)

    def how_many(self):
        self.win.lblHowMany.setText(f"How Many {self.win.cbWhat.currentText()}:")

    def adjust(self):
        if self.win.entFileName.text() == "":
            QMessageBox.critical(self, "Hey!", "Enter the file path first!")
        elif self.win.entHowMany.text() == "":
            QMessageBox.critical(self, "Hey!", "Enter the amount!")
        else:
            try:
                Adjuster(self.win.entFileName.text()).add_sub(int(self.win.entHowMany.text()), self.win.cbWhat.currentText(), self.win.cbAddSub.currentText())
                QMessageBox.information(self, "Worked!", "Adjustment successful!")
            except:
                QMessageBox.critical(self, "Nope!", "There is no such file!")


app = QApplication([])
win = Win()
win.show()
app.exec_()
