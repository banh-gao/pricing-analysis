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

import sim
from packet import Packet


class Log:
    """
    Defines data logging utilities
    """

    def __init__(self, output_file):
        """
        Constructor.
        :param output_file: output file name. will be overwritten if already
        existing
        """
        self.sim = sim.Sim.Instance()
        self.log_file = open(output_file, "w")
        self.log_file.write("time,src,dst,event,size\n")

    def log_packet(self, source, destination, packet):
        """
        Logs the result of a packet reception.
        :param source: source node
        :param destination: destination node id
        :param packet: the packet to log
        """
        self.log_file.write("%f,%d,%d,%d,%d\n" %
                            (self.sim.get_time(), source.get_id(),
                             destination.get_id(), packet.get_state(),
                             packet.get_size()))

    def log_queue_drop(self, source, packet_size):
        """
        Logs a queue drop
        :param source: source node
        :param packet_size: size of the packet being dropped
        """
        self.log_file.write("%f,%d,%d,%d,%d\n" %
                            (self.sim.get_time(), source.get_id(),
                             source.get_id(), Packet.PKT_QUEUE_DROPPED,
                             packet_size))

    def log_arrival(self, source, packet_size):
        """
        Logs an arrival
        :param source: source node
        :param packet_size: size of the packet being dropped
        """
        self.log_file.write("%f,%d,%d,%d,%d\n" %
                            (self.sim.get_time(), source.get_id(),
                             source.get_id(), Packet.PKT_GENERATED,
                             packet_size))
