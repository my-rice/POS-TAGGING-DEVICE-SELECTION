from data_structure.graphs.graph import Graph
class IndexOutOfRangeError(Exception):
    pass
class DeviceSelection:
    def __init__(self,N, X, data):
        """
        It is the constructor method of DeviceSelection class. It creates a new DeviceSelection object and computes the partiotions of devices.
        Input:
            - N is a tuple of strings identifying the devices.
            - X is an integer
            - data is a dictionary whose keys are the elements of N, and whose values are tuples of X-2 elements describing the
            performances of the corresponding device over sentences from 3-term to X-term.
        """

        __slots__ = '_devices','_max_words','_data','_graph','_deviceRight','_deviceLeft','_solution','_matches','_count'
        
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
        """
        The countDevies method returns the minimum number C of devices for which we need to run the expensive tests. 
        That is, C is the number of subsets in which the devices are partitioned so that every subset satisfies the non-interleaving property;
        """
        return self._count

    def nextDevice(self,i):
        """
        The nextDevice method takes in input an integer i between 0 and C-1, and returns
        the string identifying the device with highest rank in the i-th subset that has
        been not returned before, or None if no further device exists (e.g., the first call
        of nextDevice(0) returns the device with the highest rank in the first subset,
        i.e., the one that dominates all the remaining devices in this subset, the
        second call returns the device with the second highest rank, and so on). The
        method throws an exception if the value in input is not in the range [0, C-1].
        """
        if i<0 or i > (self._count-1): 
            raise IndexOutOfRangeError("Index:",i,"is out of range!")
        if len(self._solution[i]) == 0:
            return None
        return self._solution[i].pop(0)


    def _dominates(self,d1: Graph.Vertex,d2: Graph.Vertex):
        """
        This method takes in input two verteces of a graph, d1 and d2, and returns:
            - True, if d1 dominates d2.
            - False, if d1 does not dominate d2.
        A device A dominates a device B if the performances of the device A are strictly better than the performances of the
        the device B, on all possible sentence lengths.
        """
        result = True
        t1 = self._data[d1.element()]
        t2 = self._data[d2.element()]
        for i in range(0,len(t1)):
            if t1[i] <= t2[i]:
                result = False
        return result
    
    def _create_FlowNetwork_on_BipartiteGraph(self):
        """
        This method creates a flow network based on a bipartite graph. The bipartite graph is built as follows:
        We represent devices on a bipartite graph with N (N = number of devices) nodes on each side, 
        with an edge between node u and node v only if u represents a device
        that dominates the device represented by v. Note that u and v belong to different sides of the bipartite graph.
        """
        #Create a bipartite graph
        self.source = self._graph.insert_vertex("S")
        self.target = self._graph.insert_vertex("T")

        #Creating all vertices and edges from verteces to target and from source to target  
        for d in self._devices:
            device = self._graph.insert_vertex(d)
            self._deviceLeft.append(device)
            self._graph.insert_edge(self.source,device,1)
            
            device = self._graph.insert_vertex(d)
            self._deviceRight.append(device)
            self._graph.insert_edge(device,self.target,1) 
        #Creating all edges from left verteces to right verteces based on domination relationship  
        for d1 in self._deviceLeft:
            for d2 in self._deviceRight:
                if d1.element() == d2.element():
                    continue
                if self._dominates(d1,d2):
                    self._graph.insert_edge(d1,d2,1)
                
    
    def _maxFlow(self):
        """
        This methods compute the max flow of a flow network built on a bipartite graph.
        The idea is that computing the max flow means finding the maximum cardinality matching between all the devices, 
        in other words the purpose of this method is finding a matching that covers as many vertices as possible.
        The final operation of this method is to partition the N devices in subsets using the matching previously computed. 
        In this way each subset enjoys the no-interleaving property and the computation is made such that we have the minimum number of subsets.
        In addition, in each subset the position of each device represents its rank.
        """
        #Create a bipartite graph
        self._create_FlowNetwork_on_BipartiteGraph()

        #Iterate all the simple paths from source to target of the residual graph and then update it, reversing the edges of the found path.
        path = {}
        while _customDFS(self._graph,self.source,self.target,path):
            node = self.target
            while(node != self.source):
                edge = path.get(node)
                prev_node = edge.origin() #next node
                
                self._graph.reverse_edge(prev_node,node)
                node = prev_node
            path.clear()
            
        #Computing the matches

        for device in self._deviceRight:
            match = self._graph.get_outgoing_edge(device)
            #L'assunzione/osservazione è che nel dominio del nostro problema (flow network di un grafo bipartito), un vertice ha sempre un solo arco uscente.
            #Questo può rappresentare un match con un altro device oppure un collegamento con il vertice Target
            #Se l'arco uscente incide sul Target, allora il nodo non ha un matching. 
            #Se l'arco uscente incide su un altro nodo del grafo, detto X, allora il nodo ha un matching e significa che quest'ultimo nodo è dominato da X.
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
        
        #Inserting the discovered partitions in the solution list and computing the number of partitions.  
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
          
    def _makePartitions(self):
        """
        This method partition the devices in subsets using the matching previously computed.
        """
        #Creating a copy of the keys of the dictionary self._matches
        keys = list(self._matches.keys())
        #Saving all the visited_keys in the following iteretion
        visited_keys = set()

        #Iterate all the keys of self._matches
        for k in keys:
            if k in visited_keys:
                continue
            else:
                visited_keys.add(k)

            value = self._matches.get(k)
            if (value == None or len(value) == 0):
                continue
            #print(value)
            #I have to check the value associated to k. If the value appears in another match, the two matches must be merged into a single partition  
            _check_value(self._matches,k,value[0],visited_keys)
        


def _check_value(matches: dict,k: str,value: str,visited_keys: set): 
    """
    This is an helper function for _makePartitions method. It is a recursive function. 
    """ 
    #print("k:",k,"value:",value)
    check = matches.get(value)
    if (check == None or len(check) == 0): #La lista è vuota. Il valore della entry considerata non domina nessun altro device.
        return

    #In questo punto del codice, il valore della entry considerata domina un altro device
    merge_entry = matches.pop(value) #Rimuovo la entry dal dizionario per fonderla con l'entry considerata.
                                     #merge_entry è una tupla
    #print(merge_entry)

    #Merging...
    #Due casi possibili:
    # 1 caso: Il valore della entry considerata si mappa con una key già visitata in una precedente iterazione
    if value in visited_keys:
        for elem in merge_entry: #Faccio l'append della list della entry di chiave k con la lista recuperata
            matches[k].append(elem)
        return
    else:
    # 2 caso: Il valore della entry considerata si mappa con una key non ancora visitata.
    #         Dopo aver fuso le due entry devo controllare se il valore di merge_entry (la nuova entry) si mappa con un'ulteriore entry.
    # Nota: Nel ramo else il valore di merge_entry è sicuramente di un solo valore perché il merge viene fatto sull'iterazione corrente ed un match ancora non visitato NON può contenere più di un valore. 
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
    This function is a customization of the traditional DFS function.
    It performs DFS and stops searching when it finds a path from the source node and the target node. 
    It takes in input a graph g that is a flow network built on bipartite graph, a vertex s that is the source node, a vertex t that is the sink/target node, and a dict called "discovered". 
        - discovered is a dictionary mapping each vertex to the edge that was used to
        discover it during the DFS. (s should be "discovered" prior to the call. So, s is not in discovered but the edge that goes to s is memorized)
        Newly discovered vertices will be added to the dictionary as a result.
    The function returns:
        - True if there is a path from s to t. Note that the discovered path must be read starting from the Vertex t and proceeding backword using the dictionary discovered.
        - False if there is not a path from s to t.
    """
    # Iterating every outgoing edge from s
    for e in g.incident_edges(s):    
        v = e.opposite(s)
        if v not in discovered:        #If v is an unvisited vertex
            discovered[v] = e        
            if(v != t): #If the vertex is the target I have found a path.
                if(_customDFS(g,v,t,discovered)):
                    return True
            else: 
                return True
    return False
                    
def _printGraphDebug(graph: Graph):
    """
    Utility function. This function prints the graph taken in input.
    """
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