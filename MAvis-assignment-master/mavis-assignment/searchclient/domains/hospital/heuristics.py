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
        for (goal_position, goal_char, is_positive_literal) in goal_description.agent_goals:
            char = state.object_at(goal_position)
            
            if is_positive_literal and goal_char != char:
                self.num_goals_to_reach += 1 
            elif not is_positive_literal and goal_char == char:
                self.num_goals_to_reach += 1 

        return self.num_goals_to_reach

class HospitalAdvancedHeuristics:
    # best-first search expands nodes with lower h-values before nodes with higher h-values
    # h-values should ideally always decrease when getting closer to the goal.
    # must be a greater improvement from goal count heuristic.

    def __init__(self):
        self.distances = {}
        self.goal_chars = None
        self.agent_chars = None
        self.goals = None

    
    def preprocess(self, level: h_level.HospitalLevel):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        # initially compute all exact distances between pairs of cells in the level.
        # then look up distances in O(1) time when computing your heuristic values.

        # TO-DO:
        # initialize a dictionary(hash table) to store lookup table to store distance between one cell and another
        # size us (# of cells in the map)^2 ?
        # fill in lookup table by calculating exact/Manhattan distance
        # reference lookup table by calling table(row, column) ?

        # Heuristic 1: Manhattan Distance

        rows = len(level.walls)
        cols = len(level.walls[0])

        # print("rows, cols", rows, cols)
    
                # distance = tuple of two positions : Manhattan Distance
                # [[x1, y1], [x2, y2]]
        
        for x1 in range(rows):
            for y1 in range(cols):
                for x2 in range(rows):
                    for y2 in range(cols):
                        self.distances[(x1, y1), (x2, y2)] = (abs(x2 - x1) + abs(y2 - y1))


    def h(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:
        # look up the distance and add to h

        total_distance = 0

        # forloop thru agents and their corresponding goals
            # calculate distance and add to total_distance
            
        agent_index = 0
        for (goal_position, goal_char, is_positive_literal) in goal_description.agent_goals:
            # print("num goals: ", len(goal_description.agent_goals))
            agent = state.agent_positions[agent_index]
            total_distance += self.distances[goal_position, agent[0]]
            agent_index += 1


            # print("agent index: ", agent_index)
            # print("agent ", agent[1])
            # print("goal at ", goal_position)
            # print("agent ", agent[1], " at position ", agent[0], " and distance: ", self.distances[goal_position, agent[0]])

        # for agent_pos in state.agent_positions:
        #     print("position of agent?: " + agent_pos[0])
    
        #     goal_pos = goal_description.agent_goals
        #     print("position of goal?: " + goal_pos[0])
            
        #     total_distance += self.distances[agent_pos, goal_pos]
        #     agent_num += 1
        
        # for box_pos in state.box_positions:
        #     boxgoal_pos = goal_description.box_goals[box_pos]
        #     total_distance += self.distances[box_pos[0], boxgoal_pos]
        # print("goal: ", goal_position)
        # print("agent: ", agent[0])
        # print("total distance: ", total_distance)
        return total_distance

        # total_distance = 0

        # for (goal_position, goal_char, is_positive_literal) in goal_description.agent_goals:
        #     char = state.object_at(goal_position)

        #     if is_positive_literal and goal_char != char:
        #         total_distance += min(
        #             self.distances[(goal_position, agent_position)]
        #             for agent_position in state.agent_positions
        #         )

        #     elif not is_positive_literal and goal_char == char:
        #         total_distance += min(
        #             self.distances[(goal_position, agent_position)]
        #             for agent_position in state.agent_positions
        #         )
        
        
        
        # pass

    