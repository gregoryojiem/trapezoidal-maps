import random
from dir_acyc_graph import DAG


def randomized_incremental_algorithm(segments, bbox):
    """
    Loops through all line segments in a randomized order and calls the DAG to update itself
    :param trap_map: TrapezoidalMap containing all important data
    :returns: Directed Acyclic Graph
    """
    # TODO remove seeding
    random.Random(4).shuffle(segments)
    num_segments = len(segments)
    dag = DAG(bbox)
    for _ in range(0, num_segments):
        segment = segments.pop(0)
        dag.add_new_segment(segment)
    print("Done generating DAG")
    return dag
