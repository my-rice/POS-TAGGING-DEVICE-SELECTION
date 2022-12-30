from data_structure.graphs.graph import Graph
class DeviceSelection:
    def __init__(self,N, X, data):
        #TODO: RENDERE ATTRIBUTI E METODO PRIVATE ECCETTO I 3 DI INTERFACCIA
        #TODO: METTERE SLOTS
        self.devices = N
        self.max_words = X
        self.data = data
        self.graph = Graph(True) #Residual graph
        self.flow = dict()
        self.deviceRight = list()
        self.deviceLeft = list()

    def countDevices(self):
        pass
        return 1

    def nextDevice(self,i):
        pass
        return None


    def dominates(self,d1,d2):
        result = True
        for i in len(d1):
            if d1[i] <= d2[i]:
                result = False
        return result
    
    def createBipartiteGraph(self):
        #Create a bipartite graph
        self.source = self.graph.insert_vertex("S")
        self.target = self.graph.insert_vertex("T")

        for d in self.devices:
            device = self.graph.insert_vertex(d)
            self.deviceLeft.append(device)
            self.graph.insert_edge(self.source,device,1)
            
            device = self.graph.insert_vertex(d)
            self.deviceRight.append(device)
            self.graph.insert_edge(device,self.target,1)        

        for d1 in self.deviceLeft:
            for d2 in self.deviceRight:
                if d1.element() == d2.element():
                    continue
                if self.dominates(d1,d2):
                    self.graph.insert_edge(d1,d2,1)
                
    def augment(P,f):
        pass
    def maxFlow(self):
        #Create a bipartite graph
        self.createBipartiteGraph()
        path = []

        while self.BFS(path):
            s = self.target
            #flow = s.
            #while 



