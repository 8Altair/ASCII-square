# ASCII Square Construction

An optimized code and GUI application for generating dynamic ASCII art square patterns with performance monitoring and several rendering modes.

---

## Overview

This project combines a high-performance ASCII square generation algorithm with a Tkinter-based graphical interface. It builds an _n_×_n_ square by computing the minimum distance of each cell to the nearest border, mapping that distance to a character, and rendering the result in a fully interactive window.

---

## Workflow

1. **Input Validation**  
   - Ensure the square size is a positive integer (1–1000).  
   - Ensure the starting character is a single alphabetic letter.  
   - GUI fields enforce maximum lengths (size: 4 digits; character: 1 letter) and display error messages on invalid input.

2. **Pattern Construction**  
   - Precompute a list of row/column offsets: each entry is the minimum distance to any edge.  
   - Build a character lookup table by shifting from the starting character through the alphabet (wrapping A–Z, then a–z).  
   - For each row, use the smaller of row-offset and column-offset to index into the lookup table and assemble the row string.  
   - Combine all rows into the final square pattern.

3. **Performance Monitoring & Caching**  
   - A decorator measures execution time on “cold” runs and reports whether a result came from cache.  
   - An LRU cache stores recent square patterns (up to 128 sizes) to serve repeated requests instantly.

4. **GUI Rendering**  
   - Launch a Tkinter window with input fields, palette selector, mode radios, Generate button, and a scrollable canvas.  
   - On generation: clear any ongoing animations, validate inputs, compute or retrieve the square pattern, display execution time, and draw the square incrementally.  
   - Incremental drawing via short delays keeps the UI responsive even for large patterns.  
   - Copy-on-double-click for individual cells or labels, plus a “Copy ASCII square” button to copy the entire pattern to the clipboard.

---

## GUI Features

- **Input Controls**  
  - Square size entry  
  - Starting character entry  
  - Color palette dropdown  
  - Rendering mode radio buttons

- **Rendering Modes**  
  - **One-color**: uniform color for all characters  
  - **Alternating**: cycle through palette by layer  
  - **Snake**: animate a “snake” of colors following a spiral path

- **Color Palettes**  
  - None (default black), Red, Green, Blue, Orange, Purple, Cyan

- **Interactive Canvas**  
  - Vertical and horizontal scrollbars  
  - Click-and-drag panning  
  - Double-click copy for any text element  
  - Hover message confirming clipboard copy

---

## Performance Enhancements

- **Offset Precomputation**  
  Eliminates per-cell distance calculations by computing each index’s distance once.

- **Memoization**  
  Caches both the square construction and the spiral-order generator for instant retrieval on repeated inputs.

- **Decorator-Based Timing**  
  Automatically logs elapsed time for profiling and displays it in the GUI as milliseconds, seconds, or “Cached.”

- **Incremental Drawing**  
  Splits rendering into per-row tasks scheduled with short delays, preventing the UI from freezing during large draws.

---

## Limitations of Tkinter

- **Single-Threaded Event Loop**  
  Heavy rendering can block user interactions because drawing and event handling share the same thread.

- **No Native Animation Support**  
  Lacks hardware acceleration or double-buffered canvases, so animations may stutter.

- **Canvas Overhead**  
  Thousands of text items slow redraw, scrolling, and event processing.

---

## License

Released under the MIT License. See the accompanying **LICENSE** file for full terms.
