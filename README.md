# ASCII Square Construction

This project implements an optimized algorithm to generate an ASCII art square pattern using Python.

## Overview

The algorithm constructs an _n_×_n_ square where each cell’s character is determined by its minimum distance from any border. Starting from the border with the character **A**, the value increments as the distance to an edge increases. In this version, offsets for rows and columns are precomputed to reduce redundant calculations and further enhance performance.

## Algorithm Details

- **Precomputation of Offsets:**  
  A list of offset values is computed for both rows and columns. Each offset represents the minimum distance of an index to any edge of the square. This precomputation avoids recalculating these distances during the inner loops. This implementation is much quicker than the initial one.

- **Cell Character Calculation:**  
  For each cell, the algorithm uses the precomputed offsets to determine the minimum distance. This distance is then added to the ASCII value of **A** to derive the corresponding character.

- **Row Generation:**  
  The square is built row by row using nested generator expressions, ensuring efficient memory usage.

- **String Assembly:**  
  All rows are joined with newline characters to form the final ASCII square representation.

## Functions

### `timer`

- **Purpose:**  
  Measures and prints the execution time of the decorated function.

- **Implementation:**  
  Wraps the target function to record the start and end times, computes the elapsed time, and prints the duration without affecting the function’s return value.

### `ascii_square_construction`

- **Purpose:**  
  Generates and returns the ASCII square pattern for a specified dimension.

- **Key Features:**  
  - **LRU Caching:**  
    Decorated with an unlimited `lru_cache` to store results for repeated inputs, which improves performance for multiple calls with the same dimension.
  
  - **Optimized Construction:**  
    Uses precomputed offsets to efficiently calculate each cell's character, reducing the overhead in nested loops.

## Performance Enhancements

- **Decorator-Based Timing:**  
  The `timer` decorator provides insights into the execution time of the square construction, helping with performance monitoring.
  
- **Memoization:**  
  The use of `lru_cache` ensures that repeated calls with the same parameters return the cached result, avoiding unnecessary recalculations.

---
