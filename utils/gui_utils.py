import datetime
import json
import os

from PyQt5.QtWidgets import QFileDialog, QMessageBox,QApplication


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
    # Convert dictionary
    for key, array in sliding_surface_data.items():
        # Check if the array is a numpy array
        if isinstance(array, np.ndarray):
            # Convert it to a list of floats
            sliding_surface_data[key] = array.tolist()
            sliding_surface_data[key] = [float(element) for element in array]
        elif isinstance(array, list):
            print(key)
            if len(array)>1:
                if isinstance(array[0], list):
                    # Convert the nested list to a list of floats using a list comprehension
                    sliding_surface_data[key] = [float(x) for sublist in array for element in sublist for x in element]
                else:
                    sliding_surface_data[key] = [float(element) for element in array]                
            else:
                # Convert the single-element list to a float
                sliding_surface_data[key] = float(array[0])
    
    # Get current datetime in YYYYMMDD_HHMMSS format
    now = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

    # Create the filename by joining the metadata and adding .json extension
    filename = layer_name + "-" + field_name + "-" + line_name + "-" + now + ".json"

    # Open the save file dialog and get the directory path
    dir_path = QFileDialog.getExistingDirectory()

    if dir_path:
        try:
            # Join the directory path and the filename
            file_path = os.path.join(dir_path, filename)

            # Open the file in write mode and dump the dictionary as JSON
            with open(file_path, "w") as f:
                json.dump(sliding_surface_data, f)

            # Create a message box
            msg = QMessageBox()
            msg.setWindowTitle("INFO MESSAGE")
            msg.setText("Data correctly saved.")
            x = msg.exec_()

        except Exception as e:
            print(
                f"An error occurred while trying to save the dictionary to a JSON file: {e}"
            )
            # Create a message box
            msg = QMessageBox()
            msg.setWindowTitle("ERROR MESSAGE")
            msg.setText(
                f"An error occurred while trying to save the dictionary to a JSON file: {e}."
            )
            x = msg.exec_()


def load_dicts_from_json():
    """
    Open a file dialog, select multiple JSON files, and load dictionaries from the files.

    Returns:
    dict: The merged dictionary from the JSON files, or None if an error occurs.
    """
    app = QApplication([])
    # Open the file dialog and get the file paths
    file_paths, _ = QFileDialog.getOpenFileNames(filter="JSON files (*.json)")

    merged_data = {}

    for file_path in file_paths:        
        # Create a message box
        msg = QMessageBox()
        msg.setWindowTitle("INFO MESSAGE")
        msg.setText(f"File {file_path} selected.")
        x = msg.exec_()
        
        # Get the file name from the file path
        file_name = os.path.basename(file_path)

        try:
            # Open the file in read mode and load the dictionary from the JSON file
            with open(file_path, "r") as f:
                data = json.load(f)
                
            # Store the dictionary into the merged data dictionary with the file name as the key
            merged_data[file_name] = data
                
        except Exception as e:
            print(
                f"An error occurred while trying to load the dictionary from the JSON file: {e}"
            )

            # Create a message box
            msg = QMessageBox()
            msg.setWindowTitle("ERROR MESSAGE")
            msg.setText(
                f"An error occurred while trying to load the dictionary from the JSON file: {e}."
            )
            x = msg.exec_()
            return None

    return merged_data

