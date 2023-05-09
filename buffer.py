
from misc import *

class buffer_component:
	# configuration
	capacity = 0
	array_delay = 0
	read_port_count = 0
	write_port_count = 0
	upper_component = None

	# internal
	used_capacity = 0
	used_port = [0, 0] # format: [Used Read Port, Used Write Port]
	content = [] # format: [[data_block_id, size, access_cycle],...]
	port_next_available_cycle = [[],[]] # format: [[next available cycle for each read port], [next available cycle for each write port]]
	array_next_available_cycle = 0

	# statistic
	access_count = 0
	hit_count = 0
	miss_count = 0
	eviction_count = 0
	utilization = 0
	eviction_data_size = 0

	# misc
	name = None
	component_id = 0
	
	def __init__(self, name, component_id):
		self.name = name
		self.component_id = component_id

	def config(self, capacity, array_delay, read_port_count, write_port_count):
		self.capacity = capacity
		self.array_delay = array_delay
		self.read_port_count = read_port_count
		self.write_port_count = write_port_count
		for idx in range(0, read_port_count):
			self.port_next_available_cycle[MemAccessType.Read.value].append(0)
		for idx in range(0, write_port_count):
			self.port_next_available_cycle[MemAccessType.Write.value].append(0)


	def set_upper_component(self, upper_component):
		self.upper_component = upper_component

	def _check_hit(self, data_block_id):
		for idx in range(0, len(self.content)):
			if self.content[idx][0] == data_block_id:
				return idx
		return -1

	def _eviction(self, evict_idx, new_datablock_id, data_block_size, cur_cycle):
		self.used_capacity = self.used_capacity - self.content[evict_idx][1] + data_block_size
		self.eviction_data_size += self.content[evict_idx][1]
		self.content.remove(evict_idx)
		self._add_data(data_block_id, data_block_size, cur_cycle)


	def _get_evict_idx(self, data_block_size):
		item_idx = -1
		min_cycle = 0
		for idx in range(0, len(self.content)):
			if self.content[idx][1] >= data_block_size:
				if min_cycle > 0 - self.content[idx][2]:
					min_cycle = 0 - self.content[idx][2]
					item_idx = idx
		return item_idx

	def _add_data(self, data_block_id, data_block_size, cur_cycle):
		self.content.append([data_block_id, data_block_size, cur_cycle])


	def get_next_available_cycle(self, access_type):
		return min(self.port_next_available_cycle[access_type.value])



	def access(self, data_block_id, data_block_size, cur_cycle, access_type):
		assert(access_type == MemAccessType.Read or access_type == MemAccessType.Write)
		assert(data_block_size <= self.capacity)
		access_delay = 1
		access_available_cycle = self.get_next_available_cycle(access_type)
		access_port_idx = self.port_next_available_cycle[access_type.value].index(access_available_cycle)
		if (cur_cycle + 1) >= self.array_next_available_cycle:
			access_delay += self.array_delay
			self.array_next_available_cycle = cur_cycle + 1 + self.array_delay
		else:
			access_delay += (self.array_next_available_cycle - cur_cycle - 1 + self.array_delay)
			self.array_next_available_cycle = self.array_next_available_cycle + self.array_delay
		hit_idx = self._check_hit(data_block_id)
		if hit_idx == -1: # miss
			self.miss_count += 1
			if self.upper_component != None:
				access_delay += self.upper_component.access(data_block_id, data_block_size, cur_cycle+access_delay, MemAccessType.Read) 
			if self.capacity - self.used_capacity < data_block_size: 
				evict_idx = self._get_evict_idx(data_block_size)
				assert(evict_idx > -1)
				self.eviction_count += 1
				self._eviction(evict_idx, data_block_id, data_block_size, cur_cycle+access_delay)
			else:
				self._add_data(data_block_id, data_block_size, cur_cycle+access_delay)
		else: # hit
			self.hit_count += 1
			self.content[hit_idx][2] = cur_cycle + access_delay
		self.port_next_available_cycle[access_type.value][access_port_idx] = cur_cycle + access_delay
		self.access_count += 1
		return access_delay

