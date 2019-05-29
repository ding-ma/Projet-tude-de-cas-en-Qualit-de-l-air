# 1. TT, UU, WW
#set Data(SpLst)      "TT UU WW"
# 2. P0, HR, TCC
set Data(SpLst)      "P0 HR TCC"
#set Data(SpLst)      "TT UU WW P0 HR TCC"

### Tag name for FST file
set Data(TAG1)   "TEST2"
# 1 ou 2


set Data(TAG3)   "Surface_Heures" 
##--Output files.
set Data(outTXT)       "TEST" 

## --- vertical level :12001 12040 12079
set Data(levels) "12000"
 
###-- Path for FST file. 
set Data(Path)       /cnfs/dev/regions/que/rio/Requete_ETS/EDITFST/operation.forecasts.regeta
#set Data(Path) /cnfs/dev/regions/que/afqsfrc/Requete_ETS/EDITFST/
#set Data(PathOut) /fs/cetus/fs4/aq/afsumeh/dev_aq01/Extraction_CRIAQ/EDITFST/operation.forecasts.regeta
set Data(PathOut) /cnfs/dev/regions/que/rio/Requete_ETS/EDITFST/operation.forecasts.regeta


##-- Start and end dates
set Data(Start)      "201512"
set Data(End)        "201512"

# Define CA cities and their lat lon coordinates 
# CITY       Lat     Lon   

set Data(point) "Longueuil"
set Data(coord) "45.5 -73.50"

# Les jours et les heures de la journee
set Data(days) "01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31"
#set Data(days) "01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28"
#set Data(days) "01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30"
# Pour 2016 bissextile
#set Data(days) "01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29"