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
# Last modified: 2014-07-18 15:56
#
#   DESCRIPTION:
#
#         USAGE:
#
#====================================================================================
"""
from subprocess import check_output as rn

class queue:
    """ A Torque queue handling object.

        Allows queue monitoring, automatic resubmission, and
        improved job information. """

    def __init__(self):
        self.nodes = [ i.split(' ')[0] for i in rn(['qstat', '-q']).decode('utf8').split('\n')[5:-3] ]

class job:
    """ A job before it is a job """

    def submit(self):
        """ Submit the job and return a job number """
        pass
