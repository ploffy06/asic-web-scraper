import time
from scraper import scrape_asic_notices
from database import create_database, check_for_new_entries

if __name__ == "__main__":
    create_database()
    while True:
        liquidations = scrape_asic_notices()
        check_for_new_entries(liquidations)
        time.sleep(1)
