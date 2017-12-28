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

import scipy.stats as stats
import sys


class Distribution:
    """
    Generic distribution class that implements different distributions depending
    on the parameters specified in a configuration
    """

    # distribution type field
    DISTRIBUTION = "distribution"
    # mean field
    MEAN = "mean"
    # lambda field
    LAMBDA = "lambda"
    # min field
    MIN = "min"
    # max field
    MAX = "max"
    # integer distribution field
    INT = "int"
    # shape distribution field
    SHAPE = "shape"
    # mode distribution field
    MODE = "mode"
    # constant random variable
    CONSTANT = "const"
    # uniform random variable
    UNIFORM = "unif"
    # exponential random variable
    EXPONENTIAL = "exp"
    # pareto random variable
    PARETO = "pareto"

    def __init__(self, config):
        """
        Instantiates the distribution
        :param config: an object used for configuring the distribution in the
        format {"distribution":NAME,"par1":value[,"par2":value,...]}.
        Accepted values so far are:
        {"distribution" : "const", "mean" : value}, constant variable
        {"distribution" : "exp", "mean" : value}, exponential random variable
        with mean being 1/lambda. "lambda" : value can also be used
        {"distribution" : "unif", "min" : value, "max" : value}, uniform random
        variable between min and max
        {"distribution" : "pareto", "shape": value, "mode": value}, pareto
        random variable with shape and mode
        """
        try:
            # find the correct distribution depending on the specified name
            if config[Distribution.DISTRIBUTION] == Distribution.CONSTANT:
                self.d = Const(config[Distribution.MEAN])
            elif config[Distribution.DISTRIBUTION] == Distribution.UNIFORM:
                integer = False
                try:
                    int_distribution = config[Distribution.INT]
                    if int_distribution == 1:
                        integer = True
                except Exception:
                    integer = False
                self.d = Uniform(config[Distribution.MIN],
                                 config[Distribution.MAX], integer)
            elif config[Distribution.DISTRIBUTION] == Distribution.PARETO:
                integer = False
                try:
                    int_distribution = config[Distribution.INT]
                    if int_distribution == 1:
                        integer = True
                except Exception:
                    integer = False
                self.d = Pareto(config[Distribution.SHAPE], config[Distribution.MODE], integer)
            elif config[Distribution.DISTRIBUTION] == Distribution.EXPONENTIAL:
                if Distribution.MEAN in config:
                    self.d = Exp(config[Distribution.MEAN])
                else:
                    self.d = Exp(1.0/config[Distribution.LAMBDA])
            else:
                print("Distribution error: unimplemented distribution %s",
                      config[Distribution.DISTRIBUTION])
        except Exception as e:
            print("Error while reading distribution parameters")
            print(e.message)
            sys.exit(1)

    def get_value(self):
        return self.d.get_value()

    def get_probability(self, a, b):
        """ Get the probability of assuming values in the given interval"""
        return self.d.get_probability(a, b)

    def get_mean(self):
        return self.d.get_mean()

class Const:
    """
    Constant random variable
    """

    def __init__(self, value):
        """
        Constructor
        :param value: returned constant value
        """
        self.value = value

    def get_value(self):
        return self.value

    def get_probability(self, a, b):
        if a <= self.value and self.value <= b:
            return 1
        else:
            return 0

class Uniform:
    """
    Uniform random variable
    """

    def __init__(self, min, max, integer=False):
        """
        Constructor
        :param min: minimum value
        :param max: maximum value
        :param integer: whether to use integer or floating point numbers
        """
        self.min = min
        self.max = max
        self.integer = integer

    def get_value(self):
        value =  stats.uniform.rvs(self.min, self.max - self.min)
        if self.integer:
            return round(value)
        else:
            return value

    def get_mean(self):
        return stats.uniform.mean(self.min, self.max - self.min)

    def get_probability(self, a, b):
        return stats.uniform.cdf(b, self.min, self.max - self.min) - \
            stats.uniform.cdf(a, self.min, self.max - self.min)

class Exp:
    """
    Exponential random variable
    """

    def __init__(self, mean):
        """
        Constructor
        :param mean: mean value
        """
        self.mean = mean

    def get_value(self):
        return stats.expon.rvs(0, self.mean)

    def get_probability(self, a, b):
        return stats.expon.cdf(b, 0, self.mean) - \
            stats.expon.cdf(a, 0, self.mean)

class Pareto:
    """
    Pareto random variable
    """

    def __init__(self, shape, mode, integer=False):
        """
        Constructor
        :param shape: pareto shape parameter
        :param mode: pareto mode parameter
        :param integer: whether to use integer or floating point numbers
        """
        self.shape = shape
        self.mode = mode
        self.integer = integer

    def get_value(self):
        value = stats.pareto.rvs(self.shape, self.mode)
        if self.integer:
            return round(value)
        else:
            return value

    def get_probability(self, a, b):
        return stats.pareto.cdf(b, self.shape, self.mode) - \
            stats.pareto.cdf(a, self.shape, self.mode)

    def get_mean(self):
        return stats.pareto.mean(self.shape, self.mode)
