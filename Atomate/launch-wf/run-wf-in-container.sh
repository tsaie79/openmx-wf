#!/bin/bash

singularity exec --bind /scratch:/scratch --bind /shared:/shared ~/ht-openmx-db.sif bash -c "

module load intel-oneapi/2021.1_u9;
export PATH=$HOME/openmx3.9_neu/source:$PATH;
source /shared/centos7/intel/oneapi/2021.1_u9-base/setvars.sh;

ssh -Nf db-sinica;

$${pre_rocket};
cd $${launch_dir};
$${rocket_launch};
$${post_rocket};
"


#!/bin/bash

# Create a FIFO file
FIFO_FILE=/tmp/my_fifo
mkfifo $FIFO_FILE

# Write commands to FIFO file
echo "module load intel-oneapi/2021.1_u9;
export PATH=$HOME/openmx3.9_neu/source:$PATH;
source /shared/centos7/intel/oneapi/2021.1_u9-base/setvars.sh;
which mpiexec > ~/out
" > $FIFO_FILE &

# Run commands from FIFO file in the container
singularity exec --bind /scratch:/scratch --bind /shared:/shared ~/ht-openmx-db.sif bash -c "bash < $FIFO_FILE"