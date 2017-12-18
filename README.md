# abc_add_custom_attribute
This is a sciprt to export abc file with custom attribute in vertex scope for selected mesh in maya scene.


How to excute?

1. Select mesh in maya scene

2. Excute python command below:
	from abc_add_custom_attribute.maya.export import main
	main()

3. Then it will export abc file for each mesh you selected. 
   The abc file will save to your current workspace.