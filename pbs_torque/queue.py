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
# Last modified: 2014-07-18 12:02
#
#   DESCRIPTION:
#
#         USAGE:
#
#====================================================================================
"""
from . import defaults

class Queue:
    """ A Torque queue handling object.

        Allows queue monitoring, automatic resubmission, and
        improved job information. """


    class Job:
        """ A single Torque job object for managing and interacting
            with queue jobs.

            Allows intelligent resubmission. """

        def __init__(self, template):
            pass

        def submit(self):
            """ Submit a job using qsub and return job number """
            pass
