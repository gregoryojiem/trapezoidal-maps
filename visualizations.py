import matplotlib.pyplot as plt
from trapezoidal_map import Segment, Point


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


def plot_dag(dag):
    pass