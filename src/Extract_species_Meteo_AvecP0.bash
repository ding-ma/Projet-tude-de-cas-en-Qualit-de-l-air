#!/bin/bash

################################################################################ 
# Environnement et Changement Climatique Canada 
#
# SOP du Centre  
#
# 7810-800 rue de la Geuchetiere Ouest
#
# Montreal, QC 
#
# Projet    : Script d extraction de champs des especes chimiques meteo pris dans les archives du CMC (regeta, glbeta, etc.)
# 
# Nom du fichier   : Extract_species_Meteo.bash
#
# Creation  : Unite AIQA -- (Fev. 2017)
#
################################################################################


#######################################################
#                                                     #
#               DEFINIR LES VARIABLES                 #         
#                                                     # 
#######################################################


PathOut=/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest

PathIn/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach

DateDebut=201904
DateFin=201904
ListeMois="04"


Annee=2019

Tag1=TEST
#Tag1=TEST1
# 1 ou 2 si subdivision, sinon pas de chiffre en suffixe

#editfst=/ssm/net/rpn/utils/15.2/ubuntu-12.04-amd64-64/bin/editfst
editfst=/fs/ssm/eccc/mrd/rpn/utils/16.2/ubuntu-14.04-amd64-64/bin/editfst


Type=species

Grille=regeta

#FichierTICTAC=/cnfs/dev/regions/que/afqsfrc/Requete_ETS/2015/operation.forecasts.regeta/${DateDebut}2200_000
FichierTICTAC=/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/operation.forecasts.mach/${DateDebut}0500_000

ListeVersionsGEM="operation.forecasts.mach"



#ListeEspeces="TT UU VV WW"
#ListeEspeces="HR P0 TCC"
ListeEspeces="O3"
# premiere moitie TT UU VV WW
# deuxieme moitie HR P0 TCC
#ListeEspeces="TT UU VV WW HR P0 TCC"

#ListeNiveaux="12000"
ListeNiveaux="93423264 76696048"


ListeJours="05"
#"01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31"

ListePasse="00 12"
ListeHeures="000 001 002 003 004 005 006 007 008 009 010 011"



#######################################################
#                                                     #
#               DEBUT DE L EXTRACTION                 #         
#                                                     # 
#######################################################

# Boucle sur les scenarios que l on veut traiter
for VersionGEM in  ${ListeVersionsGEM}

do
    
    FileOut1=${PathOut}/${VersionGEM}/${Tag1}.${DateDebut}_${DateFin}_${Grille}.fst
    if [  ${FileOut1}  ]; then
	rm -rf  ${FileOut1}
    else 
	
	continue
    fi
    
    # Obtenir les champ TIC et TAC de n importe quel fichier a condition que ce soit la meme grille dans ce fichier
    FileIn=${FichierTICTAC}
    
    ${editfst} -s ${FileIn} -d ${FileOut1} <<EOF

    DESIRE(-1,['>>','^^'],-1,-1,-1,-1,-1)

EOF
    
# Boucle sur les mois
    for mois in ${ListeMois}
    
    do
	
	echo ${mois}
	
       # Boucle sur les jours
	for jour in ${ListeJours} 
	
	do
	    
            # Boucle sur les passes
	    for passe  in ${ListePasse} 
	    do 
  # Boucle sur les heures
		for heure in ${ListeHeures} 
		
		do
		    echo ${heure}
		    
		    FileIn1=${PathIn}/${VersionGEM}/${DateDebut}${jour}${passe}_${heure}
		    
                # Verifier si le fichier existe
		    if [ ! ${FileIn1}  ]; then
			
			continue
			
		    else 
			
			echo "-------------"
			echo ${FileIn1} "file does exist"
			
		    fi
		    
		    echo ${FileIn1}
                # Fin de la verification si le fichier existe
		    
                # Extraire les champs desires
	        # Boucle sur les variables 
		    for Espece in ${ListeEspeces}
		    do  
			if [ "$Espece" = "P0" ] || [ "$Espece" = "TCC" ] ; then
			    ${editfst} -s ${FileIn1} -d ${FileOut1} <<EOF
			
                DESIRE (-1,"$Espece",-1, -1, 0, -1, -1) 
			
EOF

#			elif [ "$Espece" = "NF" ]; then

#			    editfst2000 -s ${FileIn1} -d ${FileOut1} <<EOF
			
#               DESIRE (-1,"$Espece",-1, -1, 0, -1, -1) 
			
#EOF


			else
			    
                    # Boucle sur les niveaux 
			    for niveau in  ${ListeNiveaux}
			    
			    do 
				${editfst} -s ${FileIn1} -d ${FileOut1} <<EOF
               
              
                DESIRE (-1,"$Espece",-1, -1, $niveau, -1, -1) 

EOF
				
				
		   # Fin de la boucle sur les niveau verticaux
			    done
			    
			    
	     # Fin de la boucle sur les especes
			fi
		    done
	 # Fin de la boucle sur les heures
		done	
            # Fin de la boucle sur les passes
	    done
	    
	done 
        # Fin de la boucle sur les jours
	
    done 
    # Fin de la boucle sur les mois
    
done
# Fin de la boucle sur les scenarios

#######################################################
#                                                     #
#               FIN DE L EXTRACTION                   #         
#                                                     # 
#######################################################
