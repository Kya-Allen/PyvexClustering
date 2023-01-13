import numpy as np

def dimension_penalty(data_matrix, n_samples, dimension, intradimensional_means): #add some notes on what this does
    candidate_penalties = np.array([[0,0]])

    for parameter in range(1, n_samples):
        # temporarily setting the dimension as 0
        denomenator = n_samples / parameter
        numerator = intradimensional_means[dimension] - np.mean(data_matrix[:, dimension][0:parameter])
        function = numerator / denomenator
        candidate_pair = [[function, parameter]]
        candidate_penalties = np.concatenate((candidate_penalties, candidate_pair), axis=0)  # appends function output to first array, and parameter value to 2nd array

    max_index = np.argmax(candidate_penalties[0])
    return candidate_penalties[1][max_index]

def max_penalty(data_matrix, n_samples: int, p_dimensions: int) -> float:
    intradimensional_means = np.mean(data_matrix, axis=0)
    dimensional_penalties = []

    for dimension in range(p_dimensions):
        dimensional_penalties.append(dimension_penalty(data_matrix, n_samples, dimension, intradimensional_means))

    return max(dimensional_penalties)

def possible_partial_centroids(partial_observations, penalties, n):
    partial_centroid_1 = partial_observations[0] + penalties[0]
    centroid_stack = [partial_centroid_1]
    s_stack = [1]
    i_stack = [-partial_observations[0]]

    for k in range(1, n-1):
        s = 1
        i = -partial_observations[k]
        B = (penalties[k] - penalties[k-1] - i) / s

        while centroid_stack[-1] > B:
            s += s_stack[-1]
            i += i_stack[-1]
            centroid_stack.pop(), s_stack.pop(), i_stack.pop()
            B = (penalties[k] - penalties[len(centroid_stack) - 1] - i) / s
            if len(centroid_stack) == 0:
                break
        
        u = B
        centroid_stack.append(u), s_stack.append(s), i_stack.append(i)
        print(centroid_stack)
    print(centroid_stack)
    return centroid_stack


def Dynamic_ConvexCluster(partial_observations, penalty, n_samples):
    final_penalties = []  # initialize new penalty alteration
    for i in range(1, n_samples):
        entry = i * (n_samples - i) * penalty
        final_penalties.append(entry)

    #compute possible partial_centroid
    alternative_list = list(reversed(possible_partial_centroids(partial_observations, final_penalties, n_samples)))
    print(alternative_list)
    centroids = alternative_list
    for k in range (1, n_samples):
        centroids[k] = max(centroids[k-1], alternative_list[k])
    
    return centroids.reverse()


def c_paint(data_matrix, path_length: int):
        # takes a numpy array as the data matrix
        # A dynamic programming algorithm that splits the problem into each of it's dimensions, and solves them sequentially
        # path_length gives the number of different penalty parameter values, to explicate the path structure as the penalty parameter goes from max -> 0
    n_samples = len(data_matrix)
    p_dimensions = len(data_matrix[0])

    
    array_of_matrices = np.array([])
    for i in range(1, path_length):
        empty = []
        np.concatenate((array_of_matrices, empty), axis=0)
        # initialize penalties for the full clusterpath
    max_penalty_result = max_penalty(data_matrix, n_samples, p_dimensions)
    penalty_sequence = []
    for penalty in range(1, path_length+1):
        pathstep_penalty = max_penalty_result * (penalty / path_length)
        penalty_sequence.append(pathstep_penalty)
       
        #core function
    for dimension in range(0, p_dimensions):
        #sort the x_i elements from this singular dimension in descending order
        unsorted_prototypes = data_matrix[:, dimension]
        mapping = list(zip(unsorted_prototypes, [i for i in range(0, len(unsorted_prototypes))]))
        index_map = []
        for value, index in sorted(mapping, reverse=True):
            index_map.append(index)  
            # now the item at each index represents the index to map back to, later. [8, 2, 6] means the element at index 0 in sorted form, corresponds to... 
            # ...index 8 in unsorted form

        sorted_prototypes = np.sort(data_matrix[:, dimension][::-1])
        proper_order = []  # after a single loop, should be a list of sublists, with each sublist being a re-unordered list of partial centroids for each penalty
                           # need to figure out how to order this so that it feeds into seperate matrices for each penalty 
        temp = []
        for penalty in penalty_sequence:
            #for each dimension, run Dynamic_ConvexCluster()
            partial_centroids = Dynamic_ConvexCluster(sorted_prototypes, penalty, n_samples) 
            temp.append(partial_centroids)
        
        for i in temp:
            proper = i
            for j in i:
                proper[index_map[j]] = j
            proper_order.append(proper) 
                
        for i in range(0, len(proper_order)):
            np.concatenate((array_of_matrices[i], proper_order[i]), axis=0)
    return array_of_matrices

test_data = np.array([[1], [3], [4], [6], [15], [89], [92], [100], [101], [94]])

print(c_paint(test_data, 4))

#current problem: each u = B needs to be saved as the possible cluster centroids. Need to clear up how this algorithm works and what is stored in the stack updates