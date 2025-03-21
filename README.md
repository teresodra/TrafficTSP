# TrafficTSP

## Overview
This project aims to showcase various of my skills, such as Python, SQL, CI/CD, Mixed-Integer Linear Programming, and Machine Learning models. It also demonstrates creativity to formulate problems, propose solutions, and compare them.

## Project Description
TrafficTSP is a simulation and optimisation project for **Travelling Salesman Problems (TSPs)** in which the weights (travel times) between nodes are not constant but rather depend on the time of day, simulating traffic.

## Features
- **TSP Instance Generator**: Create time-dependent graphs for routing problems.
- **Optimisation Strategies**:
  - Greedy heuristic approach.
  - Discretisation-based solutions.
- **Evaluation Tools**: Compare different strategies on time to get a solution and performance.
- **Machine Learning Integration (Possibly)**:
  - Optimise number of bins in discretisation for better performance.

## Technologies Used
- **Programming Language**: Python
- **Optimisation**: OR-TOOLS to solve Mixed-Integer Linear Programming (MILP)
- **Database**: SQL
- **CI/CD & Testing**: GitHub Actions, Pytest
- **Machine Learning**: Scikit-learn, TensorFlow/PyTorch

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/TrafficTSP.git
   cd TrafficTSP
   ```
2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Linux, use venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To generate a random TD-TSP problem with 10 nodes and compare the different approaches:
```bash
python main.py --nodes 10
```

## Known limitations
- Route costs establishes after a long time (after exceeding upper value of mean_range in create_random_weight_function)
- create_graphs is not guaranteed to generate graphs that satisfy the triangular inequality
- The greedy approach only is guaranteed to work for connected graphs