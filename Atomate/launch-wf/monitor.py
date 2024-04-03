from multiprocessing import Pool
from fireworks import LaunchPad
import numpy as np
import matplotlib.pyplot as plt
import concurrent.futures

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
        num_reserved_fws = len(self.lpad.get_fw_ids({"state": "RESERVED"}))
        print(f"Number of reserved fireworks: {num_reserved_fws} ({num_reserved_fws/total_num_fws*100:.2f}%)")


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

        with concurrent.futures.ProcessPoolExecutor() as executor:
            runtimes = list(executor.map(self.get_runtime, fws))

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

    def get_launch_dir(self, fw_id):
        path = self.lpad.get_launchdir(fw_id)
        # get the last two parts of the path
        return path

    def get_fw_dir_by_state(self, state):
        fws = self.lpad.get_fw_ids({"state": state})

        with concurrent.futures.ProcessPoolExecutor() as executor:
            dirs = list(executor.map(self.get_launch_dir, fws))
        
        # return a pretty table of the data
        from prettytable import PrettyTable
        x = PrettyTable()
        x.field_names = ["fw_id", "launch_dir"]
        for i in range(len(fws)):
            x.add_row([fws[i], dirs[i]])
        return x
    

class FwRerunner:
    def __init__(self, launchpad_file):
        """
        Initialize the FwRerunner with a LaunchPad.

        Args:
            lpad (LaunchPad): The LaunchPad to use for rerunning Fireworks.
        """
        self.lpad = LaunchPad.from_file(launchpad_file)

    def rerun_fw(self, fw_id, recover_from_last=False):
        """
        Rerun a Firework given its id.

        Args:
            fw_id (int): The id of the Firework to rerun.
        """
        self.lpad.rerun_fw(fw_id, recover_launch="last" if recover_from_last else None, recover_mode="prev_dir" if recover_from_last else None)


    def rerun_fw_by_state(self, state, recover_from_last=False):
        """
        Rerun all Fireworks with a given state.

        Args:
            state (str): The state of the Fireworks to rerun.
        """
        fws = self.lpad.get_fw_ids({"state": state})

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.rerun_fw, fw, recover_from_last=recover_from_last): fw for fw in fws}
            for future in concurrent.futures.as_completed(futures):
                fw = futures[future]
                try:
                    future.result()
                except Exception as exc:
                    print(f'Firework {fw} generated an exception: {exc}')


if __name__ == "__main__":
    monitor = JobMonitor("/workspaces/openmx-wf/Atomate/setting/my_launchpad.yaml")
    monitor.check_fw()
    # monitor.eval_time_per_fw(plot=False)
    # print(monitor.get_fw_dir_by_state("FIZZLED"))
    
    # rerunner = FwRerunner("/workspaces/openmx-wf/Atomate/setting/my_launchpad.yaml")
    # rerunner.rerun_fw_by_state("FIZZLED", recover_from_last=False)