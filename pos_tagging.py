def _get_max(myList,R,nextRole,T):
    """
    This function takes in input a list, a tuple R with all the roles, a string identifying the next role and the dictionary T.
    It returns the max value of the products between the values in the list and the corrisponding trasmission cost for the next role.
    It returns also the index of the role that generates the max value.
    """
    role = R[0]
    max_value = myList[0]*T[R[0]][nextRole]
    max_index = 0
    for index in range(1,len(R)): # R = 4. Gli indici sono: 0,1,2,3. Range (1,len(R)) = 1,2,3
        value = myList[index]*T[R[index]][nextRole]
        if(value > max_value):
            max_value = value
            max_index = index 
        
    return (max_value,max_index)

def _get_max_final_word(myList,R,nextRole,T):
    """
    This function is a variant of the function _get_max(). It must be used when it is the last word of the sentence.
    """
    role = R[0]
    max_value = myList[0]*T[R[0]][nextRole]*T[nextRole]["End"]
    max_index = 0
    for index in range(1,len(R)): # R = 4. Gli indici sono: 0,1,2,3. Range (1,len(R)) = 1,2,3
        value = myList[index]*T[R[index]][nextRole]*T[nextRole]["End"]
        if(value > max_value):
            max_value = value
            max_index = index 
        
    return (max_value,max_index)


def _get_max_from_list(myList):
    """
    This funtion takes in input a list and returns the max value and its index in the list.
    """
    max_value = myList[0]
    max_index = 0

    for i in range(1,len(myList)):
        value = myList[i]
        if(value > max_value):
            max_value = value
            max_index = i

    return (max_value,max_index)


def pos_tagging(R, S, T, E):
    """
    The function pos_tagging takes in input:
        - a tuple R of roles,
        - a tuple S of strings,
        - a dictionary T whose keys are the roles in R plus the special role Start and
        values are dictionaries T[r] such that:
            ○ the keys of T[r] are the roles in R plus the special role End
            ○ the values of T[r] are the transition probabilities between r and the corresponding role defined by the key
        - a dictionary E whose keys are the strings in S and value are dictionaries E[s]
        such that:
            ○ the keys of E[s] are the roles in R
            ○ the values in E[s] are the emission probabilities between s and the corresponding role defined by the key
    The function returns a dictionary whose keys are the words in S and the values are the roles assigned to these words,
    so that the selected assignment is the one of maximum likelihood.
    """
    """
    I used a dynamic programming approach. I consider shorter sentence as sub-problem.
    """
    result = {} #
    probabilities = [] #Matrix constructed by a list of list. It saves the probability of a word to have a certain role. The probability is calculated using the probability of the previous words. 
    indices = [] #Matrix constructed by a list of list. It saves the index of role of the previous word that has maximized the probability.
    last = len(S)-1
    previous_role = None

    index_to_role = {} #In order to convert the indeces to roles, I use this dict. The keys represent an index and the value the corresponding Role from R.
    index = 0

    #Populating the dict for the conversion of the indeces in roles of R.  
    for r in R:
        index_to_role[index] = r
        index = index +1

    if(last == 0):
        #Edge case. If the sentence has one word. 
        # It is different from the boundary condition because I must consider the probability that the only word of the sentence ends with a specific role. 
        word_index = 0
        probabilities.insert(word_index, list())
        role_index = 0
        for r in R:
            weight = E[S[word_index]][r]*T["Start"][r]*T[r]["End"]
            probabilities[word_index].insert(role_index, weight)
            role_index += 1
    else: #All other cases.
        word_index = 0
        for word in S: #Iterating all words in the sentence.
            probabilities.insert(word_index, list()) 
            indices.insert(word_index,list())
            role_index = 0
            for r in R: #For each word, iterating all roles of R.
                if(word_index == 0):
                    #Boundary condition. Since I consider shorter sentence as sub-problem, the boundary condition is the sentence with a single word.
                    previous_role = "Start"
                    weight = E[word][r]*T[previous_role][r]
                    probabilities[word_index].insert(role_index, weight)

                elif(word_index == last):
                    #If the word is the last I must consider the probability that the word ends with the role r. 
                    max,max_index = _get_max_final_word(probabilities[word_index-1],R,r,T)
                    weight = max*E[word][r]
                    probabilities[word_index].insert(role_index, weight)
                    indices[word_index].insert(role_index, max_index)
                else:
                    max,max_index = _get_max(probabilities[word_index-1],R,r,T)
                    weight = max*E[word][r]
                    probabilities[word_index].insert(role_index,weight)
                    indices[word_index].insert(role_index, max_index)

                role_index = role_index+1
            word_index = word_index + 1
    
    #print(indices)

    #Finding the max probability of the last word in the probabilities matrix.
    #I choose the role of the last word with the highest probability and proceed backward reconstructing the solution.
    maxValue,max_index = _get_max_from_list(probabilities[len(S)-1])

    length = len(S)-2
    result[S[-1]] = index_to_role[max_index]
    # Finding the solution using the indeces matrix.
    for i in range(length,-1,-1): #It stops at 0.
        temp = indices[i+1][max_index]
        result[S[i]] = index_to_role[indices[i+1][max_index]]
        max_index = temp

    return result


def _print_matrix(matrix):
    """
    This is an utility function that prints the values of the matrix in input.
    """
    print(matrix)