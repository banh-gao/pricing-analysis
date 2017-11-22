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
from pprint import pprint
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

    def __init__(self):
        self.sim = sim.Sim.Instance()
        self.logger = self.sim.get_logger()

    def initialize(self, config):
        self.run_number = config.run_number
        self.application = config.get_param(Cluster.APPLICATION)
        self.size = Distribution(config.get_param(Cluster.SIZE))
        self.offer = Distribution(config.get_param(Cluster.OFFER))
        self.resource = config.get_param(Cluster.RESOURCE)

        Configuration().host = config.get_param(Cluster.ENDPOINT)
        self.api = swagger_client.DeploymentsApi()

        self.index = 0

    def finalize(self):
        deployments = self.api.get_deployments_collection()

        for d in deployments.deployments:
            self.api.delete_deployment(d.name)

    def get_allocated(self):
        '''Get currently allocated resources size'''
        deployments = self.api.get_deployments_collection()

        allocation = 0
        for d in deployments.deployments:
            for res in d.resources:
                if res['name'] == self.resource:
                    allocation += res['amount']

        return allocation

    def request_allocation(self):
        size = self.size.get_value()

        app_name = "test-%s-%s" % (self.run_number, self.index)
        self.index += 1

        request = swagger_client.DeploymentRequest(self.application,
                                                   str(self.offer.get_value()),
                                                   [{'name': self.resource, 'amount': str(size) }])

        # Request an application deployment
        try:
            allocation = self.api.put_deployment(app_name, request)
            self.logger.log_allocation(allocation)
        except ApiException as e:
            self.logger.log_failure(request)
