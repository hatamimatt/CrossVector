import datetime
import json
import os

from PyQt5.QtWidgets import QApplication, QFileDialog


def save_dict_to_json(sliding_surface_data, layer_name, field_name, line_name):
    """
    Save a dictionary containing sliding surface data to a JSON file.
    
    Parameters:
    sliding_surface_data (dict): The dictionary with the data to save.
    layer_name (str): The name of the layer where the sliding surface is located.
    line_name (str): The name of the line that intersects the sliding surface.
    
    Returns:
    None
    """
    # Get current datetime in YYYYMMDD_HHMMSS format
    now = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    
    # Create the filename by joining the metadata and adding .json extension
    filename = layer_name + "-" + field_name + "-" + line_name + "-" + now + '.json'
    
    # Open the save file dialog and get the directory path
    app = QApplication([])
    dir_path = QFileDialog.getExistingDirectory()
    
    if dir_path:
        try:
            # Join the directory path and the filename
            file_path = os.path.join(dir_path, filename)
            
            # Open the file in write mode and dump the dictionary as JSON
            with open(file_path, 'w') as f:
                json.dump(sliding_surface_data, f)
                
        except Exception as e:
            print(f"An error occurred while trying to save the dictionary to a JSON file: {e}")


def load_dict_from_json(filename):
    """
    Load a dictionary from a JSON file.

    Parameters:
    filename (str): The name of the JSON file to load.

    Returns:
    dict: The dictionary loaded from the JSON file.
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"An error occurred while trying to load the dictionary from a JSON file: {e}")

