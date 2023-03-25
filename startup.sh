#!/bin/bash

# Get the number of CPU cores available on the server
num_cpus=$(nproc)

# Calculate the number of workers to use (2 per CPU core)
num_workers=$((2 * $num_cpus))

# Start the FastAPI app with the specified number of workers
uvicorn myapp:app --workers $num_workers
