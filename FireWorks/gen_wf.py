from fireworks import Workflow, Firework, LaunchPad, ScriptTask, TemplateWriterTask
import os
import time


LPAD = LaunchPad.from_file('my_launchpad.yaml')

def ersap_wf(wf_id, nnode=1, qos="debug", walltime="00:30:00", category="ersap-node1"):
    # if walltime is larger than 1 hour, give warning and replace it with 30 miiutes
    if walltime > "01:00:00" and qos == "debug":
        print("Warning: walltime is larger than 1 hour, replace it with 30 minutes")
        walltime = "00:30:00"
    
    fw_name = f"ersap-node{wf_id}"
    
    vk_string = ("#!/bin/bash\n\n"
                "export NODENAME=" + fw_name + "\n"
                "export KUBECONFIG=/global/homes/j/jlabtsai/run-vk/kubeconfig/mylin\n\n"
                "ssh -NfL 46859:localhost:46859 mylin\n\n"
                "shifter --image=docker:jlabtsai/vk-cmd:no-vk-container -- /bin/bash -c \"cp -r /vk-cmd `pwd`\"\n\n"
                "cd `pwd`/vk-cmd\n\n"
                "./start.sh $KUBECONFIG $NODENAME")


    task1 = ScriptTask.from_str(vk_string)
    
    fw = Firework([task1], name=fw_name)
    fw.spec["_category"] = category
    fw.spec["_queueadapter"] = {"job_name": fw_name, "walltime": walltime,
                                "qos": qos, "nodes": nnode}
    # preempt has min walltime of 2 hours (can get stop after 2 hours)
    # debug_preempt has max walltime of 30 minutes (can get stop after 5 minutes)
    wf = Workflow([fw], {fw: []})
    wf.name = fw_name
    return wf


def add_wf(number_of_wfs=8, job_setting={"nnode": 1, "qos": "regular", "walltime": "02:00:00", "category": "ersap-node1"}):
# this script is to launch the workflows based on:
# 1. Constantly check if the latest added workflow is running
# 2. If not, waith for 30 seconds and check again
# 3. If yes, wait for 120 seconds and add the next workflow
# 4. If the latest launched workflow is the last one, exit
# 5. add the first workflow when no workflow is reserving or running
    while True:
        # get the list of workflows
        wfs = LPAD.get_wf_ids()
        wfs.sort()
        if len(wfs) == 0:
            print("No workflow is running or reserving, add the first workflow")
            LPAD.add_wf(ersap_wf(wf_id=1, **job_setting))
            continue
        # get the latest workflow
        latest_wf = wfs[-1]
        print(f"Latest workflow is {latest_wf}")
        # get the status of the latest workflow
        wf_status = LPAD.get_wf_summary_dict(latest_wf)["state"]
        wf_name = LPAD.get_wf_summary_dict(latest_wf)["name"]
        # if the latest workflow is not running, wait for 30 seconds and check again
        while wf_status != "RUNNING":
            time.sleep(3)
            wf_status = LPAD.get_wf_summary_dict(latest_wf)["state"]
            print(f"Workflow {wf_name} is in {wf_status} state")
        # if the latest workflow is running, wait for 120 seconds and add the next workflow
        # launch the pod tha has the label name of the wf name
        print(f"Workflow {wf_name} is running; launch the pod {wf_name}")
        # check if the pod is already running
        if os.system(f"kubectl get pods -l app={wf_name} | grep {wf_name}"):
            print(f"Pod {wf_name} is not running; launch the pod")
            os.system(f"kubectl apply -f /workspaces/JIRIAF-test-platform/vk/configmap/jobs/pod.yml -l app={wf_name}")
        else:
            print(f"Pod {wf_name} is running; do nothing")
        # print("Wait for 120 seconds")
        # time.sleep(120)
        # if the latest workflow is the last one, exit
        if latest_wf == number_of_wfs:
            print(f"The last workflow {wf_name} is running; exit")
            return # exit the script
        # add the next workflow
        else:
            next_wf = latest_wf + 1
            LPAD.add_wf(ersap_wf(wf_id=next_wf, **job_setting))
            print(f"Add workflow {next_wf}")
            # subprocess.run(["qlaunch", "-r", "singleshot", "-f", f"{next_wf.fws[-1].fw_id}"])

if __name__ == "__main__":
    add_wf(number_of_wfs=1, job_setting={"nnode": 1, "qos": "debug", "walltime": "00:30:00", "category": "ersap-node1"})
    # LPAD.add_wf(ersap_wf(wf_id=1, nnode=2, qos="preempt", walltime="02:00:00"))
