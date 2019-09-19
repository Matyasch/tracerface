class Model():
    def __init__(self, data):
        self.__data = data


    def get_nodes(self):
        return self.__data.nodes


    def get_edges(self):
        return self.__data.edges