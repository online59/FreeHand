import sys
import pandas as pd
import time
import auto as at
import stylesheet
from PyQt5.QtWidgets import QWidget, QTableView, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QAbstractItemView, QHBoxLayout, QVBoxLayout, QPushButton, QAbstractScrollArea, QLabel, QFileDialog
from threading import Thread

def read_data_and_convert_to_string(text_file = "test_data.csv"):
    text_df = pd.read_csv(text_file, encoding='tis-620')
    text_df = text_df.astype(str)
    return text_df

class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.keys_file = 'test_instruction.csv'
        self.text_file = 'test_data.csv'

        self.keys_df = read_data_and_convert_to_string(self.keys_file)
        self.text_df = read_data_and_convert_to_string(self.text_file)
        self.interval = 0.5
        self.main_loop_running = False

        self.setup_ui()
        self.add_menus()
        self.add_widgets()

    def setup_ui(self):
        self.setWindowTitle('Auto Key Simulation')
        self.resize(1200, 800)

    # Add top bar menu
    def add_menus(self):
        menubar = self.menuBar()
        menubar.setStyleSheet(stylesheet.menubar_ss)
        # Add menu name 'File'
        file_menu = menubar.addMenu('ไฟล์')
                
        # Under the 'File' menu add 'Open File' menu
        select_database_action = file_menu.addAction('นำเข้าไฟล์ข้อมูลบัญชี')
        select_database_action.triggered.connect(self.load_data_file)

        # Under the 'File' menu add 'Open Instruction File' menu
        open_instruction_action = file_menu.addAction('นำเข้าไฟล์คำสั่ง')
        open_instruction_action.triggered.connect(self.load_instruction_file)


        # Add menu name 'Data'
        data_menu = menubar.addMenu('คำสั่ง Express')

        # Under the 'Data' menu add 'Load Instruction' menu and its child menu
        load_instruction_menu = data_menu.addMenu('เลือกคำสั่ง')
        instruction_1_action = load_instruction_menu.addAction('Test Instruction')
        instruction_1_action.triggered.connect(lambda: self.load_instruction('test_instruction.csv'))
        instruction_2_action = load_instruction_menu.addAction('Non Vat Instruction')
        instruction_2_action.triggered.connect(lambda: self.load_instruction('nonvat_instruction.csv'))
        instruction_3_action = load_instruction_menu.addAction('Creadit RR Instruction')
        instruction_3_action.triggered.connect(lambda: self.load_instruction('credit_rr_instruction.csv'))


    # User open file and select their new instruction file
    def load_instruction_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        self.keys_file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CSV Files (*.csv);;All Files (*)", options=options)
        
        # Display which file is loaded
        self.instruction_file_status_label.setText('ไฟล์คำสั่ง: ' + self.keys_file)

        if self.keys_file:
            self.keys_df = read_data_and_convert_to_string(self.keys_file)
            self.keys_table.setRowCount(len(self.keys_df))
            self.keys_table.setColumnCount(len(self.keys_df.columns))
            self.keys_table.setHorizontalHeaderLabels(self.keys_df.columns)
            for i in range(len(self.keys_df)):
                for j in range(len(self.keys_df.columns)):
                    self.keys_table.setItem(i, j, QTableWidgetItem(str(self.keys_df.iloc[i, j])))
    
    # User open file and select their new data file
    def load_data_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        # Load data file
        self.text_file, _ = QFileDialog.getOpenFileName(self, "Select Database", "", "CSV Files (*.csv);;All Files (*)", options=options)

        self.data_file_status_label.setText('ไฟล์ข้อมูล: ' + self.text_file)

        if self.text_file:
            self.text_df = read_data_and_convert_to_string(self.text_file)
            self.data_table.setRowCount(len(self.text_df))
            self.data_table.setColumnCount(len(self.text_df.columns))
            self.data_table.setHorizontalHeaderLabels(self.text_df.columns)
            for i in range(len(self.text_df)):
                for j in range(len(self.text_df.columns)):
                    self.data_table.setItem(i, j, QTableWidgetItem(str(self.text_df.iloc[i, j])))

    # Load instruction from prepared CSV file
    def load_instruction(self, instruction_file):
       
        # Load file
        self.keys_df = pd.read_csv(instruction_file, encoding='tis-620')

        self.keys_table.setRowCount(len(self.keys_df))
        self.keys_table.setColumnCount(len(self.keys_df.columns))
        self.keys_table.setHorizontalHeaderLabels(self.keys_df.columns)
        for i in range(len(self.keys_df)):
            for j in range(len(self.keys_df.columns)):
                self.keys_table.setItem(i, j, QTableWidgetItem(str(self.keys_df.iloc[i, j])))


    def add_widgets(self):

        # Display instruction in window
        self.keys_table = QTableWidget()
        self.keys_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.keys_table.setAlternatingRowColors(True)
        self.keys_table.setStyleSheet("QTableView {border: none;}")
        self.keys_table.setSelectionBehavior(QTableView.SelectRows)
        self.keys_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.keys_table.setFixedWidth(300)
        self.keys_table.setRowCount(len(self.keys_df))
        self.keys_table.setColumnCount(len(self.keys_df.columns))
        self.keys_table.setHorizontalHeaderLabels(self.keys_df.columns)
        for i in range(len(self.keys_df)):
            for j in range(len(self.keys_df.columns)):
                self.keys_table.setItem(i, j, QTableWidgetItem(str(self.keys_df.iloc[i, j])))

        # Display data in window
        self.data_table = QTableWidget()
        self.data_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.data_table.setAlternatingRowColors(True)
        self.data_table.setStyleSheet("QTableView {border: none;}")
        self.data_table.setSelectionBehavior(QTableView.SelectRows)
        self.data_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.data_table.setRowCount(len(self.text_df))
        self.data_table.setColumnCount(len(self.text_df.columns))
        self.data_table.setHorizontalHeaderLabels(self.text_df.columns)
        for i in range(len(self.text_df)):
            for j in range(len(self.text_df.columns)):
                self.data_table.setItem(i, j, QTableWidgetItem(str(self.text_df.iloc[i, j])))

        # Add start and stop button
        self.start_button = QPushButton('เริ่มลงลงข้อมูล', self)
        self.start_button.clicked.connect(self.start_main_loop)
        self.stop_button = QPushButton('หยุดลงข้อมูล', self)
        self.stop_button.clicked.connect(self.stop_main_loop)
        self.stop_button.setEnabled(False) # First, the stop button should stay inactivate

        # Add label tell status of selected file
        self.data_file_status_label = QLabel()
        self.data_file_status_label.setText('ไฟล์ข้อมูล: ' + self.text_file)
        self.instruction_file_status_label = QLabel()
        self.instruction_file_status_label.setText('ไฟล์คำสั่ง: ' + self.keys_file)

        # Top layout for file selection status
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.data_file_status_label)
        top_layout.addWidget(self.instruction_file_status_label)

        # Middle layout for displaying data from instruction and data sheet
        display_layout = QHBoxLayout()
        display_layout.addWidget(self.data_table)
        display_layout.addWidget(self.keys_table)

        # Add status label to indicating program status
        self.status_label = QLabel()

        # Bottom layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.status_label)

        # Main layout wrap the whole layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(display_layout)
        main_layout.addLayout(button_layout)

        # Set main layout as the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # Start simulating keys press
    def start_main_loop(self):

        at.send_keys('%TAB')

        # Wait for a moment before sending the next key press
        time.sleep(1)

        # Main loop start here ...
        self.enableStartButton(False)

        # Start loop on other thread prevent program to freeze to death
        self.main_loop_thread = Thread(target=self.main_loop)
        self.main_loop_thread.start()


    # Stop simulating ket press, stop program
    def stop_main_loop(self):
        self.enableStartButton(True)
        self.status_label.setText('หยุด')

    # Main loop
    def main_loop(self):

	  # Get total lenght of data
        data_row_num = self.text_df.shape[0]
	  # Get total lenght of instruction
        key_row_num = self.keys_df.shape[0]

        # Iterate through each data row
        for data_row in range(data_row_num):

            # Check whether to run main loop or not
            if not self.main_loop_running:
                break

            # Change status
            self.status_label.setText(f'กำลังลงข้อมูลแถวที่ {data_row + 1}')
            
            # Iterate through each instruction row
            for key_row in range(key_row_num):

                # Check whether to run main loop or not
                if not self.main_loop_running:
                    break

                # On each instruction iteration, store key instruction in 'key' variable
                key = self.keys_df.loc[key_row, 'key']

                # On each instruction iteration, store things to do in 'field' variable
                field = self.keys_df.loc[key_row, 'field']

                # Check if the instruction request to type a text
                # Then we send text to type to 'send_keys' function
                if key == '$text':
                    try:
                        text_to_send = self.text_df.loc[data_row, field]
                    except:
                        print('Error main.py/248: Key and value pair error, may be you not match instruction with data')
                        self.enableStartButton(True)
                        self.status_label.setText('ข้อมูลบัญชีไม่ตรงกับข้อมูลคำสั่งลงบัญชี')
                        return
                else:
                    text_to_send = None

                try:
			    # Return boolean value whether to stop program
                    self.main_loop_running = at.send_keys(key, field, text_to_send)
                except Exception as e:
                    print(e)
                    break

                # Wait for a moment before sending the next key press
                time.sleep(self.interval)

        
        # When finied tell user the status of finishing
        self.status_label.setText('เสร็จสิ้น')
        self.enableStartButton(True)
                
    def enableStartButton(self, value):
        self.main_loop_running = not value
        self.start_button.setEnabled(value)
        self.stop_button.setEnabled(not value)

    def main(self):

        self.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("* { font-size: 12pt; }")
    gui = MyWindow()
    gui.main()

