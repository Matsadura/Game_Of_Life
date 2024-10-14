import customtkinter as ctk


class StylishButton(ctk.CTkButton):
    """
    A custom button class with a smooth color transition
    effect using CustomTkinter.

    Attributes:
        default_background (str): The default background color of the button.
        default_foreground (str): The default text color of the button.
        hover_color (str): The color the button transitions to when hovered.
        transition_steps (int): The number of steps for the color transition.
        current_step (int): Tracks the current step during the transition.
        after_id (int or None): Stores the ID of the scheduled after call
        for the transition.
    """

    def __init__(self, master, **kwargs):
        """
        Initialize the StylishButton with color transition functionality.

        Parameters:
            master: The parent widget.
            kwargs: Other arguments passed to the CTkButton.
        """
        super().__init__(master, **kwargs)
        self.default_background = self.cget("fg_color")
        self.default_foreground = self.cget("text_color")
        self.hover_color = "#3CBBB1"  # Color when hovered
        self.transition_steps = 20  # Number of steps for the transition
        self.current_step = 0  # Track the current step of the transition
        self.after_id = None  # Track the after call

    def transition_color(self, start_color, end_color):
        """
        Gradually transitions the button's background color
        from start_color to end_color.

        Parameters:
            start_color (str): The initial color in hex format.
            end_color (str): The target color to transition to in hex format.
        """
        # Split the color into RGB components
        start_rgb = self.hex_to_rgb(start_color)
        end_rgb = self.hex_to_rgb(end_color)

        # Calculate the difference between the two colors
        step_r = (end_rgb[0] - start_rgb[0]) / self.transition_steps
        step_g = (end_rgb[1] - start_rgb[1]) / self.transition_steps
        step_b = (end_rgb[2] - start_rgb[2]) / self.transition_steps

        # Update the button color
        if self.current_step <= self.transition_steps:
            new_color = (
                f'#{int(start_rgb[0] + step_r * self.current_step):02x}' +
                f'{int(start_rgb[1] + step_g * self.current_step):02x}' +
                f'{int(start_rgb[2] + step_b * self.current_step):02x}'
            )

            self.configure(fg_color=new_color)
            self.current_step += 1
            self.after_id = self.after(int(20), lambda: self.transition_color(
                start_color, end_color))  # Schedule the next color update
        else:
            # Cancel the after call if it exists
            self.after_cancel(self.after_id)

    def hex_to_rgb(self, hex_color):
        """
        Convert a hex color code to an RGB tuple.

        Parameters:
            hex_color (str): The color in hex format (e.g., '#FFFFFF').

        Returns:
            tuple: The RGB representation of the color as a tuple (R, G, B).
        """
        if not isinstance(hex_color, str):
            return (255, 255, 255)
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
