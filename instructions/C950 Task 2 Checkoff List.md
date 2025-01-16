# C950 Task 2 - WGUPS Delivery Route Algorithm Checklist

## 1. File Structure and Organization

- **Create a new Python project in PyCharm**
- Establish the following Python files:
  - `main.py` – Contains the main logic and program flow
  - `truck.py` – Contains the Truck class
  - `package.py` – Contains the Package class
  - `hash_table.py` – Contains the hash table data structure
- Add the following data files to the project:
  - `WGUPS Package File.xlsx` – Package data
  - `WGUPS Distance Table.xlsx` – Distance matrix
  - `addresses.csv` – Address list
- **Documentation:**
  - `README.md` – Overview of the project, installation, and usage instructions
  - `task2_documentation.docx` – Comprehensive project documentation and explanation
- **Screenshot Folder:**
  - `screenshots/` – Contains required screenshots for submission

---

## 2. Implementation Steps (Code Development)

### A. Identify and Implement Algorithm
- Choose and document the algorithm (e.g., Nearest Neighbor)
- Write pseudocode explaining the algorithm’s logic
- Implement the delivery algorithm (truck delivery simulation)

### B. Code Development and Structure
- Create and populate the hash table with package data:
  - Define insertion and look-up methods for the hash table
- Develop the following classes:
  - **Truck Class** – Attributes: speed, mileage, current address, package list
  - **Package Class** – Attributes: ID, address, deadline, weight, status
- Write the main program logic:
  - Instantiate truck and package objects
  - Implement package loading based on constraints
  - Simulate delivery using the algorithm
- Develop a user interface (UI):
  - Allow the user to input a time and check package status
  - Display total mileage and delivery status

---

## 3. Testing and Verification

- Verify that the total mileage is under 140 miles
- Ensure all packages are delivered by the required deadlines
- Check algorithm performance with various data sets
- Implement error handling for missing or invalid data
- Debug and ensure the program runs without errors

---

## 4. User Interface (Console Interaction)

- Create a menu with the following options:
  1. Print all package statuses and total mileage
  2. Lookup single package status at a specific time
  3. Lookup all package statuses at a specific time
  4. Exit
- Ensure the program loops until the user exits
- Display delivery results, package statuses, and total mileage

---

## 5. Documentation and Reporting

- Write a project overview:
  - Describe the algorithm used
  - Explain space-time complexity (Big-O)
  - Discuss software scalability and efficiency
- Document the data structure (hash table):
  - Explain how it handles package data and retrieval
- List strengths and weaknesses of the algorithm
- Compare the chosen algorithm to two other algorithms
- Provide screenshots of the program running at the following times:
  - Between 8:35 a.m. and 9:25 a.m.
  - Between 9:35 a.m. and 10:25 a.m.
  - Between 12:03 p.m. and 1:12 p.m.
- Include screenshots of successful program execution showing:
  - Total mileage
  - Completion without errors

---

## 6. Final Checks (Rubric Alignment)

- Verify each rubric point is addressed:
  - Algorithm selection
  - Code explanation with comments
  - UI demonstration
  - Hash table implementation
- Provide clear instructions for evaluators on how to run the project

---

## File List for Submission

- `main.py` – Core program logic
- `truck.py` – Truck class definition
- `package.py` – Package class definition
- `hash_table.py` – Hash table implementation
- `packages.csv` – Package data
- `distance.csv` – Distance matrix
- `addresses.csv` – Address list
- `README.md` – Project overview and instructions
- `task2_documentation.docx` – Full project documentation
- `screenshots/` – Screenshots showing the program running and results

---

## Notes (Tasks to Complete Outside This Chat)

- Screenshots – Must be taken after running the program

