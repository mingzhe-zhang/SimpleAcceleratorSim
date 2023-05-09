class pipeline_component_simple:
	# configuration
	pipeline_stage_count = 0
	delay = 0
	output_per_cycle = 0
	frequency = 0

	# statistics
	utilization = 0
	input_count = 0
	#output_count = 0
	idle_cycle = 0
	busy_cycle = 0

	# internal variables
	next_available_cycle = 0

	# misc
	name = None
	component_id = 0

	def __init__(self, name, component_id):
		self.name = name
		self.component_id = component_id

	def config(self, stage_count, delay, cycle_per_output, frequency):
		self.pipeline_stage_count = stage_count
		self.delay = delay
		self.cycle_per_output = cycle_per_output
		self.frequency = frequency

	def input(self, cur_cycle):
		assert(cur_cycle >= self.next_available_cycle)
		if self.next_available_cycle - 1 + self.delay < cur_cycle:
			self.idle_cycle = self.idle_cycle + cur_cycle - (self.next_available_cycle - 1 + self.delay)
			self.busy_cycle = self.busy_cycle + self.delay
		else:
			self.busy_cycle = self.busy_cycle + (cur_cycle - self.next_available_cycle + 1)
		self.next_available_cycle = cur_cycle + 1
		self.input_count = self.input_count + 1
		return (cur_cycle + self.delay)

	def get_next_available_cycle(self):
		return self.next_available_cycle

	def check_available(self, cur_cycle):
		return (cur_cycle >= self.next_available_cycle)

	def output_stat(self):
		self.utilization = self.busy_cycle / (self.busy_cycle + self.idle_cycle)
		return [self.utilization, self.input_count, self.idle_cycle, self.busy_cycle]

class pipeline_component_detail:
	# configuration
	pipeline_stage_delay = []
	pipeline_stage_cost = []
	pipeline_stage_count = 0
	delay = 0
	cycle_per_output = 0
	frequency = 0

	# statistics
	utilization = 0
	input_count = 0
	#output_count = 0
	idle_cycle = []
	busy_cycle = []

	# internal variables
	next_available_cycle = []
	last_cycle = 0

	# misc
	name = None
	component_id = 0

	def __init__(self, name, component_id):
		self.name = name
		self.component_id = component_id

	def config(self, stage_delay, stage_cost, frequency):
		assert(len(stage_delay) == len(stage_cost))
		self.pipeline_stage_count = len(stage_delay)
		self.delay = sum(stage_delay)
		self.output_per_cycle = max(stage_delay)
		self.frequency = frequency
		for idx in range(0, self.pipeline_stage_count):
			self.pipeline_stage_delay.append(stage_delay[idx])
			self.pipeline_stage_cost.append(stage_cost[idx])
			self.idle_cycle.append(0)
			self.busy_cycle.append(0)
			self.next_available_cycle.append(0)

	def input(self, cur_cycle):
		assert(cur_cycle >= self.next_available_cycle[0])
		ptr_cycle = cur_cycle
		for idx in range(0, self.pipeline_stage_count):
			if ptr_cycle >= self.next_available_cycle[idx]:
				self.idle_cycle[idx] = self.idle_cycle[idx] + (ptr_cycle - self.next_available_cycle[idx])
				self.busy_cycle[idx] = self.busy_cycle[idx] + self.pipeline_stage_delay[idx]
				ptr_cycle = ptr_cycle + self.pipeline_stage_delay[idx]
				self.next_available_cycle[idx] = ptr_cycle
			else:
				self.busy_cycle[idx] = self.busy_cycle[idx] + self.pipeline_stage_delay[idx]
				ptr_cycle = self.next_available_cycle[idx] + self.pipeline_stage_delay[idx]
				self.next_available_cycle[idx] = self.next_available_cycle[idx] + self.pipeline_stage_delay[idx]
		self.last_cycle = ptr_cycle
		self.input_count = self.input_count + 1
		return ptr_cycle

	def get_next_available_cycle(self):
		return self.next_available_cycle[0]

	def check_available(self, cur_cycle):
		return (cur_cycle >= self.next_available_cycle[0])

	def output_utilization(self, total_cycles):
		sum_busy = 0
		for idx in range(0, self.pipeline_stage_count):
			sum_busy = sum_busy + self.busy_cycle[idx] * self.pipeline_stage_cost[idx]
		return (sum_busy / (sum(self.pipeline_stage_cost) * total_cycles))

	def output_stat(self):
		self.utilization = self.output_utilization(self.last_cycle)
		return [self.utilization, self.input_count, self.idle_cycle, self.busy_cycle]

class non_pipeline_component:
	# configuration
	delay = 0
	frequency = 0

	# statistics
	utilization = 0
	input_count = 0
	#output_count = 0
	idle_cycle = 0
	busy_cycle = 0

	# internal variables
	next_available_cycle = 0

	# misc
	name = None
	component_id = 0

	def __init__(self, name, component_id):
		self.name = name
		self.component_id = component_id

	def config(self, delay, frequency):
		self.delay = delay
		self.frequency = frequency

	def input(self, cur_cycle):
		assert(cur_cycle >= self.next_available_cycle)
		self.idle_cycle = self.idle_cycle + cur_cycle - self.next_available_cycle
		self.busy_cycle = self.busy_cycle + self.delay
		self.next_available_cycle = cur_cycle + self.delay
		self.input_count = self.input_count + 1
		return (self.next_available_cycle - 1)

	def get_next_available_cycle(self):
		return self.next_available_cycle

	def check_available(self, cur_cycle):
		return (cur_cycle >= self.next_available_cycle)

	def output_stat(self):
		self.utilization = self.busy_cycle / (self.busy_cycle + self.idle_cycle)
		return [self.utilization, self.input_count, self.idle_cycle, self.busy_cycle]

