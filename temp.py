
        # looping through the line of sight datasets
        for los_dataset in los_datasets:
            
            self.los_layer_name = los_dataset.get('LOSlayer', self.los_layer_name)
            self.los_field_name = los_dataset.get('LOSfield', self.los_field_name)
            self.los_layer_color = los_dataset.get('LOScolor', self.los_layer_color)
            self.los_scale_factor = los_dataset.get('LOSLayerScale', self.los_scale_factor)
            self.los_layer_bufferRadius = los_dataset.get('BufferRadius', self.los_layer_bufferRadius)
            self.los_layer_cell_number = los_dataset.get('LOSBufferCellSize', self.los_layer_cell_number)
            self.los_layer_label = los_dataset.get('LOSlabel', self.los_layer_label)
            self.los_layer_dip_angle = los_dataset.get('Dip_Angle', self.los_layer_dip_angle)
            self.los_layer_dipd_angle = los_dataset.get('DipD_Angle', self.los_layer_dipd_angle)


            dip = np.radians(float(los_dataset.get('Dip_angle', 0.0)))
            dipd = np.radians(float(los_dataset.get('DipD_angle', 0.0)))

            buffer_radius = float(los_dataset.get('LOSBufferRadius', 0.0))

            los_buffer_geometry = line_geometry.buffer(buffer_radius, 0)

            
            self.segments = [line_geometry.interpolate(distance) for distance in np.linspace(0, line_geometry.length(),int(float(self.los_layer_cell_number)))]  # Creates 6 points dividing the line into 5 segments

            
            los_layer_name = self.los_layer_name  # Assuming you have the layer name directly in self.los_layer_name

            if not los_layer_name:
                print("No value found for los_layer_name. Skipping...")
                continue

            los_layer = QgsProject.instance().mapLayersByName(los_layer_name)

            
            if not los_layer:
                print(f"Couldn't find a 'los' layer named {los_layer_name} in the project. Skipping...")
                continue

            los_layer = los_layer[0]
            
            los_layer.removeSelection()


            spatial_index = QgsSpatialIndex(los_layer.getFeatures())


            segment_averages = []  # This will store the average values for each segment
            feature = None  
            
            for i in range(len(self.segments) - 1):
                # Create a segment geometry from two points
                segment_geometry = QgsGeometry.fromPolyline([QgsPoint(self.segments[i].asPoint()), QgsPoint(self.segments[i+1].asPoint())])


                # Buffer the segment
                segment_buffer_geometry = segment_geometry.buffer(buffer_radius, 0)
                
                potential_segment_matches = spatial_index.intersects(segment_buffer_geometry.boundingBox())
                
                sum_values = 0
                count_features = 0
                for feature_id in potential_segment_matches:

                    feature = los_layer.getFeature(feature_id)
                    if segment_buffer_geometry.intersects(feature.geometry()):
                        sum_values += feature[los_dataset['LOSfield']]  
                        count_features += 1

                
                # Calculate average and store it
                average_value = round(sum_values / count_features, 2) if count_features else 0
                segment_averages.append(average_value)

                los_vectors_data = []
                fixed_angle = math.radians(60)


                for i, segment_average in enumerate(segment_averages):
                    # Use the segment_average as the magnitude
                    magnitude = segment_average
                    
                    # Calculate the direction of the vector
                    beta = dip
                    
                   # Calculate the coordinates of the vector's start and end points along the cross-section line
                    segment_start_point = self.segments[i].asPoint()  # Start point of the segment
                    segment_end_point = self.segments[i + 1].asPoint()  # End point of the segment

                    start_point_coords = QgsPoint(segment_start_point.x(), segment_start_point.y())
                    feature_coords = feature.geometry().asPoint()
                    distance = start_point_coords.distance(QgsPoint(feature_coords[0], feature_coords[1]))
                
                    if abs(magnitude) > 15:
                        # Store information about the vector
                        los_vectors_data.append({
                            'Magnitude': magnitude,
                            'Dip': beta,
                            'DipDirection': dipd,
                            'Distance':  distance,  
                            'label': f'LOS {i+1}',  
                            'segment_start_point': segment_start_point,
                            'segment_end_point': segment_end_point,
                            'color': self.los_layer_color,
                            'los_scale_factor': self.los_scale_factor,
                        })


            potential_matches = spatial_index.intersects(los_buffer_geometry.boundingBox())


            
            # Filter the potential matches
            for feature_id in potential_matches:
                feature = los_layer.getFeature(feature_id)
                if los_buffer_geometry.intersects(feature.geometry()):
                    los_layer.selectByIds([feature.id()], QgsVectorLayer.AddToSelection)

            selected_features = los_layer.selectedFeatures()

            
            # Step 8: Iterate through LOS datasets


