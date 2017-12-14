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
import sim
from distribution import Distribution

import swagger_client
from swagger_client.rest import ApiException
from swagger_client.configuration import Configuration

class Cluster:
    """
    This class allocates resources on the cluster by calling the cluster API
    """

    SIZE = "size"
    OFFER = "offer"
    APPLICATION = "application"
    ENDPOINT = "endpoint"
    RESOURCE = "resource"
    RESOURCE_SCALE = "resource_scale"

    def __init__(self):
        self.sim = sim.Sim.Instance()
        self.logger = self.sim.get_logger()
        self.requests = []

    def initialize(self, config):
        self.run_number = config.run_number
        self.application = config.get_param(Cluster.APPLICATION)
        self.size = Distribution(config.get_param(Cluster.SIZE))
        self.offer = Distribution(config.get_param(Cluster.OFFER))
        self.resource = config.get_param(Cluster.RESOURCE)
        self.resource_scale = int(config.get_param(Cluster.RESOURCE_SCALE))
        Configuration().host = config.get_param(Cluster.ENDPOINT)
        self.api = swagger_client.DeploymentsApi()

        self.index = 0

    def finalize(self):
        for app in self.requests:
            try:
                self.api.delete_deployment(app)
            except ApiException:
                pass

    def request_allocation(self):

        app_name = "test-%s-%s" % (self.run_number, self.index)
        self.index += 1

        unity_offer = self.offer.get_value()

        scaled_size = self.size.get_value()

        # Offer for the requested size (same magnitude)
        offer = scaled_size * unity_offer

        raw_size = scaled_size * self.resource_scale
        request = swagger_client.DeploymentRequest(self.application,
                                                   str(offer),
                                                   [{'name': self.resource, 'amount': str(raw_size) }])

        self.requests.append(app_name)

        # Request an application deployment
        try:
            allocation = self.api.put_deployment(app_name, request)
            allocation.resources[self.resource]['allocated'] = scaled_size
            self.logger.log_allocation(allocation, self.resource)
        except ApiException as e:
            request.resources[0]['amount'] = scaled_size
            self.logger.log_failure(request)
