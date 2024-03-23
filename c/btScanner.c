#include <hackrf.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define START_FREQ 2402000000ULL // Start of the Bluetooth Low Energy range in Hz
#define END_FREQ   2480000000ULL // End of the Bluetooth Low Energy range in Hz
#define STEP_FREQ  2000000       // Frequency step corresponding to Bluetooth channel spacing

int rx_callback(hackrf_transfer* transfer) {
    printf("Received %d bytes of I/Q data on frequency.\n", transfer->valid_length);
    // Placeholder for I/Q processing logic
    return 0; // Success
}

void scan_bluetooth_frequencies(hackrf_device* device) {
    uint64_t freq;
    for (freq = START_FREQ; freq <= END_FREQ; freq += STEP_FREQ) {
        if (hackrf_set_freq(device, freq) != HACKRF_SUCCESS) {
            fprintf(stderr, "Failed to set frequency to %llu Hz\n", freq);
            continue;
        }
        printf("Scanning %llu Hz\n", freq);
        sleep(1); // Simulate time for capturing and processing I/Q samples
    }
}

int main() {
    hackrf_device* device = NULL;

    if (hackrf_init() != HACKRF_SUCCESS) {
        fprintf(stderr, "Failed to init HackRF\n");
        return EXIT_FAILURE;
    }

    if (hackrf_open(&device) != HACKRF_SUCCESS) {
        fprintf(stderr, "Failed to open HackRF device\n");
        hackrf_exit();
        return EXIT_FAILURE;
    }

    // Start RX mode. This should ideally run in a separate thread or process
    // since the rx_callback needs to handle data continuously.
    if (hackrf_start_rx(device, rx_callback, NULL) != HACKRF_SUCCESS) {
        fprintf(stderr, "Failed to start RX\n");
        hackrf_close(device);
        hackrf_exit();
        return EXIT_FAILURE;
    }

    // Scan through the Bluetooth frequencies
    scan_bluetooth_frequencies(device);

    // Stop RX mode
    if (hackrf_stop_rx(device) != HACKRF_SUCCESS) {
        fprintf(stderr, "Failed to stop RX\n");
    }

    // Cleanup
    hackrf_close(device);
    hackrf_exit();

    return EXIT_SUCCESS;
}
