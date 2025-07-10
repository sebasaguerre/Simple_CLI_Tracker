#!/usr/bin/env python3
import os
import sys
import csv
import argparse
from datetime import datetime

class Tracker:
    def __init__(self):
        
        self.log = [datetime.now().strftime("%d-%m-%Y %H:%M")]
        self.metrics = {
            "Mental clarity": None,
            "Emotional clarity/processing" : None,
            "Need for stimulation" : None,
            "Focus quaility" : None,
            "Mental energy" : None,
            "Social drive/ease" : None,
            "Sleep quality" : None,
            "Microdosing": None
            }
        
        self.stats = {}

    def collect_data(self):

        i = 0
        ms = [metric for metric in self.metrics.keys()]

        # collect data 
        while i < len(ms):

            # log data and enable program interuption
            try:
                value = input(f"{ms[i]}: 1-10 or 'quit': ")
                # catch quit
                if value.lower().strip() == "q":
                    print("\nLog process interupted... exiting program.")
                    sys.exit(0)
                else:
                    self.metrics[ms[i]] = float(value)
                    i += 1

            except ValueError:
                print("Enter a numerical value or 'q' to quit...")
                continue
        
        # transform data into log format
        for value in self.metrics.values():
            self.log.append(value)

    def log_data(self):
        # log data 
        if os.path.exists("data.csv"):
            with open("data.csv", "a") as fhand:
                writer = csv.writer(fhand)
                writer.writerow(self.log)
        
        else:
            with open("data.csv", "w", newline="", encoding="utf-8") as fhand:
                writer = csv.writer(fhand)
                
                # create headers
                headers = ["Time"] + [metric for metric in self.metrics.keys()]
                self.log = [headers] + [self.log]

                writer.writerows(self.log)
    
    def test():
        pass
    
    def get_stats(self, t_window=5):
        """Per metric we show:
            - Initial measurment 
            - Average
            - Running average (default is window of 5)
            - Weighted average with exponential decay
        """
        pass

    def display_stats():
        pass


def main():
    
    # create comandline arguments with parser 
    parser = argparse.ArgumentParser(description="Options to interact with trcker")
    
    parser.add_argument("--log", action="store_true",
                        help="Log new data")
    parser.add_argument("--stats", action="store_true",
                        help="Brief overview of data until that point")
    
    parser.add_argument("--test", action="store_true",
                        help="Run a small dummy test for login and displaying data")
    
    args = parser.parse_args()

    if not any([args.log, args.stats, args.test]):
        print("""No arguments where give...
              
            Intended use:
            
            tracker [-h] [--log] [--stats] [-test]
            
            For more information use the [-h] (help) argument.
            """)

    tracker = Tracker()

    if args.log == True:
        tracker.collect_data()
        tracker.log_data()

    if args.stats == True:
        tracker.get_stats()
        tracker.display_stats()
    
    if args.test == True:
        tracker.test()

if __name__ == "__main__":
    main()

