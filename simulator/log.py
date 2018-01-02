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

class Log:
    """
    Defines data logging utilities
    """

    TYPE_SUCCESS = "1"
    TYPE_FAILURE = "0"

    def __init__(self, output_file):
        """
        Constructor.
        :param output_file: output file name. will be overwritten if already
        existing
        """
        self.log_file = open(output_file, "w")
        self.log_file.write("accepted,size,node,utilization,offer,price,unit_price\n")

    def log_allocation(self, allocation, resource):
        """
        Logs the result of an allocation request
        :param allocation: resource allocation
        """
        self.log_file.write(self.TYPE_SUCCESS + ",%f,%s,%f,%f,%f,%f\n" %
                            (float(allocation.resources[resource]['used']),
                             allocation.node,
                             float(allocation.utilization),
                             float(allocation.offer),
                             float(allocation.price),
                             float(allocation.unit_price)))

    def log_failure(self, request):
        """
        Logs the result of an allocation request
        :param allocation: resource allocation
        """
        self.log_file.write(self.TYPE_FAILURE + ",%f,,,%f,,\n" %
                            (float(request.resources[0]['amount']),
                             float(request.offer)))
