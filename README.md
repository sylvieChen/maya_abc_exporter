# abc_add_custom_attribute
This is a sciprt to export abc file with custom attribute in vertex scope for selected mesh in maya scene.


How to excute?

1. Select mesh in maya scene

2. Excute python command below:
	abc_exporter = MayaAbcExporter()
	abc_exporter.export_selected_mesh()

3. Then it will export abc file for each selected mesh. 
   Save abc file to current workspace directory.
