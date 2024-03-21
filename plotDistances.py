import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def csv_check():
    # Initialize lists to store valid records
    records = []

    # Open and read the CSV file
    with open("distances.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            try:
                # Convert timestamp to datetime object
                timestamp = datetime.fromisoformat(row[0])
                identifier = ":".join(row[1].split(":")[-2:])
                distance_meters = float(row[2])
                records.append((timestamp, identifier, distance_meters))
            except ValueError as e:
                print(f"Error converting row to float: {row}. Error: {e}")

    # Sort records by timestamp
    sorted_records = sorted(records, key=lambda x: x[0])

    # Extract data for plotting
    timestamps = [record[0] for record in sorted_records]
    identifiers = [record[1] for record in sorted_records]
    distances = [record[2] for record in sorted_records]

    # Create a polar chart if we have valid data
    if distances:
        angles = np.linspace(
            0, 2 * np.pi, len(identifiers), endpoint=False
        )  # Distribute identifiers evenly around the circle

        # Create polar plot
        fig, ax = plt.subplots(
            figsize=(14, 10), subplot_kw={"projection": "polar"}
        )  # Adjust the figure size as needed

        # Define colormap
        colors = plt.cm.viridis(
            np.linspace(0, 1, len(identifiers))
        )  # Adjust the colormap as needed

        bars = ax.bar(angles, distances, color=colors, align="center")

        # Set the angle of the identifiers
        ax.set_xticks(angles)
        ax.set_xticklabels(identifiers)

        # Set the label for distance
        ax.set_ylabel("Distance (meters)")

        # Add a legend showing full MAC addresses (or whatever your identifier is)
        # Note: This assumes that `row[1]` contains the full MAC address or identifier you wish to show in the legend
        ax.legend(
            bars,
            [record[1] for record in sorted_records],
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
