import os

# import psutil
import resource

# limit max memory usage
# available_memory = psutil.virtual_memory().available
available_memory = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
_, hard_limit = resource.getrlimit(resource.RLIMIT_DATA)
# if hard_limit == resource.RLIM_INFINITY:
#     hard_limit = available_memory
# Ensure that the new limit does not exceed the hard limit
limit = min(int(available_memory * 0.9), hard_limit)
resource.setrlimit(resource.RLIMIT_DATA, (limit, limit))
