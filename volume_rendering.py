import sys
import vtk

# Function to perform volume rendering with color and opacity transfer functions
def volume_render(input_file, use_phong_shading):

    """
    Args:
        input_file: Path to the VTK ImageData file (.vti)
        use_phong_shading: Boolean indicating whether to enable Phong shading
    """
    
  
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    
    volumeData = reader.GetOutput()
    
   #Creating Color transfer function
    ctf = vtk.vtkColorTransferFunction()
    
    ctf.AddRGBPoint(-4931.54, 0, 1, 1)   
    ctf.AddRGBPoint(-2508.95, 0, 0, 1)   
    ctf.AddRGBPoint(-1873.9, 0, 0, 0.5)    
    ctf.AddRGBPoint(-1027.16, 1, 0, 0)  
    ctf.AddRGBPoint(-298.031, 1, 0.4, 0)   
    ctf.AddRGBPoint(2594.97, 1, 1, 0)      
    
    #Opacity transfer function
    otf = vtk.vtkPiecewiseFunction()
    
    # Data Value, Opacity Value
    otf.AddPoint(-4931.54, 1.0)
    otf.AddPoint(101.815, 0.002)
    otf.AddPoint(2594.97, 0.0)
    
    # Create volume property and apply transfer functions
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(ctf)
    volumeProperty.SetScalarOpacity(otf)
    volumeProperty.SetInterpolationTypeToLinear()
  
    # Set up Phong shading if requested by user
    if use_phong_shading:
        volumeProperty.ShadeOn()
        #Phong shading parameters
        volumeProperty.SetAmbient(0.5)
        volumeProperty.SetDiffuse(0.5)
        volumeProperty.SetSpecular(0.5)
    else:
        volumeProperty.ShadeOff()
    
    # Create smart volume mapper for efficient volume rendering
    mapper = vtk.vtkSmartVolumeMapper()
    mapper.SetInputData(volumeData)
    
    #Create Volume actor
    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)
    volume.SetProperty(volumeProperty)
    
    # Create outline filter to show volume boundaries
    outlineFilter = vtk.vtkOutlineFilter()
    outlineFilter.SetInputData(volumeData)
    outlineFilter.Update()
    
    # Create mapper for the outline
    outlineMapper = vtk.vtkPolyDataMapper()
    outlineMapper.SetInputConnection(outlineFilter.GetOutputPort())
    
    #Outline actor
    outlineActor = vtk.vtkActor()
    outlineActor.SetMapper(outlineMapper)
    outlineActor.GetProperty().SetColor(0, 0, 0)  # Set outline color to black
    

    # Create renderer and set background color
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.95, 0.95, 0.95)  # Light gray background
    renderer.AddActor(volume)                 
    renderer.AddActor(outlineActor)           
    renderer.ResetCamera()                 
    
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(1000, 1000)  # Window size: 1000 x 1000 pixels
    renderWindow.AddRenderer(renderer)
    
    #Interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)
    
    # Render the scene and start interactive mode
    renderWindow.Render()
    interactor.Start()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("How to use: python volume_rendering.py <use_phong_shading>")
        print("Example: python volume_rendering.py yes/no")
        sys.exit(1)
    
    use_phong_input = sys.argv[1]
    
    if use_phong_input== 'yes':
        use_phong = True
        print("Phong Shading Status: ON")
    elif use_phong_input == 'no':
        use_phong = False
        print("Phong Shading Status: OFF")
    else:
        print("Error: Invalid input. Please enter 'yes' or 'no' for Phong shading parameter")
        sys.exit(1)
    
    # Set input file path
    input_file = "Data/Isabel_3D.vti"
    
    # Display rendering status to user
    print("Rendering Status: Starting volume rendering with the specified parameters...")
    volume_render(input_file, use_phong)
