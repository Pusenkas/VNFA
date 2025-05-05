from mip import Model, xsum, maximize, BINARY, minimize, INTEGER, CONTINUOUS
from data3 import N_comp, F, Resource, Resource_required, SFCs, Delay, App_to_comp_delay, N_app


def find_ilp_solution(N_comp, F, Resource, Resource_required, SFCs, Delay, App_to_comp_delay, N_app):
    m = Model("VNFA")
    m.verbose = 0

    x = [[m.add_var(var_type=BINARY, name=f"{f}x{n}") for n in range(N_comp)] for f in range(F)]
    for f in range(F):
        m += xsum(x[f]) == 1
        
    for n in range(N_comp):
        m += xsum((x[f][n] * Resource_required[f] for f in range(F))) <= Resource[n]

    delay = m.add_var(var_type=INTEGER, name="result")
    for u, sfc in enumerate(SFCs):
        sum = 0  
        f_first = sfc[0]            
 
        for n in range(N_comp):
            sum += x[f_first][n] * App_to_comp_delay[u][n]
        
        f_first = sfc[0]            
        for f1, f2 in zip(sfc[:-1], sfc[1:]):
            for n1 in range(N_comp):
                for n2 in range(N_comp):
                    z = m.add_var(var_type=BINARY, name=f"{f1}z{f2}z{n1}z{n2}")
                    m += z <= x[f1][n1]
                    m += z <= x[f2][n2]
                    m += z >= x[f1][n1] - 1 + x[f2][n2]
                    sum += z * Delay[n1][n2]
        m += delay >= sum
    m.objective = minimize(delay)
    m.optimize()
    return m, x

def find_ilp_obj(m):
    return int(m.var_by_name("result").x)

if __name__ == "__main__":
    m, x = find_ilp_solution(N_comp, F, Resource, Resource_required, SFCs, Delay, App_to_comp_delay, N_app)
    for i in range(F):
        for j in range(N_comp):
            print(x[i][j].x, end=" ")
        print()
    val = m.var_by_name("result").x
    print(f"Variables: {m.num_cols}, Result: {val}")
