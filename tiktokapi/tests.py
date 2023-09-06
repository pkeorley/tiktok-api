import os
from utils.visualizer import Visualizer

if __name__ == "__main__":

    path = os.listdir("../datas")[0]
    print(path)

    statistics = Visualizer("../datas/" + path).get_statistics()

    for key, value in sorted(dict(statistics["counter"]).items(), key=lambda x: x[1]):
        print(f"{key}   =>   {value} штук.")

    print(statistics)

