import xml.etree.ElementTree as ET

def parse_xml(xml_file_path):
    dtm_layers = []
    los_datasets = []
    vector_datasets = []

    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        for child in root:
            # DTM data
            if child.tag == 'DTMdataset':
                dtm_layer_name = child.find('layer').text
                dtm_layers.append(dtm_layer_name)

            # LOS data
            elif child.tag == 'LOSdataset':
                los_data = {}
                for item in child:
                    los_data[item.tag] = item.text
                los_datasets.append(los_data)

            # VECTOR data
            elif child.tag == 'VECTORdataset':
                vector_data = {}
                buffer_radius = 0.0  # Default buffer radius
                for item in child:
                    if item.tag == 'BufferRadius':
                        # Convert buffer radius to float and store it
                        buffer_radius = float(item.text)
                    else:
                        vector_data[item.tag] = item.text
                vector_data['BufferRadius'] = buffer_radius  # Store buffer radius
                vector_datasets.append(vector_data)
                #print(vector_data)

                # Print the parsed vector data for debugging
                print("Parsed VECTORdataset:")
                #for key, value in vector_data.items():
                   # print(f"{key}: {value}")

    except Exception as e:
        print('Error parsing XML file: ', str(e))
        return {
            'error': f"Error parsing XML file: {str(e)}"
        }
    #print(f'los_datasets: {los_datasets}')
    return dtm_layers, los_datasets, vector_datasets
