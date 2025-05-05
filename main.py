#from data3 import N_comp, F, Resource, Resource_required, SFCs, Delay, App_to_comp_delay, N_app
from ilp import find_ilp_solution, find_ilp_obj
from simple import find_greedy_solution1, find_greedy_solution2, find_obj
from parse_data import parse_edge_data, parse_sfc_data
import time

def prepare_data(filename_sfc, filename_users, filename_edges):
    N_comp, N_app, app_comp_delay, comp_comp_delay = parse_edge_data('users-melbcbd-generated.csv', 'site-optus-melbCBD.csv')
    F, resources_req, SFCs = parse_sfc_data('alibaba-trace-2017/batch_task.csv', N_app)
    Resources = [1] * N_comp
    
    greedy1_time1 = time.time_ns()
    res_greedy1 = find_greedy_solution2(N_comp, F, Resources, resources_req, SFCs, comp_comp_delay, app_comp_delay, N_app)
    greedy1_time2 = time.time_ns()
    print(f"Greedy: {greedy1_time2 - greedy1_time1}")
    obj_greedy1 = find_obj(app_comp_delay, comp_comp_delay, res_greedy1)
    print(obj_greedy1)

def other():
    greedy1_time1 = time.time_ns()
    res_greedy1 = find_greedy_solution1(N_comp, F, Resource, Resource_required, SFCs, Delay, App_to_comp_delay, N_app)
    greedy1_time2 = time.time_ns()
    print(f"Greedy: {greedy1_time2 - greedy1_time1}")

    #time.sleep(1)
    greedy2_time1 = time.time_ns()
    res_greedy2 = find_greedy_solution2(N_comp, F, Resource, Resource_required, SFCs, Delay, App_to_comp_delay, N_app)
    greedy2_time2 = time.time_ns()
    print(f"Random: {greedy2_time2 - greedy2_time1}")

    ilp_time1 = time.time_ns()
    model, _x = find_ilp_solution(N_comp, F, Resource, Resource_required, SFCs, Delay, App_to_comp_delay, N_app)
    ilp_time2 = time.time_ns()
    print(f"ILP: {(ilp_time2 - ilp_time1) / 10**9}")

    obj_greedy1 = find_obj(App_to_comp_delay, Delay, res_greedy1)
    obj_greedy2 = find_obj(App_to_comp_delay, Delay, res_greedy2)
    obj_ilp = find_ilp_obj(model)
    print(f"Obj value greedy: {res_greedy1}, random: {res_greedy2}, ilp: {obj_ilp}")

if __name__ == "__main__":
    prepare_data('alibaba-trace-2017/batch_task.csv', 'users-melbcbd-generated.csv', 'site-optus-melbCBD.csv')

