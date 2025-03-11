# ASCII Square Construction

This project implements an algorithm to generate an ASCII art square pattern using Python.

## Overview

The algorithm constructs an _n_×_n_ square where each cell’s character is determined by its minimum distance from any border. Starting from the border with the character **A**, the value increments as the distance to an edge increases.

## Algorithm Details

- **Cell Character Calculation:**  
  For each cell in the grid, the algorithm calculates the minimum distance to any edge (top, bottom, left, or right). This distance is then added to the ASCII value of **A** to determine the cell's character.

- **Row Generation:**  
  The square is built row by row using nested generator expressions, ensuring memory-efficient string construction.

- **String Assembly:**  
  All rows are joined with newline characters to form the final ASCII square representation.

## Functions

### `timer`

- **Purpose:**  
  Measures and prints the execution time of the decorated function.

- **How It Works:**  
  It records the start and end times around the function call, computes the elapsed time, and outputs the duration without altering the function's return value.

### `ascii_square_construction`

- **Purpose:**  
  Generates and returns the ASCII square pattern for a specified dimension.

- **Key Features:**  
  - **LRU Caching:**  
    The function is wrapped with an unlimited least-recently-used cache (`lru_cache`) to store results for repeated inputs, thereby improving performance for multiple calls with the same dimension.
  
  - **Efficient Construction:**  
    It uses concise generator expressions to construct each row and assembles them into the complete pattern.

## Performance Enhancements

- **Decorator-Based Timing:**  
  The `timer` decorator allows you to monitor the execution time, offering insights into performance.
  
- **Memoization:**  
  Using Python's built-in `lru_cache` avoids redundant computations when the function is invoked with the same parameters, making the algorithm highly efficient for repeated calls.

---
