Gordon Tools
============

Simple scripts for interacting with the Gordon cluster.

Currently housed in /home/peanut/gordon_tools
Active user-available scripts are installed in /oasis/projects/nsf/sua131/peanut/usr/bin/

ezqsub
------

Python3 script that splits a file full of commands and submits jobs in batches on 
the Gordon cluster.

It makes use of the multithreading module in python for script execution on the nodes.

The main issue right now is that it leaves temp files in the /tmp directory, so the
user must manually delete them, otherwise they will just live there until the system
clears them.  I think this isn't a major issue as these files are so small, but it is
still not ideal.

```
usage: ezqsub [-h] [-i [INFILE]] [-n NAME] [-t THREADS] [--commands COMMANDS]
              [-d TMPDIR] [-q QUEUE] [-m MODULES [MODULES ...]] [-w WALLTIME]
              [-p PARAMS] [-a BILLING] [--cleanup]

====================================================================================

          FILE: ezqsub (python 3)
        AUTHOR: Michael D Dacre, mike.dacre@gmail.com
  ORGANIZATION: Stanford University
       LICENSE: MIT License
       VERSION: 0.1
       CREATED: 2013-12-26 17:37
 Last modified: 2014-01-21 07:55

   DESCRIPTION: Take a file of scripts and submit it to the gordon cluster
                The file should be one line per job, the lines can be arbitrarily
                long and complex bash scripts, just use semi-colons instead of new-
                lines.

         USAGE: ezqsub script_file.txt or ezqsub < script_file.txt

====================================================================================

optional arguments:
  -h, --help            show this help message and exit
  -i [INFILE], --infile [INFILE]
                        Input file, Default STDIN
  -n NAME, --name NAME  Job Name, will be prefix in qstat. Default: job
  -t THREADS, --threads THREADS
                        Over-ride number of threads per node, you should use
                        this if you want less than 16 to run at once on a
                        single node. Note that you will still be billed for
                        all 16 cores. Default: 16
  --commands COMMANDS   Over-ride number of commands sent to each node. This
                        defaults to the same as '-t'. If you want less than
                        16commands to run on a node, you can just set '-t'. If
                        however, you want jobs to run in serial on a node,
                        this can be a good option. This option should be
                        completely unnecessary most of the time Default: 16
  -d TMPDIR, --tmpdir TMPDIR
                        Where to store job files - you must delete them
                        manually, Default: /oasis/scratch/peanut/temp_project/
  -q QUEUE, --queue QUEUE
                        Queue Choice, Default: normal
  -m MODULES [MODULES ...], --modules MODULES [MODULES ...]
                        Choose modules to load, Default: python
  -w WALLTIME, --walltime WALLTIME
                        Set walltime, use least possible, max=336:00:00,
                        Default: python
  -p PARAMS, --params PARAMS
                        qsub parameters. These are any additional qsub flags
                        you wish to pass. Note that they should be enclosed in
                        parentheses e.g. "-l mem=32GB", not just plain
                        'mem=32GB', If you don't include the flags, it won't
                        work. Default:
  -a BILLING, --billing BILLING
                        Choose the address to bill to, find this with
                        show_account or on portal.xsedeq.org, Default: sua135
  --cleanup             Cleanup your temporary directory. Please run this
                        every now and then. IMPORTANT: DO NOT RUN IF YOU HAVE
                        JOBS IN THE QUEUE!!!.Default temp directory:
                        /oasis/scratch/peanut/temp_project/Default prefix:
                        'job'. If you use the -n flag in any of your runs, use
                        that same flag. e.g. if you ran with 'ezqsub -n my_job
                        -i my_job_script.txt', cleanup with 'ezqsub -n my_job
                        --cleanup'
```

Signature file is updated on every github upload

