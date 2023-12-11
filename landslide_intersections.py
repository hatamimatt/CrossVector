"""
The method we’re using here is a mathematical equivalent of the graphical method originally proposed by Carter and Bentley in 1985 and later generalized by Cruden in 1986. This method is used to predict the subsurface geometry of a landslip, which is a type of landslide, from the measurement of superficial ground motion. 

The method involves the calculation of intersections of circles and lines, where the circle represents a path of motion and the line represents a construction line. The intersection points, which represents the points of intersection between the landslip and the ground surface, are calculated by solving a system of two equations simultaneously.

The algorithm proceeds as follows:

1. Calculate the radius of the first circle using the equation `r1=sqrt(x_01^2+y_01^2)`.
2. Determine the location of the first predicted point of the slip surface (V1), which corresponds to the intersection between the circle and the prolongation of the normal to the second vector. This is done by solving the system of equations:
   `(x_v1-x_01)^2+(y_v1-y_01)^2=r1^2` and `y_v1=m2*(x_v1-x_n2)`.
3. Calculate the radius of the second circle using the equation `r2=sqrt((x_02-x_v1)^2+(y_02-y_v1))`.

This process is repeated for each normal to the slipping vector positions. The result is a set of intersection points that can be used to predict the subsurface geometry of the landslip.

The script uses the displacement_vectors module, which has two main functions: prepare_data and calculate_coordinates.
The `calculate_landslide_intersections` function takes a dictionary that contains the output values of the prepare_data function, and returns a dictionary that contains the coordinates of the circles and lines, where the circles represent the paths of motion and the lines represent the construction lines normal to the vectors. The function also calculates the end point of the displacement vector, and the order of the intersection points in the order of occurrence.
"""

import numpy as np
import pandas as pd
from dateutil.parser import parse as parse_date
from typing import List, Union, Dict

from .utils import displacement_vectors_utils as dv


def printTest(input):
    print(input)
    


def calculate_landslide_intersections(
    data: pd.DataFrame,
    selected_rows: Union[List[int], None] = None,
    selected_position: str = "Foot",
    known_position_index: int = 0,
    impute_angle: str = "dot_product",
) -> Dict[str, Union[int, List[float], List[np.ndarray]]]:
    """
    This function calculates the intersections of circles with construction lines, based on the given data and selected position. It also calculates the circle centers, circle coordinates, radii, and solution values.

    Parameters
    ----------
    data : pd.DataFrame
        A DataFrame containing the x and y coordinates, lengths, and angles.
    selected_rows : list of int or None, optional
        A list of row indices (default is None).
    selected_position : str, optional
        A string indicating the selected position ("Head" or "Foot", default is "Foot").
    known_position_index : int, optional
        Index of the known intersection with the profile (default is 0).
    impute_angle : str, optional
        Selected algorithm for computing the angle in case of unknown vector displacement for the known_position_index ("dot_product" or "linear", default is "dot_product").

    Returns
    -------
    output : dict
        A dictionary that contains the following keys and values:
            known_position_index (int): Index of the known intersection with the profile (default is 0).
            'x' (list of float): A list of x coordinates of the vector positions.
            'y' (list of float): A list of y coordinates of the vector positions.
            'x_intersection' (list of float): A list of x coordinates of the intersection points.
            'y_intersection' (list of float): A list of y coordinates of the intersection points.
            'x_center' (list of float): A list of x coordinates of the centers of the circles.
            'y_center' (list of float): A list of y coordinates of the centers of the circles.
            'xy_r_list' (list of np.ndarray): A list of arrays of x and y values of the circles.
            'x_solution_values' (list of float): A list of x coordinates of the intersection points.
            'y_solution_values' (list of float): A list of y coordinates of the intersection points.

    Examples
    --------
    >>> data = pd.DataFrame({'x': [10, 12, 15, 18], 'y': [20, 22, 25, 28], 'length': [5, 6, 7, 8], 'angle': [30, 40, 50, 60]})
    >>> selected_rows = [0, 1, 2]
    >>> selected_position = 'Foot'
    >>> known_position_index = 0
    >>> impute_angle = 'dot_product'
    >>> calculate_landslide_intersections(data, selected_rows, selected_position, known_position_index, impute_angle)
    {'known_position_index': 0, 'x': [10, 12, 15], 'y': [20, 22, 25], 'x_intersection': [10.0, 11.0, 13.0], 'y_intersection': [20.0, 21.0, 23.0], 'x_center': [10.0, 11.0, 13.0], 'y_center': [20.0, 21.0, 23.0], 'xy_r_list': [array([[10.        , 10.        ],
       [10.        , 20.        ]]), array([[11.        , 11.        ],
       [11.        , 21.        ]]), array([[13.        , 13.        ],
       [13.        , 23.        ]])], 'x_solution_values': [10.0, 11.0, 13.0], 'y_solution_values': [20.0, 21.0, 23.0]}
    """
    # Prepare data
    preprocessed_data = dv.prepare_data(
        data, selected_rows, selected_position, known_position_index, impute_angle
    )
    
    # Calculate coordinates
    coordinates = dv.calculate_coordinates(preprocessed_data, selected_position)
    output = {
        "known_position_index": known_position_index,
        "x": preprocessed_data["x"],
        "y": preprocessed_data["y"],
        **coordinates,
    }
    
    if output["x_intersection"]:
        # Get the known point and the started point from the output dictionary
        known_point_x = (
            output["x"][0] if selected_position == "Head" else output["x"][-1]
        )
        
        started_point_x = (
            float(output["x_intersection"][0])
            if selected_position == "Head"
            else float(output["x_intersection"][-1])
        )
        
        known_point_y = (
            output["y"][0] if selected_position == "Head" else output["y"][-1]
        )
        
        started_point_y = (
            float(output["y_intersection"][0])
            if selected_position == "Head"
            else float(output["y_intersection"][-1])
        )
        
        # Check if the known point is different from the selected position
        if known_point_x != started_point_x:
            # Calculate the average number of points in the existing elements of xy_r_list
            num_points = int(np.mean([len(x) for x, y in output["xy_r_list"]]))
            
            # Create a linear connection between the known point and the started point with the same number of points
            surf0_x = np.linspace(known_point_x, started_point_x, num=num_points)
            surf0_y = np.linspace(known_point_y, started_point_y, num=num_points)
            surf0 = [surf0_x, surf0_y]
            
            # Add surf0 as an element to xy_r_list before its first element if selected_position is 'Head', otherwise after its last element
            if selected_position == "Head":
                output["xy_r_list"].insert(0, surf0)
            else:
                output["xy_r_list"].append(surf0)

    return output
