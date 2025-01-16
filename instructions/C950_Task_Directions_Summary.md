# C950 Task Directions and Rubric Summary

## Alternative Task Directions and FAQ

### Scenario
The Western Governors University Parcel Service (WGUPS) needs to determine the best route and delivery distribution for their Daily Local Deliveries.  
- **Route Details:**  
  - Salt Lake City DLD route  
  - 2 trucks, 2 drivers  
  - Average of 40 packages daily, each with specific criteria and delivery requirements  

**Your Task:**  
- Write code that determines and presents a solution to deliver all 40 packages (see "packages.csv") on time according to their criteria and constraints under special notes.  
- Reduce the total number of miles traveled by the trucks.  
- Use "distance.csv" and "addresses.csv" for distances and address information.  

**Program Requirements:**  
- Supervisor must be able to check the status of any package at any given time using package IDs.  
- Include delivery times and indicate which packages are at the hub or en route.  
- Code should be well-commented, following industry standards, to support future expansion to other locations.

---

### Project Summary

**Program Specifications:**  
- Written in Python  
- **Must:**  
  - Store package information in a custom hash table (dictionaries are prohibited).  
  - Use a self-adjusting heuristic algorithm to solve the delivery problem under 140 miles.  
  - Allow the user to check the status of any package at any time.  

**Additional Documentation:**  
- Code comments explaining logic and time complexity.  
- Separate documentation covering:  
  - Algorithms used, alternatives, efficiency, and scalability.  
  - Data structures used, alternatives, efficiency, and scalability.  

---

### Technical Requirements and Resources

**Execution:**  
- Code must run using only submitted files and Python’s standard library (excluding dictionaries for the hash table).  

**Data Files:**  
- Use the provided `distance.csv` and `packages.csv` 
**Note on Data Discrepancies:**  
- **Distance file:** `5383 S 900 East #104 (84117)`  
- **Package file:** `5383 South 900 East #104`  

---

### Assumptions

- Two drivers and two trucks available.  
- Trucks move at **18 mph**.  
- Maximum of **16 packages** per truck.  
- Trucks leave the hub **no earlier than 8:00 a.m.**  
- Trucks can only be loaded at the hub.  
- **Ignore** time for loading/unloading.  
- **Package #9:** Wrong delivery address corrected at **10:20 a.m.** to `"410 S State St., Salt Lake City, UT 84111"`.  
- **Packages #13–16, #19–20:** Must be delivered on the **same truck**.  
- **Packages #3, #18, #36, #38:** Must be delivered by **truck 2**.  
- **Packages #6, #25, #28, #32:** Cannot leave the hub before **9:05 a.m.**  

---

## Rubric Requirements Summary

### A: Algorithm Selection  
- Identify the **self-adjusting algorithm** used to deliver packages while meeting all scenario requirements.

### B: Code Documentation  
- Provide **pseudocode** explaining algorithm logic.  
- Describe the **development environment**.  
- Explain **space-time complexity** (Big-O notation).  
- Discuss **adaptability** and **maintainability**.

### C: Original Code  
- Code must be **original** and run **error-free**.  
- Include **identification information** in `main.py`.

### D: Data Structure  
- Implement a **self-adjusting hash table** for package storage.

### E & F: Hash Table Functions  
- **Insert** all package information.  
- **Retrieve** package information by ID.

### G: User Interface  
- Provide an **intuitive interface** for checking package statuses and total mileage.

### H: Proof of Code Execution  
- Include **screenshots** of successful execution and total mileage.

### I: Verification  
- Validate that **all requirements** are met and verifiable through the interface.

### J: Process Improvements  
- Discuss potential **improvements** to the program.

### K: Data Structure Verification  
- Confirm the **functionality** and **performance** of the hash table.

### L: Sources  
- Use proper **APA citations** if applicable.

### M: Professional Communication  
- Ensure **grammar**, **clarity**, and **professional presentation**.