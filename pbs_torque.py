#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8 tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# Copyright © Mike Dacre <mike.dacre@gmail.com>
#
# Distributed under terms of the MIT license
"""
#====================================================================================
#
#          FILE: queue (python 3)
#        AUTHOR: Michael D Dacre, mike.dacre@gmail.com
#  ORGANIZATION: Stanford University
#       LICENSE: MIT License, Property of Stanford, Use as you wish
#       VERSION: 0.1
#       CREATED: 2014-07-18 10:11
# Last modified: 2014-07-18 21:44
#
#   DESCRIPTION:
#
#         USAGE:
#
#====================================================================================
"""
from subprocess import check_output as rn
from subprocess import Popen, PIPE
from datetime import timedelta as delta
from sys import stderr
from re import split as s
from re import findall as find

class queue:
    """ A Torque queue handling object.

        Allows queue monitoring, automatic resubmission, and
        improved job information. """

    def __init__(self):
        self.queues = [ i.split(' ')[0] for i in rn(['qstat', '-q']).decode('utf8').split('\n')[5:-3] ]
        self.nodes  =

    def get_job_list(self):
        """ Run qstat -n -1 and return a dictionary of job information """
        qstat = rn(['qstat', '-n', '-1']).decode('utf8').split('\n')

        self.jobs = {}
        for i in qstat:
            f = s(r' +', i)
            # Get elapsed seconds
            e = f[10].split(':')
            e2 = (int(e[0]) * pow(60, 2)) + (int(e[1]) * 60) + int(e[2])
            self.jobs[find(r'[0-9]+', f[0])] = {'user'     : f[1],
                                                'queue'    : f[2],
                                                'job_name' : f[3],
                                                'sess_id'  : '' if f[4] == '--' else f[4],
                                                'nodes'    : f[5],
                                                'tasks'    : f[6],
                                                'memory'   : f[7],
                                                'walltime' : '' if f[8] == '--' else f[8],
                                                'state'    : f[9],
                                                'elapsed'  : '' if f[10] == '--' else f[10],
                                                'elapseds' : int(e2),
                                                'nodes'    : [] if f[11] == '--' else f[11].split('/')
                                                }


    def check_job(self, job_no):
        """ Execute qstat and return:
            (state, elapsed_time, [node_list] if job in list,
            if not, return 0 """

        job_list = queue.get_job_list()

        if job_no in job_list:
            return(job_list[job_no])
        else:
            return(0)

class job:
    """ A job before it is a job

        There is only one absolutely required parameter:
        command = The actual command to execute on the cluster, as a shell script (string)

        Optional but important parameters are:
        walltime    = How long the job should run e.g. 01:00:00 for 1 hour
        memory      = How much memory each job should have e.g. 20GB
        queue       = Which queue to put the job in e.g. 'default'
        node_string = A correctly formatted string specifying number of nodes/cores
                        e.g. nodes=1:ppn=16:native

        Standard torque parameters that are commonly modified:
        name = A name for this job
        mail = Mail flag

        Other possible parameters:
        modules = If you are working on a rocks cluster, a list of modules
        address = the PBS -A parameter, used by some clusters, such as
                  the SDSC clusters, to keep track of billing hours

        Manual overrides:
        template    = The qsub virtual file as a string, optional
        pbs_command = The actual qsub submission command as a tuple (optional)
        flags       = Provide any other flags to qsub (string) e.g. '-l nodes=1'

        Note, if you provide a template or pbs_command, this function will use those
        verbatim, and will not modify them (other than to add the execution command
        to the end of the template file. If you don't provide them, I will create
        them using this job's variables."""

    queue = ''
    walltime = ''
    name = ''
    mail = ''
    flags = ''

    # Specify details about the nodes you want
    node_string = ''

    # Address refers to the PBS -A parameter, used by some clusters, such as
    # the SDSC clusters, to keep track of billing hours
    address = ''

    # The actual execution command
    command = ''

    # The pbs submission command
    pbs_command = ''

    # Internal control variables
    _prepared  = False
    _submitted = False

    def prepare(self):
        """ Create a template file and qsub command for submission """

        # Abort it there is no command
        if not self.command:
            raise Exception("No command provided, cannot continue")

        # Create the virtual file  for pbs
        if not self.template:
            self.template    = "#!/bin/bash\n#PBS -S /bin/bash\n"
            if self.queue:
                self.template = self.template + "\n#PBS -q " + self.queue
            if self.name:
                self.template = self.template + "\n#PBS -n " + self.name
            if self.walltime:
                self.template = self.template + "\n#PBS -l walltime=" + self.walltime
            if self.mail:
                self.template = self.template + "\n#PBS -m " + self.mail
            self.template = ''.join([template, '\n\ncd $PBS_O_WORKDIR\n\n'])

            # Add Rocks modules if those are present
            if self.modules:
                for module in self.modules:
                    self.template = self.template + 'module load '
                    self.template = self.template + module + '\n'
                self.template = self.template + '\n'

        # Append the command to execute to the template file
        self.template = self.template + command

        # Create the command to execute qsub
        if not self.qsub_command:
            self.pbs_command = ('qsub',)
            if self.queue:
                self.pbs_command = self.pbs_command + ('-q', self.queue)
            if self.flags:
                self.pbs_command = self.pbs_command + tuple(self.flags.split(' '))
            if self.address:
                self.pbs_command = self.pbs_command + ('-A', self.address)
            if self.node_string:
                self.pbs_command = self.pbs_command + ('#PBS -l ', self.node_string)

        self._prepared = True

    def submit(self):
        """ Submit the job and return a job number """

        if not self.prep_done:
            self.prepare()

        # Submit
        pbs_submit = Popen(pbs_command, stdin=PIPE, stdout=PIPE)
        pbs_submit.stdin.write(self.template.encode())
        pbs_submit.stdin.close()

        # Return the job number
        self.job_no = (pbs_submit.stdout.read().decode().rstrip())

        self.submit_time = time.time()
        print(self.job_no, "submitted at", ctime(self.submit_time), file=stderr)

        return(self.job_no)

    def check_status(self):
        """ Check if job is running of queued
            Returns a tuple: (exit_code, exit_message)

            Code values:
                0: Not submitted
                1: Queued
                2: Running
                3: Completed
                4: Completed, not in queue
               -1: FAILED
            """

        if self._prepared:
            if self._submitted:
                j = queue.check_job(self.job_no)
                if j:
                    j2 = j['state']
                    if j2 == 'R':
                        status = (2, "Running, elapsed time = " + j['elapsed'])
                    elif j2 == 'C':
                        if j['elapseds']= < 2:
                             status == (-1, "Failed: Completed in less than 2 seconds")
                        else:
                            status = (3, "Completed, elapsed time = " + j['elapsed'])
                    elif j2 == 'E':
                        status = (-1, "Failed, error state")
                    elif j2 == 'Q':
                        status = (1, "In Queue")
                else:
                    status = (4, "Completed, no longer in queue")
            else:
                status = (0, "Not submitted")
        else:
            status = "Not prepped; not submitted"

        return(status)

    def did_i_fail(self):
        """ Check if job failed """
        status = check_status()
        submit_to_now = int(self.submitted) - int(time.time())
        elapsed_to_now = int(

        if status == "Completed"

def submit_multiple(jobs, delay=1, max_running=500):
    """ Submit an array of jobs, at one second intervals.
        These jobs must be job classes, not job numbers

        Specify a delay time a max number of running jobs

        Returns an array of job numbers"""
    from time import sleep

    # Find out how many jobs are already running
    job_length = check_qstat(user)

    m = False

    print("\nSubmitting jobs now")

    while 1:
        if job_length > max_running:
            if not m:
                print("There are", job_length, "job queued or running in the queue",
                      "which is greater than the max of", max_running,
                      "\nWaiting for other jobs to run...", file=sys.stderr)
                m = True
            sleep(delay)
            job_length = check_qstat(user)
            continue

        m = False

        job = jobs.pop(0)

        # Submit
        job_numbers.append(job.submit())

    return(job_numbers)

def check_multiple(jobs):
    """ Check every job in an array for running status.

        Return a tuple of arrays:

        (running, queued, complete, error) """
    pass
