# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2016 Michele Segata <segata@ccs-labs.org>
# Copyright (C) 2018 Daniel Zozin <d.zozin@fbk.eu>

import sys
import random
import scipy
import time
import math
import curses
from singleton import Singleton
from config import Config
from cluster import Cluster
from log import Log

# VT100 command for erasing content of the current prompt line
ERASE_LINE = '\x1b[2K'


@Singleton
class Sim:
    """
    Main simulator class
    """

    # name of the section in the configuration file that includes all simulation
    # parameters
    PAR_SECTION = "Simulation"

    # seed for PRNGs
    PAR_SEED = "seed"


    # Run simulation as long as the probability of allocating resources is
    # higher than this value
    HALTING_THRESHOLD = "halting_threshold"

    def __init__(self):
        """
        Constructor initializing current cluster allocation to 0
        """
        # initialize() should be called before running the simulation
        self.initialized = False
        # empty config file
        self.config_file = ""
        # empty section
        self.section = ""

    def set_config(self, config_file, section):
        """
        Set config file and section
        :param config_file: file name of the config file
        :param section: the section within the config file
        """
        self.config_file = config_file
        self.section = section
        # instantiate config manager
        self.config = Config(self.config_file, self.section)

    def get_runs_count(self):
        """
        Returns the number of runs for the given config file and section
        :returns: the total number of runs
        """
        if self.config_file == "" or self.section == "":
            print("Configuration error. Call set_config() before "
                  "get_runs_count()")
            sys.exit(1)
        return self.config.get_runs_count()

    def initialize(self, run_number):
        """
        Simulation initialization method
        :param run_number: the index of the simulation to be run
        """
        if self.config_file == "" or self.section == "":
            print("Configuration error. Call set_config() before initialize()")
            sys.exit(1)
        # set and check run number
        self.run_number = run_number
        if run_number >= self.config.get_runs_count():
            print("Simulation error. Run number %d does not exist. Please run "
                  "the simulator with the --list option to list all possible "
                  "runs" % run_number)
            sys.exit(1)
        self.config.set_run_number(run_number)
        # instantiate data logger
        self.logger = Log(self.config.get_output_file())

        # get seeds. each seed generates a simulation repetition
        self.seed = self.config.get_param(self.PAR_SEED)
        random.seed(self.seed)
        scipy.random.seed(self.seed)

        self.halting_threshold = self.config.get_param(self.HALTING_THRESHOLD)

        self.cluster = Cluster()

        # initialize cluster
        self.cluster.initialize(self.config)

        # all done. simulation can start now
        self.initialized = True

    def get_logger(self):
        """
        Returns the data logger to modules
        """
        return self.logger

    def run(self):
        """
        Runs the simulation.
        """
        # first check that everything is ready
        if not self.initialized:
            print("Cannot run the simulation. Call initialize() first")
            sys.exit(1)
        # save the time at which the simulation started, for statistical purpose
        start_time = time.time()
        # last time we printed the simulation percentage
        prev_time = start_time
        self.expected_deployments = self.cluster.get_expected_deployments()
        self.deployments = 0
        self.failed = 0
        self.allocation_prob = self.cluster.get_allocation_probability()

        try:
            self.stdscr = curses.initscr()

            # print percentage for the first time (0%)
            self.print_percentage(True)
            # main simulation loop
            while self.allocation_prob > self.halting_threshold:
                # request next allocation
                if(self.cluster.request_allocation()):
                    self.deployments += 1
                else:
                    self.failed += 1

                # get current real time
                curr_time = time.time()
                # if more than a second has elapsed, update the percentage bar
                if curr_time - prev_time >= 1:
                    self.print_percentage(False)
                    prev_time = curr_time

                # Update allocation probability
                self.allocation_prob = self.cluster.get_allocation_probability()

            #Clean up
            self.cluster.finalize()

            # simulation completed, print the percentage for the last time (100%)
            self.print_percentage(False)
        finally:
            curses.endwin()

        # compute how much time the simulation took
        end_time = time.time()
        total_time = round(end_time - start_time)
        print("Reached allocation probability of %.2f. Terminating." % self.allocation_prob)
        print("Failed deployments: %d" % self.failed)
        print("Successful deployments: %d" % self.deployments)
        print("Total simulation time: %d hours, %d minutes, %d seconds" %
              (total_time / 3600, total_time % 3600 / 60,
               total_time % 3600 % 60))

    def print_percentage(self, first):
        self.stdscr.addstr(0, 0, "Expected successful deployments: %d" % self.expected_deployments)

        self.stdscr.addstr(2, 0, "Allocation probability: %.2f (halting under %.2f)" %
                           (self.allocation_prob, self.halting_threshold))
        perc = min(100, int(math.floor(float(self.deployments) / self.expected_deployments*100)))
        self.stdscr.addstr(3, 0, "[%-20s] %d%% (%d/%d)" % ('='*(perc/5), perc, self.deployments,  self.expected_deployments))

        self.stdscr.refresh()

    def get_params(self, run_number):
        """
        Returns a textual representation of simulation parameters for a given
        run number
        :param run_number: the run number
        :returns: textual representation of parameters for run_number
        """
        return self.config.get_params(run_number)
