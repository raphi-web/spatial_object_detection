
Python script that creates a generic startingpoint that can be used for 
object identification with darknet. 


1) Folders:
    1 - inputs -> inputs for python script
    2 - outputs -> outputs of python script
    3 - static_data -> contains config and weight data do not modify, modify the
    	.cfg-file in the output

2) Copy the images you want to analize and the inputs folder 

3) Copy the labels you created in yolo.txt format to the inputs folder
   labels should have the same name as image file (img1.jpg, img1.txt ...) 
   
   * you can use this for labeling:
     https://github.com/tzutalin/labelImg

4. Execute the py file, only standard library dependencies
   $ python3 wrap.py

   it will ask you for a project name, that name is used to create a folder
   inside "outputs".

5. After its finished a commandline string is given out, 
   copy the project in "outputs" to the darknet folder 

   Open the darknet folder inside the terminal 
   if all is well you can execute the commandline string that wrap.py generated
   inside the terminal and the learning should start.
   
   
 
** Edit: Removed numpy and pandas depandancy
   Only use images with matching label files
   
