import sys
import vtk

def volume_render(input_file, use_phong_shading):

    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    
    volumeData = reader.GetOutput()
    
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
    
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(ctf)
    volumeProperty.SetScalarOpacity(otf)
    volumeProperty.SetInterpolationTypeToLinear()
  
    if use_phong_shading:
        volumeProperty.ShadeOn()
        #Phong shading parameters
        volumeProperty.SetAmbient(0.5)
        volumeProperty.SetDiffuse(0.5)
        volumeProperty.SetSpecular(0.5)
    else:
        volumeProperty.ShadeOff()
    
    #volume mapper
    mapper = vtk.vtkSmartVolumeMapper()
    mapper.SetInputData(volumeData)
    
    #volume actor
    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)
    volume.SetProperty(volumeProperty)
    
    #outline filter
    outlineFilter = vtk.vtkOutlineFilter()
    outlineFilter.SetInputData(volumeData)
    outlineFilter.Update()
    
    #mapper for the outline
    outlineMapper = vtk.vtkPolyDataMapper()
    outlineMapper.SetInputConnection(outlineFilter.GetOutputPort())
    
    #outline actor
    outlineActor = vtk.vtkActor()
    outlineActor.SetMapper(outlineMapper)
    outlineActor.GetProperty().SetColor(0, 0, 0)  #black outline
    

    #renderer 
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.95, 0.95, 0.95)  # White background
    renderer.AddActor(volume)
    renderer.AddActor(outlineActor)
    renderer.ResetCamera()
    
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(1000, 1000)  #windoe size
    renderWindow.AddRenderer(renderer)
    
    #Interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)
    
    #Display
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
    elif use_phong_input =='no' :
        use_phong = False
    else:
        print("Error: put yes/no for phong shading")
        sys.exit(1)
    
    input_file = "Data/Isabel_3D.vti"
    
    print("Rendering")
    volume_render(input_file, use_phong)
