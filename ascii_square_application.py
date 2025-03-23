import tkinter as tk
import sys

from random import choice
from collections import deque
from functools import lru_cache

from ASCII_square import ascii_square_construction
from ascii_square_validation import validate_square_size, validate_size_length, validate_starting_character, \
    validate_char_length


class AsciiSquareApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.copy_button = None
        self.pan_start_y = None
        self.pan_start_x = None
        self.ascii_text = None
        self.snake_colors = None
        self.alternating_mode = None
        self.snake_mode = None
        self.default_mode = None
        self.mode = None
        self.text_items = None
        self.vertical_scrollbar = None
        self.horizontal_scrollbar = None
        self.canvas = None
        self.error_label = None
        self.generate_button = None
        self.palette_menu = None
        self.palette_options = None
        self.palette = None
        self.char_entry = None
        self.size_entry = None
        self.execution_time_label = None

        # Store the ASCII square here so we can copy it later
        self.current_ascii_square = ""

        self.title("ASCII Square")
        self.geometry("1100x800")  # Set main window size with padding.

        # Initialize snake animation variables.
        self.snake_animation_id = None
        self.snake_items = []
        self.spiral_order = []

        self.create_widgets()
        self.bind_mousewheel()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """
            Create and layout all UI widgets.
        """
        # Top frame for input controls.
        top_frame = tk.Frame(self, padx=10, pady=10, bg="#add8e6")
        top_frame.pack(fill=tk.X)

        # Left frame: square size and starting character fields.
        left_frame = tk.Frame(top_frame, bg="#add8e6")
        left_frame.pack(side=tk.LEFT, padx=10)
        square_size_label = tk.Label(left_frame, text="Square size:", font=("TkDefaultFont", 13), bg="#add8e6")
        square_size_label.grid(row=0, column=0, sticky="w")
        square_size_label.bind("<Double-Button-1>", self.copy_text)

        # Create a validation command so that only 4 characters can be entered.
        vcmd = (self.register(validate_size_length), '%P')
        self.size_entry = tk.Entry(left_frame, width=5, validate="key", validatecommand=vcmd)
        self.size_entry.insert(0, "13")
        self.size_entry.grid(row=0, column=1, padx=5)

        starting_char_label = tk.Label(left_frame, text="Starting character:", font=("TkDefaultFont", 13), bg="#add8e6")
        starting_char_label.grid(row=1, column=0, sticky="w")
        starting_char_label.bind("<Double-Button-1>", self.copy_text)

        # Limit the starting character entry to one character.
        vcmd_char = (self.register(validate_char_length), '%P')
        self.char_entry = tk.Entry(left_frame, width=5, validate="key", validatecommand=vcmd_char)
        self.char_entry.insert(0, "A")
        self.char_entry.grid(row=1, column=1, padx=5)

        # Palette dropdown.
        palette_frame = tk.Frame(top_frame, bg="#add8e6")
        palette_frame.pack(side=tk.LEFT, padx=10)
        palette_label = tk.Label(palette_frame, text="Color palette:", font=("TkDefaultFont", 13), bg="#add8e6")
        palette_label.grid(row=0, column=0, sticky="w")
        palette_label.bind("<Double-Button-1>", self.copy_text)
        self.palette = tk.StringVar(value="None")
        self.palette_options = \
            (
                ("None", "None"),
                ("Red", "#FF0000"),
                ("Green", "#00FF00"),
                ("Blue", "#0000FF"),
                ("Orange", "#FFA500"),
                ("Purple", "#800080"),
                ("Cyan", "#00FFFF")
            )
        self.palette_menu = tk.OptionMenu(palette_frame, self.palette,
                                          *[name for name, code in self.palette_options])
        self.palette_menu.config(width=12)
        self.palette_menu.grid(row=1, column=0, padx=5)

        # Radio buttons for mode selection.
        mode_frame = tk.Frame(top_frame, bg="#add8e6")
        mode_frame.pack(side=tk.LEFT, padx=10)
        mode_label = tk.Label(mode_frame, text="Mode:", font=("TkDefaultFont", 13), bg="#add8e6")
        mode_label.pack(anchor="w")
        mode_label.bind("<Double-Button-1>", self.copy_text)

        # Set default selection to "default"
        self.mode = tk.StringVar(value="default")

        self.default_mode = tk.Radiobutton(mode_frame, text="One-color", variable=self.mode, value="default")
        self.default_mode.pack(anchor="w")
        self.alternating_mode = tk.Radiobutton(mode_frame, text="Alternating colors", variable=self.mode,
                                               value="alternating")
        self.alternating_mode.pack(anchor="w")
        self.snake_mode = tk.Radiobutton(mode_frame, text="Snake mode", variable=self.mode, value="snake")
        self.snake_mode.pack(anchor="w")
        # Bind toggle function so a selected button can be deselected.
        for radio_button in (self.default_mode, self.alternating_mode, self.snake_mode):
            radio_button.bind("<Button-1>", self.toggle_mode)

        # Generate button and execution time label.
        generate_frame = tk.Frame(top_frame, bg="#add8e6")
        generate_frame.pack(side=tk.LEFT, padx=10)
        self.generate_button = tk.Button(generate_frame, text="Generate", command=self.generate_square)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        self.execution_time_label = tk.Label(generate_frame, text="", font=("Arial", 14))
        self.execution_time_label.pack(side=tk.LEFT, padx=10)

        # Bind the Enter key to trigger the generate_square method.
        self.bind("<Return>", lambda event: self.generate_square())

        # Error label.
        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.pack()

        # Copy button (centered above canvas).
        copy_button_frame = tk.Frame(self)
        copy_button_frame.pack(fill=tk.X)
        self.copy_button = tk.Button(copy_button_frame, text="Copy ASCII square",
                                     command=self.copy_ascii_square)
        # Center the button horizontally:
        self.copy_button.pack(pady=0, anchor="center")

        # Canvas frame with vertical and horizontal scrollbars.
        canvas_frame = tk.Frame(self, padx=10, pady=5)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        # Pack the scrollbars first.
        self.vertical_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, width=30)
        self.vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.horizontal_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, width=30)
        self.horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas = tk.Canvas(canvas_frame, bg="white",
                                yscrollcommand=self.vertical_scrollbar.set,
                                xscrollcommand=self.horizontal_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vertical_scrollbar.config(command=self.canvas.yview)
        self.horizontal_scrollbar.config(command=self.canvas.xview)

        self.canvas.bind("<ButtonPress-2>", self.start_pan)
        self.canvas.bind("<B2-Motion>", self.do_pan)

    def copy_text(self, event):
        """
            Copy text from the widget that was double-clicked and place it in the clipboard.
        """
        widget = event.widget
        try:
            if widget == self.canvas:
                # For canvas text items, find the closest item and get its "text" attribute.
                item = self.canvas.find_closest(event.x, event.y)[0]
                text = self.canvas.itemcget(item, "text")
            else:
                text = widget.cget("text")
        except (IndexError, tk.TclError):
            text = ""
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)

    def copy_ascii_square(self):
        """
            Copies the entire ASCII square (the same one generated by ascii_square_construction)
            to the clipboard, then shows a small hovering message for 5 seconds.
        """
        if self.current_ascii_square:
            self.clipboard_clear()
            self.clipboard_append(self.current_ascii_square)
            self.show_copy_message()

    def show_copy_message(self):
        """
            Pop up a small 'copied' message for 5 seconds.
        """
        message = tk.Toplevel(self)
        # Remove window decorations:
        message.overrideredirect(True)
        message.config(bg="lightyellow")

        label = tk.Label(message, text="ASCII square copied.", bg="lightyellow", font=("TkDefaultFont", 10))
        label.pack(padx=10, pady=5)

        self.update_idletasks()  # Make sure geometry info is up to date

        # Position the popup to the right of the time label
        time_label_x = self.execution_time_label.winfo_rootx()
        time_label_y = self.execution_time_label.winfo_rooty()
        x = time_label_x + self.execution_time_label.winfo_width() + 10
        y = time_label_y
        message.geometry(f"+{x}+{y}")

        # Destroy after 5 seconds.
        message.after(5000, message.destroy)

    def toggle_mode(self, event):
        """
            Allow a radiobutton to be deselected if already active.
            Only allow deselection for snake and alternating modes.
            In this design the default mode should remain selected unless another is chosen.
        """
        widget = event.widget
        # If the default mode is active, don't allow it to be deselected.
        if self.mode.get() == widget["value"] and widget["value"] != "default":
            self.mode.set("")
            widget.deselect()
            return "break"

    def bind_mousewheel(self):
        """
            Bind mouse wheel events to scroll the canvas.
        """
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Button-4>", self.on_mousewheel)
        self.canvas.bind_all("<Button-5>", self.on_mousewheel)

    def on_mousewheel(self, event):
        """
            Scroll the canvas vertically based on the mouse wheel movement.
        """
        region = self.canvas.bbox("all")
        if region:
            region_height = region[3] - region[1]
            if region_height <= self.canvas.winfo_height():
                return  # No vertical scrolling needed if content fits
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-3, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(3, "units")

    def start_pan(self, event):
        """
            Pan the canvas based on the movement from the initial pan coordinates.
        """
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def do_pan(self, event):
        """
            Pan the canvas based on the movement from the initial pan coordinates.
        """
        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y
        # Invert the default behavior: positive dx scrolls right, positive dy scrolls down.
        self.canvas.xview_scroll(int(dx), "units")
        self.canvas.yview_scroll(int(dy), "units")
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def generate_square(self):
        """
            Generate the ASCII square based on user inputs and display it on the canvas.
        """
        # Cancel any ongoing snake animation.
        if self.snake_animation_id is not None:
            self.after_cancel(self.snake_animation_id)
            self.snake_animation_id = None

        self.canvas.delete("all")
        self.snake_items = []
        self.spiral_order = []

        size_value = self.size_entry.get()
        char_value = self.char_entry.get()
        valid_size, error_size = validate_square_size(size_value)
        valid_char, error_character = validate_starting_character(char_value)

        if not valid_size or not valid_char:
            error_message = error_size if not valid_size else error_character
            self.error_label.config(text=error_message)
            return
        else:
            self.error_label.config(text="")

        try:
            square_size = int(size_value)
        except ValueError:
            self.error_label.config(text="Square size must be an integer.")
            return

        if square_size > 10000:
            self.error_label.config(text="Square size must be 10000 or less.")
            return

        selected_palette = self.palette.get()
        palette_hex = None
        palette_list = []
        for name, hex_code in self.palette_options:
            if name == selected_palette:
                palette_hex = hex_code if hex_code != "None" else None
            if hex_code != "None":
                palette_list.append(hex_code)

        mode = self.mode.get()
        if mode == "snake":
            use_snake = True
            use_alternating = False
            use_default = False
        elif mode == "alternating":
            use_alternating = True
            use_snake = False
            use_default = False
        else:
            use_default = True
            use_alternating = False
            use_snake = False

        uniform_color = palette_hex if use_default else None

        # Synchronously compute the ASCII square.
        try:
            ascii_square = ascii_square_construction(square_size, char_value)
            execution_time = ascii_square_construction.last_execution_time
            self.current_ascii_square = ascii_square  # Store the full ASCII square for later copying:
        except Exception as e:
            self.error_label.config(text=str(e))
            return

        self.draw_and_update(ascii_square, palette_list,
                             uniform_color, execution_time, use_alternating, use_snake)

    def draw_and_update(self, ascii_square, palette_list, uniform_color, execution_time, use_alternating,
                        use_snake):
        """
            Update the execution time label and draw the ASCII square on the canvas.
        """
        # Update the execution time label.
        if execution_time is not None:
            if execution_time < 1:
                formatted_time = f"{execution_time * 1000:.6f}ms"
            else:
                formatted_time = f"{execution_time:.6f}s"
            self.execution_time_label.config(text=f"Time: {formatted_time}")
        else:
            self.execution_time_label.config(text="Time: Cached")

        self.draw_square(ascii_square, use_alternating, use_snake, palette_list,
                         uniform_color)  # Draw the square on the canvas

    def draw_square_incremental(self, rows, cell_width, cell_height, start_x, start_y,
                                palette_list, alternating, snake, uniform_color, row_index=0):
        """
            Incrementally draw each row of the ASCII square on the canvas.
        """
        if row_index >= len(rows):
            # Finished drawing; update the scroll region if needed
            bbox = self.canvas.bbox("all")
            if bbox:
                self.canvas.config(scrollregion=(bbox[0] - 4, bbox[1] - 4, bbox[2] + 4, bbox[3] + 4))
            # Bind copy event to new items
            self.canvas.tag_bind("copyable", "<Double-Button-1>", self.copy_text)
            # If snake mode, set up animation
            if snake:
                self.spiral_order = list(self.get_spiral_order(len(rows)))
                self.snake_items = [self.text_items[i][j] for (i, j) in self.spiral_order]
                self.snake_colors = deque([self.canvas.itemcget(item, "fill") for item in self.snake_items])
                self.animate_snake(palette_list, len(rows))
            return

        # Process a single row
        row = rows[row_index]
        letters = row.split(" ")
        item_row = []

        for j, letter in enumerate(letters):
            x = start_x + j * cell_width
            y = start_y + row_index * cell_height
            fill_color = "black"
            if snake:
                fill_color = choice(palette_list)
            elif alternating:
                layer = min(row_index, j, len(rows) - 1 - row_index, len(letters) - 1 - j)
                fill_color = palette_list[layer % len(palette_list)]
            elif uniform_color is not None:
                fill_color = uniform_color

            item = self.canvas.create_text(x, y, text=letter, anchor="nw",
                                           font=("Courier", 16), fill=fill_color, tags="copyable")
            item_row.append(item)

        # Append this row to text_items (initialize if needed)
        if not hasattr(self, "text_items") or self.text_items is None:
            self.text_items = []
        self.text_items.append(item_row)

        # Schedule drawing of the next row after a short delay.
        self.after(1, lambda: self.draw_square_incremental(rows, cell_width, cell_height,
                                                           start_x, start_y, palette_list,
                                                           alternating, snake, uniform_color,
                                                           row_index + 1))

    def draw_square(self, ascii_square, alternating, snake, palette_list, uniform_color):
        """
            Clear the canvas and initiate the incremental drawing of the ASCII square.
        """
        cell_width = 30
        cell_height = 30
        start_x = 24
        start_y = 24

        rows = ascii_square.split("\n")

        self.text_items = []
        self.canvas.delete("all")  # Clear previous items

        # Start incremental drawing.
        self.draw_square_incremental(rows, cell_width, cell_height, start_x, start_y,
                                     palette_list, alternating, snake, uniform_color)

    @staticmethod
    @lru_cache(maxsize=128)
    def get_spiral_order(n):
        """
            Return a tuple of (row, col) positions in spiral order for a square of size n.
        """
        def spiral_generator():
            top, left = 0, 0
            bottom, right = n - 1, n - 1
            while top <= bottom and left <= right:
                for j in range(left, right + 1):
                    yield top, j
                top += 1
                for i in range(top, bottom + 1):
                    yield i, right
                right -= 1
                if top <= bottom:
                    for j in range(right, left - 1, -1):
                        yield bottom, j
                    bottom -= 1
                if left <= right:
                    for i in range(bottom, top - 1, -1):
                        yield i, left
                    left += 1

        # Convert generator output to a tuple for caching and reuse
        return tuple(spiral_generator())

    def animate_snake(self, palette_list, square_size):
        """
            Animate snake mode by rotating the colors of canvas text items.
        """
        if not self.snake_items:
            return

        # Rotate the stored deque of colors (O(1) rotation)
        self.snake_colors.rotate(1)

        # Update each canvas item's fill color using the rotated deque.
        for item, color in zip(self.snake_items, self.snake_colors):
            self.canvas.itemconfig(item, fill=color)

        # Set delay based on square size.
        delay = 300 if square_size <= 50 else 1000
        self.snake_animation_id = self.after(delay, lambda: self.animate_snake(palette_list, square_size))

    def on_closing(self):
        """
            Cancel any scheduled animations and cleanly close the application.
        """
        # Cancel any scheduled callbacks before quitting.
        if self.snake_animation_id is not None:
            self.after_cancel(self.snake_animation_id)
        self.quit()  # Stop the main loop.
        self.destroy()
        sys.exit(0)


if __name__ == "__main__":
    app = AsciiSquareApp()
    app.mainloop()
