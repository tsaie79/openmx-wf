import os
from monty.serialization import loadfn, dumpfn
import sys

def create_fworker(proj, i):
    path = '/global/homes/j/jlabtsai/opt/fireworks/project/{}'.format(proj)
    os.makedirs(os.path.join(path, i), exist_ok=True)
    f = loadfn("my_fworker.yaml")
    q = loadfn("my_qadapter.yaml")
    l  = loadfn("my_launchpad.yaml")

    f.update({"category":i})
    q.update({"rocket_launch":"rlaunch -c {} singleshot".format(os.path.join(path,i))})
    l.update({"name":proj})

    dumpfn(f, os.path.join(path, i, "my_fworker.yaml"))
    dumpfn(q, os.path.join(path, i, "my_qadapter.yaml"))
    dumpfn(l, os.path.join(path, i, "my_launchpad.yaml"))

    os.makedirs(os.path.join("/global/homes/j/jlabtsai/scratch",  proj), exist_ok=True)

create_fworker(sys.argv[1], sys.argv[2])


#qlaunch -c /home/j.tsai/config/project/defect_qubit_in_36_group/charge_state/ -r rapidfire -m 10