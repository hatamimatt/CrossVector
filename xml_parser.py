import xml.etree.ElementTree as ET

def parse_xml(xml_file_path):
    dtm_layers = []
    los_datasets = []
    vector_datasets = []
    radar_datasets = []

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

            # RADAR data
            elif child.tag == 'RADARdataset':
                radar_data = {}
                for item in child:
                    radar_data[item.tag] = item.text
                radar_datasets.append(radar_data)

            # VECTOR data
            elif child.tag == 'VECTORdataset':
                vector_data = {}
                for item in child:    
                    vector_data[item.tag] = item.text
                vector_datasets.append(vector_data)



    except Exception as e:
        print('Error parsing XML file: ', str(e))
        return {
            'error': f"Error parsing XML file: {str(e)}"
        }
    #print(f'vector dataset in xml parser: {vector_datasets}')
    return dtm_layers, los_datasets, vector_datasets, radar_datasets 
