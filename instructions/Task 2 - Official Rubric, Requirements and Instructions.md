# NHP3 TASK 2: WGUPS ROUTING PROGRAM IMPLEMENTATION

---
## OFFICIAL REQUIREMENTS

---
**DATA STRUCTURES AND ALGORITHMS II — C950**

---
## TASK OVERVIEW

This task is the implementation phase of the WGUPS Routing Program.

The Western Governors University Parcel Service (WGUPS) needs to determine an efficient route and delivery distribution for their daily local deliveries (DLD) because packages are not currently being consistently delivered by their promised deadline. The Salt Lake City DLD route has three trucks, two drivers, and an average of 40 packages to deliver each day. Each package has specific criteria and delivery requirements that are listed in the attached "WGUPS Package File."

Your task is to determine an algorithm, write code, and present a solution where all 40 packages will be delivered on time while meeting each package’s requirements and keeping the combined total distance traveled under 140 miles for all trucks. The specific delivery locations are shown on the attached "Salt Lake City Downtown Map," and distances to each location are given in the attached "WGUPS Distance Table." The intent is to use the program for this specific location and also for many other cities in each state where WGU has a presence. As such, you will need to include detailed comments to make your code easy to follow and to justify the decisions you made while writing your scripts.

The supervisor should be able to see, at assigned points, the progress of each truck and its packages by any of the variables listed in the "WGUPS Package File," including what has been delivered and at what time the delivery occurred.

---

## SCENARIO

The Western Governors University Parcel Service (WGUPS) needs to develop an efficient routing program to ensure all deliveries are completed on time while optimizing total mileage under 140 miles. This program must accommodate specific delivery constraints for each package.

---

## ASSUMPTIONS

- Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.
- Trucks travel at an average speed of 18 miles per hour with infinite gas and no stops required.
- Three trucks and two drivers are available. Each driver stays with the same truck while it is in service.
- Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for additional packages if necessary.
- Delivery and loading times are instantaneous.
- Package #9's delivery address is incorrect and will be updated to 410 S. State St., Salt Lake City, UT 84111 at 10:20 a.m.
- Distances provided in the "WGUPS Distance Table" are bidirectional and consistent regardless of travel direction.
- The day ends when all 40 packages are delivered.

---

## REQUIREMENTS

### A. Develop a Hash Table
Develop a hash table, without using any additional libraries or classes, that has an insertion function that takes the package ID as input and inserts each of the following data components into the hash table:

- delivery address
- delivery deadline
- delivery city
- delivery zip code
- package weight
- delivery status (i.e., at the hub, en route, or delivered), including the delivery time

### B. Look-Up Function
Develop a look-up function that takes the package ID as input and returns each of the following corresponding data components:

- delivery address
- delivery deadline
- delivery city
- delivery zip code
- package weight
- delivery status (i.e., at the hub, en route, or delivered), including the delivery time

### C. Original Program
Write an original program that will deliver all packages and meet all requirements using the attached supporting documents “Salt Lake City Downtown Map,” “WGUPS Distance Table,” and “WGUPS Package File.”

1. Create an identifying comment within the first line of a file named “main.py” that includes your student ID.

2. Include comments in your code to explain both the process and the flow of the program.

### D. Interface
Provide an intuitive interface for the user to view the delivery status (including the delivery time) of any package at any time and the total mileage traveled by all trucks. (The delivery status should report the package as at the hub, en route, or delivered. Delivery status must include the time.)

1. Provide screenshots to show the status of all packages loaded onto each truck at a time between 8:35 a.m. and 9:25 a.m.

2. Provide screenshots to show the status of all packages loaded onto each truck at a time between 9:35 a.m. and 10:25 a.m.

3. Provide screenshots to show the status of all packages loaded onto each truck at a time between 12:03 p.m. and 1:12 p.m.

### E. Code Execution
Provide screenshots showing successful completion of the code that includes the total mileage traveled by all trucks.

### F. Algorithm Analysis
Justify the package delivery algorithm used in the solution as written in the original program by doing the following:

1. Describe two or more strengths of the algorithm used in the solution.

2. Verify that the algorithm used in the solution meets all requirements in the scenario.

3. Identify two other named algorithms that are different from the algorithm implemented in the solution and would meet all requirements in the scenario.

   a. Describe how both algorithms identified in part F3 are different from the algorithm used in the solution.

### G. Different Approach
Describe what you would do differently, other than the two algorithms identified in part F3, if you did this project again, including details of the modifications that would be made.

### H. Data Structure Verification
Verify that the data structure used in the solution meets all requirements in the scenario.

1. Identify two other data structures that could meet the same requirements in the scenario.

   a. Describe how each data structure identified in H1 is different from the data structure used in the solution.

### I. Sources
Acknowledge sources, using in-text citations and references, for content that is quoted, paraphrased, or summarized.

### J. Professional Communication
Demonstrate professional communication in the content and presentation of your submission.

---

## RUBRIC

**NOTE:** Every section MUST fulfill the requirements stated 100%. Any partially missing or incorrect portion of a requirement will result in failing the evaluation.

### A: HASH TABLE
The hash table is free from errors and has an insertion function, without using any additional libraries or classes, that takes the package ID as input and inserts each of the given data components.

### B: LOOK-UP FUNCTION
The look-up function completes without runtime errors and takes the package ID as input and returns each of the given data components.

### C: ORIGINAL PROGRAM
The program and code are original. They run without errors or warnings, deliver all packages, and meet all requirements.

### C1: IDENTIFICATION INFORMATION
The identifying comment is located within the first line of a file named “main.py” that includes the student ID.

### C2: PROCESS AND FLOW COMMENTS
The code includes detailed comments that accurately explain both the process and the flow of the program.

### D: INTERFACE
The interface provides an intuitive means for the user to both view the delivery status and for the user to determine the total mileage traveled by all trucks. The delivery status includes the delivery time.

### D1: FIRST STATUS CHECK
The screenshots provided capture all packages loaded onto each truck and they capture the status of each package at a time between 8:35 a.m. and 9:25 a.m.

### D2: SECOND STATUS CHECK
The screenshots provided capture all packages loaded onto each truck and they capture the status of each package at a time between 9:35 a.m. and 10:25 a.m.

### D3: THIRD STATUS CHECK
The screenshots provided capture all packages loaded onto each truck and they capture the status of each package at a time between 12:03 p.m. and 1:12 p.m.

### E: SCREENSHOTS OF CODE EXECUTION
The screenshots capture a complete execution of the code that is free from runtime errors or warnings and include the total mileage traveled by all trucks.

### F1: STRENGTHS OF THE CHOSEN ALGORITHM
The description accurately explains two or more strengths of the algorithm used in the solution.

### F2: VERIFICATION OF ALGORITHM
The submission verifies that the algorithm used in the solution meets all requirements in the scenario.

### F3: OTHER POSSIBLE ALGORITHMS
The submission identifies two algorithms different from the one used in the solution, and both algorithms meet all requirements in the scenario.

### F3A: ALGORITHM DIFFERENCES
The description thoroughly and accurately compares how both algorithms identified in part F3 are different from the algorithm used in the solution.

### G: DIFFERENT APPROACH
The description appropriately explains what would be done differently and includes details of the modifications that would be made.

### H: VERIFICATION OF DATA STRUCTURE
The submission verifies the data structure used in the solution meets all requirements in the scenario.

### H1: OTHER DATA STRUCTURES
The submission identifies two data structures that are different from the one used in the solution, and both data structures meet all requirements in the scenario.

### H1A: DATA STRUCTURE DIFFERENCES
The description thoroughly and accurately compares how each data structure identified in H1 is different from the data structure used in the solution.

### I: SOURCES
The submission includes in-text citations for sources that are properly quoted, paraphrased, or summarized and a reference list that accurately identifies the author, date, title, and source location as available.

### J: PROFESSIONAL COMMUNICATION
This submission demonstrates correct use of spelling, grammar, punctuation, and sentence fluency. You have demonstrated quality professional communication skills in this submission.

---


