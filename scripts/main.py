import math
import sys
import select
from threading import Timer # Import only used with stop at floor flag. 
                            # Could make more sense as an instance local import.

"""
Basic Elevator class implementation
NOTE: This leaves out a lot of "real" functionality that would exist in a more fleshed out system
Of note, a continuation would have more structure. Additions such as a button class as an attr of the elevator to handle input validation,
A building class that stores more static info such has number of floors, etc. The input loop would obviously be more sophisticated
Another todo is adding argparse module to make num floors and stop at floor params be dynamic to runtime
Can also add dict or enum mapping to allow for common variations of floors. i.e. 'G' for Ground(lowest maybe?) or 'B' for Basement(floor -1?)
Assumption: That floors are visited in order they were entered. Project I/O guidelines imply this was the expected output so I stuck to that. 
I'd note a future feature would be to limit travel direction and travel relative to current floor. i.e. every iteration is next_floor = closest_floor(current_floor, floors_to_visit).
"""
class Elevator:
    TRAVEL_TIME = 10

    def __init__(self, starting_floor: int, num_floors: int = 100, stop_at_floor: bool = False):
        """
        Init function.
        @param starting_floor: starting floor of the elevator
        @param num_floors: total number of floors building has
        @stop_at_floor: optional param to stop at floor and allow more buttons to be pressed
        """
        self._current_floor = starting_floor
        self._number_of_floors = num_floors
        self._stop_at_floor = stop_at_floor

    @property
    def number_of_floors(self) -> int:
        return self._number_of_floors
            
    def _validate_input(self, floors: int) -> list:
        """
        Expect comma seperated list of floors
        Invalid floors will be ignored, but logged
        @param: floors: list of floors
        """

        if not isinstance(floors, str):
            print(f'Expected input to be of type str, but got {type(floors)}')
            return []

        ret_list = []
        for floor in floors.split(','):
            try:
                floor_int = int(floor)
                # Technically this does assume floor numbers have to be ints that are positives(no 'G' or floor -5)
                if 0 < floor_int <= self.number_of_floors:
                    ret_list.append(floor_int)
                else:
                    print(f'Floor number {floor_int} not in valid range of [1-{self.number_of_floors}]...Ignoring')
            except ValueError as ex:
                print(f'Error parsing input: {ex}')
        return ret_list

    def _goto_floor(self, target_floor: int) -> list | None:
        """
        Go to target floor.
        @param target_floor: target floor to go to
        """
        # Assumes valid input done in _validate_input
        # Scaled system *shouldn't* need validation here since that would be done through button interface.
        # Function is only really useful with stop_at_floors attr. 
        # Otherwise calcs are just len(floor_list) * TRAVEL_TIME
        def input_with_timeout(prompt):
            sys.stdout.write(prompt)
            sys.stdout.flush()
            ready, _, _ = select.select([sys.stdin], [],[], 10)
            if ready:
                return sys.stdin.readline().rstrip('\n') # expect stdin to be line-buffered
            return ""

        print(f'Traveling to floor {target_floor}....Arrived')
        if self._stop_at_floor:
            new_floors = input_with_timeout('Enter next floors: ') # Assumes as soon as input given doors will close
            print('Doors closing.....')
            return self._validate_input(new_floors)

    def run(self):
        while True:
            travel_time = 0
            floors = input('Enter floors to visit: ')
            valid_floor_list = self._validate_input(floors)
            if not valid_floor_list:
                print('No valid floors selected!')
                continue

            for target_floor in valid_floor_list:
                print(valid_floor_list)
                new_input = self._goto_floor(target_floor)

                if new_input:
                    # Note: this is safe in python
                    valid_floor_list.extend(new_input)
                travel_time += Elevator.TRAVEL_TIME
            print(f'Trip complete. Total travel time was {travel_time} seconds. Visited floors: {", ".join(map(str, valid_floor_list))}')

def main():
    ev = Elevator(1)
    ev.run()

if __name__ == '__main__':
    main()
