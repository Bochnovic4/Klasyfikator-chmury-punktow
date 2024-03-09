import laspy
import numpy as np
import matplotlib.pyplot as plt


def plot_histogram(values, title, xlabel, ylabel, bins_number=1000, color='blue', alpha=0.7):
    """
    Plot a histogram of the given values.

    Parameters:
    - values: Array-like, the values to be histogrammed.
    - title: str, the title of the histogram.
    - xlabel: str, the label for the x-axis.
    - ylabel: str, the label for the y-axis.
    - bins: int, the number of bins for the histogram.
    - color: str, the color of the histogram bars.
    - alpha: float, the alpha transparency for the histogram bars.
    """
    plt.hist(values, bins=bins_number, color=color, alpha=alpha)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()


def intensity_to_color(intensity):
    if intensity < 0.5:
        # Map from blue to green
        green = 2 * intensity
        blue = 1 - green
        red = 0
    else:
        # Map from green to red
        red = (intensity - 0.5) * 2
        green = 1 - red
        blue = 0
    return red, green, blue


# Read the LAS file
las_file_path = './../Kortowo.las'
las = laspy.read(las_file_path)

intensities = las.intensity

# Plot histogram of intensities
plot_histogram(intensities, 'Histogram of Intensities', 'Intensity', 'Frequency')

# Normalize intensities
normalized_intensities = (intensities - np.min(intensities)) / (np.max(intensities) - np.min(intensities))

# Plot histogram of normalized intensities
plot_histogram(normalized_intensities, 'Histogram of Normalized Intensities', 'Normalized Intensity', 'Frequency')

# Histogram equalization
hist, bins = np.histogram(normalized_intensities, bins=256, range=(0, 1), density=True)
cdf = hist.cumsum()
cdf_normalized = cdf / cdf[-1]

equalized_intensities = np.interp(normalized_intensities, bins[:-1], cdf_normalized)

# Plot histogram of equalized intensities
plot_histogram(equalized_intensities, 'Histogram of Equalized Intensities', 'Equalized Intensity', 'Frequency')

# Map each intensity to a color
colors = np.array([intensity_to_color(i) for i in equalized_intensities])

header = laspy.LasHeader(version="1.4", point_format=2)
las_with_colors = laspy.LasData(header)

# Copy coordinates
las_with_colors.x = las.x
las_with_colors.y = las.y
las_with_colors.z = las.z

# Assign colors
las_with_colors.red = colors[:, 0] * 65535.0
las_with_colors.green = colors[:, 1] * 65535.0
las_with_colors.blue = colors[:, 2] * 65535.0

# Write the modified LAS file to disk
las_with_colors.write("./Kortowo_intensity.las")
