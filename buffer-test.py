from buffer import *
from misc import *

test_component = buffer_component("test-buffer", 1)
test_component.config(16, 3, 2, 2)
test_component.access(1,1,1,MemAccessType.Read)