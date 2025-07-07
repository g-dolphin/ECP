SCRIPTS_DIR = /Users/gd/GitHub/ECP/_code/reporting
OUTPUT_DIR = /Users/gd/GitHub/ECP/_output/_reports

charts:
	python $(SCRIPTS_DIR)/charts/generate_charts.py

report-html:
	mkdir -p $(OUTPUT_DIR)
	quarto $(SCRIPTS_DIR)/reports/report.qmd --to html --output wcpd_report.html

report-pdf:
	mkdir -p $(OUTPUT_DIR)
	quarto render $(SCRIPTS_DIR)/reports/report.qmd --to pdf --output wcpd_report.pdf

all: charts report-html

#clean:
#	rm -rf /Users/gd/GitHub/ECP/_output/_figures/*
#	rm -rf /Users/gd/GitHub/ECP/_output/_reports/*

.PHONY: charts report-html report-pdf all clean
