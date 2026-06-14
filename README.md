CS661 Assignment 1 - Isocontour and Volume Visualization - Group Number: 18
--------------------------------------------------------
PREREQUISITES
--------------------------------------------------------

Requirements:
    - Python 3.x
    - VTK Library

Install VTK using:
    pip install vtk

--------------------------------------------------------
FOLDER / FILE STRUCTURE
--------------------------------------------------------

Run all scripts from the submission folder. Maintain
the following directory structure:

    [submission folder]/
    ├── isocontour_2d.py
    ├── volume_rendering.py
    ├── README.txt
    └── Data/
        ├── Isabel_2D.vti      <- Required for Task 1
        └── Isabel_3D.vti      <- Required for Task 2

Both scripts use hardcoded paths (Data/Isabel_2D.vti
and Data/Isabel_3D.vti), so run them from the folder
that contains the Data/ directory.

--------------------------------------------------------
TASK 1: 2D ISOCONTOUR EXTRACTION
--------------------------------------------------------

Script      : isocontour_2d.py
Input File  : Data/Isabel_2D.vti
Output File : isocontour_<isovalue>.vtp

How to Run:
    python isocontour_2d.py <isovalue>

Arguments:
    <isovalue>
        Floating-point isovalue for contour extraction.
        Valid range for this dataset: [-1438, 630]

Examples:
    python isocontour_2d.py 100      ->  isocontour_100.0.vtp
    python isocontour_2d.py -500     ->  isocontour_-500.0.vtp
    python isocontour_2d.py 0.0      ->  isocontour_0.0.vtp

--------------------------------------------------------
TASK 2: VOLUME RENDERING WITH TRANSFER FUNCTIONS
--------------------------------------------------------

Script      : volume_rendering.py
Input File  : Data/Isabel_3D.vti
Output      : Interactive 1000 x 1000 VTK render window

How to Run:
    python volume_rendering.py <use_phong_shading>

Arguments:
    <use_phong_shading>
        Controls whether Phong shading is enabled.
        Accepted values (case-sensitive):
            yes  ->  Enable Phong shading
            no   ->  Disable Phong shading

Examples:
    python volume_rendering.py yes
    python volume_rendering.py no

--------------------------------------------------------
END OF README
--------------------------------------------------------
