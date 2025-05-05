from dataclasses import dataclass
import numpy as np
from geopy import distance
import csv

SPEED_OF_LIGHT = 3 * 10**8



def parse_edge_data(user_data_filename, node_data_filename, user_data_size=None, node_data_size=None):
    applications = []
    with open(user_data_filename, 'r') as file:
        reader = csv.reader(file)
        header = list(next(reader))
        for line in reader:
            applications.append((float(line[0]), float(line[1])))
            
    compute_nodes = []
    with open(node_data_filename, 'r') as file:
        reader = csv.reader(file)
        header = list(next(reader))
        for line in reader:
            compute_nodes.append((float(line[1]), float(line[2])))
    
    if user_data_size:
        applications = applications[:user_data_size]
    if node_data_size:
        compute_nodes = compute_nodes[:node_data_size]

    delay1_distance = []
    for i, app in enumerate(applications):
        delay1_distance.append([])
        for comp in compute_nodes:
            delay1_distance[i].append(distance.distance(app, comp).m)

    delay2_distance = []
    for i, comp1 in enumerate(compute_nodes):
        delay2_distance.append([])
        for comp2 in compute_nodes:
            delay2_distance[i].append(distance.distance(comp1, comp2).m)

    delay1 = []
    for distances in delay1_distance:
        delay1.append([1000 * distance / SPEED_OF_LIGHT for distance in distances])
        
    delay2 = []
    for distances in delay2_distance:
        delay2.append([1000 * distance / SPEED_OF_LIGHT for distance in distances])
        
    return (len(delay2), len(delay1), delay1, delay2)
    
def parse_sfc_data(filename, sfc_size=None):
    data = dict()
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            if line[5] != 'Terminated' or line[7] == '':
                continue
            job = int(line[2])
            data[job] = data.get(job, []) + [float(line[7])]
    data = list(data.values())
    result = []
    for elem in data:
        if 2 < len(elem) < 9:
            result.append(elem)    
    if sfc_size:
        result = result[:sfc_size]
    
    resource_req = []
    F = 0
    for i in range(len(result)):
        for j in range(len(result[i])):
            resource_req.append(result[i][j])
            result[i][j] = F
            F += 1
    return F, resource_req, result
    
if __name__ == "__main__":
    # with open("app_to_node.data", "w") as f:
    #     for app_delay1 in delay1:
    #         f.write(" ".join(map(str, app_delay1)))
            
    # with open("node_to_node.data", "w") as f:
    #     for app_delay2 in delay2:
    #         f.write(" ".join(map(str, app_delay1)))

    # x, y, delay1, delay2 = get_data('users-melbcbd-generated.csv', 'site-optus-melbCBD.csv')
    # print(delay1)
    # print(delay2)
    # print(delay2[30][30])
    # print(f"App to Node data, size={len(delay1)}x{len(delay1[0])}")
    # print(f"Node to Node data, size={len(delay2)}x{len(delay2[0])}")
    
    x, y = parse_sfc_data('alibaba-trace-2017/batch_task.csv', 1000)
    print(type(x))
    print(x)
    z = 0
    for elem in y:
        z += sum(elem)
    print(z)
