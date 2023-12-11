import plotly.graph_objects as go


def plot_known_point(fig, x, y, known_position_index):
    """
    Plots a known point on the graph.

    Parameters:
    fig (go.Figure): The figure object for the plot.
    x (pd.Series): The x-coordinates.
    y (pd.Series): The y-coordinates.
    known_position_index (int): The index of the known point.
    """
    fig.add_trace(
        go.Scatter(
            x=[x[known_position_index]],
            y=[y[known_position_index]],
            mode="markers",
            marker=dict(color="cyan", size=8),
            name="Known point",
        )
    )

    # fig.show()


def plot_vector_displacements(fig, x, y, end_x_displacement, end_y_displacement):
    """
    Plots the displacements of all points.

    Parameters:
    fig (go.Figure): The figure object for the plot.
    x (pd.Series): The x-coordinates.
    y (pd.Series): The y-coordinates.
    end_x_displacement, end_y_displacement (list): The lists of coordinates of ending point for the displacement vectors
    """
    # Get the number of fig.data before new plot
    num_data = len(fig.data)

    for k in range(len(end_x_displacement)):
        fig.add_trace(
            go.Scatter(
                x=[x[k], end_x_displacement[k]],
                y=[y[k], end_y_displacement[k]],
                mode="lines",
                line=dict(color="red"),
                name="Displacements",
            )
        )

    for i, trace in enumerate(fig.data):
        if i > num_data:
            trace.showlegend = False

    # fig.show()


def plot_vector_locations(fig, x, y, known_position_index):
    """
    Plots the locations of all points except the known one.

    Parameters:
    fig (go.Figure): The figure object for the plot.
    x (pd.Series): The x-coordinates.
    y (pd.Series): The y-coordinates.
    known_position_index (int): The index of the known point.
    """
    idx = [i for i in range(len(x)) if i != known_position_index]
    fig.add_trace(
        go.Scatter(
            x=x[idx],
            y=y[idx],
            mode="markers",
            marker=dict(color="blue", size=5),
            name="Locations",
        )
    )

    # fig.show()


def plot_circle_centers(fig, x_center, y_center):
    """
    Plots the centers of the circles.

    Parameters:
    fig (go.Figure): The figure object for the plot.
    x_center (list): The x-coordinates of the circle centers.
    y_center (list): The y-coordinates of the circle centers.
    """
    fig.add_trace(
        go.Scatter(
            x=x_center,
            y=y_center,
            mode="markers",
            marker=dict(color="red"),
            name="Centers",
        )
    )

    # fig.show()


def plot_surface(fig, xy_r_list):
    """
    Plots the surface for each pair of 'x' and 'y' coordinates in xy_r_list.

    Parameters:
    fig (go.Figure): The figure object for the plot.
    xy_r_list (list): A list of pairs of 'x' and 'y' coordinates for the arcs.
    """
    # Get the number of fig.data before new plot
    num_data = len(fig.data)

    for i, xy_r in enumerate(xy_r_list):
        # Convert the Float objects to numbers
        x = [float(x) for x in xy_r[0]]
        y = [float(y) for y in xy_r[1]]
        # Add the trace to the figure
        fig.add_trace(
            go.Scatter(
                x=x, y=y, mode="lines", line=dict(color="magenta"), name="Surface"
            )
        )

    for i, trace in enumerate(fig.data):
        if i > num_data:
            trace.showlegend = False

    # fig.show()


import numpy as np


def plot_construction_lines(
    fig,
    x_center_plot,
    y_center_plot,
    x_construction_lines,
    y_construction_lines,
    intersection_order,
):
    """
    Plots the construction lines on fig.

    Parameters:
    fig (go.Figure): The figure object for the plot.
    x_center_plot, y_center_plot (list): Lists of x and y coordinates of the circle centers.
    x_construction_lines, y_construction_lines (list): Lists of x and y coordinates of the intersections.
    intersection_order (list): List of indices for the intersection order.
    """
    # Get the number of fig.data before new plot
    num_data = len(fig.data)

    for k in intersection_order:
        # Add a black dashed line trace
        fig.add_trace(
            go.Scatter(
                x=[float(x_construction_lines[k]), x_center_plot[k]],
                y=[float(y_construction_lines[k]), y_center_plot[k]],
                mode="lines",
                line=dict(color="black", dash="dash"),
                name="Constr. Lines",
            )
        )

    for i, trace in enumerate(fig.data):
        if i > num_data:
            trace.showlegend = False

    # fig.show()


def plot_intersections(fig, x_intersection, y_intersection):
    """
    Plots the intersections, which are the points where the construction lines intersect the surfaces.

    Parameters:
    fig (go.Figure): The figure object for the plot.
    x_intersection (list): The x-coordinates of the intersections.
    y_intersection (list): The y-coordinates of the intersections.
    """
    # Convert the Float objects to numbers or strings
    x = [float(x) for x in x_intersection]  # or [str(x) for x in x_intersection]
    y = [float(y) for y in y_intersection]  # or [str(y) for y in y_intersection]
    # Add the trace to the figure
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=dict(color="green", size=5),
            name="Intersections",
        )
    )
