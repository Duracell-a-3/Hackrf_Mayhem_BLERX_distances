import csv
from mac_vendor_lookup import MacLookup


def get_vendor(mac_address):
    try:
        return MacLookup().lookup(mac_address)
    except Exception:
        return "Vendor Not Found"


def main():
    #

    # Specify the name of your MAC address file
    input_file = "extract_ouis.csv"
    # Create an output CSV file
    output_file = "mac_vendors.csv"
    with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
        mac_addresses = infile.readlines()  # Read MAC addresses from the file
        writer = csv.writer(outfile)
        writer.writerow(["MAC Address", "Vendor"])  # Write the header row
        for mac_address in mac_addresses:
            mac_address = mac_address.strip()  # Remove any extra whitespace
            vendor = get_vendor(mac_address)
            writer.writerow([mac_address, vendor])
    print("MAC Address lookup complete! Results saved in {0}".format(outfile.name))


main()
