# System defaults for comparison
default_max_user_instances = 128
default_max_queued_events = 16384
default_max_user_watches = 8192

# Total available memory in KB for the inotify settings
available_memory_kb = 2 * 1024 * 1024  # 2 GB in KB

# Calculate the total "weight" based on default values to keep the same ratio
total_weight = default_max_user_watches + default_max_user_watches + default_max_user_watches

# Calculate how much memory each "unit" represents
memory_per_unit = available_memory_kb / total_weight

# Allocate memory based on the original ratio
print("fs.inotify.max_user_watches =", int(memory_per_unit * default_max_user_watches))
print("fs.inotify.max_user_instances =", int(memory_per_unit * default_max_user_instances))
print("fs.inotify.max_queued_events =", int(memory_per_unit * default_max_queued_events))