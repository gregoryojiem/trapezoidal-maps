import matplotlib.pyplot as plt
from dag_structures import Node, PointNode, SegNode, Leaf
import numpy as np


def plot_segments(segments, bounds):
    fig, ax = plt.subplots()

    for i, segment in enumerate(segments):
        ax.plot([segment.p1.x, segment.p2.x], [segment.p1.y, segment.p2.y], color="dodgerblue")
        ax.plot([segment.p1.x, segment.p2.x], [segment.p1.y, segment.p2.y],
                color="dodgerblue", marker='o', markersize=4.5)
        mid_p_x = (segment.p1.x + segment.p2.x) / 2
        mid_p_y = ((segment.p1.y + segment.p2.y) / 2) + 4
        ax.text(mid_p_x, mid_p_y, f"S{i + 1}", color="dodgerblue")

    ax.set_xlim(bounds[0], bounds[2])
    ax.set_ylim(bounds[1], bounds[3])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Line Segments")
    plt.show()


def plot_dag(dag, bounds):
    fig, ax = plt.subplots()
    plot_dag_recursive(dag.head, ax)
    ax.set_xlim(bounds[0], bounds[2])
    ax.set_ylim(bounds[1], bounds[3])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("DAG Data")
    plt.show()


trap_region_count = 0
regions_seen = []
colors = plt.cm.get_cmap('hsv', 10)


def plot_dag_recursive(node, ax):
    global trap_region_count
    global regions_seen
    curr_node = node.data
    if isinstance(curr_node, PointNode):
        point = curr_node.point
        ax.plot(point.x, point.y, color="dodgerblue", marker='o', markersize=4.5)
        ax.text(point.x, point.y + 4, point.name, ha='center', va='center', color='black')
        plot_dag_recursive(curr_node.left, ax)
        plot_dag_recursive(curr_node.right, ax)

    if isinstance(curr_node, SegNode):
        seg = curr_node.seg
        ax.plot([seg.p1.x, seg.p2.x], [seg.p1.y, seg.p2.y], color="dodgerblue")
        midpoint_x, midpoint_y = np.mean([[seg.p1.x, seg.p1.y], [seg.p2.x, seg.p2.y]], axis=0)
        ax.text(midpoint_x, midpoint_y + 4, seg.name, ha='center', va='center', color='black')
        plot_dag_recursive(curr_node.left, ax)
        plot_dag_recursive(curr_node.right, ax)

    if isinstance(curr_node, Leaf):
        trap = curr_node.trap
        vertices = trap.get_vertices()
        midpoint_x, midpoint_y = np.mean(vertices, axis=0)
        if (midpoint_x, midpoint_y) in regions_seen:
            return

        print("Drawing trapezoid: " + str(trap))
        color = colors(trap_region_count % 10)
        print(f"Color: {int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)}")
        print("vertices: " + str(vertices))
        print()

        polygon = np.array(vertices)
        ax.fill(polygon[:, 0], polygon[:, 1], color=color, alpha=0.5)
        ax.text(midpoint_x, midpoint_y, trap.name, ha='center', va='center', color='black')
        trap_region_count += 1
        regions_seen.append((midpoint_x, midpoint_y))
