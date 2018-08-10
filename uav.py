#!/usr/bin/python
from z3 import *


# Return the first "M" models of formula list of formulas F
def get_models(F, M):
    result = []
    s = Solver()
    s.add(F)
    while len(result) < M and s.check() == sat:
        m = s.model()
        result.append(m)
        # Create a new constraint that blocks the current model
        block = []
        for d in m:
            # d is a declaration
            if d.arity() > 0:
                raise Z3Exception("uninterpreted functions are not supported")
            # create a constant from declaration
            c = d()
            if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                raise Z3Exception("arrays and uninterpreted sorts are not supported")
            block.append(c != m[d])
        s.add(Or(block))
    return result


resolutions = range(200, 1801, 200)
fovs = range(15, 91, 15)


def enumerated_constraint(thing, rang):
    return Or([thing == r for r in rang])


constraints = set()

eo_res = Int('eo_res')
constraints.add(enumerated_constraint(eo_res, resolutions))
eo_fov = Int('eo_fov')
constraints.add(enumerated_constraint(eo_fov, fovs))

ir_res = Int('ir_res')
constraints.add(enumerated_constraint(ir_res, resolutions))
ir_fov = Int('ir_fov')
constraints.add(enumerated_constraint(ir_fov, fovs))

engine_type = Int('engine_type')
constraints.add(Or(engine_type == 0, engine_type == 1))

wingspan = Int('wingspan')
constraints.add(Or([wingspan == i for i in range(2, 13, 1)]))

models = get_models(constraints, 90000)
print(len(models))
# print(models)
