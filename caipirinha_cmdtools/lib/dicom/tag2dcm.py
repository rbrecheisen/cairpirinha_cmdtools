import os
import numpy as np
import pydicom
import binascii
import struct
import SimpleITK as sitk


class Tag2Dcm(object):

    def __init__(self):
        self._input_dicom_file_path = None
        self._input_tag_file_path = None
        self._output_dir = '.'
        self._output_file_path = None
        self._overwrite_output = False
        self._shape = None
        self._spacing = None
        self._origin = None
        self._direction = None
        self._verbose = True

    # INTERFACE

    def set_input_dicom_file_path(self, file_path):
        self._input_dicom_file_path = file_path

    def set_input_tag_file_path(self, file_path):
        self._input_tag_file_path = file_path

    def set_output_dir(self, output_dir):
        self._output_dir = output_dir

    def get_output_file_path(self):
        return self._output_file_path

    def set_overwrite_output(self, value):
        self._overwrite_output = value

    def set_verbose(self, verbose):
        self._verbose = verbose

    # INTERNAL METHODS

    def _get_info_from_dicom(self, f, verbose):
        reader = sitk.ImageFileReader()
        reader.SetImageIO('GDCMImageIO')
        reader.SetFileName(f)
        image = reader.Execute()
        self._shape = image.GetSize()
        self._spacing = image.GetSpacing()
        self._origin = image.GetOrigin()
        self._direction = image.GetDirection()
        min_max_filter = sitk.MinimumMaximumImageFilter()
        min_max_filter.Execute(image)
        minimum = min_max_filter.GetMinimum()
        maximum = min_max_filter.GetMaximum()
        # p = pydicom.read_file(f)
        # # Make sure to put the 1 at the front because the NumPy indexing is differently ordered than
        # # SimpleITK pixel indexing
        # self._shape = (1, p.Rows, p.Columns)
        # self._spacing = (float(p.PixelSpacing[0]), float(p.PixelSpacing[1]), 1.0)
        # self._origin = (
        #     float(p.ImagePositionPatient[0]),
        #     float(p.ImagePositionPatient[1]),
        #     float(p.ImagePositionPatient[2])
        # )
        # self._direction = (
        #     float(p.ImageOrientationPatient[0]),
        #     float(p.ImageOrientationPatient[1]),
        #     float(p.ImageOrientationPatient[2]),
        #     float(p.ImageOrientationPatient[3]),
        #     float(p.ImageOrientationPatient[4]),
        #     float(p.ImageOrientationPatient[5]),
        #     0, 0, 1,
        # )
        if verbose:
            print('File: {}, Size: {}, Spacing: {}, Origin: {}, Direction: {}, Min: {}, Max: {}'.format(
                f, self._shape, self._spacing, self._origin, self._direction, minimum, maximum))

    @staticmethod
    def _get_pixels(tag_file_path):
        f = open(tag_file_path, 'rb')
        f.seek(0)
        byte = f.read(1)
        # Make sure to check the byte-value in Python 3!!
        while byte != b'':
            byte_hex = binascii.hexlify(byte)
            if byte_hex == b'0c':
                break
            byte = f.read(1)
        values = []
        f.read(1)
        while byte != b'':
            v = struct.unpack('b', byte)
            values.append(v)
            byte = f.read(1)
        values = np.asarray(values)
        values = values.astype(np.uint16)
        return values

    # EXECUTE

    def execute(self):
        os.makedirs(self._output_dir, exist_ok=True)
        self._get_info_from_dicom(self._input_dicom_file_path, self._verbose)
        pixels = self._get_pixels(self._input_tag_file_path)

        # pixels.shape = self._shape
        pixels.shape = (1, self._shape[1], self._shape[0])
        image = sitk.GetImageFromArray(pixels)
        image.SetSpacing(self._spacing)
        image.SetOrigin(self._origin)
        image.SetDirection(self._direction)
        # print(image)

        # f = open(self._input_dicom_file_path, 'rb')
        # p = pydicom.read_file(f)
        # p.pixel_array.setflags(write=True)
        # p.pixel_array.flat = pixels
        # p.PixelData = p.pixel_array.tobytes()
        # p.RescaleIntercept = 0
        # p.RescaleSlope = 1

        file_name = os.path.split(self._input_tag_file_path)
        file_name = file_name[1]
        file_name = os.path.splitext(file_name)
        file_name = file_name[0]
        file_name = '{}_tag.dcm'.format(file_name)
        file_path = os.path.join(self._output_dir, file_name)

        try:
            os.stat(file_path)
            if not self._overwrite_output:
                print('Error: file {} already exists!'.format(file_path))
                return
        except FileNotFoundError:
            pass

        self._output_file_path = file_path

        writer = sitk.ImageFileWriter()
        writer.SetFileName(self._output_file_path)
        writer.SetImageIO('GDCMImageIO')
        writer.Execute(image)
        # p.save_as(file_path)
        # f.close()
        # print(self._output_file_path)


if __name__ == '__main__':
    node = Tag2Dcm()
    node.set_input_dicom_file_path('/Volumes/USB_SECURE1/data/radiomics/projects/004_ovarium/data/test/IM_1.dcm')
    node.set_input_tag_file_path('/Volumes/USB_SECURE1/data/radiomics/projects/004_ovarium/data/test/IM_1.tag')
    node.set_output_dir('/Volumes/USB_SECURE1/data/radiomics/projects/004_ovarium/data/test/out')
    node.set_overwrite_output(True)
    node.execute()
