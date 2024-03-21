package main

import (
	"encoding/csv"
	"fmt"
	"html/template"
	"io"
	"log"
	"math"
	"net/http"
	"os"
	"strconv"
	"time"
)

// HomePageVars variables for the HTML template
type HomePageVars struct {
	Title string // Title of the page
}

// uploadPageHandler renders the page with the upload form
func uploadPageHandler(w http.ResponseWriter, r *http.Request) {
	t, err := template.New("upload.html").Parse(`
<!DOCTYPE html>
<html>
<head>
    <title>{{.Title}}</title>
</head>
<body>
    <h1>{{.Title}}</h1>
    <form enctype="multipart/form-data" action="/upload" method="post">
        <input type="file" name="file" />
        <input type="submit" value="Upload" />
    </form>
</body>
</html>
`)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	data := HomePageVars{
		Title: "Upload CSV File",
	}

	if err := t.Execute(w, data); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

// uploadHandler handles the file upload and processes the CSV data, outputting results to a new CSV.
func uploadHandler(w http.ResponseWriter, r *http.Request) {
	r.ParseMultipartForm(10 << 20) // Limit the client to upload files up to 10 MB

	file, _, err := r.FormFile("file")
	if err != nil {
		http.Error(w, "Could not process uploaded file", http.StatusBadRequest)
		return
	}
	defer file.Close()

	// Prepare to write the processed data to a new CSV file
	outputFile, err := os.Create("distances.csv")
	if err != nil {
		log.Printf("Error creating output file: %v", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}
	defer outputFile.Close()

	csvWriter := csv.NewWriter(outputFile)
	defer csvWriter.Flush()

	// Write the header to the new CSV file
	csvWriter.Write([]string{"Timestamp", "Identifier", "Distance"})

	csvReader := csv.NewReader(file)
	csvReader.FieldsPerRecord = -1 // Allow variable number of fields per record
	var processedRows int
	for {
		record, err := csvReader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Printf("Error reading a row: %v", err)
			continue // This skips problematic rows and continues with the next
		}

		if len(record) < 7 { // Ensure there are enough fields
			log.Printf("Skipping row with insufficient fields: %v", record)
			continue
		}

		identifier := record[2] // Attempt to use Name as the identifier
		if identifier == "" {
			identifier = record[1] // Use MAC Address if Name is empty
		}

		dB, err := strconv.Atoi(record[6]) // Parse dB value
		if err != nil {
			log.Printf("Error parsing dB value: %v", err)
			continue
		}

		distance := signalStrengthToDistance(dB)
		timestamp := time.Now().Format(time.RFC3339)
		csvWriter.Write([]string{timestamp, identifier, fmt.Sprintf("%.2f", distance)})

		fmt.Printf("%s is approximately %.2f meters away.\n", identifier, distance)
		processedRows++
	}

	fmt.Fprintf(w, "File processed successfully. %d rows processed. Check server logs for output.", processedRows)
}

// signalStrengthToDistance converts signal strength (dB) to an estimated distance
func signalStrengthToDistance(dB int) float64 {
	// Simple inverse square law estimation
	RSSIAtOneMeter := -40.0
	pathLossExponent := 2.0
	return math.Pow(10, (RSSIAtOneMeter-float64(dB))/(10*pathLossExponent))
}

func main() {
	http.HandleFunc("/", uploadPageHandler)
	http.HandleFunc("/upload", uploadHandler)

	fmt.Println("Server started at http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
