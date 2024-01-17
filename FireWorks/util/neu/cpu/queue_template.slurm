#!/bin/bash -l

#SBATCH --nodes=$${nodes}
#SBATCH --ntasks=$${ntasks}
#SBATCH --ntasks-per-node=$${ntasks_per_node}
#SBATCH --cpus-per-task=$${cpus_per_task}
#SBATCH --mem=$${mem}
#SBATCH --gres=$${gres}
#SBATCH --qos=$${qos}
#SBATCH --time=$${walltime}
#SBATCH --partition=$${queue}
#SBATCH --account=$${account}
#SBATCH --job-name=$${job_name}
#SBATCH --license=$${license}
#SBATCH --output=$${job_name}-%j.out
#SBATCH --error=$${job_name}-%j.error
#SBATCH --constraint=$${constraint}


ssh -N -f -L localhost:12349:localhost:27017 tsai@129.10.50.43
ssh -N -f -L localhost:12350:localhost:22 tsai@129.10.50.43


module load intel/compilers-2022.0.1
module load intel/mpi-2021.5.0
module load hdf5/1.12.1-intel2022
source /shared/centos7/intel/oneapi/2022.1.0/setvars.sh


source /home/j.tsai/software/anaconda3/etc/profile.d/conda.sh
conda activate wf


$${pre_rocket}
cd $${launch_dir}
$${rocket_launch}
$${post_rocket}

# CommonAdapter (SLURM) completed writing Template
