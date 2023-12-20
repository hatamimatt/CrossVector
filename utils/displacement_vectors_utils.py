"""
This Python performs some calculations on a data set of displacement vectors.

The script has two main functions: `prepare_data` and `calculate_coordinates`.

The `prepare_data` function takes a data frame that contains the x and y coordinates, angles, and lengths of the displacement vectors, and returns a dictionary that contains the same values along with the slopes and filtered versions of them based on the selected position ('Head' or 'Foot'). The function also sorts and filters the data according to the selected position and the known intersection with the profile.

The `calculate_coordinates` function takes a dictionary that contains the output values of the `prepare_data` function, and returns a dictionary that contains the coordinates of the circles and lines, where the circles represent the paths of motion and the lines represent the construction lines normal to the vectors. The function also calculates the end point of the displacement vector, and the order of the intersection points in the order of occurrence.

The script uses the modules pandas, numpy, sympy, and math to perform the calculations. The script also uses some helper functions to calculate the circle centers, the trigonometric angles, the intersections, and the construction lines.

Usage examples:

# Import the script
import displacement_vectors as dv

#Define the sample data frame
data = pd.DataFrame({ 'x': [350, 351, 403, 429, 460], 'y': [169, 168, 111, 81, 50], 'angle': [np.nan, 55, 76, 85, 98], 'length': [np.nan, 105, 140, 35, 105] })

# Prepare the data
preprocessed_data = dv.prepare_data(data, selected_rows, selected_position, known_position_index)

# Calculate the coordinates
coordinates = dv.calculate_coordinates(output, 'Foot')

# Plot the results
dv.plot_all(**coordinates)
"""

import numpy as np
import pandas as pd
from dateutil.parser import parse as parse_date
from typing import List, Union, Dict

#from .utils import math_utils as math

from . import math_utils as math


# Define a function to prepare the data for further calculations
def prepare_data(
    raw_data: pd.DataFrame,
    selected_rows: Union[List[int], None] = None,
    selected_position: str = "Foot",
    known_position_index: int = 0,
    impute_angle: str = "dot_product",
) -> Dict[str, np.ndarray]:
    """
    Prepares the data for further calculations.

    This function takes a data frame that contains the x and y coordinates, angles, and lengths of the displacement vectors, and returns a dictionary that contains the same values along with the slopes and filtered versions of them based on the selected position.
    The function sorts and filters the data according to the selected position (head or foot) and rows. It also calculates the beta angle as 180 degrees plus or minus the alpha angle, depending on the position. Then, it extracts the x, y, alpha, beta, and length values as numpy arrays. It only keeps the data from the known position index to the end. If the angle of the first or last vector is missing, it estimates it using one of two methods, depending on the 'impute_angle' parameter. The default method is 'linear', which uses the next point with a known angle for the calculations, and at the end it draws a straight line between that point and the original point. The other method is 'dot_product', which uses the dot product and the arccosine function to find the angle between the vector and the adjacent vector.

    Parameters
    ----------
    raw_data : pd.DataFrame
        The input data. It should have four columns: 'x', 'y', 'angle', and 'length'.
    selected_rows : list of int or None, optional
        The rows of the data to be selected. If None, all rows are selected. Default is None.
    selected_position : str, optional
        The known position ('Head' or 'Foot'). It determines how the data is sorted and filtered. Default is 'Foot'.
    known_position_index : int, optional
        The index of the known intersection with the profile. It determines the starting point of the filtered data. Default is 0.
    impute_angle : str, optional
        Selected algorithm for computing the angle in case of unknown vector displacement for the known_position_index. It can be either 'linear' or 'dot_product'. Default is 'linear'.

    Returns
    -------
    preprocessed_data : dict
        A dictionary that contains the following keys and values:
            'x' (np.array): The x coordinates of the displacement vectors.
            'y' (np.array): The y coordinates of the displacement vectors.
            'alpha' (np.array): The angles of the displacement vectors.
            'x_filtered' (np.array): The filtered x coordinates of the displacement vectors.
            'y_filtered' (np.array): The filtered y coordinates of the displacement vectors.
            'alpha_filtered' (np.array): The filtered angles of the displacement vectors.
            'beta_filtered' (np.array): The filtered complementary angles of the displacement vectors.
            'm_filtered' (np.array): The filtered slopes of the construction lines normal to the displacement vectors.

    Examples
    --------
    >>> data = pd.DataFrame({'x': [10, 12, 15, 18], 'y': [20, 22, 25, 28], 'length': [5, 6, 7, 8], 'angle': [30, 40, 50, 60]})
    >>> selected_rows = [0, 1, 2]
    >>> selected_position = 'Foot'
    >>> known_position_index = 0
    >>> impute_angle = 'dot_product'
    >>> prepare_data(data, selected_rows, selected_position, known_position_index, impute_angle)
    {'x': array([10, 12, 15]), 'y': array([20, 22, 25]), 'alpha': array([30, 40, 50]), 'x_filtered': array([10, 12, 15]), 'y_filtered': array([20, 22, 25]), 'alpha_filtered': array([30, 40, 50]), 'beta_filtered': array([210, 220, 230]), 'm_filtered': array([-0.57735027, -0.36397023, -0.26794919])}
    """
    data = raw_data.copy()
    
    # Adjust the angle 'angle' in the dataset. Originally, 'angle' is defined with respect to the horizontal axis, with positive values indicating a negative y-direction. This line of code redefines 'angle' to be with respect to the vertical axis, with positive values indicating a positive x-direction. For example, an original 'angle' of 5 degrees becomes 85 degrees, and an 'angle' of -7 degrees becomes 7 degrees.
    data.angle = np.where(data.angle >= 0, 90 - data.angle, abs(data.angle))

    # Check the profile direction and filter the data according to the angles
    data = math.loop_until_no_change(data, selected_position)
    
    # Sort the data by the y coordinate
    data = data.sort_values(
        by="x", ascending=(selected_position == "Head"), ignore_index=True
    )

    print(f' data being printed from displacement vectors utils after being sorted on x: {data}')

    if data.empty or len(data) < 2:
        print(
        "ERROR - For this particular geometry, it is impossible to calculate the rotational or roto-translational sliding surface."
    )
        return {}
    
    # Filter the data by the selected rows, if any
    if selected_rows is not None:
            # Check if any selected row is out of bounds
        if max(selected_rows) >= len(data):
            print("WARNING - One or more selected rows are out of bounds.")
            pass
        else:
            data = data.iloc[selected_rows].reset_index(drop=True)

    # Estimate the length of the first or last vector, if needed
    if np.isnan(data.length[known_position_index]):
        # Get the length of the data.length dictionary
        n = len(data.length)
        # Use the modulo operator to wrap around the index when it is negative
        index = (known_position_index + (-1) ** (selected_position == "Foot")) % n
        # Assign the value to the DataFrame using the corrected index
        data.iloc[known_position_index, data.columns.get_loc("length")] = data.length[
            index
        ]

    # Initialize original_position_index
    original_position_index = []
    # Estimate the angle of the first or last vector, if needed
    if np.isnan(data.angle[known_position_index]):
        if impute_angle == "linear":
            # Store original known_position_index
            original_position_index = known_position_index
            # Use the next point with a known angle for the calculations
            known_position_index += (-1) ** (selected_position == "Foot")
        else:
            # Use the estimate_missing_vector function to find the angle
            data = math.estimate_missing_vector(
                data, selected_position, known_position_index
            )

    # Remove any other point which has angle NaN
    data = data.dropna(subset=["angle"])

    # Calculate the beta angle
    # The beta angle is the angle between the vector and the horizontal line, and it is opposite to the alpha angle for the head position, but equal to the alpha angle for the foot position.
    data["beta"] = 180 + (-1) ** (selected_position == "Head") * data["angle"]

    # Convert the data to numpy arrays
    x, y, alpha, beta, length = [
        data[col].to_numpy() for col in ["x", "y", "angle", "beta", "length"]
    ]

    # Slice the data from the known position index to the end
    data_filtered = data.iloc[known_position_index:].reset_index(drop=True)

    # Convert the filtered data to numpy arrays
    x_filtered, y_filtered, alpha_filtered, length_filtered = [
        data_filtered[col].to_numpy() for col in ["x", "y", "angle", "length"]
    ]
    beta_filtered = 180 + (-1) ** (selected_position == "Head") * alpha_filtered

    # Calculate the slopes of the construction lines as the tangent of alpha
    m = np.tan(np.deg2rad(alpha))
    m_filtered = np.tan(np.deg2rad(alpha_filtered))

    # Return the preprocessed data as a dictionary
    preprocessed_data = {
        "x": x,
        "y": y,
        "alpha": alpha,
        "beta": beta,
        "length": length,
        "m": m,
        "x_filtered": x_filtered,
        "y_filtered": y_filtered,
        "alpha_filtered": alpha_filtered,
        "beta_filtered": beta_filtered,
        "length_filtered": length_filtered,
        "m_filtered": m_filtered,
        "original_position_index": original_position_index,
    }

    # Return the output dictionary
    return preprocessed_data


# Define a function to calculate the coordinates of the circles and lines
def calculate_coordinates(preprocessed_data: Dict[str, np.ndarray], selected_position: str) -> Dict[str, Union[List[float], List[np.ndarray]]]:
    """
    Calculates the coordinates of the circles and lines, where the circles represent the paths of motion and the lines represent the construction lines normal to the vectors.

    Parameters
    ----------
    preprocessed_data : dict
        A dictionary that contains the output values of the prepare_data function.
    selected_position : str
        The known position ('Head' or 'Foot').

    Returns
    -------
    coordinates : dict
        A dictionary that contains the following keys and values:
            'x_center' (list of float): A list of x coordinates of the centers of the circles.
            'y_center' (list of float): A list of y coordinates of the centers of the circles.
            'x_intersection' (list of float): A list of x coordinates of the intersection points.
            'y_intersection' (list of float): A list of y coordinates of the intersection points.
            'xy_r_list' (list of np.ndarray): A list of arrays of x and y values of the circles.
            'x_solution_values' (list of float): A list of x coordinates of the intersection points.
            'y_solution_values' (list of float): A list of y coordinates of the intersection points.

    Examples
    --------
    >>> preprocessed_data = {'x': array([10, 12, 15]), 'y': array([20, 22, 25]), 'alpha': array([30, 40, 50]), 'x_filtered': array([10, 12, 15]), 'y_filtered': array([20, 22, 25]), 'alpha_filtered': array([30, 40, 50]), 'beta_filtered': array([210, 220, 230]), 'm_filtered': array([-0.57735027, -0.36397023, -0.26794919])}
    >>> selected_position = 'Foot'
    >>> calculate_coordinates(preprocessed_data, selected_position)
    {'x_center': [10.0, 11.0...
    """
    # Calculate the circle centers and the displacement vectors
    circles = math.calculate_circle_centers(preprocessed_data)
    displacements = math.calculate_displacement_vectors(preprocessed_data)

    # Initialize empty dictionaries for the intersections and the construction lines
    intersections = {}
    construction_lines = {}

    # Only proceed if there are circle centers
    if not math.check_empty_values(circles):
        # Calculate the trigonometric angles, the intersections and the construction lines
        linear_spaced_angles = math.calculate_trigonometric_angles(
            preprocessed_data, circles
        )
        intersections = math.calculate_intersections(
            preprocessed_data, circles, linear_spaced_angles, selected_position
        )
        construction_lines = math.calculate_construction_lines(
            preprocessed_data, circles, intersections, selected_position
        )

    # Return the coordinates as a dictionary
    coordinates = {**circles, **intersections, **construction_lines, **displacements}

    return coordinates
