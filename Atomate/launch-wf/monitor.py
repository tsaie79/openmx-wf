from multiprocessing import Pool
from fireworks import LaunchPad
import numpy as np
import matplotlib.pyplot as plt

class JobMonitor:
    def __init__(self, launchpad_file):
        self.lpad = LaunchPad.from_file(launchpad_file)

    def check_fw(self):
        total_num_fws = len(self.lpad.get_fw_ids({}))
        num_completed_fws = len(self.lpad.get_fw_ids({"state": "COMPLETED"}))
        print(f"Number of completed fireworks: {num_completed_fws} ({num_completed_fws/total_num_fws*100:.2f}%)")
        num_fizzled_fws = len(self.lpad.get_fw_ids({"state": "FIZZLED"}))
        print(f"Number of fizzled fireworks: {num_fizzled_fws} ({num_fizzled_fws/total_num_fws*100:.2f}%)")
        num_running_fws = len(self.lpad.get_fw_ids({"state": "RUNNING"}))
        print(f"Number of running fireworks: {num_running_fws} ({num_running_fws/total_num_fws*100:.2f}%)")
        num_pending_fws = len(self.lpad.get_fw_ids({"state": "PENDING"}))
        print(f"Number of pending fireworks: {num_pending_fws} ({num_pending_fws/total_num_fws*100:.2f}%)")
        num_ready_fws = len(self.lpad.get_fw_ids({"state": "READY"}))
        print(f"Number of ready fireworks: {num_ready_fws} ({num_ready_fws/total_num_fws*100:.2f}%)")

    def get_runtime(self, fw_id):
        try:
            launch = self.lpad.get_launch_by_id(fw_id)
            runtime = launch.runtime_secs
            if type(runtime) != float:
                return 0
            return runtime
        except:
            return 0

    def eval_time_per_fw(self, plot=False):
        fws = self.lpad.get_fw_ids({"state": "COMPLETED"})
        with Pool(len(fws)) as p:
            runtimes = p.map(self.get_runtime, fws)
        print(f"Total number of completed fireworks: {len(runtimes)}")
        runtimes = np.array(runtimes)
        runtimes = runtimes/60
        runtimes = runtimes[runtimes != 0]
        print(f"Average runtime: {runtimes.mean():.2f}min")
        print(f"Standard deviation: {runtimes.std():.2f}min")

        if plot:
            plt.hist(runtimes, bins=100, edgecolor='black')
            plt.xlabel('Runtime (min)')
            plt.ylabel('Frequency')
            plt.title('Runtime Distribution')
            plt.show()


if __name__ == "__main__":
    monitor = JobMonitor("/workspaces/openmx-wf/Atomate/setting/my_launchpad.yaml")
    monitor.check_fw()
    monitor.eval_time_per_fw(plot=True)