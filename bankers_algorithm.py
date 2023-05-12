from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QLineEdit, QMessageBox, QComboBox, QDialog, QVBoxLayout, QListWidget, QScrollArea
from PyQt5.QtCore import Qt

def banker_algorithm(num_processes, total_resources, available_resources, process_allocation, max_need, process_request=[0,0,0,0], process_num=0):
    # initialize the needed and finished lists
    needed_resources = [[max_need[i][j] - process_allocation[i][j] for j in range(len(total_resources))] for i in range(num_processes)]
    finished_processes = [False] * num_processes

    # initialize the safe sequence list
    safe_sequence = []
    steps = []
    # print the initial state
    print("Initial state:")
    steps.append("Initial state:")

    print(f"Available resources: {available_resources}")
    steps.append(f"Available resources: {available_resources}")

    print("Process allocation:")

    for i in range(num_processes):
        print(f"Process {i}: {process_allocation[i]}")
        # steps.append(f"Process {i}: {process_allocation[i]}")

    print("Max need:")
    for i in range(num_processes):
        print(f"Process {i}: {max_need[i]}")
    print()






    # check if the request can be granted
    if all(process_request[i] <= needed_resources[i][j] and process_request[i] <= available_resources[j] for i in range(num_processes) for j in range(len(total_resources))):
        # assume deadlock will occur unless a process can be found that can complete
        deadlock_detected = True

        # update the needed_resources and available_resources lists
        for j in range(len(total_resources)):
            needed_resources[process_num][j] -= process_request[j]
            available_resources[j] -= process_request[j]

        for _ in range(num_processes):
            for i in range(num_processes):
                # check if the process has already finished or if its needed resources are greater than the available resources
                if not finished_processes[i] and all(needed_resources[i][j] <= available_resources[j] for j in range(len(total_resources))):
                    # process can complete
                    deadlock_detected = False

                    # add the process to the safe sequence
                    safe_sequence.append(i)

                    # update the available resources and finished_processes list
                    for j in range(len(total_resources)):
                        available_resources[j] += process_allocation[i][j]
                    finished_processes[i] = True

                # print the current state
                print(f"Safe sequence so far: {safe_sequence}")
                steps.append(f"Safe sequence so far: {safe_sequence}")
                print(f"Process {i} can complete")
                steps.append(f"Process {i} can complete")
                print(f"Available resources: {available_resources}")
                steps.append(f"Available resources: {available_resources}")
                print("Process allocation:")
                # steps.append("Process allocation:")
                for k in range(num_processes):
                    print(f"Process {k}: {process_allocation[k]}")
                    # steps.append(f"Process {k}: {process_allocation[k]}")
                print("Needed resources:")
                # steps.append("Needed resources:")
                for k in range(num_processes):
                    print(f"Process {k}: {needed_resources[k]}")
                    # steps.append(f"Process {k}: {needed_resources[k]}")


                print("Max need:")
                for k in range(num_processes):
                    print(f"Process {k}: {max_need[k]}")
                print()


            # if deadlock is detected and not all processes have finished, then it is not safe to grant any more requests
            if deadlock_detected and False in finished_processes:
                # revert the needed_resources and available_resources lists to their original values
                for j in range(len(total_resources)):
                    needed_resources[process_num][j] += process_request[j]
                    available_resources[j] += process_request[j]
                print("Unsafe state")
                return None, False, steps

            # if all processes have finished, then the system is in a safe state
            elif all(finished_processes):
                break

        # print the final state
        print("Final state:")
        steps.append("Final state:")
        print(f"Safe sequence: {safe_sequence}")
        steps.append(f"Safe sequence: {safe_sequence}")
        print(f"Available resources: {available_resources}")
        steps.append(f"Available resources: {available_resources}")
        
        print("Process allocation:")
        # steps.append("Process allocation:")
        for i in range(num_processes):
            print(f"Process {i}: {process_allocation[i]}")
            # steps.append(f"Process {i}: {process_allocation[i]}")
            
        print("Needed resources:")
        # steps.append("Needed resources:")
        for i in range(num_processes):
            print(f"Process {i}: {needed_resources[i]}")
            # steps.append(f"Process {i}: {needed_resources[i]}")
        
        print("Max need:")
        # steps.append("Max need:")
        
        for i in range(num_processes):
            print(f"Process {i}: {max_need[i]}")
            # steps.append(f"Process {i}: {max_need[i]}")
        
        print("Done")
        steps.append("Done")
        

        # print the safe sequence
        print("Request can be granted.\nSafe sequence:")
        for i in safe_sequence:
            print(f"Process {i}", end=" -> ")
        print("Done")

    else:
        print("Request cannot be granted.")
        return None, False, steps # just added

    return safe_sequence, True, steps

class BankersAlgorithmApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Banker\'s Algorithm')
        self.setFixedSize(1200, 800)
    # Create labels
        self.total_res_label = QLabel('Total Resources:')
        self.avail_res_label = QLabel('Available Resources:')
        self.max_need_label = QLabel('Max Need:')
        self.proc_alloc_label = QLabel('Process Allocation:')
        self.req_res_label = QLabel('Request Resources:')
        self.status_label = QLabel('Status:')

        # Create line edit widgets for input
        self.total_res_inputs = [QLineEdit() for _ in range(4)]
        self.avail_res_inputs = [QLineEdit() for _ in range(4)]
        self.max_need_inputs = [[QLineEdit() for _ in range(4)] for _ in range(3)]
        self.proc_alloc_inputs = [[QLineEdit() for _ in range(4)] for _ in range(3)]
        self.req_res_inputs = [QLineEdit() for _ in range(4)]

        self.process_selection = QComboBox()
        self.process_selection.clear()
        self.process_selection.addItems(['', 'P1', 'P2', 'P3'])
      
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit_button_clicked)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

 # gui
       
 # Add labels and line edits to grid
        self.grid.addWidget(self.total_res_label, 0, 0)
        for i, input_widget in enumerate(self.total_res_inputs):
            self.grid.addWidget(input_widget, 0, i + 1)

        self.grid.addWidget(self.avail_res_label, 1, 0)
        for i, input_widget in enumerate(self.avail_res_inputs):
            self.grid.addWidget(input_widget, 1, i + 1)

        self.grid.addWidget(self.max_need_label, 2, 0)
        for i, input_row in enumerate(self.max_need_inputs):
            for j, input_widget in enumerate(input_row):
                self.grid.addWidget(input_widget, i + 2, j + 1)

        self.grid.addWidget(self.proc_alloc_label, 5, 0)
        for i, input_row in enumerate(self.proc_alloc_inputs):
            for j, input_widget in enumerate(input_row):
                self.grid.addWidget(input_widget, i + 6, j + 1)

        self.grid.addWidget(self.req_res_label, 9, 0)
        self.grid.addWidget(self.process_selection, 9, 1)
        for i, input_widget in enumerate(self.req_res_inputs):
            input_widget.setText("0")
            self.grid.addWidget(input_widget, 9, i + 2)
            

        self.grid.addWidget(self.submit_button, 10, 2)
        self.grid.addWidget(self.status_label, 11, 0, 1, 4)

        # Set layout
        self.setLayout(self.grid)
       

    def get_input_data(self):
        total_resources = [int(input_widget.text()) for input_widget in self.total_res_inputs]
        available_resources = [int(input_widget.text()) for input_widget in self.avail_res_inputs]
        max_need = [[int(input_widget.text()) for input_widget in input_row] for input_row in self.max_need_inputs]
        process_allocation = [[int(input_widget.text()) for input_widget in input_row] for input_row in self.proc_alloc_inputs]
        request_resources = [int(input_widget.text()) for input_widget in self.req_res_inputs]
        process = self.process_selection.currentText()
        return total_resources, available_resources, max_need, process_allocation, request_resources, process

    def display_steps(self, items):
        # Create a new dialog window
        dialog = QDialog(self)
        dialog.setWindowTitle('List of Items')  
        # Create a layout for the window
        layout = QVBoxLayout()

        # Add a label for each item in the list
        for item in items:
            label = QLabel(item)
            layout.addWidget(label)
##################################################################
        # Set the layout for the window
        dialog.setLayout(layout)

        # Show the window
        dialog.exec_()    
        
    def submit_button_clicked(self):
        # Get input data
        total_resources, available_resources, max_need, process_allocation, request_resources, process = self.get_input_data()

        if process == "P1":
            process = 0
        elif process =="P2":
            process = 1
        else:
            process = 2

        # Run banker's algorithm
        # safe_sequence, status = banker_algorithm(total_resources, available_resources, max_need, process_allocation, request_resources)
        
        safe_sequence, status, steps = banker_algorithm(3, total_resources, available_resources, process_allocation, max_need, request_resources, process)

        print(safe_sequence, status)
        # Display result
        if safe_sequence:
            self.status_label.setText(f'Safe sequence: {safe_sequence}\nStatus: {status}')
        else:
            self.status_label.setText(f'Status: {status}')
        self.display_steps(steps)




app = QApplication([])
window = BankersAlgorithmApp()
window.show()
app.exec_()