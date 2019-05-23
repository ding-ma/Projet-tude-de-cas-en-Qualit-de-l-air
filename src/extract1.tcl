#!/bin/bash
# : - \
    exec /fs/ssm/eccc/cmo/cmoe/apps/SPI_7.12.0_all/tclsh "$0" "$@"
package require TclData

################################################################################ 
# Environnement et Changement Climatique Canada 
# SOP du Centre - Unite AIQA -- (Avril. 2017)  
# 7810-800 rue de la Geuchetiere Ouest
# Montreal, QC 
#
# Projet    : Extraction des donnees meteologiques pour l ETS
#             1: prend la valeur dans tous les niveaux pour 0Z et 12Z, et 
#             2: extrait les valeurs en un point de grille pour les variables demandees.
#                Le site est supposee etre represente par ses coordonnees geographiques(lat lon). 
# 
# Nom du script   : Extract_Site_regeta_Profils_0Z_12Z.tcl
#
# Nom du fichier de configuration du script: config_Site_regeta_Profils_0Z_12Z.tcl
#
# Comment ca marche?: Extract_Site_regeta_Profils_0Z_12Z.tcl config_Site_regeta_Profils_0Z_12Z.tcl 
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
# retirer la ligne suivante pour la seconde passe du mois
#    puts $fileId "AnMoisJour Heure NiveauML Valeur"
    set anMois $start 
    puts $anMois
    
    ############ get and open the input .fst file
    set FileIn [ lsort -dictionary [ glob $Data(Path)/$Data(TAG1).fst ] ]
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
            set Eticket  $Data(Eticket)

             foreach hour $Data(hours) { 
                
		
                set hour1 [format "%02d" $hour]
		puts "Hour1 $hour1" 
		
                set laDate [ fstdstamp fromdate "${anMois}${day}" "${hour1}000000" ]
                set lejour [ fstdstamp fromdate "${anMois}${day}" "00000000" ]
		puts "Hour2 $hour1"
                # loop on vertical levels  
		set fieldsLevels ""
		foreach level $Data(levels) {
	
		    if { $sp =="P0"   } {
			    
			    set level 0.0
			}
			set fld [ fstdfield find 1 "${laDate}" "" "${level}" -1 -1 "" "$sp" ]
			puts "Hour3 $hour1"
			
			if { $fld != ""  } {
				set fld  [ fstdfield find 1 "$laDate" "$Eticket" "$level" -1 -1 "" "$sp" ]
			#	lappend fieldsLevels $fld
                       # puts "fieldsLevels:$fieldsLevels"
			    }
            puts "HH$hour "
		 puts "Level $level "
                ############## On fait l<interpolation niveau ETA --> Mandatory Levels (Pression)
			
	          
                            fstdfield read FLD1 1 $fld
                    
		#	incr nbHour 1
                            
                #####  Extrait la valeur en un point donne
			    
			    set coordGrid [fstdfield stats FLD1 -coordpoint [lindex $Data(coord) 0] [lindex $Data(coord) 1] ]
			    
			    puts "coord=$coordGrid"
			    set value1 [fstdfield stats FLD1 -gridvalue [lindex $coordGrid 0]  [lindex $coordGrid 1] ]
			    
			    puts "value 1: $value1"
			    puts "SP=$sp" 
			    
                            # Get mandatory Level from the list
			    
			    set idx [lsearch -exact $Data(levels) "$level"]
			    puts "idx $idx"
			    set levelML  [lindex  $Data(MandatoryLevels) $idx]
			    puts "levelML $levelML"

			    if { $sp == "UU" } {
				    set value2 [lindex $value1 0]
				    set value3 [lindex $value1 1]

				    set value2 [format "%.3f" $value2]
				    set value3 [format "%.3f" $value3]

				    puts $fileId "${anMois}${day} $hour $levelML ${value2} ${value3}"
				} else {

				    set value2 [format "%.3f" $value1]
				    puts $fileId "${anMois}${day} $hour $levelML ${value2}"   
				}



			    fstdfield free FLD1
			    
               }; # Fin boucle sur les niveau

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


