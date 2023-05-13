import sys
import traceback
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QComboBox, \
    QPushButton, QTableWidget


class DataVisualizationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = None

        self.setWindowTitle('Data Visualization Dashboard')
        self.setGeometry(100, 100, 800, 600)

        self.choose_file_button = QPushButton('Choose Data File', self)
        self.choose_file_button.setGeometry(20, 20, 120, 30)
        self.choose_file_button.clicked.connect(self.choose_data_file)

        self.data_table = QTableWidget(self)
        self.data_table.setGeometry(20, 60, 760, 400)

        self.plot_button = QPushButton('Plot Data', self)
        self.plot_button.setGeometry(20, 480, 120, 30)
        self.plot_button.clicked.connect(self.plot_data)

        self.x_column_combo = QComboBox(self)
        self.x_column_combo.setGeometry(150, 480, 200, 30)

        self.y_column_combo = QComboBox(self)
        self.y_column_combo.setGeometry(360, 480, 200, 30)

        self.chart_type_combo = QComboBox(self)
        self.chart_type_combo.setGeometry(570, 480, 200, 30)
        self.chart_type_combo.addItem('Line')
        self.chart_type_combo.addItem('Bar')
        self.chart_type_combo.addItem('Scatter')

    def choose_data_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Choose Data File', '', 'CSV Files (*.csv)')

        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.data_table.setRowCount(len(self.data))
                self.data_table.setColumnCount(len(self.data.columns))
                self.data_table.setHorizontalHeaderLabels(self.data.columns)

                for i, row in enumerate(self.data.values):
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        self.data_table.setItem(i, j, item)

                self.x_column_combo.clear()
                self.y_column_combo.clear()
                self.x_column_combo.addItems(self.data.columns)
                self.y_column_combo.addItems(self.data.columns)

            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error loading data file:\n{str(e)}')
                traceback.print_exc()

        else:
            QMessageBox.warning(self, 'Warning', 'No file chosen.')

    def plot_data(self):
        if self.data is None:
            QMessageBox.warning(self, 'Warning', 'No data loaded.')
            return

        x_column = self.x_column_combo.currentText()
        y_column = self.y_column_combo.currentText()
        chart_type = self.chart_type_combo.currentText()

        if x_column and y_column:
            try:
                plt.figure()
                if chart_type == 'Line':
                    plt.plot(self.data[x_column], self.data[y_column])
                elif chart_type == 'Bar':
                    plt.bar(self.data[x_column], self.data[y_column])
                elif chart_type == 'Scatter':
                    plt.scatter(self.data[x_column], self.data[y_column])

                plt.xlabel(x_column)
                plt.ylabel(y_column)
                plt.title(f'{y_column} vs {x_column}')
                plt.show()

            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error plotting data:\n{str(e)}')
                traceback.print_exc()

        else:
            QMessageBox.warning(self, 'Warning', 'Please select X and Y columns.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataVisualizationApp()
    window.show()
    sys.exit(app.exec_())

