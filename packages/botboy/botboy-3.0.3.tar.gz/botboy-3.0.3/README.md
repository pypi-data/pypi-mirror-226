# BotBoy
Multithreading &amp; processing worker that executes functions and prints the
result

## Installation
```
pip install botboy
```

## Usage
### Instantiation
```
from botboy.core import BotBoy

name = 'Adder' # Name of thread/process
task = lambda x, y: x + y # Function to run on separate thread/process
params = [1, 2] # Task arguments
verbose = True # Logging

bot = BotBoy(name=name, task=task, params=params, verbose=verbose)

# You may also instantiate with the setup() method
name = 'Subtracter'
task = lambda x, y: x - y
params = [2, 3]

bot = BotBoy()
bot.setup(name=name, task=task, params=params)

# Print params
print(bot)

# Turn logging on
bot.verbose()

# Turn logging off
bot.silent()

```

### Execute task
```
result = bot.execute()

# Wait for execution to finish
result = bot.execute(wait=True)

# Execute on separate process
result = bot.execute(is_process=True) # Wait does not work for process
```

### Repeat Task
```
# Will repeat the assigned task amount of times with an interval inbetween
results = bot.repeat(amt=2, interval=2, wait=True, is_process=False)
```

### Getters
```
print(bot.name())
print(bot.task())
print(bot.params())
print(bot.result()) # Result will be None unless task was executed

# Or print all params together
print(bot)
```

### Store result in a file or provide a path
```
# Store result in a file at current directory
bot.save('test.txt')

# Store result at path
import os
bot.save(os.getcwd() + '/test2.txt')
```

### Run multiple tasks with Sequencer
```
from botboy.core import BotBoy, Sequencer

tasks = [lambda x, y: x + y, lambda x, y: x - y, lambda x, y: x * y]
params = [[1, 2], [3, 4], [5, 6]]

# Create list of BotBoys
bots = Sequencer.pack(tasks=tasks, params=params, verbose=True)

# Instantiate
seq = Sequencer(bots)

# Retrieve results
# Default is false (runs tasks on threads)
# Set to true to run each task on process
results = seq(is_process=False)
```

## Test
Runs the tests on the BotBoy Module
```
make test-init: Test Initialization
make test-wrapper: Test _wrapper method
make test-client: Test client methods
make test-sequencer: Test Sequencer
```
