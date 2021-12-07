import re

input = open("input.txt", "r")

# lanturn fish class
class Fish:
    # Create the fish
    def __init__(self, counter):
        self.counter = counter

    # Create a fish with a counter at 8
    def new_spawn():
        return Fish(8)
    
    # Ages the fish a day, decreasing there counter
    def age(self):
        self.counter -= 1
    
    # Checks if the fish should spawn more
    def should_spawn(self):
        return self.counter < 0

    # Returns a new fish and resets the counter
    def spawn(self):
        # Reset the counter to 6
        self.counter = 6
        return Fish.new_spawn()

# Split up the list into counter string and convert them to ints
counters = list(map(lambda x: int(x),
    re.split(r",", input.read())))

# From each counter create a fish
fishes = list(map(lambda x: Fish(x),
    counters))

# For 80 days
for i in range(80):
    new_fishes = []
    for fish in fishes:
        # Age the fish
        fish.age()
        # Check if the fish should spawn
        if fish.should_spawn():
            # spawn the new fish and add it to new fishes
            new_fishes.append(fish.spawn())

    # Add all the fishes in new fishes to fishes
    for fish in new_fishes:
        fishes.append(fish)

# Print the number of fishes
print(len(fishes))
