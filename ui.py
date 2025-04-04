import sys
import mysql.connector
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget,
    QLineEdit, QFormLayout, QDialog, QMessageBox
)
from actions import fetch_all_data, fetch_serial_number_data, insert_data, search_data  # Import insert_data and search_data

class AddDataWindow(QDialog):
    """
    A dialog window for adding new data to the V1550A table.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Data")
        self.setGeometry(200, 200, 400, 400)

        # Create a form layout
        layout = QFormLayout()

        # Input fields
        self.model_number_input = QLineEdit()
        self.serial_number_input = QLineEdit()
        self.operator_input = QLineEdit()
        self.voa_sn_input = QLineEdit()
        self.connectorization_input = QLineEdit()
        self.min_attenuation_input = QLineEdit()
        self.max_attenuation_input = QLineEdit()
        self.max_current_input = QLineEdit()
        self.per_a_input = QLineEdit()
        self.per_b_input = QLineEdit()
        self.qc_inspector_input = QLineEdit()
        self.date_closed_input = QLineEdit()

        # Add input fields to the form
        layout.addRow("Model Number:", self.model_number_input)
        layout.addRow("Serial Number:", self.serial_number_input)
        layout.addRow("Operator:", self.operator_input)
        layout.addRow("VOA SN:", self.voa_sn_input)
        layout.addRow("Connectorization:", self.connectorization_input)
        layout.addRow("Min Attenuation:", self.min_attenuation_input)
        layout.addRow("Max Attenuation:", self.max_attenuation_input)
        layout.addRow("Max Current:", self.max_current_input)
        layout.addRow("PER A:", self.per_a_input)
        layout.addRow("PER B:", self.per_b_input)
        layout.addRow("QC Inspector:", self.qc_inspector_input)
        layout.addRow("Date Closed (YYYY-MM-DD):", self.date_closed_input)

        # Add a submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.handle_submit)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def handle_submit(self):
        """
        Handles the submission of new data.
        """
        # Get input values
        model_number = self.model_number_input.text()
        serial_number = self.serial_number_input.text()
        operator = self.operator_input.text()
        voa_sn = self.voa_sn_input.text()
        connectorization = self.connectorization_input.text()
        min_attenuation = self.min_attenuation_input.text()
        max_attenuation = self.max_attenuation_input.text()
        max_current = self.max_current_input.text()
        per_a = self.per_a_input.text()
        per_b = self.per_b_input.text()
        qc_inspector = self.qc_inspector_input.text()
        date_closed = self.date_closed_input.text()

        # Insert data into the database
        result = insert_data(model_number, serial_number, operator, voa_sn, connectorization, min_attenuation, max_attenuation, max_current, per_a, per_b, qc_inspector, date_closed)

        # Show a message box with the result
        QMessageBox.information(self, "Result", result)
        self.close()


class SearchWindow(QDialog):
    """
    A dialog window for searching data in the V1550A table.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search Data")
        self.setGeometry(200, 200, 400, 200)

        # Create a form layout
        layout = QFormLayout()

        # Input fields
        self.serial_number_input = QLineEdit()
        self.model_number_input = QLineEdit()

        # Add input fields to the form
        layout.addRow("Serial Number:", self.serial_number_input)
        layout.addRow("Model Number:", self.model_number_input)

        # Add buttons
        button_layout = QVBoxLayout()
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.handle_search)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(search_button)
        button_layout.addWidget(cancel_button)
        layout.addRow(button_layout)

        self.setLayout(layout)

    def handle_search(self):
        """
        Handles the search operation.
        """
        serial_number = self.serial_number_input.text().strip()
        model_number = self.model_number_input.text().strip()

        result = search_data(serial_number if serial_number else None, model_number if model_number else None)

        if result:
            self.parent().output_box.setText(result)
            self.close()
        else:
            QMessageBox.information(self, "No Results", "No entries found matching the search criteria.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Query UI")
        self.setGeometry(100, 100, 600, 400)

        # Create a central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Create a text box for output
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        layout.addWidget(self.output_box)

        # Create a button to fetch all data
        fetch_all_button = QPushButton("Fetch All Data")
        fetch_all_button.clicked.connect(self.handle_fetch_all_data)
        layout.addWidget(fetch_all_button)

        # Create a button to fetch data for a specific serial number
        fetch_serial_button = QPushButton("Fetch Serial Number Data")
        fetch_serial_button.clicked.connect(self.handle_fetch_serial_number_data)
        layout.addWidget(fetch_serial_button)

        # Create a button to add new data
        add_data_button = QPushButton("Add New Data")
        add_data_button.clicked.connect(self.open_add_data_window)
        layout.addWidget(add_data_button)

        # Create a button to search data
        search_button = QPushButton("Search Data")
        search_button.clicked.connect(self.open_search_window)
        layout.addWidget(search_button)

        # Set the layout and central widget
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def handle_fetch_all_data(self):
        """
        Handles the "Fetch All Data" button click.
        """
        result = fetch_all_data()
        self.output_box.setText(result)

    def handle_fetch_serial_number_data(self):
        """
        Handles the "Fetch Serial Number Data" button click.
        """
        serial_number = "U12345"  # Replace with the desired serial number
        result = fetch_serial_number_data(serial_number)
        self.output_box.setText(result)

    def open_add_data_window(self):
        """
        Opens the Add Data window.
        """
        self.add_data_window = AddDataWindow()
        self.add_data_window.exec_()

    def open_search_window(self):
        """
        Opens the Search Data window.
        """
        self.search_window = SearchWindow(self)
        self.search_window.exec_()


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
