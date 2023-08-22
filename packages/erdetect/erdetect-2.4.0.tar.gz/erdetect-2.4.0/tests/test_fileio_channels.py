import unittest
import time

from erdetect.fileio.IeegDataReader import IeegDataReader
from erdetect.fileio.EdfReader import EdfReader
from erdetect.fileio.BrainVisionReader import BrainVisionReader


class TestFileIO(unittest.TestCase):

    def test_fileio_edf_channel(self):
        hdr = EdfReader.edf_read_header('D:\\BIDS_erdetect\\sub-EDF\\ses-ieeg01\\ieeg\\sub-EDF_ses-ieeg01_ieeg.edf')
        start = time.time()

        _, data = EdfReader.edf_read_data('D:\\BIDS_erdetect\\sub-EDF\\ses-ieeg01\\ieeg\\sub-EDF_ses-ieeg01_ieeg.edf', channels=('DC12-Ref',))

        #reader = IeegDataReader("D:\EDF_Data\sub-MSEL01872_ses-ieeg01_task-languagePPT_run-01_ieeg.edf")
        #data = reader.retrieve_channel_data('DC12-Ref')


        print('EDF channel: ' + str(time.time() - start))
        self.assertEqual(1, 1)


    def test_fileio_bv_channel(self):
        hdr = BrainVisionReader.bv_read_header('D:\\BIDS_erdetect\\sub-BV\\ses-1\\ieeg\\sub-BV_ses-1_ieeg.vhdr')
        start = time.time()

        _, data = BrainVisionReader.bv_read_data('D:\\BIDS_erdetect\\sub-BV\\ses-1\\ieeg\\sub-BV_ses-1_ieeg.eeg', channels=('CH11',))

        #reader = IeegDataReader('D:\\BIDS_erdetect\\sub-BV\\ses-1\\ieeg\\sub-BV_ses-1_ieeg.eeg')
        #data = reader.retrieve_channel_data('CH11')

        print('EDF channel: ' + str(time.time() - start))
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
