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
# Copyright (C) 2018 Daniel Zozin <d.zozin@fbk.eu>

import time

class Cluster:
    """
    This class allocates resources on the cluster by calling the cluster API
    """

    def __init__(self, config):
        self.config = config
        self.allocation = 0

    def initialize(self):
        #TODO clean cluster from previous allocations
        pass

    def get_allocated(self):
        #TODO get currently allocated resources size
        return self.allocation

    def get_total_size(self):
        #TODO get total cluster size
        return 10

    def request_allocation(self):
        #TODO call allocation API
        if(self.allocation < self.get_total_size()):
            self.allocation += 1
            time.sleep(1)
