SCRIPTS_DIR := $(CURDIR)/_code/reporting
OUTPUT_DIR := $(CURDIR)/_output/_reports

charts:
	python $(SCRIPTS_DIR)/charts/generate_charts.py

report-html:
	mkdir -p $(OUTPUT_DIR)
	quarto render $(SCRIPTS_DIR)/reports/report.qmd --to html --output wcpd_report.html

report-pdf:
	mkdir -p $(OUTPUT_DIR)
	quarto render $(SCRIPTS_DIR)/reports/report.qmd --to pdf --output wcpd_report.pdf

all: charts report-html

.PHONY: charts report-html report-pdf all clean
