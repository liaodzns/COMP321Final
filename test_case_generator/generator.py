import random
import os
import subprocess

max_buildings = 500         

def generate_test_case(filename, location):
    output_dir = os.path.join("data", location)
    os.makedirs(output_dir, exist_ok=True)

    n = random.randint(3, max_buildings) 
    buildings = list(range(1, n+1))
    
    inspect_count = random.randint(1, n)
    to_inspect = random.sample(buildings, k=inspect_count)
    
    adjacency = {b: set() for b in buildings}
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < 0.006:  # Creating a low percentage change of being connected so that buildings aren't always in the same sector.
                adjacency[buildings[i]].add(buildings[j])
                adjacency[buildings[j]].add(buildings[i])
    
    input_path = os.path.join(output_dir, filename + ".in")
    with open(input_path, "w") as f:
        f.write(f"{n} {inspect_count}\n")
        f.write(" ".join(map(str, to_inspect)) + "\n")
        for b in buildings:
            adj_list = list(adjacency[b])
            f.write(f"{b} {len(adj_list)} " + " ".join(map(str, adj_list)) + "\n")
    
    solution_path = os.path.join("submissions", "accepted", "solution.py")

    with open(input_path, "r") as infile:
        result = subprocess.run(
            ["py", solution_path],
            stdin=infile,   
            text=True,
            capture_output=True
        )
    
    output_path = os.path.join(output_dir, filename + ".ans")
    with open(output_path, "w") as f:
        f.write(result.stdout.strip() + "\n")

def edge_case_only_one_sector(filename, location):
    output_dir = os.path.join("data", location)
    os.makedirs(output_dir, exist_ok=True)

    n = random.randint(3, 50) 
    buildings = list(range(1, n+1))
    
    inspect_count = random.randint(1, n)
    to_inspect = random.sample(buildings, k=inspect_count) 

    adjacency = {b: set(buildings) - {b} for b in buildings}

    input_path = os.path.join(output_dir, filename + ".in")
    with open(input_path, "w") as f:
        f.write(f"{n} {inspect_count}\n")
        f.write(" ".join(map(str, to_inspect)) + "\n")
        for b in buildings:
            adj_list = list(adjacency[b])
            f.write(f"{b} {len(adj_list)} " + " ".join(map(str, adj_list)) + "\n")

    output_path = os.path.join(output_dir, filename + ".ans")
    with open(output_path, "w") as f:
        f.write("0\n")

def edge_case_all_sectors(filename, location):
    output_dir = os.path.join("data", location)
    os.makedirs(output_dir, exist_ok=True)

    n = random.randint(3, max_buildings) 
    buildings = list(range(1, n+1))
    
    inspect_count = random.randint(1, n)
    to_inspect = random.sample(buildings, k=inspect_count) 

    adjacency = {b: set() for b in buildings}

    input_path = os.path.join(output_dir, filename + ".in")
    with open(input_path, "w") as f:
        f.write(f"{n} {inspect_count}\n")
        f.write(" ".join(map(str, to_inspect)) + "\n")
        for b in buildings:
            adj_list = list(adjacency[b])
            f.write(f"{b} {len(adj_list)} " + " ".join(map(str, adj_list)) + "\n")

    output_path = os.path.join(output_dir, filename + ".ans")
    with open(output_path, "w") as f:
        drives = max(len(to_inspect) - 1, 0)
        f.write(f"{drives}\n")

for i in range(1, 4):
    generate_test_case(f"test{i}", "sample")

for i in range(4, 25):
    generate_test_case(f"test{i}", "secret")

edge_case_only_one_sector("test25", "secret")
edge_case_all_sectors("test26", "secret")