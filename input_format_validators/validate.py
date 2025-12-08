#!/usr/bin/env python3

# This is an input validator for building inspection problem, written in Python 3.

import sys
import re

# First line: number of buildings and number to inspect
first_line = sys.stdin.readline()
print(repr(first_line))
assert re.match('^[1-9][0-9]* [1-9][0-9]*\n$', first_line)
parts = first_line.strip().split()
assert len(parts) == 2, "First line must have exactly two integers"
num_buildings = int(parts[0])
num_to_inspect = int(parts[1])
assert 1 <= num_buildings < 1000
assert 1 <= num_to_inspect < 1000

# Second line: sequence of building IDs to inspect
inspect_line = sys.stdin.readline()
print(repr(inspect_line))
inspect_parts = inspect_line.strip().split()
assert len(inspect_parts) == num_to_inspect, \
    f"Expected {num_to_inspect} building IDs to inspect, but got {len(inspect_parts)}"
inspect_ids = []
for building_id in inspect_parts:
    assert re.match('^[1-9][0-9]*$', building_id)
    bid = int(building_id)
    assert 1 <= bid < 1000
    inspect_ids.append(bid)

# Verify uniqueness of building IDs to inspect
assert len(inspect_ids) == len(set(inspect_ids)), "Building IDs to inspect must be distinct"

# Following lines: one for each building
building_ids = set()
for _ in range(num_buildings):
    building_line = sys.stdin.readline()
    print(repr(building_line))
    parts = building_line.strip().split()
    assert len(parts) >= 2, "Each building line must have at least ID and connection count"
    
    # Parse building ID
    building_id = parts[0]
    assert re.match('^[1-9][0-9]*$', building_id)
    building_id_int = int(building_id)
    assert 1 <= building_id_int < 1000
    
    # Verify building ID uniqueness
    assert building_id_int not in building_ids, f"Duplicate building ID: {building_id_int}"
    building_ids.add(building_id_int)
    
    # Parse number of connections
    num_connections = int(parts[1])
    assert 0 <= num_connections < 999
    
    # Verify we have the right number of connected building IDs
    assert len(parts) == num_connections + 2, \
        f"Building {building_id_int} claims {num_connections} connections but has {len(parts) - 2}"
    
    # Validate each connected building ID and verify uniqueness
    connected_ids = set()
    for i in range(2, len(parts)):
        connected_id = parts[i]
        assert re.match('^[1-9][0-9]*$', connected_id)
        connected_id_int = int(connected_id)
        assert 1 <= connected_id_int < 1000
        
        # Verify distinctness of connected building IDs
        assert connected_id_int not in connected_ids, \
            f"Duplicate connection {connected_id_int} for building {building_id_int}"
        connected_ids.add(connected_id_int)

# ensure no extra input
assert sys.stdin.readline() == ''

# if we get here, all is well; use exit code 42.
sys.exit(42)

