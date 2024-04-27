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

# pos_add and pos_sub are helper methods for performing element-wise addition and subtractions on positions
# Ex: Given two positions A = (1, 2) and B = (3, 4), pos_add(A, B) == (4, 6) and pos_sub(B, A) == (2,2)
from utils import pos_add, pos_sub
from typing import Union, Tuple
import domains.hospital.state as h_state

# A dictionary mapping action names to the corresponding direction deltas2
direction_deltas = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1),
}

# An action class must implement three types be a valid action:
# 1) is_applicable(self, agent_index, state) which return a boolean describing whether this action is valid for
#    the agent with 'agent_index' to perform in 'state' independently of any other action performed by other agents.
# 2) result(self, agent_index, state) which modifies the 'state' to incorporate the changes caused by the agent
#    performing the action. Since we *always* call both 'is_applicable' and 'conflicts' prior to calling 'result',
#    there is no need to check for correctness.
# 3) conflicts(self, agent_index, state) which returns information regarding potential conflicts with other actions
#    performed concurrently by other agents. More specifically, conflicts can occur with regard to the following
#    two invariants:
#    A) Two objects may not have the same destination.
#       Ex: '0  A1' where agent 0 performs Move(E) and agent 1 performs Push(W,W)
#    B) Two agents may not move the same box concurrently,
#       Ex: '0A1' where agent 0 performs Pull(W,W) and agent 1 performs Pull(E,E)
#    In order to check for these, the conflict method should return two lists:
#       a) destinations which contains all newly occupied cells.
#       b) moved_boxes which contains the current position of boxes moved during the action, i.e. their position
#          prior to being moved by the action.
# Note that 'agent_index' is the index of the agent in the state.agent_positions list which is often but *not always*
# the same as the numerical value of the agent character.


Position = Tuple[int, int] # Only for type hinting

class NoOpAction:

    def __init__(self):
        self.name = "NoOp"

    def is_applicable(self, agent_index: int,  state: h_state.HospitalState) -> bool:
        # Optimization. NoOp can never change the state if we only have a single agent
        return len(state.agent_positions) > 1

    def result(self, agent_index: int, state: h_state.HospitalState):
        pass

    def conflicts(self, agent_index: int, state: h_state.HospitalState) -> tuple[list[Position], list[Position]]:
        current_agent_position, _ = state.agent_positions[agent_index]
        destinations = [current_agent_position]
        boxes_moved = []
        return destinations, boxes_moved

    def __repr__(self) -> str:
        return self.name


class MoveAction:

    def __init__(self, agent_direction):
        self.agent_delta = direction_deltas.get(agent_direction)
        self.name = "Move(%s)" % agent_direction

    def calculate_positions(self, current_agent_position: Position) -> Position:
        return pos_add(current_agent_position, self.agent_delta)

    def is_applicable(self, agent_index: int,  state: h_state.HospitalState) -> bool:
        current_agent_position, _ = state.agent_positions[agent_index]
        new_agent_position = self.calculate_positions(current_agent_position)
        return state.free_at(new_agent_position)

    def result(self, agent_index: int, state: h_state.HospitalState):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        new_agent_position = self.calculate_positions(current_agent_position)
        state.agent_positions[agent_index] = (new_agent_position, agent_char)

    def conflicts(self, agent_index: int, state: h_state.HospitalState) -> tuple[list[Position], list[Position]]:
        current_agent_position, _ = state.agent_positions[agent_index]
        new_agent_position = self.calculate_positions(current_agent_position)
        # New agent position is a destination because it is unoccupied before the action and occupied after the action.
        destinations = [new_agent_position]
        # Since a Move action never moves a box, we can just return the empty value.
        boxes_moved = []
        return destinations, boxes_moved

    def __repr__(self):
        return self.name

# Add your Push and Pull classes here.. Hint: follow the Move class as a template. 

class PushAction:
    # Add PushAction here.. 
    def __init__(self, agent_direction, box_direction):
        self.agent_delta = direction_deltas.get(agent_direction)
        self.box_delta = direction_deltas.get(box_direction)
        self.name = "Push(%s, %s)" % (agent_direction, box_direction)

    def calculate_agent_position(self, current_agent_position: Position) -> Position:
        return pos_add(current_agent_position, self.agent_delta)

    def calculate_box_position(self, current_box_position: Position) -> Position:
        return pos_add(current_box_position, self.box_delta)
    
    def is_applicable(self, agent_index: int, state: h_state.HospitalState) -> bool:

        current_agent_position, _ = state.agent_positions[agent_index]
        new_agent_position = self.calculate_agent_position(current_agent_position)

        # agent will move into where the box is currently
        # (hence agent's new position is the current box's position)
        
        current_box_position = [-1, -1]
        for box_pos in state.box_positions: 
            if box_pos[1]:
                current_box_position = box_pos[0][0] # corresponding box index to agent index?
                
        # old code: current_box_position = new_agent_position
        new_box_position = self.calculate_box_position(current_box_position)  # maybe box and agent are in same cell, hence can't push???
        
        _, box_char = state.box_at(current_box_position)                        # to ask?? should we instead check if there is a box next to agent, instead of when it's actually in the same cell?
        _, agent_char = state.agent_at(current_agent_position)                  # new...? todo: print coordinates!
        # print("box_char tuple", box_char)
        # print("agent_char tuple", agent_char)


        print("Is_applicable Box is at ", current_box_position)
        print("Is_applicable Agent is at ", current_agent_position,"\n")
        print("Box char: ", box_char)
        
        return state.free_at(new_box_position) and (state.level.colors[box_char] == state.level.colors[agent_char]) # and box_char

    def result(self, agent_index: int, state: h_state.HospitalState):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        new_agent_position = self.calculate_agent_position(current_agent_position)
        state.agent_positions[agent_index] = (new_agent_position, agent_char)
        print("New Agent Position in result: ", new_agent_position)
        
        current_box_position = new_agent_position
        box_index, box_char = state.box_at(current_box_position) 
        
        new_box_position = self.calculate_box_position(current_box_position)
        state.box_positions[box_index] = (new_box_position, box_char)
        print("New Box position in result: ", new_box_position)

    def conflicts(self, agent_index: int, state: h_state.HospitalState) -> tuple[list[Position], list[Position]]:
        current_agent_position, _ = state.agent_positions[agent_index]
        new_agent_position = self.calculate_agent_position(current_agent_position)

        current_box_position = new_agent_position
        new_box_position = self.calculate_box_position(current_box_position)
        
        # Destination contains all newly occupied cells
        destinations = [new_agent_position, new_box_position]
        print("Destinations: ",destinations)
        # boxes_moved contains the current location of the box because 2 agents cannot try to pull the same box at the same time
        boxes_moved = [current_box_position]
        print("Boxes_moved: ",boxes_moved)
        return destinations, boxes_moved
        
    def __repr__(self):
        return self.name


# class PullAction:
#     # Add PullAction.. 
#     def __init__(self, agent_direction, box_direction):
#         self.agent_delta = direction_deltas.get(agent_direction)
#         self.box_delta = direction_deltas.get(box_direction)
#         self.name = "Pull(%s, %s)" % (agent_direction, box_direction)

    # def calculate_agent_position(self, current_agent_position: Position) -> Position:
    #     return pos_add(current_agent_position, self.agent_delta)

    # def calculate_box_position(self, current_box_position: Position) -> Position:
    #     return pos_add(current_box_position, self.box_delta)

#     def is_applicable(self, agent_index: int,  state: h_state.HospitalState) -> bool:
#         current_agent_position, _ = state.agent_positions[agent_index]
#         new_agent_position = self.calculate_positions(current_agent_position)
#         return state.free_at(new_agent_position)

#     def result(self, agent_index: int, state: h_state.HospitalState):
#         current_agent_position, agent_char = state.agent_positions[agent_index]
#         new_agent_position = self.calculate_positions(current_agent_position)
#         state.agent_positions[agent_index] = (new_agent_position, agent_char)

#     def conflicts(self, agent_index: int, state: h_state.HospitalState) -> tuple[list[Position], list[Position]]:
#         current_agent_position, _ = state.agent_positions[agent_index]
#         new_agent_position = self.calculate_positions(current_agent_position)
#         # New agent position is a destination because it is unoccupied before the action and occupied after the action.
#         destinations = [new_agent_position]
#         # Since a Move action never moves a box, we can just return the empty value.
#         boxes_moved = []
#         return destinations, boxes_moved

#     def __repr__(self):
#         return self.name


AnyAction = Union[NoOpAction, MoveAction, PushAction] # Only for type hinting


# An action library for the multi agent pathfinding domain using the Move action you implemented

DEFAULT_MAPF_ACTION_LIBRARY = [
    NoOpAction(),
    MoveAction("N"),
    MoveAction("S"),
    MoveAction("E"),
    MoveAction("W"),
]


# An action library for the full hospital domain using the Push and Pull actions you implemented
DEFAULT_HOSPITAL_ACTION_LIBRARY = [
    NoOpAction(),
    MoveAction("N"),
    MoveAction("S"),
    MoveAction("E"),
    MoveAction("W"),

    # push
    PushAction("N", "N"),
    PushAction("N", "W"),
    PushAction("N", "E"),
    PushAction("S", "S"),
    PushAction("S", "W"),
    PushAction("S", "E"),
    PushAction("E", "E"),
    PushAction("E", "N"),
    PushAction("E", "S"),
    PushAction("W", "N"),
    PushAction("W", "S"),
    PushAction("W", "W")

    # pull
]



