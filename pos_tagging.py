def get_max(myList,R,nextRole,T):
    role = R[0]
    max_value = myList[0]*T[R[0]][nextRole]
    max_index = 0
    for index in range(1,len(R)): # R = 4. Gli indici sono: 0,1,2,3. Range (1,len(R)) = 1,2,3
        value = myList[index]*T[R[index]][nextRole]
        if(value > max_value):
            max_value = value
            max_index = index 
        
    return (max_value,max_index)

def get_max_final_word(myList,R,nextRole,T):
    role = R[0]
    max_value = myList[0]*T[R[0]][nextRole]*T[nextRole]["End"]
    max_index = 0
    for index in range(1,len(R)): # R = 4. Gli indici sono: 0,1,2,3. Range (1,len(R)) = 1,2,3
        value = myList[index]*T[R[index]][nextRole]*T[nextRole]["End"]
        if(value > max_value):
            max_value = value
            max_index = index 
        
    return (max_value,max_index)


def get_max_from_list(myList):
    max_value = myList[0]
    max_index = 0

    for i in range(1,len(myList)):
        value = myList[i]
        if(value > max_value):
            max_value = value
            max_index = i

    return (max_value,max_index)


def pos_tagging(R, S, T, E):
    result = {}    
    probabilities = []
    indices = []
    last = len(S)-1
    previous_role = None

    index_to_role = {}
    index = 0
    for r in R:
        index_to_role[index] = r
        index = index +1

    word_index = 0
    for word in S:
        probabilities.insert(word_index, list()) 
        indices.insert(word_index,list())
        role_index = 0
        for r in R:
            if(word_index == 0):
                previous_role = "Start"
                weight = E[word][r]*T[previous_role][r]
                probabilities[word_index].insert(role_index, weight)
                
                #print(word,r,"weight: ",weight)
            elif(word_index == last):
                
                max,max_index = get_max_final_word(probabilities[word_index-1],R,r,T)
                weight = max*E[word][r]
                probabilities[word_index].insert(role_index, weight)
                indices[word_index].insert(role_index, max_index)

                #print(word,r,"weight: ",weight,max_index)

            else:
                max,max_index = get_max(probabilities[word_index-1],R,r,T)
                weight = max*E[word][r]
                probabilities[word_index].insert(role_index,weight)
                indices[word_index].insert(role_index, max_index)
                #print(word,r,"weight: ",weight,max_index)
            
            role_index = role_index+1

        word_index = word_index + 1
    
    #print(probabilities)

    maxValue,max_index = get_max_from_list(probabilities[len(S)-1])

    length = len(S)-2
    result[S[-1]] = index_to_role[max_index]

    for i in range(length,-1,-1):
        temp = indices[i+1][max_index]
        result[S[i]] = index_to_role[indices[i+1][max_index]]
        max_index = temp

    return result


def print_matrix(matrix):
    print(matrix)