import sys
import vtk

def volume_render(input_file, use_phong_shading):

    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    
    volume_data = reader.GetOutput()
    
    #color transfer function
    ctf = vtk.vtkColorTransferFunction()
    
    ctf.AddRGBPoint(-4931.54, 0, 1, 1)   
    ctf.AddRGBPoint(-2508.95, 0, 0, 1)   
    ctf.AddRGBPoint(-1873.9, 0, 0, 0.5)    
    ctf.AddRGBPoint(-1027.16, 1, 0, 0)  
    ctf.AddRGBPoint(-298.031, 1, 0.4, 0)   
    ctf.AddRGBPoint(2594.97, 1, 1, 0)      
    
    #opacity transfer function
    otf = vtk.vtkPiecewiseFunction()
    
    # Data Value, Opacity Value
    otf.AddPoint(-4931.54, 1.0)
    otf.AddPoint(101.815, 0.002)
    otf.AddPoint(2594.97, 0.0)
    
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(ctf)
    volume_property.SetScalarOpacity(otf)
    volume_property.SetInterpolationTypeToLinear()
  
    if use_phong_shading:
        volume_property.ShadeOn()
        #Phong shading parameters
        volume_property.SetAmbient(0.5)
        volume_property.SetDiffuse(0.5)
        volume_property.SetSpecular(0.5)
    else:
        volume_property.ShadeOff()
    
    #volume mapper
    mapper = vtk.vtkSmartVolumeMapper()
    mapper.SetInputData(volume_data)
    
    #volume actor
    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)
    volume.SetProperty(volume_property)
    
    #outline filter
    outline_filter = vtk.vtkOutlineFilter()
    outline_filter.SetInputData(volume_data)
    outline_filter.Update()
    
    #mapper for the outline
    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline_filter.GetOutputPort())
    
    #outline actor
    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)
    outline_actor.GetProperty().SetColor(0, 0, 0)  #black outline
    

    #renderer 
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.95, 0.95, 0.95)  # White background
    renderer.AddActor(volume)
    renderer.AddActor(outline_actor)
    renderer.ResetCamera()
    
    render_window = vtk.vtkRenderWindow()
    render_window.SetSize(1000, 1000)  #windoe size
    render_window.AddRenderer(renderer)
    
    #Interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    
    #Display
    render_window.Render()
    interactor.Start()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("How to use: python volume_rendering.py <use_phong_shading>")
        print("Example: python volume_rendering.py yes/no")
        sys.exit(1)
    
    use_phong_input = sys.argv[1]
    
    if use_phong_input== 'yes':
        use_phong = True
    elif use_phong_input =='no' :
        use_phong = False
    else:
        print("Error: put yes/no for phong shading")
        sys.exit(1)
    
    input_file = "Data/Isabel_3D.vti"
    
    print("Rendering")
    volume_render(input_file, use_phong)
