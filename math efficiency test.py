import math
import time
import random
from shapely.geometry import Point
import statistics

# Define a test parameters
approach1 = []
approach2 = []
c = 50
d = 20000

for z in range(c):
    
    # Approach 1: Convert the angle to radians once and reuse the result
    start_time = time.time()
    for i in range(d):
        with open('message_ids.txt', 'r', encoding='utf-8') as f:
            message_ids = set(line.strip() for line in f)
    end_time = time.time()
    approach1.append(end_time - start_time)
    print("Approach 1 -", z+1,": {:.4f} seconds".format(end_time - start_time))



    # Approach 2: Convert the angle to radians twice
    start_time = time.time()
    for i in range(d):
        with open('message_ids.txt', 'r', encoding='utf-8') as f:
            message_ids = set(f.readlines())
    end_time = time.time()
    approach2.append(end_time - start_time)
    print("Approach 2 -", z+1,": {:.4f} seconds".format(end_time - start_time))
    
print("Approach 1 average over", c,"tries : {:.4f}".format(statistics.mean(approach1)))
print("Approach 2 average over", c,"tries : {:.4f}".format(statistics.mean(approach2)))