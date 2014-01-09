Gordon Tools
============

Simple scripts for interacting with the Gordon cluster.

Currently housed in /home/peanut/gordon_tools

ezqsub
------

Python3 script that splits a file full of commands and submits jobs in batches on 
the Gordon cluster.

It makes use of the multithreading module in python for script execution on the nodes.

The main issue right now is that it leaves temp files in the /tmp directory, so the
user must manually delete them, otherwise they will just live there until the system
clears them.  I think this isn't a major issue as these files are so small, but it is
still not ideal.

#====================================================================================
#
#          FILE: ezqsub (python 3)
#        AUTHOR: Michael D Dacre, mike.dacre@gmail.com
#  ORGANIZATION: Stanford University
#       LICENSE: MIT License
#       VERSION: 0.1
#       CREATED: 2013-12-26 17:37
# Last modified: 2014-01-09 14:36
#
#   DESCRIPTION: Take a file of scripts and submit it to the gordon cluster
#                The file should be one line per job, the lines can be arbitrarily
#                long and complex bash scripts, just use semi-colons instead of new-
#                lines.
#                To modify the qsub parameters, use the -l command, to modify the
#                queue, use the -q command.  Note that the '-l nodes=' qsub Command
#                will always be '-l nodes=1:native' in this script.  To use multiple
#                nodes together with MPI, use the bundler.py script.
#
#          NOTE: The node string is hardcoded as -l nodes=1:ppn=16,native. To change
#                this you have to edit the source code variable 'default_nodes'. 
#                There should never be a reason to do this on Gordon
#
#         USAGE: ezqsub script_file.txt or ezqsub < script_file.txt
#
#====================================================================================
