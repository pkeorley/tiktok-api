import json
from collections import Counter
from typing import Tuple, Union, List

import networkx as nx
from matplotlib import pyplot as plt

from tiktokapi.utils.color import Color


class Visualizer:
    def __init__(self, path: str):
        self._path = path
        self._json = self._get_json_data()

    def _get_json_data(self):
        """
        Reads a JSON file from the specified path and returns the loaded data.
        Parameters:
            self._path (str): The path to the JSON file.
        Returns:
            dict: The loaded JSON data.
        """
        with open(self._path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_plt(self, fig_size: Tuple[Union[float, int], Union[float, int]] = (12, 12)):
        """
        Generates the plot of the comments graph for a user.
        Parameters:
            fig_size (Tuple[Union[float, int], Union[float, int]]): The size of the figure (default: (12, 12))
        Returns:
            plt: The matplotlib.pyplot object containing the plot.
            figure: The matplotlib.figure.Figure object representing the figure.
        """

        graph = nx.Graph()
        color_map = {}

        # for nickname, comments in self._json["comments"].items():
        #     graph.add_node(nickname, color=username_color)
        #     color_map[nickname] = username_color
        #
        #     for comment in comments:
        #         graph.add_node(comment, color=comment_color)
        #         color_map[comment] = comment_color
        #
        #         graph.add_edge(nickname, comment)

        for username, comments in self._json["comments"].items():
            color = Color()

            graph.add_node(username, color=str(color))
            color_map[username] = str(color)

            for comment in comments:
                lighter_color = color.get_much_lighter()
                graph.add_node(comment, color=lighter_color)
                color_map[comment] = lighter_color
                graph.add_edge(username, comment)

        pos = nx.spring_layout(graph, k=0.20)  # Розміщення вузлів у графі
        node_colors = [color_map[node] for node in graph.nodes()]  # Визначаємо кольори для вузлів
        figure = plt.figure(figsize=fig_size)
        nx.draw(
            graph,
            pos,
            with_labels=True,
            node_size=500,
            font_size=10,
            node_color=node_colors
        )
        plt.title(f"Граф коментарів користувача {self._json['nickname']}")

        return plt, figure

    def get_statistics(self) -> dict:
        """
        Retrieves statistics about the comments in the JSON data.
        Returns:
            dict: A dictionary containing the following statistics:
                - "length": The total length of all comments combined.
                - "length_of_users_that_commented": The number of users who commented.
                - "counter": A Counter object that counts the length of each comment.
        """
        comments: List[str, List[str]] = self._json["comments"]
        counter = Counter({comment: len(comment) for comment in self._json["comments"]})

        return {
            "length": sum([len(comment) for comment in comments]),
            "length_of_users_that_commented": len(comments),
            "counter": counter
        }
