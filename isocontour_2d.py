import vtk
import sys


def lin_interpol(p1, p2, val1, val2, isoval):
    
    if abs(val2 - val1) < 1e-10:
        # If values are same, return midpoint
        return [(p1[i] + p2[i]) / 2.0 for i in range(3)]
    
    #Parameter t where the crossing happens
    t = (isoval - val1) / (val2 - val1)
    
    # Linearly Interpolate the position
    crossing_point = [p1[i] + t * (p2[i] - p1[i]) for i in range(3)]
    return crossing_point
    #Chnage the loop


def extract_isocontour(inputFile, isoval, outputFile):
    
    # Read the input VTI file
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(inputFile)
    reader.Update()
    
    imageData = reader.GetOutput()
    
    # Get the scalar data
    scalars = imageData.GetPointData().GetScalars()
    
    # Get grid dimensions
    dims = imageData.GetDimensions()

    # Create output polyData
    points = vtk.vtkPoints()
    cells = vtk.vtkCellArray()
    
    # Counter for line segments
    segments = 0
    
    # Iterate through all cells (quads in 2D)
    for j in range(dims[1] - 1):
        for i in range(dims[0] - 1):
            # Get the 4 corners of the cell (counterclockwise from bottom-left)
            # Bottom-left, Bottom-right, Top-right, Top-left
            idx0 = j * dims[0] + i              # Bottom-left
            idx1 = j * dims[0] + (i + 1)        # Bottom-right
            idx2 = (j + 1) * dims[0] + (i + 1)  # Top-right
            idx3 = (j + 1) * dims[0] + i        # Top-left
            
            # Get coordinates of the 4 corners
            p0 = imageData.GetPoint(idx0)
            p1 = imageData.GetPoint(idx1)
            p2 = imageData.GetPoint(idx2)
            p3 = imageData.GetPoint(idx3)
            
            # Get scalar values at the 4 corners
            val0 = scalars.GetValue(idx0)
            val1 = scalars.GetValue(idx1)
            val2 = scalars.GetValue(idx2)
            val3 = scalars.GetValue(idx3)
            
            # Determine which edges cross the isoval
            # We traverse counterclockwise from the bottom edge
            # Edges: bottom (0-1), right (1-2), top (2-3), left (3-0)
            
            crossings = []  # List to store crossing points on edges
            
            # Bottom edge (0 -> 1)
            if (isoval - val0) * (isoval - val1) < 0:
                cross_pt = lin_interpol(p0, p1, val0, val1, isoval)
                crossings.append(cross_pt)
            
            # Right edge (1 -> 2)
            if (isoval - val1) * (isoval- val2) < 0:
                cross_pt = lin_interpol(p1, p2, val1, val2, isoval)
                crossings.append(cross_pt)
            
            # Top edge (2 -> 3)
            if (isoval-val2) * (isoval-val3) < 0:
                cross_pt = lin_interpol(p2, p3, val2, val3, isoval)
                crossings.append(cross_pt)
            
            # Left edge (3 -> 0)
            if (isoval-val3) * (isoval-val0) < 0:
                cross_pt = lin_interpol(p3, p0, val3, val0, isoval)
                crossings.append(cross_pt)
            
            # Create line segments from crossing points
            # Typically we get 0, 2, or 4 crossing points
            if len(crossings) == 2:
                # Create a line segment
                pt_1 = points.InsertNextPoint(crossings[0])
                pt_2 = points.InsertNextPoint(crossings[1])
                
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, pt_1)
                line.GetPointIds().SetId(1, pt_2)
                
                cells.InsertNextCell(line)
                segments += 1
            
            elif len(crossings) == 4:
                # Create two line segments
                # Connect crossings in order: 0-1 and 2-3
                pt_1 = points.InsertNextPoint(crossings[0])
                pt_2 = points.InsertNextPoint(crossings[1])
                pt_3 = points.InsertNextPoint(crossings[2])
                pt_4 = points.InsertNextPoint(crossings[3])
                
                line1 = vtk.vtkLine()
                line1.GetPointIds().SetId(0, pt_1)
                line1.GetPointIds().SetId(1, pt_2)
                cells.InsertNextCell(line1)
                
                line2 = vtk.vtkLine()
                line2.GetPointIds().SetId(0, pt_3)
                line2.GetPointIds().SetId(1, pt_4)
                cells.InsertNextCell(line2)
                
                segments += 2
    
    # Create the polyData
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.SetLines(cells)
    
    print(f"Number of line segments created: {segments}")
    print(f"Total points in output: {points.GetNumberOfPoints()}")
    
    # Write to VTP file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(outputFile)
    writer.SetInputData(polyData)
    writer.Write()
    
    print(f"Isocontour written to: {outputFile}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python isocontour_2d.py <isoval>")
        print("Example: python isocontour_2d.py 100")
        sys.exit(1)
    
    try:
        isoval = float(sys.argv[1])
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid number")
        sys.exit(1)
    
    inputFile = "Data/Isabel_2D.vti"
    outputFile = f"isocontour_{isoval}.vtp"
    
    print(f"Extracting isocontour for isoval: {isoval}")
    print(f"Input file: {inputFile}")
    
    extract_isocontour(inputFile, isoval, outputFile)
