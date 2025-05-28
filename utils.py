import pydicom
import highdicom
import os
import numpy as np
from skimage.filters import threshold_otsu
from scipy.ndimage import binary_opening
from skimage import measure


def load_ct(name):
    return pydicom.dcmread(name)

def load_segmentation(name):
    return highdicom.seg.segread(name)

def load_ct_series(dicom_folder):
    ct_slices = []
    acc_number = []
    slice_locations_sorted = []

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
    slice_locations_sorted = [s.SliceLocation if hasattr(s, 'SliceLocation') else None for s in ct_slices]

    print(f"The reference CT volume has a shape of: {ct_volume.shape}")

    return ct_volume, slice_positions, acc_number, slice_locations_sorted

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

def dist_to_center(region, volume_shape):
    volume_center = np.array(volume_shape) / 2
    return np.linalg.norm(np.array(region.centroid) - volume_center)

def segment_body(ct_volume):
    flattened = ct_volume.flatten()
    otsu_thresh = threshold_otsu(flattened)
    print(f"Umbral de Otsu: {otsu_thresh}")
    binary_mask = ct_volume > otsu_thresh

    structure = np.ones((3, 3, 3))
    mask_opened = binary_opening(binary_mask, structure=structure)

    labeled_mask, _ = measure.label(mask_opened, connectivity=3, return_num=True)

    regions = measure.regionprops(labeled_mask)
    filtered_regions = [r for r in regions if r.area > 5000]

    body_region = min(filtered_regions, key=lambda r: dist_to_center(r, ct_volume.shape))
    body_mask = (labeled_mask == body_region.label)

    return body_mask
def apply_body_mask(ct_volume, body_mask):
    body_mask = body_mask.astype(bool)
    ct_volume = np.where(body_mask, ct_volume, -1000)
    return ct_volume

def apply_windowing(image, level, width):
    lower = level - width / 2
    upper = level + width / 2
    return np.clip(image, lower, upper)