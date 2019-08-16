# Automatic Image and Data Extractor (AIDE)
This is the big project of my summer 19 internship at Environment Canada. It is a GUI tool that helps users extract data from archives easily.

# Programming languages
* SQL, extracting observation data
* Bash/TCL, extracting model data
- Used inhouse librairies to deal with .fst weather files
* Python3, main building block and GUI
- I used Tkinter as the GUI, and Pandas/CSV module to write files.

# Biggest Challenges
* Try to improve code reusability
* Making a simple UI while maintaining an optimal runtime. 
- For instance, Gemmach model files required an additional step before extracting data. However, I had to merge two scripts into one in order to only have one button.
* Designing an beautiful UI is hard
* I was limited to the program versions on the CMC servers.

# What I have learned
* Using libraries efficiently. For instance, I was writing functions to generate date lists but I can just use the datetime librarie to do that for me. 
* Designing a big project such as separating the UI and the number crunching part.

# What I should of done differently
Looking back to the code, there is a lot of repeating code even with the clean ups I have done. At the start of the project, we thought that every model has to be treated seperatly with different libraries and such. Thus, this is why they all have seperate files. The initial reasonning of making a file per model type is to ease later modifications.
I should of have a module for the UI, one for Observation, one for images,one for Umos, and one for Gemmach/Firework/Umos-mist. The code for Gemmach/FireWork/Umos-mist are really similar and the code could be reused with additional parameters.
Later modifications should include a complete architecture redesign such as a module for extracting, a module for script writing, and a module for calculations. There are different ways to redesign the program's architecture in order to make it more efficient. 
