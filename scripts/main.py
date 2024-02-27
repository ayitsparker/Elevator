import math


class Elevator:
	TRAVEL_TIME = 10

	def __init__(self, starting_floor, num_floors=100):
		self._current_floor = starting_floor
		self._number_of_floors = num_floors

	@property
	def number_of_floors(self):
		return self._number_of_floors
	
	def _validate_input(self, floors):
		"""
		Expect comma seperated list of floors
		Invalid floors will be ignored, but logged
		"""

		if not isinstance(floors, str):
			print(f'Expected input to be of type str, but got {type(floors)}')
			return []

		ret_list = []
		for floor in floors.split(','):
			try:
				floor_int = int(floor)
				if 0 < floor_int <= self.number_of_floors:
					ret_list.append(floor_int)
				else:
					print(f'Floor number {floor_int} not in valid range of [1-{self.number_of_floors}]...Ignoring')
			except ValueError as ex:
				print(f'Error parsing input: {ex}')
		return ret_list

	def _goto_floor(self, target_floor):
		print(f'Traveling to floor {target_floor}, ')

	def run(self):
		travel_time = 0
		while True:
			floors = input('Enter floors to visit: ')
			valid_floor_list = self._validate_input(floors)

			for target_floor in valid_floor_list:
				self._goto_floor(target_floor)



def main():
	ev = Elevator(1)
	ev.run()

if __name__ == '__main__':
	main()