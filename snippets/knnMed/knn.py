import math


# Example: values = [ int ] , multipliers = [ int ]
def euclidean_distance(set1, set2, multiplier1, multiplier2):
    if len(set1) != len(multipliers[0]) or len(set1) != len(set2):
        raise Exception("Values and multipliers are not the same length")
    rtn = 0
    for i in range(len(set1)):
        rtn += ((set1[i] * multiplier1[i] - set2[i] * multiplier2[i]) ** 2)
    rtn = math.sqrt(rtn)
    return rtn


def knn(new_sample, dataset, multipliers, k):
    neighbors_distance = []
    neighbors = []
    threshold = None
    counter = 1
    for sample in dataset:
        ed = euclidean_distance(new_sample, sample, multipliers[0], multipliers[counter])
        if threshold is None:
            threshold = ed
            neighbors_distance.append(ed)
            neighbors.append(sample)
        elif ed < threshold:
            neighbors_distance.append(ed)
            neighbors.append(sample)
            if len(neighbors) > k:
                tmp_max = max(neighbors_distance)
                neighbors.pop(neighbors_distance.index(tmp_max))
                neighbors_distance.remove(tmp_max)
        counter += 1
    return neighbors, neighbors_distance
            

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    new_sample = [5, 8, 7, 9]
    dataset = [
            [55, 2, 17, 95],
            [100, 238, 57, 9],
            [1, 3, 4, 8],
            [9, 0, 4, 3],
            [5, 3, 15, 3],
            [5, 8, 7, 8],
        ]
    multipliers = [[1, 0.5, 3, 0.1], [1, 0.5, 3, 0.1], [1, 0.5, 3, 0.1], [1, 0.5, 3, 0.1], [1, 0.5, 3, 0.1], [1, 0.5, 3, 0.1], [1, 0.5, 3, 100]]
    result = knn(new_sample, dataset, multipliers, 2)
    print(result)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
