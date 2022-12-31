from data_structure.graphs.graph import Graph
class DeviceSelection:
    def __init__(self,N, X, data):
        __slots__ = '_devices','_max_words','_data','_graph','_deviceRight','_deviceLeft','_solution','_matches','_count'
        #TODO: METTERE SLOTS
        self._devices = N
        self._max_words = X
        self._data = data
        self._graph = Graph(True) #Residual graph
        self._deviceRight = []
        self._deviceLeft = []
        self._solution = []
        self._matches = {}
        self._count = 0
        self._maxFlow() #Compute the maxFlow and minimum number of partitions

    def countDevices(self):
        return self._count

    def nextDevice(self,i):
        if i<0 or i > (self._count-1): 
            raise Exception()
        if len(self._solution[i]) == 0:
            return None
        return self._solution[i].pop(0)


    def _dominates(self,d1,d2):
        result = True
        t1 = self._data[d1.element()]
        t2 = self._data[d2.element()]
        for i in range(0,len(t1)):
            if t1[i] <= t2[i]:
                result = False
        return result
    
    def _createBipartiteGraph(self):
        #Create a bipartite graph
        self.source = self._graph.insert_vertex("S")
        self.target = self._graph.insert_vertex("T")

        for d in self._devices:
            device = self._graph.insert_vertex(d)
            self._deviceLeft.append(device)
            self._graph.insert_edge(self.source,device,1)
            
            device = self._graph.insert_vertex(d)
            self._deviceRight.append(device)
            self._graph.insert_edge(device,self.target,1) 

        for d1 in self._deviceLeft:
            for d2 in self._deviceRight:
                if d1.element() == d2.element():
                    continue
                if self._dominates(d1,d2):
                    self._graph.insert_edge(d1,d2,1)
                
    
    def _maxFlow(self):
        #Create a bipartite graph
        self._createBipartiteGraph()
        #Iterate all the simple paths from source to target of the residual graph and then update it.
        path = {}
        while _customDFS(self._graph,self.source,self.target,path):
            node = self.target
            while(node != self.source):

                edge = path.get(node)
                prev_node = edge.origin() #next node
                
                self._graph.reverse_edge(prev_node,node)
                node = prev_node
            path.clear()

        #_printGraphDebug(self._graph)
        
        #Computing the matches
        #print("Computing the matches*********************************")
        
        for device in self._deviceRight:
            match = self._graph.get_outgoing_edge(device)
            #L'assunzione/osservazione è che nel dominio del nostro problema (grafo bipartito), un vertice ha sempre un solo arco uscente.
            #Questo può rappresentare un match con un altro device oppure un collegamento con il vertice Target 
            temp = next(iter(match.items()))[0]
            
            if(temp != self.target):
                #print("temp:",temp.element(),"device",device.element())
                self._matches.update({temp.element():[device.element()]})
            elif device.element() not in self._matches:
                #print("device:",device.element()," Not matched")
                self._matches.update({device.element():[]})

        # print("Check the matches*********************************")
        # for key,value in self._matches.items():
        #     print("key:",key,"value:",value)
        # print("*********************************")
        

        #Computing the partitions and assigning a rank
        self._makePartitions()

        # print("Check partitions*********************************")
        # for key,value in self._matches.items():
        #     print("key:",key,"value:",value)
        # print("*********************************")
        
        for key,value in self._matches.items():
            #print("key:",key,"value",value)
            if(len(value) == 0):
                #print([key])
                self._solution.append([key])
                self._count +=1
            else:
                self._count += 1
                value.insert(0,key)
                self._solution.append(value)
                #print(value)
        #print("*********************************")
        #print(self._solution)

        
    # def _makePartitions2(self):
    #     for key,value in self._matches.entries():
            
    #         for list in self._solution:
    #             for device in list:
    #                 pass
                
                
    def _makePartitions(self):
        keys = list(self._matches.keys())
        visited_keys = set()

        for k in keys:
            if k in visited_keys:
                continue
            else:
                visited_keys.add(k)

            value = self._matches.get(k)
            if (value == None or len(value) == 0):
                continue
            #print(value)
            _check_value(self._matches,k,value[0],visited_keys)
        


def _check_value(matches: dict,k: str,value: str,visited_keys: set):  
    #print("k:",k,"value:",value)
    check = matches.get(value)
    if (check == None or len(check) == 0): #La lista è vuota. Il valore della entry considerata non domina nessun altro device.
        return

    #In questo punto del codice, il valore della entry considerata domina un altro device
    merge_entry = matches.pop(value) #Rimuovo la entry dal dizionario per fonderla con l'entry considerata.
                                            #merge_entry è una tupla
    #print(merge_entry)
    #Due casi possibili:
    # 1 caso: Il valore della entry considerata si mappa con una key già visitata
    if value in visited_keys:
        matches[k].append(merge_entry) #Faccio l'append della list della entry di chiave k con la lista recuperata
        return
    else:
    # 2 caso: il valore si mappa con una key non ancora visitata. Dopo aver fuso le due entry devo controllare con chi si mappa il valore della nuova entry.
        visited_keys.add(value)
        for elem in merge_entry:
            matches[k].append(elem)
        #print(matches[k])
        #Devo vedere se il valore merge_entry mappa un'altra entry
        new_value = merge_entry[0]
        
        _check_value(matches,k,new_value,visited_keys)
        
    return

def _customDFS(g: Graph,s: Graph.Vertex,t: Graph.Vertex,discovered: dict):
    """
    Return True if there is a path from s to t. The path must be computed starting from the Vertex t in the dictionary passed as parameter.
    Return False if there is not a path from s to t.
    """
    for e in g.incident_edges(s):    # for every outgoing edge from s
        v = e.opposite(s)
        if v not in discovered:        # v is an unvisited vertex
            discovered[v] = e          # e is the tree edge that discovered v
            if(v != t):
                if(_customDFS(g,v,t,discovered)):
                    return True
            else:
                return True
    return False
                    
def _printGraphDebug(graph: Graph):
    vertices = graph.vertices()
    l = list()
    for v in vertices:
        print("[Vertex]:",v)
        print("outgoing")
        for e in graph.incident_edges(v):
            l.append((e.origin().element(),e.destination().element()))
        print(l)
        l.clear()
        print("incoming")
        for e in graph.get_incoming_edge(v).values():
            l.append((e.origin().element(),e.destination().element()))
        
        print(l)
        l.clear()