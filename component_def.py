class pipeline_component:
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
	component_name = 0

	def __init__(self, name, component_id):
		self.name = name
		self.component_id = component_id

	def config(self, stage_count, delay, output_per_cycle, frequency):
		self.pipeline_stage_count = stage_count
		self.delay = delay
		self.output_per_cycle = output_per_cycle
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

	def output_stat(self):
		self.utilization = self.busy_cycle / (self.busy_cycle + self.idle_cycle)
		return [self.utilization, self.input_count, self.idle_cycle, self.busy_cycle]

# test
input_cycle = [1,15,23,45,46,78]
test_component = pipeline_component("tester", 0)
test_component.config(22, 22, 1, 1000)
for item in input_cycle:
	output_cyc = test_component.input(item)
	print("input cycle: "+str(item)+", output_cyc:"+str(output_cyc)+"\n")
print(test_component.output_stat())



