import pydicom
import highdicom
import os
import numpy as np

def load_ct(name):
    return pydicom.dcmread(name)

def load_segmentation(name):
    return highdicom.seg.segread(name)

def load_ct_series(dicom_folder):
    ct_slices = []
    acc_number = []

    for f in os.listdir(dicom_folder):
        dcm = load_ct(os.path.join(dicom_folder, f))
        if hasattr(dcm, 'ImagePositionPatient'):
            ct_slices.append(dcm)
        if hasattr(dcm, 'AcquisitionNumber'):
            acc_number.append(dcm.AcquisitionNumber)

    ct_slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
    ct_volume = np.stack([slice.pixel_array for slice in ct_slices], axis=0)

    slice_positions = [f.ImagePositionPatient[2] for f in ct_slices]
    sorted_indices = np.argsort(slice_positions)
    ct_volume = ct_volume[sorted_indices]

    print(f"The reference CT volume has a shape of: {ct_volume.shape}")

    return ct_volume, slice_positions, acc_number

def load_pixelarray_positions(seg):
    seg_array = seg.pixel_array
    seg_pos = []
    for slice in seg.PerFrameFunctionalGroupsSequence:
        pos = slice.PlanePositionSequence[0].ImagePositionPatient[2]
        seg_pos.append(pos)  # Use Z axis
    return seg_array, seg_pos

def reslice_segmentations(shape,segmentation_positions, slice_positions, seg_data, label_value):
    seg_volume = np.zeros(shape, dtype=np.uint8)
    for id, seg in enumerate(segmentation_positions):
        ct_idx = np.argmin(np.abs(np.array(slice_positions) - np.array(seg)))
        mask = mask = np.where(seg_data[id])
        seg_volume[ct_idx][mask]= label_value
    return seg_volume