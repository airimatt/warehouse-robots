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

    # Remember that the goal count heuristics is simply the number of goals that are not satisfied in the current state. 

    def __init__(self):
        self.num_goals_to_reach = 0

    def preprocess(self, level: h_level.HospitalLevel):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        pass

    def h(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:
        # for (goal_position, goal_char, is_positive_literal) in goal_description.agent_goals: # goals has both agent_goals ad box_goals
        #     char = state.object_at(goal_position)
            
        #     if is_positive_literal and goal_char != char:
        #         self.num_goals_to_reach += 1 
        #     elif not is_positive_literal and goal_char == char:
        #         self.num_goals_to_reach += 1 
    
        for index in range(goal_description.num_sub_goals()):
            sub_goal = goal_description.get_sub_goal(index)
            if not sub_goal.is_goal(state): self.num_goals_to_reach += 1

        return self.num_goals_to_reach



class HospitalAdvancedHeuristics:
    # best-first search expands nodes with lower h-values before nodes with higher h-values
    # h-values should ideally always decrease when getting closer to the goal.
    # must be a greater improvement from goal count heuristic.

    def __init__(self):
        self.distances = {}
        # self.agent_to_box = {}
        # self.box_to_goal = {}
        self.goal_chars = None
        self.agent_chars = None
        self.goals = None

    
    def preprocess(self, level: h_level.HospitalLevel):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        # initially compute all exact distances between pairs of cells in the level.
        # then look up distances in O(1) time when computing your heuristic values.

        # Heuristic 1: Manhattan Distance

        rows = len(level.walls)
        cols = len(level.walls[0])
        
        for x1 in range(rows):
            for y1 in range(cols):
                for x2 in range(rows):
                    for y2 in range(cols):
                        self.distances[(x1, y1), (x2, y2)] = (abs(x2 - x1) + abs(y2 - y1))
            

    def h(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:
        total_distance = 0
        box_to_goal_distance = 0
        agent_to_box_distance = 0

        # for loop thru boxes and their corresponding goals
        # find the distance from each box and add to total_distance

        # heuristic 1
        box_index = 0
        for (goal_position, goal_char, is_positive_literal) in goal_description.box_goals:
            box = state.box_positions[box_index]
            box_to_goal_distance += self.distances[goal_position, box[0]]
            box_index += 1

        total_distance += box_to_goal_distance

        # heuristic 2 -- goes with heuristic 1
        box_index = 0
        for (agent_coordinate, _) in state.agent_positions:
            box = state.box_positions[box_index]
            agent_to_box_distance += self.distances[agent_coordinate, box[0]]
            box_index += 1

        total_distance += agent_to_box_distance

        return total_distance
