
download_csv:
	wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=14JcOSJAWqKOUNyadVZDPm7FplA7XYhrU' -O ./application_data/input/trips.csv

run_ingestion:download_csv
# You might need Root privileges for building image locally
	docker-compose run application python main.py

cleanup:
	docker-compose down
	sudo rm -rf ./application_data ./psqldata