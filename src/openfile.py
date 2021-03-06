# converts file path to SampledSignal object
from classes import SampledSignal
import utility as util
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import wfdb
import csv
import numpy as np
import viewer
import pyqtgraph.exporters

from classes import MAX_SAMPLES


def browse_window(self):
    self.graph_empty = False
    self.filename = QFileDialog.getOpenFileName(
        None, 'open the signal file', './', filter="Raw Data(*.csv *.txt *.xls *.hea *.dat *.rec)")
    path = self.filename[0]
    util.printDebug("Selected path: " + path)
    open_file(self, path)
    viewer.move_to_viewer(self, "browse")


def open_file(self, path):
    # called by a function in main.py
    # gets fsampling
    # gets magnitude array
    # passes them to the returned sampledsignal object
    # can deal with csv, .dat etc..
    # maximum of 1000 points? idk yet
    temp_arr_x = []
    temp_arr_y = []
    self.fsampling = 1
    filetype = path[len(path)-3:]  # gets last 3 letters of path

    if filetype == "hea" or filetype == "rec" or filetype == "dat":
        self.record = wfdb.rdrecord(path[:-4], channels=[0])
        temp_arr_y = self.record.p_signal
        temp_arr_y = np.concatenate(temp_arr_y)
        temp_arr_y = temp_arr_y[:MAX_SAMPLES]
        self.fsampling = self.record.fs

    if filetype == "csv" or filetype == "txt" or filetype == "xls":
        with open(path, 'r') as csvFile:    # 'r' its a mode for reading and writing
            csvReader = csv.reader(csvFile, delimiter=',')

            # neglect the first line in the csv file
            next(csvReader)

            for line in csvReader:
                if len(temp_arr_x) > MAX_SAMPLES:
                    break
                else:
                    temp_arr_y.append(
                        float(line[1]))
                    temp_arr_x.append(
                        float(line[0]))

        self.fsampling = 1/(temp_arr_x[1]-temp_arr_x[0])

    self.browsed_signal = SampledSignal(self.fsampling, temp_arr_y)


def export_summed_signal(self):
    '''Saves the summed signal as csv file'''
    if len(self.sinusoid_creator_array) == 0:
        QMessageBox.warning(
            self, 'NO SIGNAL ', 'You have to plot a signal first')
    else:
        FolderPath = QFileDialog.getSaveFileName(
            None, str('Save the summed signal'), None, str("CSV FIles(*.csv)"))
        CSVfile = pyqtgraph.exporters.CSVExporter(self.summedSignal.plotItem)
        CSVfile.export(str(FolderPath[0]))
        QMessageBox.information(
            self, 'Complete ', 'The csv was exported successfuly at: \n ' + str(FolderPath[0]))

