import random
from data3 import N_comp, F, Resource, Resource_required, SFCs, Delay, App_to_comp_delay, N_app

class NotEnoughResourcesError(Exception):
    pass

def find_greedy_solution1(N_comp, F, Resource, Resource_required, SFCs, Delay, App_to_comp_delay, N_app):
    res = []
    resource_left = Resource.copy()
    for app, sfc in enumerate(SFCs):
        res.append([])
        f_first = sfc[0]
        delays = sorted(enumerate(App_to_comp_delay[app]), key=lambda x: x[1])
        for node, node_delay in delays:
            if resource_left[node] >= Resource_required[f_first]:
                res[app].append(node)
                resource_left[node] -= Resource_required[f_first]
                prev = node
                break
        else:
            raise NotEnoughResourcesError("")

        for f in sfc[1:]:
            delays = sorted(enumerate(Delay[prev]), key=lambda x: x[1])
            for node, node_delay in delays:
                if resource_left[node] >= Resource_required[f]:
                    res[app].append(node)
                    resource_left[node] -= Resource_required[f]
                    prev = node
                    break
            else:
                raise NotEnoughResourcesError("")
    return res

def find_greedy_solution2(N_comp, F, Resource, Resource_required, SFCs, Delay, App_to_comp_delay, N_app):
    res = [None] * N_app
    resource_left = Resource.copy()
    for app, sfc in enumerate(SFCs):
        f_first = sfc[0]
        delays = sorted(enumerate(App_to_comp_delay[app]), key=lambda x: x[1])
        for node, node_delay in delays:
            if resource_left[node] >= Resource_required[f_first]:
                res[app] = [node]
                resource_left[node] -= Resource_required[f_first]
                break
        else:
            raise NotEnoughResourcesError("")
    
    for app, sfc in enumerate(SFCs):
        prev = res[app][-1]
        for f in sfc[1:]:
            delays = sorted(enumerate(Delay[prev]), key=lambda x: x[1])
            for node, node_delay in delays:
                if resource_left[node] >= Resource_required[f]:
                    res[app].append(node)
                    resource_left[node] -= Resource_required[f]
                    prev = node
                    break
            else:
                raise NotEnoughResourcesError("")
    return res   
    
def find_obj(App_to_comp_delay, Delay, res):
    delay_arr = []
    for user, placements in enumerate(res):
        prev = placements[0]
        delay = App_to_comp_delay[user][prev]
        for node in placements[1:]:
            delay += Delay[prev][node]
            prev = node
        delay_arr.append(delay)    
    return max(delay_arr)

if __name__ == "__main__":
    res = find_greedy_solution2(N_comp, F, Resource, Resource_required, SFCs, Delay, App_to_comp_delay, N_app)
    # res_random = find_random_solution(N_comp, F, Resource, Resource_required, SFCs, Delay, App_to_comp_delay, N_app)
    delay = find_obj(App_to_comp_delay, Delay, res)
    print(res, delay)
