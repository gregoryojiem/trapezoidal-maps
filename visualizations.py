import matplotlib.pyplot as plt
from data_structures.dag_structures import PointNode, SegmentNode, LeafNode
import numpy as np

# Globals used for debugging while traversing the DAG
trapezoid_count = 0
trapezoids_seen = []
colors = plt.cm.get_cmap('hsv', 10)


def plot_dag(dag, bounding_trapezoid, reset):
    """
    Basic matplotlib function to create a visualization of a DAG
    Can choose to display only new trapezoids, or reset trapezoids_seen
    which will display the entire DAG
    :param dag: A directed acyclic graph
    :param bounding_trapezoid: The bounds for the plot
    :param reset: Whether to reset trapezoids_seen or not
    """
    global trapezoids_seen
    global trapezoid_count

    if reset:
        trapezoids_seen = []
        trapezoid_count = 0

    bot_seg = bounding_trapezoid.bot_seg
    top_seg = bounding_trapezoid.top_seg

    fig, ax = plt.subplots()
    ax.set_xlim(bot_seg.p1.x, bot_seg.p2.x)
    ax.set_ylim(bot_seg.p1.y, top_seg.p2.y)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("DAG Data")
    plot_dag_recursive(dag.head, ax)
    plt.show()


def plot_point(point, ax):
    """
    Plots a single point in the DAG
    :param point: The point to plot
    :param ax: matplotlib axes
    """
    hover_distance = 3
    ax.plot(point.x, point.y, color="dodgerblue", marker='o', markersize=4.5)
    ax.text(point.x, point.y + hover_distance, point.name, ha='center', va='center', color='black')


def plot_segment(segment, ax):
    """
    Plots a segment in the DAG
    :param point: The segment to plot
    :param ax: matplotlib axes
    """
    hover_distance = 4
    midpoint_x, midpoint_y = np.mean([[segment.p1.x, segment.p1.y], [segment.p2.x, segment.p2.y]], axis=0)
    ax.plot([segment.p1.x, segment.p2.x], [segment.p1.y, segment.p2.y], color="dodgerblue")
    ax.text(midpoint_x, midpoint_y + hover_distance, segment.name, ha='center', va='center', color='black')


def plot_trapezoid(trapezoid, ax):
    """
    Plots a trapezoid in the DAG
    :param point: The trapezoid to plot
    :param ax: matplotlib axes
    """
    # Used for debugging
    global trapezoid_count
    # Used to view only new regions added (e.g. see what changed after adding a left endpoint)
    global trapezoids_seen

    vertices = trapezoid.get_vertices()
    midpoint_x, midpoint_y = np.mean(vertices, axis=0)

    if (midpoint_x, midpoint_y) in trapezoids_seen:
        return

    trapezoids_seen.append((midpoint_x, midpoint_y))
    trapezoid_count += 1

    polygon = np.array(vertices)
    ax.fill(polygon[:, 0], polygon[:, 1], color=colors(trapezoid_count % 10), alpha=0.5)
    ax.text(midpoint_x, midpoint_y, trapezoid.name, ha='center', va='center', color='black')


def plot_dag_recursive(node, ax):
    """
    Recursive function that traverses the DAG and plots each node inside of it
    :param node: The current node we're plotting
    :param ax: matplotlib axes
    """
    curr_node = node.data

    if isinstance(curr_node, PointNode):
        plot_point(curr_node.point, ax)

    elif isinstance(curr_node, SegmentNode):
        plot_segment(curr_node.segment, ax)

    elif isinstance(curr_node, LeafNode):
        plot_trapezoid(curr_node.trap, ax)
        return

    plot_dag_recursive(curr_node.left, ax)
    plot_dag_recursive(curr_node.right, ax)


def debug_print(trap, vertices, color):
    print(f"Drawing trapezoid: {trap}")
    print(f"Color: {int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)}")
    print(f"vertices: {vertices}\n")
    print(f"There were: {trapezoid_count} trapezoids")

