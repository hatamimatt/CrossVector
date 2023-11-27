import os
from qgis.core import QgsProject
from .plotting_fn import plot_cross_section
from .cross_vectors import get_elevation_along_line
from .cross_vectors import parse_xml



def lineDrawn(line_geometry, dtm_layer):
    print("Step 0: Line Drawn")
    
    # Step 1: Getting elevation data
    distances, elevations = get_elevation_along_line(dtm_layer, line_geometry)
    print("Step 1: Elevation data retrieved")

    # Step 2: Get the XML file path from your configuration
    xml_file_path = os.path.join(os.getenv('APPDATA'), 'QGIS', 'QGIS3', 'profiles', 'default', 'python', 'plugins', 'combined_datasets.xml')  # Replace with the actual path
    print(f"Step 2: XML file path: {xml_file_path}")
    
    # Step 3: Call the parse_xml function to get vector datasets and buffer radii
    dtm_layers, los_datasets, vector_datasets = parse_xml(xml_file_path)
    print("Step 3: XML file parsed")
    
    if not dtm_layers:
        print("No DTM layers found in the XML file.")
        return

    # Step 4: Create a list to store data related to points within the buffer
    buffer_data = []

    # Step 5: Iterate through vector datasets

    for vector_dataset in vector_datasets:
        buffer_radius = vector_dataset.get('BufferRadius', 0.0)  # Retrieve the buffer radius from the vector dataset
        
        # Step 6: Create a buffer geometry around the drawn line
        buffer_geometry = line_geometry.buffer(buffer_radius, 500)  # Adjust buffer radius and segments as needed
        print(f"Step 6: Buffer geometry created with radius {buffer_radius}")

        # Step 7: Iterate through layers specified in the XML for this vector dataset
        print(vector_dataset)
        print(vector_dataset.get('Layers', []))

        # List of keys to iterate over
        layer_keys = ['Eastlayer', 'NorthLayer', 'VerticalLayer']

        for key in layer_keys:
            layer_name = vector_dataset.get(key)
            print(layer_name)
            
            if not layer_name:
                # Handle the case when the key doesn't exist or has an empty value
                print(f"No value found for key {key}. Skipping...")
                continue
            
            print(f"Step 7: Processing layer {layer_name}")
                        
            # Get the QgsVectorLayer object corresponding to the layer name
            vector_layer = QgsProject.instance().mapLayersByName(layer_name)

            if not vector_layer:
                print(f"Couldn't find a vector layer named {layer_name} in the project.")
                continue

            # Use QgsVectorLayer.selectByRect() to select features within the buffer geometry
            vector_layer = vector_layer[0]  # Assuming you want the first matching layer
            vector_layer.removeSelection()  # Clear previous selections
            vector_layer.selectByRect(buffer_geometry.boundingBox())

            # Get the selected features and process them
            selected_features = vector_layer.selectedFeatures()
            print(f"Selected {len(selected_features)} features in layer {layer_name} within the buffer.")
            
            for feature in selected_features:
                # Use the dynamically fetched field name from the XML
                field_name = vector_dataset.get(key)  # Assuming the XML key matches the field name
                field_value = feature[field_name]  # Access the attribute using the field name
                
                # Append the data to the buffer_data list
                buffer_data.append({
                    'LayerName': layer_name,
                    'FieldName': field_name,
                    'FieldValue': field_value,
                    'Coordinates': feature.geometry().asPoint()
                })

            # Step 8: Print the collected data for points within the buffer
            print(f"Step 8: Collected {len(buffer_data)} points within the buffer. ")
            for data in buffer_data:
                print(f"Layer: {data['LayerName']}, "
                    f"Field: {data['FieldName']}, "
                    f"Value: {data['FieldValue']}, "
                    f"Coordinates: {data['Coordinates']}")

    # Step 9: Call the plot_cross_section function with distances, elevations, and xml_file_path
    plot_cross_section(distances, elevations, xml_file_path)
    print("Step 9: Cross-section plotted")
