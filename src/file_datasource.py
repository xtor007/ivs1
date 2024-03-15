import csv
from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
from domain.parking import Parking
import config


class FileDatasource:

    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str
    ) -> None:
        self.accelerometer_data = []
        self.gps_data = []
        self.parking_data = []
        self.accelerometer_file = None
        self.gps_file = None
        self.parking_file = None
        self.accelerometer_index = 1
        self.parking_index = 1
        self.gps_index = 1
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename

    def read(self) -> AggregatedData:
        gps = self.gps_data[self.gps_index]
        accelerometer = self.accelerometer_data[self.accelerometer_index]
        parking = self.parking_data[self.parking_index]
        data = AggregatedData(
            Accelerometer(accelerometer[0], accelerometer[1], accelerometer[2]),
            Gps(gps[0], gps[1]),
            Parking(parking[0], Gps(parking[1], parking[2])),
            datetime.now(),
            config.USER_ID,
        )
        self.parking_index += 1
        self.gps_index += 1
        self.accelerometer_index += 1
        if self.gps_index >= len(self.gps_data):
            self.gps_index = 1
        if self.accelerometer_index >= len(self.accelerometer_data):
            self.accelerometer_index = 1
        if self.parking_index >= len(self.parking_data):
            self.parking_index = 1
        return data

    def startReading(self, *args, **kwargs):
        try:
            self.accelerometer_file = open(self.accelerometer_filename, 'r')
            self.accelerometer_data = list(csv.reader(self.accelerometer_file))
            self.gps_file = open(self.gps_filename, 'r')
            self.gps_data = list(csv.reader(self.gps_file))
            self.parking_file = open(self.parking_filename, 'r')
            self.parking_data = list(csv.reader(self.parking_file))
        except FileNotFoundError:
            print("One or both files not found.")
            return None, None
        except Exception as e:
            print("An error occurred:", e)
            return None, None

    def stopReading(self, *args, **kwargs):
        if self.accelerometer_file is not None:
            self.accelerometer_file.close()
        if self.gps_file is not None:
            self.gps_file.close()
        if self.parking_file is not None:
            self.parking_file.close()
