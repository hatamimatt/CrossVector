"""
The script is a collection of Python functions designed to visualize data related to a known point, displacement vectors, locations, circle centers, surfaces, construction lines, and intersections. It uses matplotlib.pyplot to create the plot. The functions are organized in a way that each function is responsible for a specific part of the plot, making the code more readable and maintainable. The functions take specific parameters related to the data and should be called in the order they appear to reproduce the same plot as the original script. The script also includes a function to set the plot limits and a function to display the plot with a legend, equal aspect ratio, and grid. Please replace 'convert_alfa_to_trig', 'calculate_circle_centers', 'calculate_trigonometric_angles', 'remove_non_consecutive_arrays', and other variables and functions with your actual data and functions. If you're using a different language or software, please let me know so I can provide a more accurate solution. If the issue persists, there might be other parts of your code that are affecting the behavior. Please provide more context if possible.
"""

import matplotlib.pyplot as plt
import numpy as np

from .math_utils import *


def plot_known_point(x, y, known_position_index):
    """
    Plots a known point on the graph.

    Parameters:
    x (pd.Series): The x-coordinates.
    y (pd.Series): The y-coordinates.
    known_position_index (int): The index of the known point.
    """
    plt.plot(
        x[known_position_index],
        y[known_position_index],
        "cs",
        linewidth=1,
        markersize=8,
        markeredgecolor="c",
        label="Known point",
    )


def plot_vector_displacements(x, y, end_x_displacement, end_y_displacement):
    """
    Plots the displacements of all points.

    Parameters:
    x (pd.Series): The x-coordinates.
    y (pd.Series): The y-coordinates.
    end_x_displacement, end_y_displacement (list): The lists of coordinates of ending point for the displacement vectors
    """
    handle_quiver = [None] * len(end_x_displacement)
    for k in range(len(end_x_displacement)):
        if k == 0:
            handle_quiver[k] = plt.quiver(
                x[k],
                y[k],
                end_x_displacement[k] - x[k],
                end_y_displacement[k] - y[k],
                angles="xy",
                scale_units="xy",
                scale=1,
                color="r",
                label="Displacements",
            )
        else:
            handle_quiver[k] = plt.quiver(
                x[k],
                y[k],
                end_x_displacement[k] - x[k],
                end_y_displacement[k] - y[k],
                angles="xy",
                scale_units="xy",
                scale=1,
                color="r",
            )


def plot_vector_locations(x, y, known_position_index):
    """
    Plots the locations of all points except the known one.

    Parameters:
    x (pd.Series): The x-coordinates.
    y (pd.Series): The y-coordinates.
    known_position_index (int): The index of the known point.
    """
    idx = [i for i in range(len(x)) if i != known_position_index]
    plt.plot(x[idx], y[idx], "bs", markersize=5, markeredgecolor="b", label="Locations")


def plot_circle_centers(x_center, y_center):
    """
    Plots the centers of the circles.

    Parameters:
    x_center (list): The x-coordinates of the circle centers.
    y_center (list): The y-coordinates of the circle centers.
    """
    plt.plot(x_center, y_center, "ro", label="Centers")


def plot_surface(xy_r_list):
    """
    Plots the surface for each pair of 'x' and 'y' coordinates in xy_r_list.

    Parameters:
    xy_r_list (list): A list of pairs of 'x' and 'y' coordinates for the arcs.
    """
    for i, xy_r in enumerate(xy_r_list):
        if i == 0:
            plt.plot(xy_r[0], xy_r[1], "m-", color = 'black', label="Surface")
        else:
            plt.plot(xy_r[0], xy_r[1], "m-")


def plot_construction_lines(
    x_center_plot,
    y_center_plot,
    x_construction_lines,
    y_construction_lines,
    intersection_order,
):
    """
    Plots the construction lines.

    Parameters:
    x_center_plot, y_center_plot (list): Lists of x and y coordinates of the circle centers positions for the construction lines.
    x_construction_lines, y_construction_lines (list): Lists of x and y coordinates of the intersections for the construction lines.
    intersection_order (list): List of indices that represent the order of the intersections.
    """
    for k in intersection_order:
        if k == 0:
            plt.plot(
                [x_construction_lines[k], x_center_plot[k]],
                [y_construction_lines[k], y_center_plot[k]],
                "k:",
                label="Constr. Lines",
            )
        else:
            plt.plot(
                [x_construction_lines[k], x_center_plot[k]],
                [y_construction_lines[k], y_center_plot[k]],
                "k:",
            )


def plot_intersections(x_intersection, y_intersection):
    """
    Plots the intersections, which are the points where the construction lines intersect the surfaces.

    Parameters:
    x_intersection (list): The x-coordinates of the intersections.
    y_intersection (list): The y-coordinates of the intersections.
    """
    plt.plot(
        x_intersection,
        y_intersection,
        "gs",
        linewidth=1,
        markersize=5,
        markeredgecolor="g",
        label="Intersections",
    )


def min_max(var):
    """
    Returns the minimum and maximum of a variable. If the variable is a list, it returns the minimum and maximum values of the list. If the variable is a single number, it returns the number itself as both the minimum and maximum.

    Parameters:
    var (list or float): The variable for which to find the minimum and maximum. It can be a list or a single number.

    Returns:
    tuple: A tuple containing the minimum and maximum of the variable.
    """
    if isinstance(var, list):
        return min(var), max(var)
    else:
        return var, var


def set_plot_limits(
    x,
    y,
    end_x_displacement,
    end_y_displacement,
    xy_r_list,
    x_center_plot,
    y_center_plot,
):
    """
    Sets the plot limits[^1^][1].

    Parameters:
    x, y (list): Lists of x and y coordinates of the vectors locations.
    end_x_displacement, end_y_displacement (list): Lists of coordinates of ending point for the displacement vectors.
    xy_r_list (list): A list of pairs of 'x' and 'y' coordinates for the arcs.
    x_center_plot, y_center_plot (list): Lists of x and y coordinates of the circle centers positions for the construction lines.
    """
    # Get min and max of 'x', 'y', 'end_x_displacement' and 'end_y_displacement'
    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)
    end_x_displacement_min, end_x_displacement_max = min(end_x_displacement), max(
        end_x_displacement
    )
    end_y_displacement_min, end_y_displacement_max = min(end_y_displacement), max(
        end_y_displacement
    )

    # Get overall min and max values
    min_x = min(x_min, end_x_displacement_min)
    max_x = max(x_max, end_x_displacement_max)
    min_y = min(y_min, end_y_displacement_min)
    max_y = max(y_max, end_y_displacement_max)

    if xy_r_list and x_center_plot and y_center_plot:
        # Get min and max of xy_r_list_x and xy_r_list_y
        min_xy_r_list_x = min([min(pair[0]) for pair in xy_r_list])
        max_xy_r_list_x = max([max(pair[0]) for pair in xy_r_list])
        min_xy_r_list_y = min([min(pair[1]) for pair in xy_r_list])
        max_xy_r_list_y = max([max(pair[1]) for pair in xy_r_list])

        # Get overall min and max values
        min_x = min(min_xy_r_list_x, min(x_center_plot), min_x)
        max_x = max(max_xy_r_list_x, max(x_center_plot), max_x)
        min_y = min(min_xy_r_list_y, min(y_center_plot), min_y)
        max_y = max(max_xy_r_list_y, max(y_center_plot), max_y)

    # Set plot limits
    plt.xlim([float(min_x) - 10, float(max_x) + 10])
    plt.ylim([float(min_y) - 10, float(max_y) + 10])


def show_plot():
    """
    Displays the plot with a legend, equal aspect ratio, and grid.
    """
    plt.legend()
    plt.axis("equal")
    plt.grid(True)
    plt.show()
