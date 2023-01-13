import numpy as np
import pandas as pd

def Fuzzy_Membership(member, Centroid, sensitivity=5):
    distance = np.linalg.norm(member - Centroid, 2)
    possibility = 1 / (1+(distance/sensitivity))

    return possibility

'''
Proximal Gradient Descent takes an objective function with a smooth differentiable part, and a non-differentiable
part that has an easy proximal operator. Use for L1 fusion penalty

the Convex Clustering (or Clusterpath) algorithm has a smooth fission term, and a non-smooth fusion penalty
''' 
def Proximal_Clusterpath(data, maxiters, penalty, threshold, error, weight_type='exponential'):

   return 0


'''
uses simple subgradient descent to solve clusterpath with an L2 fusion penality
note: clusterpath will not be entirely agglomerative with the L2 penalty
'''

def greaterSum(DataMatrix, ClusterMatrix, clustercounter):
    temp = np.array([])
    temp2 = []
    size = ClusterMatrix.shape[0]
    size2 = len(clustercounter)
    for i in range(0, size):
        for j in range(i+1, size) :
            top = np.subtract(ClusterMatrix[i], ClusterMatrix[j])
            bottom = np.linalg.norm(ClusterMatrix[i] - ClusterMatrix[j], 2)
            if bottom == 0:
                break
            Weight = Fuzzy_Membership(DataMatrix[i], ClusterMatrix[j])
            otherweight = 1 * size
            evaluation = otherweight * (top/bottom)
            #np.stack(temp, evaluation)
            temp2.append(evaluation)
            temp2.append(i)
    final = temp2

    new = []

    new2 = final[0] + final[1] + final[2] + final[3]
    new.append(new2)
    new3 = final[4] + final[5] + final[6] + final[0]
    new.append(new3)
    new4 = final[7] + final[8] + final[1] + final[4]
    new.append(new4)
    new5 = final[9] + final[2] + final[5] + final[7]
    new.append(new5)
    new6 = final[4] + final[6] + final[8] + final[9]
    new.append(new6)

    end = np.asarray(new)

    return end

def Subgradient_L2(clusters, data, FusionSpec, clustercounter):
    clusterNum = np.unique(clusters)
    X = data / clusterNum.shape[0]
    FissionSubgradient = np.subtract(clusters, X)
    FusionGradient = (FusionSpec / clusterNum.shape[0]) * greaterSum(data, clusters, clustercounter)
    Gradient = FissionSubgradient + FusionGradient
    print(Gradient)

    return Gradient

def DetectFusion(clusters, data, clustercounter):

    thresh = 9999999999999

    for i in data:
        for j in data:
            if np.array_equal(i, j):
                pass
            elif np.linalg.norm(i - j, 2) < thresh:
                thresh = np.linalg.norm(i - j, 2) / 2
    
    for i in range(0, clusters.shape[0]):
        for j in range(0, clusters.shape[0]):
            if np.array_equal(i, j):
                pass
            elif np.linalg.norm(clusters[i] - clusters[j], 2) < thresh:
                #clustercounter[i].append(clustercounter[j])
                #clustercounter.remove(clustercounter[j])
                new_clust = (clusters[i] + clusters[j]) / 2
                clusters[i] = new_clust
                clusters[j] = new_clust

                
    
    return clusters, clustercounter

def Gradient_Clusterpath(clusters, FusionSpec, data, clustercounter):
    print('hi')
    Gradient = Subgradient_L2(clusters, data, FusionSpec, clustercounter)
    iteration = 0
    while np.linalg.norm(Gradient) ** 2 > 0.1:
        iteration = iteration + 1
        stepsize = 1 / iteration
        clusters = clusters - (stepsize * Gradient)
        clusters, clustercounter = DetectFusion(clusters, data, clustercounter)
        print('hewwo')
        Gradient = Subgradient_L2(clusters, data, FusionSpec, clustercounter)
        if iteration == 1000:
            print('reached max iter')
            break

    return clusters

def Clusterpath_L2(maxiters, step, data, FusionSpec):
    clusters = data
    clustercounter = []
    k = 0

    for i in data:
        j = [k]
        clustercounter.append(j)
        k = k + 1

    clusterpath = [clusters]
    PenaltyPath = [FusionSpec]
    epoch = 0
    while len(np.unique(clusters)) > 1:
        epoch = epoch + 1
        clusters = Gradient_Clusterpath(clusters, FusionSpec, data, clustercounter)
        FusionSpec = FusionSpec * 1.5
        clusterpath.append(clusters)
        PenaltyPath.append(FusionSpec)
        if epoch == maxiters:
            print('failed')
            break

    return clusterpath, PenaltyPath
'''
algorithm for a fuzzy implementation of convex clustering. takes an n-dimensional tensor as data.
'''
def Fuzzy_Clusterpath(data, maxiters=400, step=0.005, FusionSpecs=[1], pnorm='L1'):
    Clusters = Data
    
    return clusters

a = np.array([[1, 2, 3], [2, 4, 5], [2, 1, 4], [355, 311, 112], [330, 228, 112]])
b = a

print(Clusterpath_L2(10, 0.05, a, 0))






