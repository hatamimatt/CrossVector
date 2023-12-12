"""
The `plot_all` function is a comprehensive plotting function that visualizes various elements of a given dataset. It takes in multiple parameters including the x and y coordinates of vector locations, the index of a known position, the coordinates of intersections and circle centers, a list of tuples containing coordinates, the coordinates of solution values, the end points of displacement vectors, and the coordinates for construction lines and their order. 

The function begins by plotting the known point and vector locations. It then plots the displacement vectors and the circle centers. Following this, it plots a surface using the provided list of tuples. The function then plots construction lines using the provided coordinates and order. After this, it plots the intersections. 

Finally, the function sets the plot limits based on the provided data and displays the plot. This function is a one-stop solution for visualizing all the elements of the given dataset in a single plot.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import plot_utils as plot


def plot_all(output):
    """
    Plots all the elements of the graph.

    Parameters:
    output (dict): A dictionary that contains the following keys and values:
        known_position_index (int): Index of the known intersection with the profile.
        x, y (list): Lists of x and y coordinates of the vectors locations.
        x_intersection, y_intersection (list): Lists of x and y coordinates of the intersections.
        x_center, y_center (list): Lists of x and y coordinates of the circle centers.
        xy_r_list (list): List of tuples, where each tuple contains the x and y coordinates of a point and the radius of a circle.
        x_solution_values, y_solution_values (list): Lists of x and y coordinates of the solution values.
        end_x_displacement, end_y_displacement (list): Lists of x and y coordinates of the end points of the displacement vectors.
        x_center_plot, y_center_plot (list): Lists of x and y coordinates of the circle centers for the construction lines.
        x_construction_lines, y_construction_lines (list): Lists of x and y coordinates of the intersections for the construction lines.
        intersection_order (list): List of indices that represent the order of the intersections.
    """
    # Unpack the output dictionary
    known_position_index = output["known_position_index"]
    x = output["x"]
    y = output["y"]
    x_center = output["x_center"]
    y_center = output["y_center"]
    x_intersection = output["x_intersection"]
    y_intersection = output["y_intersection"]
    xy_r_list = output["xy_r_list"]
    x_solution_values = output["x_solution_values"]
    y_solution_values = output["y_solution_values"]
    end_x_displacement = output["end_x_displacement"]
    end_y_displacement = output["end_y_displacement"]
    x_center_plot = output["x_center_plot"]
    y_center_plot = output["y_center_plot"]
    x_construction_lines = output["x_construction_lines"]
    y_construction_lines = output["y_construction_lines"]
    intersection_order = output["intersection_order"]
    
    # Plot known point
    plot.plot_known_point(x, y, known_position_index)
    # Plot vector locations
    plot.plot_vector_locations(x, y, known_position_index)
    # Plot vector displacement
    plot.plot_vector_displacements(x, y, end_x_displacement, end_y_displacement)

    # Only proceed if there are circle centers
    if len(x_center) > 0:
        # Plot circle centers
        plot.plot_circle_centers(x_center, y_center)
        # Plot surface
        print(f'xyrlist: {xy_r_list}')
        plot.plot_surface(xy_r_list)
        # Plot construction lines
        plot.plot_construction_lines(
            x_center_plot,
            y_center_plot,
            x_construction_lines,
            y_construction_lines,
            intersection_order,
        )
        # Plot intersections
        plot.plot_intersections(x_intersection, y_intersection)
    else:
        print('no circle centers found')
        # No circle centers found
        pass

    # Set plot limits
    plot.set_plot_limits(
        x,
        y,
        end_x_displacement,
        end_y_displacement,
        xy_r_list,
        x_center_plot,
        y_center_plot,
    )
    ## Show the plot
    plot.show_plot()
