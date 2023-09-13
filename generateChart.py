import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file with song data
csv_file = "song_history.csv"
df = pd.read_csv(csv_file, encoding="utf-8")

# Select only the numeric columns
numeric_columns = df.select_dtypes(include=[np.number])

# Calculate median values for each attribute
median_values = numeric_columns.median()

# Define attribute names (updated to match the number of attributes)
attributes = [
    "Acousticness",
    "Danceability",
    "Duration (ms)",
    "Energy",
    "Instrumentalness",
    "Key",
    "Liveness",
    "Loudness",
    "Speechiness",
    "Valence",
]

# Create a polar chart
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)

# Calculate angles for each attribute (based on the number of attributes)
angles = np.linspace(0, 2 * np.pi, len(attributes), endpoint=False).tolist()
angles += angles[:1]

# Plot the median values
median_values = median_values[
    attributes
]  # Filter median values for selected attributes
angles += angles[:1]  # Close the chart by repeating the first angle
median_values = median_values.tolist()
median_values += median_values[:1]  # Close the chart by repeating the first value
ax.fill(angles, median_values, "b", alpha=0.1)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(attributes)
ax.set_title("Median Attribute Values")

# Show the polar chart
plt.show()
