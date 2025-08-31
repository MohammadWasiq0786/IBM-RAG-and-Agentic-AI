import numpy as np
import matplotlib.pyplot as plt

# Step 1: Create an array of x values from -2π to 2π
x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)  # 1000 points for a smooth curve

# Step 2: Compute the sine of x
y = np.sin(x)

# Step 3: Create the plot
plt.figure(figsize=(10, 5))  # Optional: set the size of the figure
plt.plot(x, y, label='y = sin(x)', color='blue')  # Plot the sine wave
plt.title('Sine Wave from -2π to 2π')  # Add a title
plt.xlabel('x (radians)')  # Label for the x-axis
plt.ylabel('y')  # Label for the y-axis
plt.axhline(0, color='black', lw=0.5, ls='--')  # Add a horizontal line at y=0
plt.axvline(0, color='black', lw=0.5, ls='--')  # Add a vertical line at x=0
plt.grid()  # Show a grid
plt.legend()  # Show the legend

# Step 4: Save the plot as a PNG file
plt.savefig('sine_wave.png', dpi=300)  # Save with high resolution
plt.close()  # Close the plot to free up memory