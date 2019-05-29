#!/bin/sh
# : - \
    exec /fs/ssm/eccc/cmo/cmoe/apps/SPI_7.12.0_all/tclsh "$0" "$@"
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
    set FileOut $Data(Path)/$Data(TAG3)_$Data(outTXT)_5levs_${start}_${end}_$Data(point)_${sp}.txt
    file delete $FileOut
    
    # ouvrir le fichier FileOut pour des valeurs en format texte
    set fileId [ open $FileOut w 0644 ] 
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
            set nbHour 0
            for { set hours $Data(hours) 0 } { $hours < 25 } { incr hours 1 } {
                
 
                set hour1 [format "%02d" $hours]
    puts "Hour1 $hour1" 
           
                set laDate [ fstdstamp fromdate "${anMois}${day}" "${hour1}000000" ]
                set lejour [ fstdstamp fromdate "${anMois}${day}" "00000000" ]

                # loop on vertical levels  
                set fieldsLevels ""
                foreach level $Data(levels) {
                    set fld [ fstdfield find 1 "${laDate}" "" "${level}" -1 -1 "" "$sp" ]
		    
		    if { $fld != ""  } {
                            set fld  [ fstdfield find 1 "$laDate" "" "$level" -1 -1 "" "$sp" ]
                            lappend fieldsLevels $fld
                       # puts "fieldsLevels:$fieldsLevels"
			}
                } 
                #fin de la boucle sur les niveaux verticaux
		
                # Calcule la moyenne sur les niveaux verticaux
                set lngLvl [ llength  $fieldsLevels ]
                puts "$hour $lngLvl "
		
                ##############
                if { $lngLvl == "1" } {
                    ###################################### On accumule les champs verticaux pour chaque heure
                    
                    for { set j 0} {$j<$lngLvl} { incr j 1} { 
                        # puts "toto= [lindex $fieldsLevels $j]"             
                        fstdfield read FLD1 1 [lindex $fieldsLevels $j]
                        ########### case 1
                        if { ![ fstdfield is SUM1 ] } {
                            fstdfield copy SUM1 FLD1
                        ########### case 2
                        } else {
                            vexpr SUM1 SUM1+FLD1
                        }              
                        
                    }
                    fstdfield free FLD1
                    #####  On calcule la moyenne sur les niveaux verticaux
                    vexpr AVG1 SUM1/$lngLvl
                    fstdfield free SUM1
                    
                    if { ![ fstdfield is SUM_DAY ] } {
                        fstdfield copy SUM_DAY AVG1
                    } else {
                        vexpr SUM_DAY SUM_DAY + AVG1
                    }
                    incr nbHour 1
                                    
                #####  Extrait la valeur en un point donne
                
                set coordGrid [fstdfield stats AVG1 -coordpoint [lindex $Data(coord) 0] [lindex $Data(coord) 1] ]
                
                puts "coord=$coordGrid"
                set value1 [fstdfield stats AVG1 -gridvalue [lindex $coordGrid 0]  [lindex $coordGrid 1] ]
                
                puts "value 1: $value1"
                puts "SP=$sp" 
                
                puts $fileId "${anMois}${day} $nbHour ${value1}"
             
		    }; # Fin boucle sur les heures         
	    }; # Fin boucle sur les heures 
	}
 ################################### Liberer les champs 
fstdfield free AVG1
            
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


