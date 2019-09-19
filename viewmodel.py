class ViewModel():
    def __init__(self, model):
        self.__model = model


    def get_nodes(self):
        return [{'data': {'id': node}} for node in self.__model.get_nodes()]


    def get_edges(self):
        return [{'data': {'source': edge[1], 'target': edge[0]}} for edge in self.__model.get_edges()]