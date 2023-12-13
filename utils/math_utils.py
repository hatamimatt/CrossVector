"""
This Python script includes a set of functions that are used to handle and visualize data in the graphical user interface (GUI). These functions perform a variety of tasks such as solving systems of equations, converting angles from one representation to another, calculating circle centers and trigonometric angles, and creating and managing various GUI elements like buttons, labels, frames, and dropdown menus. They also manage user interactions with these elements, such as selections made in dropdown menus and button clicks. The script ensures that the application is dynamic, interactive, and user-friendly, providing a responsive and intuitive user experience.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import real  # isclose,
import sympy
from sympy import Eq, S, Symbol, linsolve, re, solve, solveset, sqrt, symbols, sympify


def check_angles(df):
    """
    This function checks if the angles in a DataFrame are in descending order.
    If not, it removes any row where the angle is greater than the next one.

    Parameters:
    df (pd.DataFrame): A DataFrame with at least two columns 'x' and 'angle'.

    Returns:
    df (pd.DataFrame): The DataFrame after removing rows where the angle is greater than the next one.
    """

    # Sort the DataFrame by 'x' in ascending order and reset the index
    df = df.sort_values(by='x').reset_index(drop=True)

    # Create a new column 'next_angle' that contains the next row's angle
    df['next_angle'] = df['angle'].shift(-1)

    # Drop any rows where the current angle is greater than the next one
    df = df.drop(df[df['angle'] > df['next_angle']].index)

    # Remove the 'next_angle' column
    df = df.drop(columns=['next_angle'])

    return df
    

def custom_solve(equations, variables):
    """
    This function solves a system of equations and handles complex solutions in a MATLAB-like manner.

    Parameters:
    equations (list): A list of sympy equations.
    variables: A tuple of sympy variables to solve for.

    Returns:
    final_solutions (list): A list of solutions to the system of equations. Complex solutions are returned as complex numbers, and real solutions are returned as real numbers.
    """
    from sympy import Symbol, solve

    # Solve the system of equations
    solutions = solve(equations, variables)

    # Initialize an empty list to store the final solutions
    final_solutions = []

    # Loop through each solution
    for sol in solutions:
        # Check if the solution is a Symbol
        if isinstance(sol, Symbol):
            # Handle Symbol solution (you can modify this part as needed)
            final_solutions.append(sol)
        else:
            # If the imaginary part is negligible, return the real part
            if isclose(sol.imag, 0, atol=1e-15):
                final_solutions.append(sol.real)
            else:
                # Otherwise, return the complex solution
                final_solutions.append(sol)

    return final_solutions


def estimate_missing_vector(data, selected_position, known_position_index):
    """
    Estimate the angle of the first vector from the known position.

    This function handles two possible edge cases: when the head position of the landslide is known but the head vector displacement is unknown, or when the foot position of the landslide is known but the foot vector displacement is unknown. It uses the known position of the intersection with the profile and the adjacent vector to estimate the missing values.

    Parameters:
    data (pd.DataFrame): The input data. It should have four columns: 'x', 'y', 'angle', and 'length'.
    selected_position (str): The known position ('Head' or 'Foot').
    known_position_index (int): The index of the known intersection with the profile.

    Returns:
    data (pd.DataFrame): The output data with updated angle of the first vector.
    """
    # Extract the x, y, and angle from the data frame
    x, y, angle = [data[col].to_numpy() for col in ["x", "y", "angle"]]

    # Define the first and second vectors as numpy arrays
    v1 = np.array([x[known_position_index], y[known_position_index]])
    v2 = np.array(
        [
            x[known_position_index + (-1) ** (selected_position == "Foot")]
            - x[known_position_index],
            y[known_position_index + (-1) ** (selected_position == "Foot")]
            - y[known_position_index],
        ]
    )

    # Calculate the angle between the vectors using the dot product and the arccosine function
    angle = np.degrees(
        np.arccos(np.dot(v1, v2) / np.linalg.norm(v1) / np.linalg.norm(v2))
    )
    # Handle the case when the denominator is close to zero or the angle is greater than 90 degrees
    angle = (
        0
        if np.isclose(np.linalg.norm(v1) * np.linalg.norm(v2), 0)
        else angle - 90
        if angle > 90
        else angle
    )

    # Update the data frame with the new angle of the first vector
    data.loc[known_position_index, "angle"] = angle

    # Return the data frame
    return data


def convert_to_degrees(angles):
    """
    This function determines if the input angles are in radians or degrees based on their values.
    If the angles are in radians, it converts them to degrees.

    Parameters:
    angles: A list or numpy array of angles in either radians or degrees.

    Returns:
    angles: A numpy array of angles in degrees.
    """
    # Convert angles to a numpy array if it's not already
    angles = np.array(angles)

    # If the maximum angle is greater than 2*pi, assume the angles are in degrees
    if np.max(angles) > 2 * np.pi:
        return angles
    # Otherwise, assume the angles are in radians and convert them to degrees
    else:
        return np.degrees(angles)


def convert_alfa_to_trig(array_alfa):
    """
    This function converts a given array of angles from alfa representation to trigonometric representation.
    The alfa representation is an angle, assumed to be in degrees, identified by the positive y-axis, taken clockwise, to the displacement vector.

    Parameters:
    array_alfa: A list or numpy array of angles in alfa representation.

    Returns:
    array_trig: A numpy array of angles in trigonometric representation.
    """
    # Initialize an empty numpy array to store the converted angles
    array_trig = np.zeros(len(array_alfa))

    # Loop through each angle in the input array
    for i in range(len(array_alfa)):
        # Convert the angle based on its value
        if array_alfa[i] <= 90:
            array_trig[i] = 270 + array_alfa[i]
        elif array_alfa[i] <= 180:
            array_trig[i] = array_alfa[i] - 90
        elif array_alfa[i] <= 270:
            array_trig[i] = 90 + (array_alfa[i] - 180)
        else:
            array_trig[i] = 180 + (array_alfa[i] - 270)

    return array_trig


def remove_non_consecutive_arrays(
    xy_r_list, x_intersection, y_intersection
):  # , xy_r_list, x_center, y_center
    """
    This function removes the arrays from a list that do not have consecutive y and x values with their neighbors. It compares three consecutive arrays at a time and deletes the first or the second array depending on the concavity of the construction line.

    Parameters:
    xy_r_list (list): A list of arrays where each array contains alternating x and y values.
    x_intersection (list): A list of x intercepts corresponding to the arrays in xy_r_list.
    y_intersection (list): A list of y intercepts corresponding to the arrays in xy_r_list.
    x_center (list): A list of x centers.
    y_center (list): A list of y centers.

    Returns:
    x_intersection (list): The modified list of x intercepts.
    y_intersection (list): The modified list of y intercepts.
    """
    if len(xy_r_list) <= 2:
        i = 0
        while i < len(xy_r_list) - 1:
            # Get the y and x values of the current and next array
            y_values_current, x_values_current = (
                xy_r_list[i][1::2][0],
                xy_r_list[i][::2][0],
            )
            y_values_next, x_values_next = (
                xy_r_list[i + 1][1::2][0],
                xy_r_list[i + 1][::2][0],
            )

            # Check the concavity of the construction line and the consecutiveness of the y values
            if abs(y_values_current[-1] - y_values_next[0]) <= 5:
                # print(f"The arrays at index {i} and {i + 1} have consecutive y values.")
                i += 1  # Move to the next array
            else:
                # print(f"The arrays at index {i} and {i + 1} have non consecutive y values.")
                xy_r_list.pop(i + 1)  # Remove the next array
                x_intersection.pop(i + 1)
                y_intersection.pop(i + 1)
    else:
        i = 0
        while i < len(xy_r_list) - 2:
            # Get the y and x values of the current, next and third array
            y_values_current, x_values_current = (
                xy_r_list[i][1::2][0],
                xy_r_list[i][::2][0],
            )
            y_values_next, x_values_next = (
                xy_r_list[i + 1][1::2][0],
                xy_r_list[i + 1][::2][0],
            )
            y_values_third, x_values_third = (
                xy_r_list[i + 2][1::2][0],
                xy_r_list[i + 2][::2][0],
            )

            # Check the concavity of the construction line and the consecutiveness of the y values
            if (
                abs(y_values_current[-1] - y_values_next[0]) <= 5
                and abs(y_values_next[-1] - y_values_third[0]) <= 5
            ):
                # print(f"The arrays at index {i}, {i + 1} and {i + 2} have consecutive y values.")
                i += 1  # Move to the next array
            elif (
                abs(y_values_current[-1] - y_values_next[0]) <= 5
                and abs(y_values_next[-1] - y_values_third[0]) > 5
            ):
                # print(f"The arrays at index {i + 1} and {i + 2} have non consecutive y values.")
                xy_r_list.pop(i + 2)  # Remove the third array
                x_intersection.pop(i + 2)
                y_intersection.pop(i + 2)
                # x_center.pop(i + 2)
                # y_center.pop(i + 2)
            elif (
                abs(y_values_current[-1] - y_values_next[0]) > 5
                and abs(y_values_next[-1] - y_values_third[0]) <= 5
            ):
                # print(f"The array at index {i} does not have consecutive y values with the next array.")
                xy_r_list.pop(i)  # Remove the current array
                x_intersection.pop(i)
                y_intersection.pop(i)
                # x_center.pop(i)
                # y_center.pop(i)
            else:
                # print(f"The array at index {i + 1} does not have consecutive y values with the next array.")
                xy_r_list.pop(i + 1)  # Remove the next array
                x_intersection.pop(i + 1)
                y_intersection.pop(i + 1)
                # x_center.pop(i + i)
                # y_center.pop(i + i)

    # return x_intersection, y_intersection, xy_r_list, x_center, y_center
    return x_intersection, y_intersection


def calculate_circle_centers(preprocessed_data):
    """
    This function calculates the centers of the circles based on the given x and y coordinates and slopes.

    Parameters:
    preprocessed_data: A dictionary contatinig:
        x, y: Lists of x and y coordinates.
        m: List of slopes.

    Returns:
    circles: Adictionary containing:
        x_center, y_center: Lists of x and y coordinates of the circle centers.
    """
    # Unpack the preprocessed_data dictionary
    x = preprocessed_data["x_filtered"]
    y = preprocessed_data["y_filtered"]
    m = preprocessed_data["m_filtered"]

    # Define the symbols
    xtmp, ytmp = symbols("x y")

    # Initialize the lists to store the coordinates of the circle centers
    x_center = []
    y_center = []

    # Loop through the data
    for i in range(len(x) - 1):
        # Define the equations of the lines
        eqn1 = ytmp - xtmp * m[i] - (y[i] - x[i] * m[i])
        eqn2 = ytmp - xtmp * m[i + 1] - (y[i + 1] - x[i + 1] * m[i + 1])

        # Solve the system of equations to find the intersection points
        sol = solve([eqn1, eqn2], (xtmp, ytmp))

        # Append the solutions to the lists
        x_center.append(float(sol[xtmp]))
        y_center.append(float(sol[ytmp]))

    # Create a dictionary
    circles = {"x_center": x_center, "y_center": y_center}

    return circles


def calculate_trigonometric_angles(preprocessed_data, circles):
    """
    This function calculates the trigonometric angles of all radius-vectors.

    Parameters:
    preprocessed_data: A dictionary containing:
        x, y: Lists of x and y coordinates.
    circles: A dictionary containing:
        x_center, y_center: Lists of x and y coordinates of the circle centers.

    Returns:
    linear_spaced_angles: List of linearly spaced angles between the first and second angle.
    """
    # Unpack the preprocessed_data and the circles dictionaries
    x = preprocessed_data["x_filtered"]
    y = preprocessed_data["y_filtered"]
    x_center = circles["x_center"]
    y_center = circles["y_center"]

    # Calculate the difference between x and x_center, and y and y_center
    x_difference = np.array(x[:-1]) - np.array(x_center)
    y_difference = np.array(y[:-1]) - np.array(y_center)

    # Calculate the first angle using arctan2
    first_angle = np.arctan2(y_difference, x_difference)

    # If the angle is negative, add 2*pi to it
    negative_indices = np.where(first_angle < 0)
    first_angle[negative_indices] += 2 * np.pi

    # Repeat the above steps for the second angle
    x_difference2 = np.array(x[1:]) - np.array(x_center)
    y_difference2 = np.array(y[1:]) - np.array(y_center)
    second_angle = np.arctan2(y_difference2, x_difference2)
    negative_indices2 = np.where(second_angle < 0)
    second_angle[negative_indices2] += 2 * np.pi

    # Create a list of linearly spaced angles between the first and second angle
    linear_spaced_angles = [
        np.linspace(first_angle[n], second_angle[n], 25)
        for n in range(len(first_angle))
    ]

    return linear_spaced_angles


def calculate_intersections(
    preprocessed_data, circles, linear_spaced_angles, selected_position
):
    """
    This function calculates the intersection points between circles and lines, where the circles represent the paths of motion and the lines represent the construction lines normal to the vectors.
    The code then defines the starting x and y coordinates and filters the data based on the known position index.
    Finally, it resets the index of the DataFrame and updates the x and y values after filtering the data. This prepares the data for further processing.

    Parameters:
    preprocessed_data: A dictionary containg:
        x, y (list): Lists of x and y coordinates of the vectors locations.
        m (list): List of slopes of the construction lines.
        beta (list): List of vector inclinations.
    circles: A dictionary containing:
        x_center, y_center (list): Lists of x and y coordinates of the circle centers.
    linear_spaced_angles (list): List of trigonometric angles.
    selected_position (str): String indicating the known position ('head' or 'foot').

    Returns:
    intersections: A dictionary containing:
        x_intersection, y_intersection (list): List of x and y coordinates of the intersections.
        xy_r_list (list): A list of arrays where each array contains alternating x and y values of the circle coordinates.
        radii (list): List of radii of the circles.
        x_solution_values, y_solution_values (list): List of x and y coordinates of the solutions.
    """
    # Unpack the preprocessed_data and the circles dictionaries
    x = preprocessed_data["x_filtered"]
    y = preprocessed_data["y_filtered"]
    m = preprocessed_data["m_filtered"]
    beta = preprocessed_data["beta_filtered"]
    x_center = circles["x_center"]
    y_center = circles["y_center"]

    # Define the starting x and y coordinates
    known_x = x[0]
    known_y = y[0]

    # Define x and y as symbolic variables
    x_sym, y_sym = symbols("x_filtered y_filtered")

    # Define a lambda function to calculate circle coordinates
    circle_coordinates = lambda radius, rad_ang, OR_X, OR_Y: [
        radius * np.cos(rad_ang) + OR_X,
        radius * np.sin(rad_ang) + OR_Y,
    ]

    # Calculate the intersections of circles with the construction line
    x_intersection = []
    y_intersection = []
    xy_r_list = []
    radii = []
    int_solutions = []
    x_solution_values = []
    y_solution_values = []

    # Loop through all x coordinates except the last one
    for j in range(len(x) - 1):
        # Calculate the radius of the circle
        r = sqrt((x_center[j] - known_x) ** 2 + (y_center[j] - known_y) ** 2)

        # Append the radius to the radii list
        radii.append(r)

        # Define the equation of the circle
        eqn1 = Eq((x_sym - x_center[j]) ** 2 + (y_sym - y_center[j]) ** 2, r**2)

        # Define the equation of the construction line (normal to the second vector)
        eqn2 = Eq(y_sym, m[j + 1] * (x_sym - x[j + 1]))

        # Solve the system of equations to find the intersection points
        sol = solve([eqn1, eqn2], (x_sym, y_sym))
        int_solutions.append(sol)

        # Determine the concavity and select the appropriate y value
        if beta[j] > beta[j + 1]:  # Concavity upwards
            y_sol_temp = min([abs(sol[1]) for sol in int_solutions[j]])
        elif beta[j] < beta[j + 1]:  # Concavity downwards
            y_sol_temp = max([abs(sol[1]) for sol in int_solutions[j]])

        y_solution_values.append(y_sol_temp)
        x_solution_values_data = [abs(sol[0][0]) for sol in int_solutions]
        x_solution_values.append(
            x_solution_values_data[y_solution_values.index(y_sol_temp)]
        )

        x_sol_temp = x_solution_values[j]

        # Create an array of x and y values of the circle
        xy_r = circle_coordinates(
            radii[j], linear_spaced_angles[j], x_center[j], y_center[j]
        )

        # Append xy_r to the list
        xy_r_list.append(xy_r)

        # Update intersection points
        if selected_position == "head":
            x_sol = xy_r[0][0]
            y_sol = xy_r[1][0]
        else:
            x_sol = xy_r[0][-1]
            y_sol = xy_r[1][-1]

        # Save the intersection points
        x_intersection.append(x_sol)
        y_intersection.append(y_sol)

    # Remove non consecutive surfaces
    x_intersection, y_intersection = remove_non_consecutive_arrays(
        xy_r_list, x_intersection, y_intersection
    )

    intersections = {
        "x_intersection": x_intersection,
        "y_intersection": y_intersection,
        "xy_r_list": xy_r_list,
        "x_solution_values": x_solution_values,
        "y_solution_values": y_solution_values,
    }

    return intersections


def calculate_displacement_vectors(preprocessed_data):
    """
    Calculates the end points of the arrows (displacement vectors).

    Parameters:
    preprocessed_data: A dictionary containg:
        x (pd.Series): The x-coordinates.
        y (pd.Series): The y-coordinates.
        alpha (pd.Series): The angles of the displacement vectors.
        length (float): The length of the displacement vectors.

    Returns:
    displacements: A dictionary containing:
        end_x_displacement, end_y_displacement (list): The lists of coordinates of ending point for the displacement vectors
    """
    # Unpack the preprocessed_data dictionary
    x = preprocessed_data["x"]
    y = preprocessed_data["y"]
    alpha = preprocessed_data["alpha"]
    length = preprocessed_data["length"]

    deg = convert_alfa_to_trig(alpha)
    len_arr = 1 * length
    end_x_displacement = []
    end_y_displacement = []

    for k in range(len(deg)):
        ex = x[k] + len_arr[k] * np.cos(np.deg2rad(deg[k]))
        ey = y[k] + len_arr[k] * np.sin(np.deg2rad(deg[k]))

        end_x_displacement.append(ex)
        end_y_displacement.append(ey)

    displacements = {
        "end_x_displacement": end_x_displacement,
        "end_y_displacement": end_y_displacement,
    }

    return displacements


def calculate_construction_lines(
    preprocessed_data, circles, intersections, selected_position
):
    """
    Calculates the construction lines, which are dotted lines connecting the known point to the circle centers.

    Parameters:
    preprocessed_data: A dictionary containing:
        x, y (list): Lists of x and y coordinates of the vectors locations.
    circles: A dictionary containing:
        x_center (list): The x-coordinates of the circle centers.
        y_center (list): The y-coordinates of the circle centers.
    intersections: A dictionary containing:
        x_intersection, y_intersection (list): List of x and y coordinates of the intersections.
    selected_position (str): String indicating the known position ('head' or 'foot').

    Returns:
    construction_lines: A dictionary containing:
        x_center_plot, y_center_plot (list): Lists of x and y coordinates of the circle centers positions for the construction lines.
        x_construction_lines, y_construction_lines (list): Lists of x and y coordinates of the intersections for the construction lines.
        intersection_order (list): List of indices that represent the order of the intersections.
    """
    # Unpack the preprocessed_data and the circles dictionaries
    x = preprocessed_data["x_filtered"]
    y = preprocessed_data["y_filtered"]
    x_center = circles["x_center"]
    y_center = circles["y_center"]
    x_intersection = intersections["x_intersection"]
    y_intersection = intersections["y_intersection"]

    # print(f'!! HERE I AM !! {len(x_center)}')
    if len(x_center) > 1:
        # Extend x_center and y_center with their last element
        x_center_plot = x_center + [x_center[-1]]
        y_center_plot = y_center + [y_center[-1]]
        # The first point is the known one (head or foot)
        x_construction_lines = [x[0]] + x_intersection
        y_construction_lines = [y[0]] + y_intersection
    else:
        x_center_plot = x_center
        y_center_plot = y_center
        x_construction_lines = [x[0]]
        y_construction_lines = [y[0]]

    # Create a list of indices that represent the order of the intersections
    intersection_order = list(range(len(x_construction_lines)))

    # If the known position is 'head', reverse the order
    if selected_position == "head":
        intersection_order = intersection_order[::-1]

    construction_lines = {
        "x_center_plot": x_center_plot,
        "y_center_plot": y_center_plot,
        "x_construction_lines": x_construction_lines,
        "y_construction_lines": y_construction_lines,
        "intersection_order": intersection_order,
    }

    return construction_lines
