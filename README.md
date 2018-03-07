# Clustering
### Single Linkage, Complete Linkage, Average Linkage and Lloyd's method
### Requirement: Python 3
### Datasets:
https://archive.ics.uci.edu/ml/datasets/iris
http://archive.ics.uci.edu/ml/datasets/Libras+Movement
https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/boot/aids.csv


## Commands
Requires 2 parameter passed via the command line:
Filename
Algorithm number: 1 - Single Linkage; 2 - Complete Linkage; 3 - Average Linkage; 4 - Lloyd's method;
                                <random> - Target Silhouette Value

Example:
```
python3 cluster.py iris.txt 1
```

Output: Hamming Distance and Silhouette Value
