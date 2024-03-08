# coding: utf-8
#
# Copyright 2021 The Technical University of Denmark
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations
import sys
import itertools
import numpy as np
from utils import pos_add, pos_sub, APPROX_INFINITY
from collections import deque, defaultdict

import domains.hospital.state as h_state
import domains.hospital.goal_description as h_goal_description
import domains.hospital.level as h_level

class HospitalGoalCountHeuristics:

    # Write your own implementation of the goal count heuristics here. 
    # Remember that the goal count heuristics is simply the number of goals that are not satisfied in the current state. 

    def __init__(self):
        self.num_goals = 0

    def preprocess(self, level: h_level.HospitalLevel):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        pass

    def h(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:
        for goal in goal_description.goals:
            if goal.is_goal(state): self.num_goals += 1

        print("num_goals: ", self.num_goals)
        return goal_description.num_sub_goals() - self.num_goals

class HospitalAdvancedHeuristics:

    def __init__(self):
        self.distances = None
        self.goal_chars = None
        self.agent_chars = None
        self.goals = None