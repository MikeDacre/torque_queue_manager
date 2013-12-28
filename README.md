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
