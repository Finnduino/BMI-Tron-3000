# BIM-Tron-3000
 
##Get started

Hey, welcome to BIMTron 3000! 
To get started, clone this repo, and install dependencies using 'pip install -r requirements.txt'

Currently, there are multiple ways of loading a model.
1. Using the file loader (only pngs at this moment). This uses an ML model to predict the building layout and dynamically constructs a 3D layout. 
2. Using the manual loader. In this context, you load in any image of your choice, and produce an outline yourself. The rest is taken of automagically.
3. Using a pre-existing model via the demo button.


It is imperative you select an elevator BEFORE selecting a world. Once you have selected both, you can load in the scene using the load button in the top left corner. 

Within the scene, there is an intuitive interface to place and manipulate the elevator. Use M2 to look around, zoom with scroll, and translate your location by moving your mouse while holding down M3.

Once you have finished placing the elevator, you can save the files and find them in the project directory.
