1. Use the following code to connect to the database at Sinica:
   ```shell
   Host db-sinica 
      HostName login.discovery.neu.edu
      User j.tsai
      LocalForward 12345 hercules.phys.sinica.edu.tw:12345

2. Use `my_launchpad.yaml` and set up the `logs` on local for launching workflows.