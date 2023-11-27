        # Step 5: Iterate through vector datasets
        for vector_dataset in vector_datasets:
            print(f'vector dataset cellnumber: {vector_dataset.get("CellNumber")} ')
            print(f' cellnumber type: {type(vector_dataset.get("CellNumber"))}')
            cell_number = vector_dataset.get('CellNumber')
            if isinstance(cell_number, str) and cell_number.isdigit():
                cell_number = int(cell_number)


            
            # Looping through the inSAR dataset
            if cell_number == 0:
                print(' cell number = 0, priesm data is given')
                #Check for field names in the vector dataset and store them
                self.east_layer_field = vector_dataset.get('Eastlayer', self.east_layer_field)
                self.north_layer_field = vector_dataset.get('NorthLayer', self.north_layer_field)
                self.vertical_layer_field = vector_dataset.get('VerticalLayer', self.vertical_layer_field)
                self.vector_layer_label = vector_dataset.get('VECTORLayerlabel', self.vector_layer_label)
                self.vector_layer_color = vector_dataset.get('VECTIRcolor', self.vector_layer_color)
                self.vector_layer_bufferRadius = vector_dataset.get('BufferRadius', self.vector_layer_bufferRadius)
                self.vector_layer_cell_number = vector_dataset.get('CellNumber', self.vector_layer_cell_number)
                
                #print(f"vector_dataset labellll: {vector_dataset.get('VECTORLayerlabel')}")

                buffer_radius = vector_dataset.get('BufferRadius', 0.0)  # Retrieve the buffer radius from the vector dataset

                # Step 6: Create a buffer geometry around the drawn line
                buffer_geometry = line_geometry.buffer(buffer_radius, 0)  # Adjust buffer radius and segments as needed
                #print(f"Step 6: Buffer geometry created with radius {buffer_radius}")

                # Step 7: Iterate through layers specified in the XML for this vector dataset
                layer_keys = [self.east_layer_field, self.north_layer_field, self.vertical_layer_field]
                #print(f"layer keys: {layer_keys} from dataset {vector_dataset}")
                for key in layer_keys:
                    #print(f"vector key: {key}")
                    if not key:
                        # Handle the case when the key doesn't exist or has an empty value
                        print(f"No value found for key {key}. Skipping...")
                        continue


                    # Get the QgsVectorLayer object corresponding to the layer name
                    vector_layer = QgsProject.instance().mapLayersByName(key)
                    #print(f" key: {key}")
                    if not vector_layer:
                        print(f"Couldn't find a vector layer named {key} in the project.")
                        continue
                    
                    vector_layer = vector_layer[0]  # Assuming you want the first matching layer

                    # Create a spatial index for the vector layer
                    spatial_index = QgsSpatialIndex(vector_layer.getFeatures())

                    # Use the spatial index to find potential matches
                    potential_matches = spatial_index.intersects(buffer_geometry.boundingBox())
                    #print(f"potential matches: {potential_matches}")
                    # Filter the potential matches
                    for feature_id in potential_matches:
                        feature = vector_layer.getFeature(feature_id)
                        if buffer_geometry.intersects(feature.geometry()):
                            # vector_layer.select(feature.id())
                            vector_layer.selectByIds([feature.id()], QgsVectorLayer.AddToSelection)

                    # Get the selected features and process them
                    selected_features = vector_layer.selectedFeatures()
                    print(f"selected features: {vector_layer}")


                    # Iterate through the selected features
                   
                    for feature in selected_features:
                        east_disp = feature[vector_dataset['EASTfield']]
                        north_disp = feature[vector_dataset['NorthField']]
                        vertical_disp = feature[vector_dataset['VerticalField']]
                        vector_label_field=feature[vector_dataset['VECTORLabelField']]
                        vector_layer_color=vector_dataset['VECTIRcolor']
                        #print(f" selected a feature from layer {vector_dataset['VECTORLayerlabel']}")
                        
                        magnitude_2d = math.sqrt(east_disp ** 2 + north_disp ** 2)
                    
                        magnitude_3d = math.sqrt(magnitude_2d ** 2 + vertical_disp ** 2)
                    
                        beta = -1 * math.atan(vertical_disp / magnitude_2d)
                        
                        magnitude = magnitude_3d * 0.001 # Convert to meters

                        projection = east_disp * normalized_direction_vector.x() + north_disp * normalized_direction_vector.y()

                        # Calculate the angle of the vector
                        alpha = math.atan2(magnitude_2d, vertical_disp)
                        #alpha = math.atan2(north_disp, east_disp)

                        
                        start_point_coords = QgsPoint(line_start_point.x(), line_start_point.y())
                        feature_coords = feature.geometry().asPoint()
                        distance = start_point_coords.distance(QgsPoint(feature_coords[0], feature_coords[1]))
                    

                        perpendicular_component = magnitude - projection


                        # Check if the coordinates already exist in the set 
                        coordinates = feature.geometry().asPoint()
                        if coordinates in unique_coordinates:
                            continue  # Skip adding duplicate coordinates

                        unique_coordinates.add(coordinates)  # Add coordinates to the set to mark them as seen

                        # Store information about the vector
                        vector_buffer_data.append({
                        'LayerName': key,
                        'FieldName': key,
                        'FieldValue': feature[key] if key in feature.fields().names() else None,
                        'Coordinates': feature.geometry().asPoint(),
                        'Magnitude': magnitude,
                        'Projection': projection,
                        'PerpendicularComponent': math.degrees(alpha), #perpendicular_component,
                        'Distance': distance,
                        'Beta': beta,
                        'label': vector_label_field,
                        'color': vector_layer_color
                    })


                    

                    if not vector_layer:
                        #print(f"Couldn't find a vector layer named {layer_name} in the project.")
                        continue

                vector_layer.removeSelection()  # Clear previous selections
            


            # Looping through the radar datset
            else:
                # this needs to be filled


        # looping through the line of sight datasets
        for los_dataset in los_datasets:
            
            self.los_layer_name = los_dataset.get('LOSlayer', self.los_layer_name)
            self.los_field_name = los_dataset.get('LOSfield', self.los_field_name)
            self.los_layer_color = los_dataset.get('LOScolor', self.los_layer_color)
            self.los_layer_bufferRadius = los_dataset.get('BufferRadius', self.los_layer_bufferRadius)
            self.los_layer_cell_number = los_dataset.get('LOSBufferCellSize', self.los_layer_cell_number)
            self.los_layer_label = los_dataset.get('LOSlabel', self.los_layer_label)
            self.los_layer_dip_angle = los_dataset.get('Dip_Angle', self.los_layer_dip_angle)
            self.los_layer_dipd_angle = los_dataset.get('DipD_Angle', self.los_layer_dipd_angle)


            dip = np.radians(float(los_dataset.get('Dip_angle', 0.0)))
            dipd = np.radians(float(los_dataset.get('DipD_angle', 0.0)))
            #print(f"los dip: {dip}")
            #print(f"los dipd: {dipd}")
            buffer_radius = float(los_dataset.get('LOSBufferRadius', 0.0))
            #print(f"los buffer_radius: {buffer_radius}")
            los_buffer_geometry = line_geometry.buffer(buffer_radius, 0)

            # Inside the loop for los_datasets, after creating los_buffer_geometry
            #self.segment_length = line_geometry.length() / 5  # Divide line length into 5 segments
            #print(f" number of segmentssssss: {self.los_layer_cell_number}")
            self.segments = [line_geometry.interpolate(distance) for distance in np.linspace(0, line_geometry.length(),int(float(self.los_layer_cell_number)))]  # Creates 6 points dividing the line into 5 segments

            
            los_layer_name = self.los_layer_name  # Assuming you have the layer name directly in self.los_layer_name

            if not los_layer_name:
                print("No value found for los_layer_name. Skipping...")
                continue

            los_layer = QgsProject.instance().mapLayersByName(los_layer_name)
            print(f"los_layer: {los_layer}")
            
            if not los_layer:
                print(f"Couldn't find a 'los' layer named {los_layer_name} in the project. Skipping...")
                continue

            los_layer = los_layer[0]
            
            los_layer.removeSelection()
            #print(f"los_layer: {los_layer}")
            
            spatial_index = QgsSpatialIndex(los_layer.getFeatures())

            print(f'number of featuers in the layer: {los_layer.featureCount()}')

            segment_averages = []  # This will store the average values for each segment
            feature = None  # Initialize feature outside the loop
            
            for i in range(len(self.segments) - 1):
                # Create a segment geometry from two points
                segment_geometry = QgsGeometry.fromPolyline([QgsPoint(self.segments[i].asPoint()), QgsPoint(self.segments[i+1].asPoint())])


                # Buffer the segment
                segment_buffer_geometry = segment_geometry.buffer(buffer_radius, 0)
                # Now you can find potential matches for each segment as you did for the entire buffer
                potential_segment_matches = spatial_index.intersects(segment_buffer_geometry.boundingBox())
                #print(f"len(potential_segment_matchesssssssss): {len(potential_segment_matches)}")
                print(f'potential segment matches numerber: {len(potential_segment_matches)}')

                sum_values = 0
                count_features = 0
                for feature_id in potential_segment_matches:

                    feature = los_layer.getFeature(feature_id)
                    if segment_buffer_geometry.intersects(feature.geometry()):
                        sum_values += feature[los_dataset['LOSfield']]  # Replace 'data_field' with the actual field name
                        count_features += 1

                
                # Calculate average and store it
                average_value = round(sum_values / count_features, 2) if count_features else 0
                segment_averages.append(average_value)

                los_vectors_data = []
                fixed_angle = math.radians(60)

                print(f"segment averages: {segment_averages}")
                for i, segment_average in enumerate(segment_averages):
                    # Use the segment_average as the magnitude
                    magnitude = segment_average
                    
                    # Calculate the direction of the vector
                    beta = dip
                    
                   # Calculate the coordinates of the vector's start and end points along the cross-section line
                    segment_start_point = self.segments[i].asPoint()  # Start point of the segment
                    segment_end_point = self.segments[i + 1].asPoint()  # End point of the segment
                    #print(f"hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                    #print(f"feature: {feature}")
                    start_point_coords = QgsPoint(segment_start_point.x(), segment_start_point.y())
                    feature_coords = feature.geometry().asPoint()
                    distance = start_point_coords.distance(QgsPoint(feature_coords[0], feature_coords[1]))
                
                    if abs(magnitude) > 15:
                        # Store information about the vector
                        los_vectors_data.append({
                            'Magnitude': magnitude,
                            'Dip': beta,
                            'DipDirection': dipd,
                            'Distance':  distance,  # Use the midpoint as the distance
                            'label': f'LOS {i+1}',  # You can use a meaningful label
                            'segment_start_point': segment_start_point,
                            'segment_end_point': segment_end_point,
                            'color': self.los_layer_color,
                        })
                #print(f"los vectors data: {los_vectors_data}")

                #print(f"segment_averagesssssss: {segment_averages}")


            potential_matches = spatial_index.intersects(los_buffer_geometry.boundingBox())

            #print(f"number of potential matches: {len(potential_matches)}")
            
            # Filter the potential matches
            for feature_id in potential_matches:
                feature = los_layer.getFeature(feature_id)
                if los_buffer_geometry.intersects(feature.geometry()):
                    los_layer.selectByIds([feature.id()], QgsVectorLayer.AddToSelection)

            selected_features = los_layer.selectedFeatures()

            #print(f"Selected {len(selected_features)} features from layer {los_layer_name} within buffer radius {buffer_radius} m")


            # Step 8: Iterate through LOS datasets
        
