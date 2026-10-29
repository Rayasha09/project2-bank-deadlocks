# Operating Systems Project 2 — Bank Deadlocks

## About the Project

This project explores **deadlocks in operating systems** using examples involving bank transfers, resource allocation, process waiting, and synchronization between threads.

The goal is to understand how deadlocks occur, how to detect them, and how to prevent threads from waiting indefinitely.

## Project Tasks

### Level A — Basic

- Demonstrate and fix a deadlock between two bank-transfer threads.
- Explain the necessary conditions for deadlock.
- Check system states using the Banker's algorithm.

### Level B — Intermediate

- Process resource requests and determine whether they can be granted safely.
- Build a wait-for graph from a resource acquisition log.
- Detect cycles and identify processes that remain blocked.

### Level C — Advanced

- Implement `TrackedLock` to track resource ownership and waiting threads.
- Detect deadlocks using a wait-for graph.
- Solve the Dining Philosophers problem using three approaches:
  - Naive approach
  - Ordered resource acquisition
  - Waiter semaphore

## Repository Structure

```text
project2-bank-deadlocks/
├── README.md
├── Aigul_Level_C/
│   ├── philosophers.py
│   ├── tracked_lock.py
│   ├── transfer_tracked.py
│   ├── README_C.md
│   ├── result_c1.txt
│   ├── result_naive.txt
│   ├── result_ordered.txt
│   └── result_waiter.txt
├── Level_A/    # To be added
└── Level_B/    # To be added
```

The Level A and Level B directories will be updated when their implementations are added. The structure above reflects the currently planned organization; verify the actual files in the repository before submission.

## Requirements

- Python 3
- Ubuntu Linux environment, as required for the project submission

Check that Python is installed:

```bash
python3 --version
```

## Running the Project

Open a terminal and navigate to the relevant directory.

For example, to run the Level C scripts:

```bash
cd Aigul_Level_C
python3 philosophers.py
```

The exact commands for the other scripts should be confirmed from their source code and `README_C.md`. Some scripts may require specific arguments or execution order.

## Testing and Results

The repository includes text files intended to store execution results for the Level C implementations:

- `result_naive.txt`
- `result_ordered.txt`
- `result_waiter.txt`
- `result_c1.txt`

Actual results and conclusions should be documented after the scripts have been executed and verified.

## Team

**Course:** Operating Systems  
**Project:** Project 2 — Bank Deadlocks

Team members and their responsibilities will be documented here.

## Conclusion

This project demonstrates important operating-system concepts related to concurrency, resource allocation, synchronization, and deadlock detection. Testing the different approaches helps explain how resource-management strategies affect the safety and progress of concurrent programs.
