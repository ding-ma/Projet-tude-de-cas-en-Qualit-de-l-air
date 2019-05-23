#!/bin/sh
#
# : - \
    exec /ssm/net/cmoe/apps/SPI_7.10.1_all/tclsh "$0" "$@"
#    exec $SPI_PATH/tclsh "$0" "$@"
package require TclData

################################################################################ 
# Environnement et Changement Climatique Canada 
# SOP du Centre  
# 7810-800 rue de la Geuchetiere Ouest
# Montreal, QC 
#
# Projet    : Extraction des donnees meteologique pour l ETS
# 1: prend la valeur dans le premier niveaux pour chaque heure, et (2) extrait les valeurs en un point de grille pour les varaibe demandees.
#             Le site est supposee etre represente par ses coordonnees (lat lon). 
# 
# Nom du script   : Extract_Site_regeta.tcl
#
# Nom du fichier de configuration du script: config_Site_regeta.tcl
#
# Comment ca marche?: Extract_Site_regeta.tcl config_Site_regeta.tcl
#
# Creation  : Mehrez Samaali (March. 2017),
#
# Modification: Frederic Chagnon (March. 2017)
#
################################################################################

namespace eval AvgAllDom { } { 
    variable Data
    source [ lindex $argv 0 ]  
}

################################################################################  
#   procedure principale  
################################################################################

proc AvgAllDom::Do { sp outTXT start end} {
    
    variable Data
    
    ####### ############################# set ouput TXT files
    set FileOut $Data(PathOut)/$Data(TAG3)_${start}_$Data(point)_${sp}.txt
    file delete $FileOut
    
    # ouvrir le fichier FileOut pour des valeurs en format texte
    set fileId [ open $FileOut w 0644 ] 
    puts $fileId "AnMoisJour Heure Valeur"
    set anMois $start 
    puts $anMois
    
    ############ get and open the input .fst file
    set FileIn [ lsort -dictionary [ glob $Data(Path)/$Data(TAG1).${start}_${end}*.fst ] ]
    fstdfile open 1 read  $FileIn 
    
    ############ loop on months
    
    while { $anMois <= $end } {
        
        set Mois [ string range $anMois 4 5 ]
        puts " mois =$Mois"
        if { [ string range $anMois 4 4 ] == 0 } {
		set Mois [ string range $anMois 5 5 ]
            }      
        if {  ${Mois} == 12  } {
		set an [ string range $anMois 0 3 ]
            set an_next [ expr $an + 1 ]
            set anMois_next ${an_next}01
            puts "${an_next}01"
        } else {
            set anMois_next [ expr $anMois + 1 ]
        }
        
 
        ##### loop on days 
        
        foreach day $Data(days) {
            
            set fields ""
            set nbHour 0
# modifier après ici quand il y a une coupure de modèle à l'intérieur d'une journée
            for { set hour 0 } { $hour < 24 } { incr hour 1 } {
                
		
                set hour1 [format "%02d" $hour]
		puts "Hour1 $hour1" 
		
                set laDate [ fstdstamp fromdate "${anMois}${day}" "${hour1}000000" ]
                set lejour [ fstdstamp fromdate "${anMois}${day}" "00000000" ]
		puts "Hour2 $hour1"
                # loop on vertical levels  
		set fieldsLevels ""
		foreach level $Data(levels) {
		    if { $sp =="P0" || $sp == "TCC"  }    {
			    
			    set level 0
			}
			set fld [ fstdfield find 1 "${laDate}" "" "${level}" -1 -1 "" "$sp" ]
			puts "Hour3 $hour1"
			
			if { $fld != ""  } {
				set fld  [ fstdfield find 1 "$laDate" "" "$level" -1 -1 "" "$sp" ]
			#	lappend fieldsLevels $fld
                       # puts "fieldsLevels:$fieldsLevels"
			    }
			    
		} 
               
                puts "$hour "
		puts "Jour=$day "
		
                ##############
               # if { $lngLvl == "1" } {
                    ###################################### On accumule les champs verticaux pour chaque heure
			
	          
                            fstdfield read FLD1 1 $fld
                    
			incr nbHour 1
                            
                #####  Extrait la valeur en un point donne
			    
			    set coordGrid [fstdfield stats FLD1 -coordpoint [lindex $Data(coord) 0] [lindex $Data(coord) 1] ]
			    
			    puts "coord=$coordGrid"
			    set value1 [fstdfield stats FLD1 -gridvalue [lindex $coordGrid 0]  [lindex $coordGrid 1] ]
			    
			    puts "value 1: $value1"
			    puts "SP=$sp" 

			    if { $sp == "UU" } {
				    set value2 [lindex $value1 0]
				    set value3 [lindex $value1 1]
				    
				    set value2 [format "%.3f" $value2]
				    set value3 [format "%.3f" $value3]

				    puts $fileId "${anMois}${day} $hour ${value2} ${value3}"
				 } else {

				    set value2 [format "%.3f" $value1]
				    puts $fileId "${anMois}${day} $hour ${value2}"
				 }   
              fstdfield free FLD1

		    #}; # Fin boucle sur les heures         
	    }; # Fin boucle sur les heures
 #fstdfield free FLD1

	}
################################### Liberer les champs 
#fstdfield free FLD1
            
################################### Passer au mois suivant             
        
        #   exit 0   
        incr anMois
        puts $anMois
        if { [ string range $anMois 4 5 ] == 13 } {
            set an [ string range $anMois 0 3 ]
            set an_next [ expr $an + 1 ]
            set anMois ${an_next}01
        }
    }

## Fermer les fichiers
    fstdfile close 1
    fstdfile close 2
    close $fileId
}
                                                                 
###################################################################
proc AvgAllDom::Main  { } {
    variable Data
    
    foreach sp $Data(SpLst) {
        puts "sp=$sp"
        
        foreach case $Data(outTXT) start $Data(Start) end $Data(End) {
            
            AvgAllDom::Do $sp $case $start $end
        }
    }
}

###################################################################
#                                                                 # 
#                  Appel general du script                        #
#                                                                 #
###################################################################
AvgAllDom::Main 


