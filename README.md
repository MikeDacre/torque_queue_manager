Torque Queue Manager
====================

Python wrapper for interacting with the Torque PBS Queue.

Includes a script for easy job batch submission (ezqsub)

Designed for use primarily with SDSC's Gordon Compute Cluster, but it will work with
any Torque based queue system.

ezqsub
------

Take a file with one job per line (lines can be arbitratily long and contain multiple
commands separated by semi-colons), and split it into batches for running with qsub.

On Gordon the default batch size is 16.

Automatically submits each batch to qsub with a one second delay between batches. It 
also monitors the queue to only allow queue submission if the queue is not too full.
If the queue contains more jobs for the current user than allowed by the threshold 
defined in the ezqsub file, ezqsub will pause submission, recheck every 2 seconds, 
and only submit jobs to the queue when more space is available.

When jobs execute on the compute nodes, they are managed by this script also, and run
in parallel using python's built-in multi-threading function.
