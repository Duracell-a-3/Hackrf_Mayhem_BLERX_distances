import csv
import matplotlib.pyplot as plt
import numpy as np


def csv_check():
    # Initialize lists to store valid records
    identifiers = []
    distances_meters = []

    # Open and read the CSV file
    with open("distances.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            try:
                # Extract only the last 2 hex values of the MAC address
                identifier = ":".join(row[1].split(":")[-2:])
                distance_meters = float(row[2])
                identifiers.append(identifier)
                distances_meters.append(distance_meters)
            except ValueError as e:
                print(f"Error converting row to float: {row}. Error: {e}")

    # Convert distances to feet or inches
    distances = []
    for distance in distances_meters:
        if distance < 0.3048:  # Less than a foot
            distance_inches = distance * 39.3701
            distances.append(distance_inches)
        else:
            distance_feet = distance * 3.28084
            distances.append(distance_feet)

    # Create a polar chart if we have valid data
    if distances:
        angles = np.linspace(
            0, 2 * np.pi, len(identifiers), endpoint=False
        )  # Distribute identifiers evenly around the circle

        # Create polar plot
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={"projection": "polar"})

        # Define colormap
        colors = plt.cm.viridis(
            np.linspace(0, 1, len(identifiers))
        )  # Adjust the colormap as needed

        bars = ax.bar(angles, distances, color=colors, align="center")

        # Set the angle of the identifiers
        ax.set_xticks(angles)
        ax.set_xticklabels(identifiers)

        # Set the label for distance
        ax.set_ylabel("Distance (feet/inches)")

        # Add a legend showing full MAC addresses (or whatever your identifier is)
        # Note: This assumes that `row[1]` contains the full MAC address or identifier you wish to show in the legend
        ax.legend(
            bars,
            [row[1] for row in csv.reader(open("distances.csv"))][1:],
            title="MAC Addresses",
            loc="upper right",
            bbox_to_anchor=(1.4, 1.1),
        )

        plt.title("Distances of Identifiers")
        plt.tight_layout()
        plt.savefig("distances_polar_plot.png")
        plt.close()
    else:
        print("No valid distance data available to plot.")


if __name__ == "__main__":
    csv_check()
