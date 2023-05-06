from component import *

# test pipeline_simple
print("\n test pipeline_simple.\n")
input_cycle = [1,35,43,45,78,99]
test_component = pipeline_component_simple("tester", 0)
test_component.config(22, 22, 1, 1000)
for item in input_cycle:
	if test_component.check_available(item):
		output_cyc = test_component.input(item)
	else:
		output_cyc = test_component.input(test_component.get_next_available_cycle())
	print("input cycle: "+str(item)+", output_cyc:"+str(output_cyc)+"\n")
print(test_component.output_stat())

# test pipeline_detail
print("\n test pipeline_detail.\n")
input_cycle = [1,35,43,45,78,99]
stage_delay = [1,1,3,1,4,1,2,1]
stage_cost = [1,1,2,1,5,1,2,4]
test_component = pipeline_component_detail("tester", 0)
test_component.config(stage_delay, stage_cost, 1000)
for item in input_cycle:
	if test_component.check_available(item):
		output_cyc = test_component.input(item)
	else:
		output_cyc = test_component.input(test_component.get_next_available_cycle())
	print("input cycle: "+str(item)+", output_cyc:"+str(output_cyc)+"\n")
print(test_component.output_stat())

# test non_pipeline
print("\n test non_pipeline.\n")
input_cycle = [1,35,43,45,78,99]
test_component = non_pipeline_component("tester", 0)
test_component.config(22, 1000)
for item in input_cycle:
	if test_component.check_available(item):
		output_cyc = test_component.input(item)
	else:
		output_cyc = test_component.input(test_component.get_next_available_cycle())
	print("input cycle: "+str(test_component.get_next_available_cycle())+", output_cyc:"+str(output_cyc)+"\n")
print(test_component.output_stat())