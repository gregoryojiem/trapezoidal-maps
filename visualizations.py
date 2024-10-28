import matplotlib.pyplot as plt


def plot_segments(segments, bounds):
    fig, ax = plt.subplots()

    for i, segment in enumerate(segments):
        ax.plot([segment.p1[0], segment.p2[0]], [segment.p1[1], segment.p2[1]], color="dodgerblue")
        ax.plot([segment.p1[0], segment.p2[0]], [segment.p1[1], segment.p2[1]],
                color="dodgerblue", marker='o', markersize=4.5)
        mid_p_x = (segment.p1[0] + segment.p2[0]) / 2
        mid_p_y = ((segment.p1[1] + segment.p2[1]) / 2) + 4
        ax.text(mid_p_x, mid_p_y, f"S{i + 1}", color="dodgerblue")

    ax.set_xlim(bounds[0], bounds[2])
    ax.set_ylim(bounds[1], bounds[3])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Line Segments")
    plt.show()
