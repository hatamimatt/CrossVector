import numpy as np

def calculate_angles(radar_position, pixel_position):
    """
    Calculate the dip and dip direction.

    Parameters:
    radar_position (tuple): A tuple of three floats representing the x, y, and z coordinates of the radar.
    pixel_position (tuple): A tuple of three floats representing the x, y, and z coordinates of the pixel.

    Returns:
    d (float): The distance between the radar position and the pixel position.
    delta_z (float): The difference in z between the radar and the pixel position.
    alpha (float): : This represents the dip direction, which is the angle relative to the north. The value of alpha can range from 0° to 360°, with both extremes indicating alignment with the north direction.
    beta (float): This represents the dip, or the angle in the z direction between the radar and the pixel. The value of beta can range from 0° to 90°. The convention is that beta is positive when the rotation starts from the ground plane and moves downward, and negative when it starts from the ground plane and moves upward.

    Note:
    The angles are calculated using spherical coordinates. The displacement vector length is calculated using the Euclidean distance formula.

    Usage:
    # Radar_position: (x_0, y_0, z_0)
    radar_position = (70595.00,23930.00,2442.00)  
    # Pixel_position : (x, y, z)
    pixel_position = (69993.00,23866.00,2206.00)  
    d, delta_z, alpha, beta = calculate_angles(radar_position, pixel_position)
    """
    # Unpack positions
    x_0, y_0, z_0 = radar_position
    x, y, z = pixel_position

    # Calculate deltas
    delta_x, delta_y, delta_z = x - x_0, y - y_0, -(z - z_0)

    # Calculate distance between the radar position and the pixel position
    d = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

    # Calculate angle beta (β)
    beta = np.degrees(np.arcsin(delta_z / d))

    # Calculate angle alpha (α) with several conditions
    initial_alpha = np.degrees(np.arctan(delta_y / delta_x))
    adjusted_alpha = initial_alpha + 360 if delta_x < 0 and delta_y >= 0 else initial_alpha + 180 if delta_x < 0 or delta_y < 0 else initial_alpha
    final_alpha = adjusted_alpha + 180 if z_0 < z else adjusted_alpha
    alpha = final_alpha - 180 if final_alpha > 360 else final_alpha

    return d, delta_z, alpha, beta


