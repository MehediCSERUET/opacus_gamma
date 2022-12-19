#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from opacus.accountants import PRVAccountant


# Computed from https://github.com/microsoft/prv_accountant
msr_values = {
    (0.8, 0.001, 100): 0.270403364058018680360362395731,
    (1.5, 0.001, 100): 0.0393694193095203287535710501288,
    (2.0, 0.001, 100): 0.0291045369484074882560076247273,
    (3.0, 0.001, 100): 0.0215200934390882663016508757892,
    (0.8, 0.05, 100): 6.74105193941409996938318727189,
    (1.5, 0.05, 100): 1.95385313568420015961635272106,
    (2.0, 0.05, 100): 1.28363737962406521120328761754,
    (3.0, 0.05, 100): 0.767933789666825572517439013609,
    (0.8, 0.2, 100): 24.3336641779225644199868838768,
    (1.5, 0.2, 100): 8.49897785912163072907787864096,
    (2.0, 0.2, 100): 5.67205560882372950004537415225,
    (3.0, 0.2, 100): 3.38122051022184422208738396876,
    (0.8, 0.001, 1000): 0.477771266184522591657923840103,
    (1.5, 0.001, 1000): 0.0998206602308474855167474970585,
    (2.0, 0.001, 1000): 0.0712187825381152272985474382949,
    (3.0, 0.001, 1000): 0.0476159308713589302097801692071,
    (0.8, 0.05, 1000): 19.5258428053837356230815203162,
    (1.5, 0.05, 1000): 6.20996924657726712126759593957,
    (2.0, 0.05, 1000): 4.17279986668931890392286732094,
    (3.0, 0.05, 1000): 2.52757432605973830774814814504,
    (0.8, 0.001, 20000): 1.29600925757016161021795142005,
    (1.5, 0.001, 20000): 0.437005108654860807693154356457,
    (2.0, 0.001, 20000): 0.305837939762453436820521801565,
    (3.0, 0.001, 20000): 0.194031030686054706269061398416,
    # (0.8, 0.05, 20000): 140.655209760074228597659384832,
    (1.5, 0.05, 20000): 38.3066179140872336006395926233,
    (2.0, 0.05, 20000): 24.4217185703225858617315680021,
    (3.0, 0.05, 20000): 13.9611146992367061159256991232,
    (0.8, 0.001, 50000): 2.03451480771586634688219419331,
    (1.5, 0.001, 50000): 0.704218384555810095193351116905,
    (2.0, 0.001, 50000): 0.491354910211401318953505779064,
    (3.0, 0.001, 50000): 0.309694161156544023327796821832,
    # (0.8, 0.05, 50000): 291.384325452396524269715882838,
    (1.5, 0.05, 50000): 73.1901767238329625797632616013,
    (2.0, 0.05, 50000): 45.2369958613306906158868514467,
    (3.0, 0.05, 50000): 24.9420056431444763234139827546,
    # (0.8, 0.001, 100000): 2.92462211935041027643933375657,
    # (1.5, 0.001, 100000): 1.01528807502760787251361307426,
    # (2.0, 0.001, 100000): 0.706719901081851564761393547087,
    # (3.0, 0.001, 100000): 0.443671720880875475323534828931,
}


class PRVAccountantTest(unittest.TestCase):
    def test_values(self):
        for (sigma, q, steps), expected_epsilon in msr_values.items():
            accountant = PRVAccountant()
            accountant.history = [(sigma, q, steps)]
            epsilon = accountant.get_epsilon(delta=1e-6)
            self.assertAlmostEqual(epsilon, expected_epsilon, places=4)