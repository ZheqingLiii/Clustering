import csv
import math
import operator
import sys
import ast
from random import randint


# define a class holding csv data
class Data():
    def __init__(self, classifier):
        self.eg = []
        self.attr = []
        self.classifier = None

class Cluster():
    def __init__(self):
        self.clusters = [] # list of clusters
        self.index = [] # index of the clusters, starts from 0
        self.number = None # number of clusters in the cluster set


# read the data from csv file into 'dataset'
def readData(filename, dataset):
    # read file, split data into lines, and put into examples
    dataset.eg = [row.split(',') for row in open(filename).read().splitlines()]
    # put first row as attribute names
    dataset.attr = dataset.eg.pop(0)

###################################################
# only cut one cluster
def merge(cluster, k, alg):
    index_list = []
    
    # initialize
    min = find_max(cluster.clusters[0], cluster.clusters[1])
    index_list = cluster.index[0] + cluster.index[1]
    rm_index_1 = 1
    rm_index_2 = 0
    
    for i,clus in enumerate(cluster.clusters):
        for j in range(cluster.number):
            # if the cluster is a list, cal distance depends on different algorithms
            if alg == '1':
                dis = find_min(clus, cluster.clusters[j])
            elif alg == '2':
                dis = find_max(clus, cluster.clusters[j])
            elif alg == '3':
                dis = find_avg(clus, cluster.clusters[j])
            else:
                print("Please give a valid input.")
                return
            
            if dis < min and i != j:
                min = dis
                index_list = cluster.index[i] + cluster.index[j]
                # store the index of the removing index list
                # remove the higher index first, to prevent index change
                if i < j:
                    rm_index_1 = j
                    rm_index_2 = i
                else:
                    rm_index_1 = i
                    rm_index_2 = j

    print(index_list)

    # delete 2 clusters in index
    cluster.index.remove(cluster.index[rm_index_1])
    cluster.index.remove(cluster.index[rm_index_2])
    # store 2 clusters in a new cluster
    new_clus = cluster.clusters[rm_index_1] + cluster.clusters[rm_index_2]
    # remove 2 clusters
    cluster.clusters.remove(cluster.clusters[rm_index_1])
    cluster.clusters.remove(cluster.clusters[rm_index_2])
    # add the new cluster
    cluster.clusters.append(new_clus)
    cluster.index.append(index_list)
    cluster.number -= 1




# find 2 nearest points between 2 clusters
# for single linkage
def find_min(cluster1,cluster2):
    min = distance(cluster1[0], cluster2[0])
    for point1 in cluster1:
        for point2 in cluster2:
            dis = distance(point1, point2)
            if dis < min:
                min = dis
    return min


# find 2 furtherest points between 2 clusters
# for complete linkage
def find_max(cluster1,cluster2):
    max = 0.0
    for point1 in cluster1:
        for point2 in cluster2:
            dis = distance(point1, point2)
            if max < dis:
                max = dis
    return max


# find the average distance between 2 clusters
# for average linkage
def find_avg(cluster1,cluster2):
    avg = 0.0
    count = 0
    for point1 in cluster1:
        for point2 in cluster2:
            avg += distance(point1, point2)
            count += 1
    return avg/count



###################################################
# find distance between 2 points
def distance(point1, point2):
    dis = 0.0
    # eliminate the class attribute
    for i in range(len(point1)-1):
        add = (float(point1[i]) - float(point2[i]))**2
        dis += add
    return dis**0.5


###################################################
# Lloyd's method: pick k random points(centers)
# assign each point to its closest center, compute means as new centers
# do until converegnce
# only need to record the index of the clusters
def Lloyd_merge(dataset, k):
    center = []
    for i in range(k):
        # get a random number as the index
        rand_i = randint(0,len(dataset.eg)-1)
        # make sure different points are selected
        while dataset.eg[rand_i] in center:
            rand_i = randint(0,len(dataset.eg)-1)
        
        # use the randomly picked centers as the first element in the index list
        center.append(dataset.eg[rand_i])

    new_clus = Cluster()
    iterations = 15
    while iterations != 0:
        iterations -= 1
        new_clus = assign_points(dataset, center, k)
        
        print(new_clus.index)

        # find new contriods until converge
        for i in range(len(center)):
            old_center = center[i]
            center[i] = find_centroid(dataset, new_clus.index[i])

    return new_clus




# find the closest center to the points, and assign the point index to that cluster index list
def assign_points(dataset, center, k):
    clus = Cluster()
    clus.number = k
    # just initialize, remove later
    for i in range(k):
        clus.index.append(['default'])
    
    for i,example in enumerate(dataset.eg):
        # find closest center, assuming closest center is the first one
        shortest_dis = distance(example, center[0])
        center_index = 0
        for j in range(1,k):
            new_dis = distance(example, center[j])
            if new_dis < shortest_dis:
                shortest_dis = new_dis
                center_index = j
        # assign the index of the point to the index list
        clus.index[center_index].append(i)

    for i in range(k):
        clus.index[i].remove('default')

    return clus





# find the center of the cluster
def find_centroid(dataset, index_list):
    count = 0
    new_center = []
    
    # set all attributes to zero, the class will just set to 0 for centers
    for num in dataset.eg[0]: new_center.append(0)
    new_center[-1] = 'default'
    
    for index in index_list:
        count += 1
        for i in range(len(new_center)-1): # eliminate the class attribute
            new_center[i] += float(dataset.eg[index][i])

    if count != 0:
        for i in range(len(new_center)-1):
            new_center[i] /= count

    return new_center


###################################################
# Calculate the Hamming Distance
def hamming_dis(dataset, cluster):
    not_match = 0
    total = 0
    # get a list of possible class values
    class_index = []
    for example in dataset.eg:
        if [example[-1]] not in class_index:
            class_index.append([example[-1]])

    # get list of index of these class values
    # let the first element be the class value
    for i,example in enumerate(dataset.eg):
        for j,val in enumerate(class_index):
            if example[-1] == val[0]:
                class_index[j].append([i])

    for i in range(len(dataset.eg)):
        for j in range(i+1,len(dataset.eg)):
            total += 1
            for i_list in class_index:
                # if in the same cluster in dataset
                if [i] in i_list and [j] in i_list:
                    # not in the same cluster in clustering
                    for ic_list in cluster.index:
                        if i in ic_list and j not in ic_list:
                            not_match += 1
            
                # not in the same cluster in dataset
                elif [i] in i_list and [j] not in i_list:
                    # in the same cluster in clustering
                    for ic_list in cluster.index:
                        if i in ic_list and j in ic_list:
                            not_match += 1

    return not_match / total




###################################################
# Calculate the Silhouette Value
def silhouette_val(dataset, cluster):
    silhouette = 0
    for data_index in range(len(dataset.eg)): # for each data point
        shortest_b = cal_dis(dataset, data_index, cluster.index[0])
        
        for index_list in cluster.index: # check in each cluster
            if data_index in index_list:
                # average distance in cluster
                a = cal_dis(dataset, data_index, index_list)
            else:
                # shortest average distance with another cluster
                b = cal_dis(dataset, data_index, index_list)
                if b < shortest_b:
                    shortest_b = b

        if a != shortest_b:
            silhouette += ((shortest_b - a) / max(shortest_b, a))

    return silhouette / len(dataset.eg)



# Calculate the distance between a point and a cluster
def cal_dis(dataset, data_index, index_list):
    avg_dis = 0
    for index in index_list:
        avg_dis += distance(dataset.eg[data_index], dataset.eg[index])
    
    return avg_dis / len(index_list)


###################################################
def main():
    args = ast.literal_eval(str(sys.argv))
    # Reading training data
    dataset = Data("")
    readData(args[1], dataset)
    
    
    # Assume k is number of possible class values by default
    class_val = []
    target = Cluster()
    # find possible class values
    for example in dataset.eg:
        if [example[-1]] not in class_val:
            class_val.append([example[-1]])
            target.index.append(['default'])
    k = len(class_val)

    # Give number of clusters here if needed
    # k = 3

    alg = args[2] # '1' for SL, '2' for CL, '3' for AL, '4' for Lloyd's

    # Lloyd's method
    if alg == '4':
        cluster_l = Cluster()
        cluster_l = Lloyd_merge(dataset, k)
        h_dis = hamming_dis(dataset, cluster_l)
        s_val = silhouette_val(dataset, cluster_l)
        print("Hamming Distance: ", h_dis)
        print("Silhouette Coefficient: ", s_val)

    # Linkages
    elif alg == '1' or alg == '2' or alg == '3':
        # initial the clusters, each example is a cluster
        cluster = Cluster()
        cluster.number = len(dataset.eg)
        for i,eg in enumerate(dataset.eg):
            cluster.clusters.append([eg])
            cluster.index.append([i])

        while cluster.number > k:
            merge(cluster, k, alg)
        h_dis = hamming_dis(dataset, cluster)
        s_val = silhouette_val(dataset, cluster)
        print("Hamming Distance: ", h_dis)
        print("Silhouette Coefficient: ", s_val)

    # Target
    else:
        # compute index to that class
        for i,example in enumerate(dataset.eg):
            for j,val in enumerate(class_val):
                if val == [example[-1]]:
                    target.index[j].append(i)
        target.number = k
        for i in range(k):
            target.index[i].remove('default')

        print(target.index)
        s_val = silhouette_val(dataset, target)
        print("Silhouette Coefficient of the target: ", s_val)



if __name__ == "__main__":
    main()
