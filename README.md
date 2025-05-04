# Final Project - 11763 Medical Image Processing

This project addresses tasks related to 3D medical imaging and analysis using DICOM data. The three main objectives are: 
- Loading and visualizing DICOM IMAGES.
- Performing 3D Image Segmentation.
- Performing 3D Rigid Coregistration. 

## 🛠 Tools & Libraries

- 3D Slicer: Visualization of DICOM series. 
- Python: 
    - PyDicom
    - HighDicom
    - Numpy
    - Matplotlib
    - OS
    - Scipy
    - OpenCV

## 📂 File Structure
- Constants.py :  Contains the paths to the Reference Image, Input Image and the ROI Masks.
- Utils.py: Contains functions for loading the CT slices and Masks, constructing the CT volumes and reslicing the segmentation. 
- Objective1_Load.ipynb: Contains the solution for the first Objective.
- Objective2_Segmentation.ipynb: Contains the solution for the second Objective.
- Objective3_Coregistration.ipynb: Contains the solution for the third objective. 

- results/ 
    - MIP/
        - AlphaCoronal/ Contains projections and rotating MIP of the Coronal Plane with the masks.
        - AlphaSagittal/  Contains projections and rotating MIP of the Sagittal Plane with the masks.
        - Coronal/  Contains projections and rotating MIP of the Coronal Plane.
        - Sagittal/  Contains projections and rotating MIP of the Sagittal Plane.

## Objectives Completed