import os
from monty.serialization import loadfn, dumpfn
import sys

def create_fworker(port, proj, i):
    path = '/home/j.tsai/config/project/{}'.format(proj)
    port = int(port)
    os.makedirs(os.path.join(path, i), exist_ok=True)
    d = loadfn("db.json")
    f = loadfn("my_fworker.yaml")
    q = loadfn("my_qadapter.yaml")
    l  = loadfn("my_launchpad.yaml")
    l.update({"name":proj, "port": port})
    d.update({"database":proj, "collection": i, "port": port})
    f.update({"category":i})
    f["env"].update({"db_file":os.path.join(path, i, "db.json")})
    q.update({"rocket_launch":"rlaunch -c {} singleshot".format(os.path.join(path,i))})
    dumpfn(d, os.path.join(path, i, "db.json"), indent=4)
    dumpfn(f, os.path.join(path, i, "my_fworker.yaml"), default_flow_style=False)
    dumpfn(q, os.path.join(path, i, "my_qadapter.yaml"), default_flow_style=False)
    dumpfn(l, os.path.join(path, i, "my_launchpad.yaml"), default_flow_style=False)
    os.makedirs(os.path.join("/home/j.tsai/scratch", proj, i), exist_ok=True)

create_fworker(sys.argv[-3], sys.argv[-2], sys.argv[-1])
