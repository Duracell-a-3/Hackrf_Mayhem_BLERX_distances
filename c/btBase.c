#include <hackrf.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define BLUETOOTH_FREQUENCY 2402000000 // 2.402 GHz, start of the Bluetooth range

int rx_callback(hackrf_transfer* transfer) {
    // Process received I/Q samples for Bluetooth packets
    // This is highly simplified. Actual processing would be much more involved.
    printf("Received %d bytes of I/Q data.\n", transfer->valid_length);
    return 0; // Return 0 on success
}

int main() {
    hackrf_device* device = NULL;

    if(hackrf_init() != HACKRF_SUCCESS) {
        fprintf(stderr, "Failed to init HackRF\n");
        return EXIT_FAILURE;
    }

    if(hackrf_open(&device) != HACKRF_SUCCESS) {
        fprintf(stderr, "Failed to open HackRF device\n");
        hackrf_exit();
        return EXIT_FAILURE;
    }

    // Set the HackRF to the Bluetooth frequency
    if(hackrf_set_freq(device, BLUETOOTH_FREQUENCY) != HACKRF_SUCCESS) {
        fprintf(stderr, "Failed to set frequency\n");
        hackrf_close(device);
        hackrf_exit();
        return EXIT_FAILURE;
    }

    // Start receiving
    if(hackrf_start_rx(device, rx_callback, NULL) != HACKRF_SUCCESS) {
        fprintf(stderr, "Failed to start RX\n");
        hackrf_close(device);
        hackrf_exit();
        return EXIT_FAILURE;
    }

    // Keep receiving for a period, e.g., 10 seconds
    sleep(10);

    // Stop receiving
    if(hackrf_stop_rx(device) != HACKRF_SUCCESS) {
        fprintf(stderr, "Failed to stop RX\n");
    }

    // Cleanup
    hackrf_close(device);
    hackrf_exit();

    return EXIT_SUCCESS;
}
