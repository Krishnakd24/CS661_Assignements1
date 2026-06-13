CS661 Assignment 1 - Isocontour and Volume Visualization
Group Number: [YOUR GROUP NUMBER]
========================================================

PREREQUISITES
========================================================

Requirements:
    - Python 3.x
    - VTK Library

Install VTK using:

    pip install vtk


FOLDER / FILE STRUCTURE
========================================================

Place the scripts and datasets as shown below before running:

    [submission folder]/
    ├── isocontour_2d.py
    ├── volume_rendering.py
    ├── README.txt
    └── Data/
        ├── Isabel_2D.vti      <- Required for Task 1
        └── Isabel_3D.vti      <- Required for Task 2

NOTE:
    Both scripts use hardcoded dataset paths:

        Data/Isabel_2D.vti
        Data/Isabel_3D.vti

    Run the scripts from the same directory that contains
    the Data/ folder.


TASK 1: 2D ISOCONTOUR EXTRACTION
========================================================

Script      : isocontour_2d.py
Input File  : Data/Isabel_2D.vti
Output File : isocontour_<isovalue>.vtp

Description:
    Extracts an isocontour from a 2D uniform grid containing Hurricane
    Simulation pressure data. The algorithm traverses each cell's four
    vertices in counterclockwise order starting from the bottom edge,
    detects edge crossings via linear interpolation, and connects them
    into line segments stored as a VTK PolyData (.vtp) file.

How to Run:

    python isocontour_2d.py <isovalue>

Arguments:

    <isovalue>
        Floating-point isovalue for contour extraction.
        Valid range for this dataset: -1438 to 630

Examples:

    python isocontour_2d.py 100
    python isocontour_2d.py -500
    python isocontour_2d.py 0.0

--------------------------------------------------------
Output File Naming
--------------------------------------------------------

The output .vtp file is named after the supplied isovalue:

    python isocontour_2d.py 100     ->   isocontour_100.0.vtp
    python isocontour_2d.py -500    ->   isocontour_-500.0.vtp

--------------------------------------------------------
Console Output
--------------------------------------------------------

The script prints:

    - Isovalue being processed
    - Input file path
    - Number of line segments created
    - Total number of points in the output polydata
    - Path of the generated .vtp file

--------------------------------------------------------
Viewing the Output in ParaView
--------------------------------------------------------

    1. Open ParaView.
    2. File -> Open -> select the generated .vtp file.
    3. Click "Apply" in the Properties panel.
    4. If the contour is hard to see against a white background,
       change the color to black or red via Properties -> Coloring.


TASK 2: VOLUME RENDERING WITH TRANSFER FUNCTIONS
========================================================

Script      : volume_rendering.py
Input File  : Data/Isabel_3D.vti
Output      : Interactive 1000 x 1000 VTK render window

Description:
    Performs direct volume rendering on a 3D Hurricane Simulation pressure
    dataset using vtkSmartVolumeMapper. Applies the color and opacity
    transfer functions specified below, adds a bounding box outline via
    vtkOutlineFilter, and opens an interactive render window.
    Phong shading can be enabled or disabled via a command-line argument.

How to Run:

    python volume_rendering.py <use_phong_shading>

Arguments:

    <use_phong_shading>
        Controls whether Phong shading is enabled.
        Accepted values (case-insensitive):

            yes   ->  Enable Phong shading
            no    ->  Disable Phong shading

Examples:

    python volume_rendering.py yes
    python volume_rendering.py no

--------------------------------------------------------
Render Window Controls
--------------------------------------------------------

    Left Mouse Button  + Drag  ->  Rotate the volume
    Right Mouse Button + Drag  ->  Zoom
    Middle Mouse Button + Drag ->  Pan
    Close Window               ->  Exit the program

--------------------------------------------------------
Console Output
--------------------------------------------------------

The script prints:

    - Input file path
    - Phong shading status (ENABLED / DISABLED)
    - If shading is enabled:
          Ambient Coefficient  : 0.5
          Diffuse Coefficient  : 0.5
          Specular Coefficient : 0.5
    - Confirmation that the opacity transfer function was created
    - Confirmation that the Smart Volume Mapper was created
    - Confirmation that the outline was created
    - Render window size (1000 x 1000)
    - "Rendering..." when rendering begins


========================================================
REFERENCE SPECIFICATIONS
========================================================

--------------------------------------------------------
Color Transfer Function
--------------------------------------------------------

    +------------+-------+-------+-------+------------+
    | Data Value |   R   |   G   |   B   |   Color    |
    +------------+-------+-------+-------+------------+
    | -4931.54   |  0.0  |  1.0  |  1.0  | Cyan       |
    | -2508.95   |  0.0  |  0.0  |  1.0  | Blue       |
    | -1873.90   |  0.0  |  0.0  |  0.5  | Dark Blue  |
    | -1027.16   |  1.0  |  0.0  |  0.0  | Red        |
    |  -298.031  |  1.0  |  0.4  |  0.0  | Orange     |
    |  2594.97   |  1.0  |  1.0  |  0.0  | Yellow     |
    +------------+-------+-------+-------+------------+

--------------------------------------------------------
Opacity Transfer Function
--------------------------------------------------------

    +------------+---------+
    | Data Value | Opacity |
    +------------+---------+
    | -4931.54   |  1.000  |
    |   101.815  |  0.002  |
    |  2594.97   |  0.000  |
    +------------+---------+

--------------------------------------------------------
Phong Shading Parameters
--------------------------------------------------------

Applied only when shading is enabled:

    Ambient Coefficient   : 0.5
    Diffuse Coefficient   : 0.5
    Specular Coefficient  : 0.5


END OF README
========================================================
