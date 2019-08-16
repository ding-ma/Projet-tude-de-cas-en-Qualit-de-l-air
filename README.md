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
