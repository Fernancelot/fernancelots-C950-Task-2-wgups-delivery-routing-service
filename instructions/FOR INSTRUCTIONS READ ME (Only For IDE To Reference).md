### Project Instructions and Formatting

This document provides a clear structure using Markdown formatting for improved readability and compatibility with IDEs and GitHub Copilot.

---
```
This is a collection of a lot of sources that I wanted to be all in one place and one document for instances where I needed to reference only one file for a question but wanted it to still consider the entirety of the information I had collected. It's mostly sloppy, unsorted, out of order, just 'whatever came next' to paste into it, and is what it is. This file isn't part of the project files and not even really part of the set of instruction files so, I wouldn't advise using it in practice, maybe for reference only if at all```
```

### Instructions for Simplified Task Completion

This project consists of two primary parts:

1. **Planning Task (Task 1)**
2. **Implementation Step (Task 2)**

#### Recommendations:

- **IDE:** Use PyCharm Community Edition for Task 2. It simplifies setup and debugging.
- **Implementation Guide:** Follow the provided implementation guide available in supplemental resources.

#### Key Steps:

1. **Data Import:**
    - Instead of creating CSV files, manually copy data into the project. CSV files are optional.
2. **Truck Loading:**
    - Manually load trucks using package IDs and ensure special instructions are met.
3. **Delivery Algorithm:**
    - Use the Nearest Neighbor Algorithm to optimize delivery routes.
4. **User Interaction:**
    - Implement a simple `while` loop for user commands (e.g., package lookup, route optimization).

---

### Object-Oriented Approach for Simplification

#### Steps:

1. **Data Preparation:** Convert Excel data files into clean CSV files.
2. **Class Creation:**
    - **Truck Class:** Define attributes and methods for trucks.
    - **Package Class:** Define attributes and include a status determination method.
3. **Hash Map Creation:** Implement a custom hash table for package data.
4. **Main File:** Centralize logic in `main.py` for clarity and structure.

#### Key Notes:

- **Algorithm Efficiency:** Use the Nearest Neighbor Algorithm for delivery optimization.
- **Command Line Interface:** Provide a simple interface for user interaction.

---

### Key Rubric Requirements

#### Scenario

Optimize delivery for WGUPS using three trucks and two drivers for daily local deliveries (DLD). The solution must:

- Deliver all packages on time.
- Keep total mileage under 140 miles.
- Use an intuitive interface for package status tracking.

#### Assumptions

- Trucks move at 18 mph and carry a maximum of 16 packages.
- Special notes for some packages must be followed.
- Wrong address for package #9 is corrected at 10:20 AM.

#### Requirements

- **Algorithm:** Self-adjusting, e.g., Nearest Neighbor.
- **Data Structures:** Use a custom hash table for package information.
- **Interface:** Display package status and total mileage.

---

### Task Breakdown

#### Part A: Algorithm Selection
- Identify and explain the chosen self-adjusting algorithm.

#### Part B: Program Overview
1. Explain logic using pseudocode.
2. Describe development environment.
3. Provide space-time complexity in Big-O notation.
4. Discuss scalability and maintainability.

#### Part C: Original Code
- Include detailed comments for process flow and logic.
- Ensure the code is error-free and runs successfully.

#### Part D: Data Structure
- Implement a self-adjusting hash table for package data.

#### Part E: Hash Table Implementation
- Create an insertion function for package information.

#### Part F: Lookup Function
- Implement a function to retrieve package information by ID.

#### Part G: User Interface
- Provide an intuitive CLI to check package status and mileage.

#### Part H: Verification
- Include screenshots showing:
    - Status of all packages at specified times.
    - Successful completion of the program with total mileage.

#### Part I: Justification
1. Highlight strengths of the algorithm.
2. Verify all requirements are met.
3. Identify alternative algorithms.

#### Part K: Data Structure Justification
1. Explain the efficiency and scalability of the hash table.
2. Compare with alternative data structures.

---

### Additional Resources

- GitHub Example Project: [FallicoFunctions C950 Project](https://github.com/FallicoFunctions/Python-Mail-Delivery-Service-Algorithm_WGU-C950)
- Python Version: 3.13.1
- IDE: PyCharm Professional 2024.3.1.1
