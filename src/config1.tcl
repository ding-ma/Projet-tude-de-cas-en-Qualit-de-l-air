
#set Data(SpLst)      "UU" 
set Data(SpLst)      "O3" 
#set Data(SpLst)      "GZ" 


### Tag name for FST file
#set Data(TAG1)   "INTERPb_UU"
set Data(TAG1)   "TEST.201904_201904_regeta"
#set Data(TAG1)   "INTERPb_GZ"


set Data(TAG3)   "First"
##--Output files.
set Data(outTXT)       "SITE" 

## --- vertical level :12001 12040 12079
#set Data(levels) "1000.0 994.0 925.0 850.0 700.0 500.0 400.0 300.0 250.0 200.0 150.0 100.0 70.0 50.0 30.0 20.0 10.0"
set Data(levels) "93423264 76696048"

#set Data(MandatoryLevels) "10000 9940 9250 8500 7000 5000 4000 3000 2500 2000 1500 1000 700 500 300 200 100"
set Data(MandatoryLevels) "93423264 76696048"
                          
###-- Path for FST file. 
set Data(Path)    /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach
#set Data(Path) /cnfs/dev/regions/que/afqsfrc/Requete_ETS/EDITFST/
set Data(PathOut) /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach

##-- Start and end dates
set Data(Start)      "201904"
set Data(End)        "201904"

##-- Eticket 
#set Data(Eticket)      "R3D28V4N"
#set Data(Eticket)      "R3D80V4N"
#set Data(Eticket)      "R1080V3N"
set Data(Eticket)     "RAQDPS020"
#set Data(Eticket)     "R1_V410_N"
#set Data(Eticket)      "R110K80N"

# Define CA cities and their lat lon coordinates 
# CITY       Lat     Lon   

set Data(point) "Dorval"
set Data(coord) "45.47 -73.74"

# Les jours et les heures de la journee
#set Data(days) "19 20 21 22 23 24 25 26 27 28 29 30 31"
#set Data(days)  "01 02 03 04 05 06 07 08 09 10 11 12 13 14 15"
set Data(days) "05"
#set Data(days) "01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31"
#set Data(hours) "00"
#set Data(hours) "00 12"
set Data(hours) "01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23"
