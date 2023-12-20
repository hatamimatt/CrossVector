import datetime
import json
import os

from PyQt5.QtWidgets import QFileDialog, QMessageBox


def save_dict_to_json(sliding_surface_data, layer_name, field_name, line_name):
    """
    Save a dictionary containing sliding surface data to a JSON file.
    
    Parameters:
    sliding_surface_data (dict): The dictionary with the data to save.
    layer_name (str): The name of the layer under analysis.
    field_name (str): The name of the field on the layer.
    line_name (str): The name of the line where the sliding surface is calculated.
    
    Returns:
    None
    """
    # Get current datetime in YYYYMMDD_HHMMSS format
    now = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    
    # Create the filename by joining the metadata and adding .json extension
    filename = layer_name + "-" + field_name + "-" + line_name + "-" + now + '.json'
    
    # Open the save file dialog and get the directory path
    dir_path = QFileDialog.getExistingDirectory()
    
    if dir_path:
        try:
            # Join the directory path and the filename
            file_path = os.path.join(dir_path, filename)
            
            # Open the file in write mode and dump the dictionary as JSON
            with open(file_path, 'w') as f:
                json.dump(sliding_surface_data, f)
                
            # Create a message box
            msg = QMessageBox()                
            msg.setWindowTitle("INFO MESSAGE")
            msg.setText("Data correctly saved.")
            x = msg.exec_()
                
        except Exception as e:
            print(f"An error occurred while trying to save the dictionary to a JSON file: {e}")
            # Create a message box
            msg = QMessageBox()   
            msg.setWindowTitle("ERROR MESSAGE")
            msg.setText(f"An error occurred while trying to save the dictionary to a JSON file: {e}.")
            x = msg.exec_()


def load_dict_from_json():
    """
    Open a file dialog, select a JSON file, and load a dictionary from the file.
    
    Returns:
    dict: The loaded dictionary from the JSON file, or None if an error occurs.
    """
    # Open the file dialog and get the file path
    file_path, _ = QFileDialog.getOpenFileName(filter="JSON files (*.json)")
    
    if file_path:
        # Create a message box
        msg = QMessageBox()
        msg.setWindowTitle("INFO MESSAGE")
        msg.setText(f"File {file_path} selected.")
        x = msg.exec_()
        
        try:
            # Open the file in read mode and load the dictionary from the JSON file
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"An error occurred while trying to load the dictionary from the JSON file: {e}")
            
            # Create a message box
            msg = QMessageBox()
            msg.setWindowTitle("ERROR MESSAGE")
            msg.setText(f"An error occurred while trying to load the dictionary from the JSON file: {e}.")
            x = msg.exec_()
            return None

