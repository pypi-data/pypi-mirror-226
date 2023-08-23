"""
Morfeus lab
The University of Texas
MD Anderson Cancer Center
Author - Caleb O'Connor
Email - csoconnor@mdanderson.org


Description:
    This is a "supposed" to be a multi data medical imagery reader. Currently, only works for dicom.
    Secondly, only images of an orientation [1, 0, 0, 0, 1 ,0] have been tested for 3D image volume and ROI volume
    output.

    Using the "DicomReader" class the user can input a folder directory and output the images in numpy arrays along with
    their respective rois (if any). The data does not need to be organized inside folder directory, the reader will
    sort the images appropriately. It does not separate different patients if they exist in the same folder.

    The reader currently imports 9 different modalites and RTSTRUCT files. The accepted modalites are:
        CT
        MR
        US
        PT
        MG
        DX
        NM
        XA
        CR

    The CT and MR modalities have been tested extensively, along with their respective ROIs. The other 7 modalities
    have been tested but only on a few datasets a piece. For RTSTRUCTS, only those referencing CT and MR have been
    tested.
"""

import os
import time
from multiprocessing import Pool

import cv2
import numpy as np
import pandas as pd
import pydicom as dicom
import SimpleITK as sitk

import vtk
from vtk.util import numpy_support
from vtk.numpy_interface import dataset_adapter as dsa
import pyacvd
import pyvista as pv


def multi_process_dicom(path):
    """
    Uses pydicom to read in dicom files.

    Parameters
    ----------
    path - this is the path for a single file

    Returns
    -------

    """
    try:
        datasets = dicom.dcmread(str(path))
    except:
        datasets = []

    return datasets, path


class DicomReader:
    def __init__(self, dicom_files, existing_image_info):
        self.dicom_files = dicom_files
        self.existing_image_info = existing_image_info

        self.ds = []
        self.ds_images = []
        self.ds_dictionary = dict.fromkeys(['CT', 'MR', 'PT', 'US', 'DX', 'MG', 'NM', 'XA', 'CR', 'RTSTRUCT'])
        self.rt_df = pd.DataFrame(columns=['FilePath', 'SeriesInstanceUID', 'RoiSOP', 'RoiNames'])

        keep_tags = ['FilePath', 'SOPInstanceUID', 'PatientID', 'PatientName', 'Modality',
                     'SeriesDescription', 'SeriesDate', 'SeriesTime', 'SeriesInstanceUID', 'SeriesNumber',
                     'AcquisitionNumber', 'SliceThickness', 'PixelSpacing', 'Rows', 'Columns', 'ImagePositionPatient',
                     'Slices', 'DefaultWindow', 'FullWindow']
        self.image_info = pd.DataFrame(columns=keep_tags)
        self.image_data = []

        self.roi_info = pd.DataFrame(columns=['FilePath', 'RoiNames', 'PhysicalCoordinates', 'ArrayCoordinates',
                                              'Volume', 'COM'])
        self.roi_contour = []
        self.roi_mask = []
        self.roi_trimesh = []

    def add_dicom_extension(self):
        """
        Will add .dcm extension to any file inside self.dicom_files that doesn't have an extension
        Returns
        -------

        """
        for ii, name in enumerate(self.dicom_files):
            a, b = os.path.splitext(name)
            if not b:
                self.dicom_files[ii] = name + '.dcm'

    def load_dicom(self):
        t1 = time.time()
        self.read()
        self.separate_modalities()
        self.separate_images()
        self.separate_rt_images()
        self.standard_useful_tags()
        self.convert_images()
        self.separate_contours()
        t2 = time.time()
        print('Dicom Read Time: ', t2 - t1)

    def read(self):
        """
        Uses the multiprocessing module to read in the data. The dicom files are sent to "multi_process_dicom"
        function outside this class, which returns the read-in dicom tags/data. The tags/data are only kept if there
        is a Modality tag.

        self.ds -> contains tag/data from pydicom read-in

        Returns
        -------

        """
        p = Pool()
        for x, y in p.imap_unordered(multi_process_dicom, self.dicom_files):
            if x and 'Modality' in x:
                self.ds.append(x)
        p.close()

    def separate_modalities(self):
        """
        Currently, separates the files into 10 different modalities. Files with a different modality are not kept.
        Certain tags are required depending on the modality, if those tags don't exist for its respective modality
        then it is not kept.

        Returns
        -------

        """
        req = {'CT': ['SeriesInstanceUID', 'AcquisitionNumber', 'ImagePositionPatient', 'SliceThickness', 'PixelData',
                      'FrameOfReferenceUID'],
               'MR': ['SeriesInstanceUID', 'AcquisitionNumber', 'ImagePositionPatient', 'SliceThickness', 'PixelData',
                      'FrameOfReferenceUID'],
               'PT': ['SeriesInstanceUID', 'ImagePositionPatient', 'SliceThickness', 'PixelData',
                      'FrameOfReferenceUID'],
               'US': ['SeriesInstanceUID', 'PixelData'],
               'DX': ['SeriesInstanceUID', 'PixelData'],
               'MG': ['SeriesInstanceUID', 'PixelData'],
               'NM': ['SeriesInstanceUID', 'PixelData'],
               'XA': ['SeriesInstanceUID', 'NumberOfFrames', 'PixelData'],
               'CR': ['SeriesInstanceUID', 'PixelData'],
               'RTSTRUCT': ['SeriesInstanceUID', 'FrameOfReferenceUID']}

        for modality in list(self.ds_dictionary.keys()):
            ds_modality = [d for d in self.ds if d['Modality'].value == modality]
            if modality == 'CT' or modality == 'MR' or modality == 'PT':
                self.ds_dictionary[modality] = [ds_mod for ds_mod in ds_modality if
                                                len([r for r in req[modality] if r in ds_mod]) == len(req[modality]) and
                                                ds_mod['SliceThickness'].value]
            else:
                self.ds_dictionary[modality] = [ds_mod for ds_mod in ds_modality if
                                                len([r for r in req[modality] if r in ds_mod]) == len(req[modality])]

    def separate_images(self):
        """
        This is used to separate the different modalities into images. Each modality has specific requirements to exist
        in the tags:
            CT/MR = SeriesInstanceUID, SliceThickness, AcquisitionNumber, ImagePositionPatient
            US = SeriesInstanceUID

        CT - the 4 main tags are pulled into a numpy array. There is a quick fix because sometimes AcquisitionNumber is
             empty, if so then '1001' is inserted in its place. All the unique combinations are found using series
             instance uid, slice thickness, acquisition number. The unique combinations are used in a for loop and
             all slices that match that criteria are selected. Those slices are then sorted by image position patient.
        MR/PT - same as CT
        US/DX/MG/NM/XA/CR - The images are just sorted using series instance uid.


        Note: slices thickness is needed because some scans are saved with the first slice being a single slice of
              coronal plane, then the rest of the slices are in the axial plane. I think it is called a scout scan,
              basically they have a single coronal slice to show the area that will be covered, then it is followed
              by your standard axial plane view. Anyway, I separate out that slice using the slice thickness because
              it will be different from the axial.

        Returns
        -------

        """
        standard_modalities = ['CT', 'MR', 'PT']
        for mod in standard_modalities:
            if len(self.ds_dictionary[mod]) > 0:
                if mod in ['CT', 'MR']:
                    sorting_tags = np.asarray([[img['SeriesInstanceUID'].value, img['SliceThickness'].value,
                                                img['AcquisitionNumber'].value, img['ImagePositionPatient'].value[2], ii]
                                               for ii, img in enumerate(self.ds_dictionary[mod])])
                else:
                    sorting_tags = np.asarray([[img['SeriesInstanceUID'].value, img['SliceThickness'].value,
                                                None, img['ImagePositionPatient'].value[2], ii]
                                               for ii, img in enumerate(self.ds_dictionary[mod])])
                sorting_tags_fix = np.asarray([[s[0], s[1], '1001', s[3], s[4]]
                                               if s[2] is None else s for s in sorting_tags])

                unique_tags = np.unique(sorting_tags_fix[:, 0:3].astype(str), axis=0)
                for tags in unique_tags:
                    unsorted_values = sorting_tags_fix[np.where((sorting_tags_fix[:, 0] == tags[0]) &
                                                                (sorting_tags_fix[:, 1] == tags[1]) &
                                                                (sorting_tags_fix[:, 2] == tags[2]))]

                    sorted_values = unsorted_values[np.argsort(unsorted_values[:, 3].astype('float'))[::-1]]

                    self.ds_images.append([self.ds_dictionary[mod][int(idx[4])] for idx in sorted_values])

        nonstandard_modalities = ['US', 'DX', 'MG', 'NM', 'XA', 'CR']
        for mod in nonstandard_modalities:
            if len(self.ds_dictionary[mod]) > 0:
                sorting_tags = np.asarray([[img['SeriesInstanceUID'].value, ii]
                                           for ii, img in enumerate(self.ds_dictionary[mod])])
                unique_tags = np.unique(sorting_tags[:, 0], axis=0)
                for tags in unique_tags:
                    unsorted_values = sorting_tags[np.where(sorting_tags[:, 0] == tags)]
                    sorted_values = unsorted_values[np.argsort(unsorted_values[:, 0])]
                    self.ds_images.append([self.ds_dictionary[mod][int(idx[1])] for idx in sorted_values])

    def separate_rt_images(self):
        """
        Loops through all RTSTRUCT files found. Some required information that will be used later in making the contours
        is pulled:
            SeriesInstanceUID
            RoiNames
            RoiSOP - this will be used to determine what slice the contour exist on
        Returns
        -------

        """
        for ii, rt_ds in enumerate(self.ds_dictionary['RTSTRUCT']):
            ref = rt_ds.ReferencedFrameOfReferenceSequence
            series_uid = ref[0]['RTReferencedStudySequence'][0]['RTReferencedSeriesSequence'][0][
                'SeriesInstanceUID'].value

            roi_sop = []
            for contour_list in rt_ds.ROIContourSequence:
                points = [c.NumberOfContourPoints for c in contour_list['ContourSequence']]
                if np.sum(np.asarray(points)) > 3:
                    roi_sop.append(contour_list['ContourSequence'][0]
                                   ['ContourImageSequence'][0]['ReferencedSOPInstanceUID'].value)

            self.rt_df.at[ii, 'FilePath'] = rt_ds.filename
            self.rt_df.at[ii, 'SeriesInstanceUID'] = series_uid
            self.rt_df.at[ii, 'RoiSOP'] = roi_sop
            self.rt_df.at[ii, 'RoiNames'] = [s.ROIName for s in rt_ds.StructureSetROISequence]

    def standard_useful_tags(self):
        """
        Important tags for each image that I use in DRAGON:
            ['FilePath', 'SOPInstanceUID', 'PatientID', 'PatientName', 'Modality',
             'SeriesDescription', 'SeriesDate', 'SeriesTime', 'SeriesInstanceUID', 'SeriesNumber',
             'AcquisitionNumber', 'SliceThickness', 'PixelSpacing', 'Rows', 'Columns', 'ImagePositionPatient',
             'Slices', 'DefaultWindow']

        Returns
        -------

        """
        for ii, image in enumerate(self.ds_images):
            for t in list(self.image_info.keys()):
                if t == 'FilePath':
                    self.image_info.at[ii, t] = [img.filename for img in image]

                elif t == 'SOPInstanceUID':
                    self.image_info.at[ii, t] = [img.SOPInstanceUID for img in image]

                elif t == 'PixelSpacing':
                    if image[0].Modality == 'US':
                        self.image_info.at[ii, t] = [
                            np.round(image[0].SequenceOfUltrasoundRegions[0].PhysicalDeltaX, 4),
                            np.round(image[0].SequenceOfUltrasoundRegions[0].PhysicalDeltaY, 4)]
                    elif image[0].Modality in ['DX', 'XA']:
                        self.image_info.at[ii, t] = image[0].ImagerPixelSpacing
                    else:
                        self.image_info.at[ii, t] = image[0].PixelSpacing

                elif t == 'ImagePositionPatient':
                    if image[0].Modality in ['US', 'CR', 'DX', 'MG', 'NM', 'XA']:
                        self.image_info.at[ii, t] = [0, 0, 0]
                    else:
                        self.image_info.at[ii, t] = image[-1].ImagePositionPatient

                elif t == 'Slices':
                    self.image_info.at[ii, t] = len(image)

                elif t == 'DefaultWindow':
                    if (0x0028, 0x1050) in image[0] and (0x0028, 0x1051) in image[0]:
                        if image[0].Modality == 'DX':
                            self.image_info.at[ii, t] = [int(image[0].WindowCenter[0]),
                                                         int(np.round(image[0].WindowWidth[0]/2))]
                        else:
                            center = image[0].WindowCenter
                            width = image[0].WindowWidth
                            if not isinstance(center, float):
                                center = center[0]
                            if not isinstance(width, float):
                                width = width[0]
                            self.image_info.at[ii, t] = [int(center), int(np.round(width/2))]
                    elif image[0].Modality == 'US':
                        self.image_info.at[ii, t] = [128, 128]
                    else:
                        self.image_info.at[ii, t] = None
                elif t == 'FullWindow':
                    self.image_info.at[ii, t] = None
                else:
                    if t in image[0]:
                        self.image_info.at[ii, t] = image[0][t].value
                    else:
                        self.image_info.at[ii, t] = None

    def convert_images(self):
        """
        Gets the 2D slice for each image and combines them into a 3D array per each image. Uses the RescaleIntercept
        and RescaleSlope to adjust the HU.

        The US is a different story. The image was saved as an RGB value, which also contained like metadata and
        patient information embedded in the image itself. Luckily there was a simple way to get the actual US out, and
        that was using the fact that when all three RGB values are the same thing it corresponds to the image (this
        pulls some additional none image stuff but not nearly as bad). The quickest way I thought would be to find the
        standard deviation of all three values and if it is zero then it is a keeper.

        Sometimes the images are in a shape [1, 10, 512, 512] meaning 10 "slices" by 512x512 array. Not sure why the 1
        is there, so it checks if the shape is 4 and if so it only saves the image as a [10, 512, 512]
        Returns
        -------

        """
        for ii, image in enumerate(self.ds_images):
            image_slices = []
            if self.image_info.at[ii, 'Modality'] in ['CT', 'MR', 'PT', 'DX', 'MG', 'NM', 'XA', 'CR']:
                for slice_ in reversed(image):
                    if (0x0028, 0x1052) in slice_:
                        intercept = slice_.RescaleIntercept
                    else:
                        intercept = 0

                    if (0x0028, 0x1053) in slice_:
                        slope = slice_.RescaleSlope
                    else:
                        slope = 1

                    image_slices.append(((slice_.pixel_array*slope)+intercept).astype('int16'))

            elif self.image_info.at[ii, 'Modality'] == 'US':
                if len(image) == 1:
                    us_data = image[0].pixel_array
                    us_binary = (1 * (np.std(us_data, axis=3) == 0) == 1)
                    image_slices = (us_binary * us_data[:, :, :, 0]).astype('uint8')
                else:
                    print('Need to finish')

            image_hold = np.asarray(image_slices)
            if len(image_hold.shape) > 3:
                self.image_data.append(image_hold[0])
            else:
                self.image_data.append(image_hold)

            image_min = np.min(self.image_data[-1])
            image_max = np.max(self.image_data[-1])
            self.image_info.at[ii, 'FullWindow'] = [image_min, image_max]

    def separate_contours(self):
        """
        existing_image_info is required if the users only loads a RTSTRUCT file, because to make the mask the spacing
        and origin from the CT is needed.

        It is pretty gross after that. For a given ROI each contour is read-in, an empty full sized image array is
        created. Using cv2 the contours are converted to a binary slice, then all the slices are combined.

        Returns
        -------

        """
        info = self.image_info
        if self.existing_image_info:
            info.append(self.existing_image_info)

        for ii in range(len(info.index)):
            img_sop = info.at[ii, 'SOPInstanceUID']
            img_series = info.at[ii, 'SeriesInstanceUID']

            image_contour_list = []
            roi_names = []
            roi_filepaths = []
            for jj in range(len(self.rt_df.index)):
                if img_series == self.rt_df.at[jj, 'SeriesInstanceUID'] and self.rt_df.at[jj, 'RoiSOP'][0] in img_sop:
                    roi_sequence = self.ds_dictionary['RTSTRUCT'][jj].ROIContourSequence
                    for kk, sequence in enumerate(roi_sequence):
                        contour_list = []
                        for c in sequence.ContourSequence:
                            if int(c.NumberOfContourPoints) > 1:
                                contour_hold = np.round(np.array(c['ContourData'].value), 3)
                                contour = contour_hold.reshape(int(len(contour_hold) / 3), 3)
                                contour_list.append(contour)

                        image_contour_list.append(contour_list)
                        if len(contour_list) > 0:
                            roi_filepaths.append(self.rt_df.at[jj, 'FilePath'])
                            roi_names.append(self.rt_df.RoiNames[jj][kk])

            if len(roi_names) > 0:
                self.roi_contour.append(image_contour_list)
                self.roi_info.at[ii, 'FilePath'] = roi_filepaths
                self.roi_info.at[ii, 'RoiNames'] = roi_names
                self.roi_info.at[ii, 'PhysicalCoordinates'] = None
                self.roi_info.at[ii, 'ArrayCoordinates'] = None
                self.roi_info.at[ii, 'Volume'] = None
                self.roi_info.at[ii, 'COM'] = None
            else:
                self.roi_contour.append(image_contour_list)
                self.roi_info.at[ii, 'FilePath'] = None
                self.roi_info.at[ii, 'RoiNames'] = None
                self.roi_info.at[ii, 'PhysicalCoordinates'] = None
                self.roi_info.at[ii, 'ArrayCoordinates'] = None
                self.roi_info.at[ii, 'Volume'] = None
                self.roi_info.at[ii, 'COM'] = None

    # def roi_trimesh(self):
    #     info = self.image_info
    #     if self.existing_image_info:
    #         info.append(self.existing_image_info)
    #
    #     for ii in range(len(info.index)):
    #         img_sop = info.at[ii, 'SOPInstanceUID']
    #         img_series = info.at[ii, 'SeriesInstanceUID']
    #         spacing_array = [info.at[ii, 'PixelSpacing'][0],
    #                          info.at[ii, 'PixelSpacing'][1],
    #                          info.at[ii, 'SliceThickness']]
    #
    #         corner_array = [float(info.at[ii, 'ImagePositionPatient'][0]),
    #                         float(info.at[ii, 'ImagePositionPatient'][1]),
    #                         float(info.at[ii, 'ImagePositionPatient'][2])]
    #
    #         rows = int(info.at[ii, 'Rows'])
    #         columns = int(info.at[ii, 'Columns'])
    #         slices = len(self.ds_images[ii])
    #
    #         mask_com = []
    #         mask_volume = []
    #         mask_reduced = []
    #         roi_filepaths, roi_names = [], []
    #         physical_coordinates, array_coordinates = [], []
    #         for jj in range(len(self.rt_df.index)):
    #             if img_series == self.rt_df.at[jj, 'SeriesInstanceUID'] and self.rt_df.at[jj, 'RoiSOP'][0] in img_sop:
    #                 roi_sequence = self.ds_dictionary['RTSTRUCT'][jj].ROIContourSequence
    #                 for kk, sequence in enumerate(roi_sequence):
    #                     slice_check = np.zeros(slices)
    #
    #                     r, col, s = [], [], []
    #                     mask = np.zeros([slices, rows, columns], dtype=np.uint8)
    #                     c_list = []
    #                     for c in sequence.ContourSequence:
    #                         if int(c.NumberOfContourPoints) > 1:
    #                             contour_hold = np.round(np.array(c['ContourData'].value), 3)
    #                             contour = contour_hold.reshape(int(len(contour_hold) / 3), 3)
    #                             c_list.append(contour)
    #                             contour_indexing = np.round(np.abs((contour - corner_array) / spacing_array))
    #                             slice_num = slices - \
    #                                         (img_sop.index(c.ContourImageSequence[0].ReferencedSOPInstanceUID) + 1)
    #
    #                             roi_contour = np.vstack((contour_indexing[:, 0:2],  contour_indexing[0, 0:2]))
    #                             new_contour = np.array([roi_contour], dtype=np.int32)
    #                             image = np.zeros([rows, columns], dtype=np.uint8)
    #                             cv2.fillPoly(image, new_contour, 1)
    #
    #                             if slice_check[slice_num] == 0:
    #                                 mask[slice_num, :, :] = image
    #                                 slice_check[slice_num] = 1
    #                             else:
    #                                 mask[slice_num, :, :] = mask[slice_num, :, :] + image
    #
    #                     if np.sum(slice_check) > 0:
    #                         label = numpy_support.numpy_to_vtk(num_array=np.asarray(mask).ravel(), deep=True,
    #                                                            array_type=vtk.VTK_FLOAT)
    #                         origin = corner_array
    #                         spacing = spacing_array
    #                         dim = [rows, columns, slices]
    #
    #                         img_vtk = vtk.vtkImageData()
    #                         img_vtk.SetDimensions(dim)
    #                         img_vtk.SetSpacing(spacing)
    #                         img_vtk.SetOrigin(origin)
    #                         img_vtk.GetPointData().SetScalars(label)
    #
    #                         MarchingCubeFilter = vtk.vtkDiscreteMarchingCubes()
    #                         MarchingCubeFilter.SetInputData(img_vtk)
    #                         MarchingCubeFilter.GenerateValues(1, 1, 1)
    #                         MarchingCubeFilter.Update()
    #
    #                         smoothing_iterations = 20
    #                         pass_band = 0.001
    #                         feature_angle = 60.0
    #                         smoother = vtk.vtkWindowedSincPolyDataFilter()
    #                         smoother.SetInputConnection(MarchingCubeFilter.GetOutputPort())
    #                         smoother.SetNumberOfIterations(smoothing_iterations)
    #                         smoother.BoundarySmoothingOff()
    #                         smoother.FeatureEdgeSmoothingOff()
    #                         smoother.SetFeatureAngle(feature_angle)
    #                         smoother.SetPassBand(pass_band)
    #                         smoother.NonManifoldSmoothingOn()
    #                         smoother.NormalizeCoordinatesOff()
    #                         smoother.Update()

    def create_masks(self):
        """
        existing_image_info is required if the users only loads a RTSTRUCT file, because to make the mask the spacing
        and origin from the CT is needed.

        It is pretty gross after that. For a given ROI each contour is read-in, an empty full sized image array is
        created. Using cv2 the contours are converted to a binary slice, then all the slices are combined. To save
        memory allocation the binary mask is reduced to the minimum box size possible. Which is why the physical and
        array coordinates are stored. Physical means the distance location on the array in mm, and array is the
        voxel number the box first start on.

        Returns
        -------

        """
        info = self.image_info
        if self.existing_image_info:
            info.append(self.existing_image_info)

        for ii in range(len(info.index)):
            img_sop = info.at[ii, 'SOPInstanceUID']
            img_series = info.at[ii, 'SeriesInstanceUID']
            spacing_array = [info.at[ii, 'PixelSpacing'][0],
                             info.at[ii, 'PixelSpacing'][1],
                             info.at[ii, 'SliceThickness']]

            corner_array = [float(info.at[ii, 'ImagePositionPatient'][0]),
                            float(info.at[ii, 'ImagePositionPatient'][1]),
                            float(info.at[ii, 'ImagePositionPatient'][2])]

            rows = int(info.at[ii, 'Rows'])
            columns = int(info.at[ii, 'Columns'])
            slices = len(self.ds_images[ii])

            mask_com = []
            mask_volume = []
            mask_reduced = []
            roi_filepaths, roi_names = [], []
            physical_coordinates, array_coordinates = [], []
            for jj in range(len(self.rt_df.index)):
                if img_series == self.rt_df.at[jj, 'SeriesInstanceUID'] and self.rt_df.at[jj, 'RoiSOP'][0] in img_sop:
                    roi_sequence = self.ds_dictionary['RTSTRUCT'][jj].ROIContourSequence
                    for kk, sequence in enumerate(roi_sequence):
                        slice_check = np.zeros(slices)

                        r, col, s = [], [], []
                        mask = np.zeros([slices, rows, columns], dtype=np.uint8)
                        for c in sequence.ContourSequence:
                            if int(c.NumberOfContourPoints) > 1:
                                contour_hold = np.round(np.array(c['ContourData'].value), 3)
                                contour = contour_hold.reshape(int(len(contour_hold) / 3), 3)

                                contour_indexing = np.round(np.abs((contour - corner_array) / spacing_array))
                                slice_num = slices - \
                                            (img_sop.index(c.ContourImageSequence[0].ReferencedSOPInstanceUID) + 1)

                                roi_contour = np.vstack((contour_indexing[:, 0:2],  contour_indexing[0, 0:2]))
                                new_contour = np.array([roi_contour], dtype=np.int32)
                                image = np.zeros([rows, columns], dtype=np.uint8)
                                cv2.fillPoly(image, new_contour, 1)

                                if slice_check[slice_num] == 0:
                                    mask[slice_num, :, :] = image
                                    slice_check[slice_num] = 1
                                else:
                                    mask[slice_num, :, :] = mask[slice_num, :, :] + image

                                x1, y1, x2, y2 = cv2.boundingRect(image)
                                r.append(x1)
                                r.append(x1+x2)
                                col.append(y1)
                                col.append(y1+y2)
                                s.append(slice_num)

                        if len(s) > 0:
                            region = [np.min(s), np.max(s)+1,
                                      np.min(col), np.max(col),
                                      np.min(r), np.max(r)]

                            new_mask = mask[region[0]:region[1], region[2]:region[3], region[4]:region[5]]
                            if new_mask.size > 1:
                                roi_filepaths.append(self.rt_df.at[jj, 'FilePath'])
                                roi_names.append(self.rt_df.RoiNames[jj][kk])

                                physical_coordinates.append([(region[0]*spacing_array[2]) + corner_array[2],
                                                             (region[2]*spacing_array[1]) + corner_array[1],
                                                             (region[4]*spacing_array[0]) + corner_array[0]])
                                array_coordinates.append([[region[0], region[1]],
                                                          [region[2], region[3]],
                                                          [region[4], region[5]]])

                                new_mask_sitk = sitk.GetImageFromArray(new_mask)
                                new_mask_sitk.SetSpacing(spacing_array)
                                new_mask_sitk.SetOrigin(physical_coordinates[-1])

                                label_statistic = sitk.LabelShapeStatisticsImageFilter()
                                label_statistic.Execute(new_mask_sitk)
                                mask_com.append(np.round(label_statistic.GetCentroid(1), 2))

                                volume = np.sum(new_mask) * spacing_array[0] * spacing_array[1] * spacing_array[2]
                                mask_volume.append(np.round(volume/(10*10*10), 2))
                                mask_reduced.append(new_mask)

            if len(mask_reduced) > 0:
                self.roi_mask.append(mask_reduced)
                self.roi_info.at[ii, 'FilePath'] = roi_filepaths
                self.roi_info.at[ii, 'RoiNames'] = roi_names
                self.roi_info.at[ii, 'PhysicalCoordinates'] = physical_coordinates
                self.roi_info.at[ii, 'ArrayCoordinates'] = array_coordinates
                self.roi_info.at[ii, 'Volume'] = mask_volume
                self.roi_info.at[ii, 'COM'] = mask_com
            else:
                self.roi_mask.append(mask_reduced)
                self.roi_info.at[ii, 'FilePath'] = None
                self.roi_info.at[ii, 'RoiNames'] = None
                self.roi_info.at[ii, 'PhysicalCoordinates'] = None
                self.roi_info.at[ii, 'ArrayCoordinates'] = None
                self.roi_info.at[ii, 'Volume'] = None
                self.roi_info.at[ii, 'COM'] = None

    def get_image_info(self):
        return self.image_info

    def get_image_data(self):
        return self.image_data

    def get_roi_contour(self):
        return self.roi_contour

    def get_roi_mask(self):
        return self.roi_mask

    def get_roi_trimesh(self):
        return self.roi_trimesh

    def get_roi_info(self):
        return self.roi_info

    def get_ds_images(self):
        return self.ds_images


def main():
    from parsar import file_parsar

    path = r'C:\Users\csoconnor\Desktop\read_test_3'
    files = file_parsar(path, [])
    dicom_reader = DicomReader(files['Dicom'], None)
    dicom_reader.load_dicom()

    print(1)


if __name__ == '__main__':
    main()
