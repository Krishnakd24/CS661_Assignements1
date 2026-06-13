import sys
import vtk

def volume_render(input_file, use_phong_shading):
    """
    Perform volume rendering on 3D scalar data with transfer functions
    """
    
    # Read the 3D VTI file
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    
    volume_data = reader.GetOutput()
    
    # Create color transfer function (CT)
    ctf = vtk.vtkColorTransferFunction()
    
    # Add color transfer function points (from assignment)
    # Data Value, Red, Green, Blue
    ctf.AddRGBPoint(-4931.54, 0, 1, 1)      # Cyan
    ctf.AddRGBPoint(-2508.95, 0, 0, 1)      # Blue
    ctf.AddRGBPoint(-1873.9, 0, 0, 0.5)     # Dark blue
    ctf.AddRGBPoint(-1027.16, 1, 0, 0)      # Red
    ctf.AddRGBPoint(-298.031, 1, 0.4, 0)    # Orange
    ctf.AddRGBPoint(2594.97, 1, 1, 0)       # Yellow
    
    # Create opacity transfer function (Piecewise)
    otf = vtk.vtkPiecewiseFunction()
    
    # Add opacity transfer function points (from assignment)
    # Data Value, Opacity Value
    otf.AddPoint(-4931.54, 1.0)
    otf.AddPoint(101.815, 0.002)
    otf.AddPoint(2594.97, 0.0)
    
    print("Opacity transfer function created")
    
    # Create volume property
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(ctf)
    volume_property.SetScalarOpacity(otf)
    volume_property.SetInterpolationTypeToLinear()
    
    # Set shading properties
    if use_phong_shading:
        volume_property.ShadeOn()
        # Set Phong shading parameters (from assignment)
        volume_property.SetAmbient(0.5)
        volume_property.SetDiffuse(0.5)
        volume_property.SetSpecular(0.5)
        print("Phong shading ENABLED")
        print(f"  Ambient: 0.5")
        print(f"  Diffuse: 0.5")
        print(f"  Specular: 0.5")
    else:
        volume_property.ShadeOff()
        print("Phong shading DISABLED")
    
    # Create volume mapper
    mapper = vtk.vtkSmartVolumeMapper()
    mapper.SetInputData(volume_data)
    
    print("Smart volume mapper created")
    
    # Create volume actor
    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)
    volume.SetProperty(volume_property)
    
    # Create outline filter for the volume
    outline_filter = vtk.vtkOutlineFilter()
    outline_filter.SetInputData(volume_data)
    outline_filter.Update()
    
    # Create mapper for the outline
    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline_filter.GetOutputPort())
    
    # Create outline actor
    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)
    outline_actor.GetProperty().SetColor(0, 0, 0)  # White color
    
    print("Outline created")
    
    # Create renderer and render window
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.95, 0.95, 0.95)  # Black background
    renderer.AddActor(volume)
    renderer.AddActor(outline_actor)
    renderer.ResetCamera()
    
    render_window = vtk.vtkRenderWindow()
    render_window.SetSize(1000, 1000)  # 1000x1000 sized render window
    render_window.AddRenderer(renderer)
    
    print("Render window created (1000x1000)")
    
    # Create interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    
    # Render and display
    print("Rendering...")
    render_window.Render()
    interactor.Start()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python volume_render.py <use_phong_shading>")
        print("Example: python volume_render.py yes")
        print("Example: python volume_render.py no")
        sys.exit(1)
    
    use_phong_input = sys.argv[1].lower()
    
    if use_phong_input== 'yes':
        use_phong = True
    elif use_phong_input =='no' :
        use_phong = False
    else:
        print(f"Error: '{sys.argv[1]}' is not valid. Please use 'yes' or 'no'")
        sys.exit(1)
    
    input_file = "Data/Isabel_3D.vti"
    
    print("=" * 50)
    print("3D Volume Rendering with VTK")
    print("=" * 50)
    print(f"Input file: {input_file}")
    print(f"Phong shading: {use_phong}")
    print("=" * 50)
    
    volume_render(input_file, use_phong)
