#!/bin/bash
PathOut=/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest
PathIn=/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach
DateDebut=201601
DateFin=201603
ListeMois="01 02 03"
Annee=2016
Tag1=TEST
editfst=/fs/ssm/eccc/mrd/rpn/utils/16.2/ubuntu-14.04-amd64-64/bin/editfst
Type=species
Grille=regeta
FichierTICTAC=/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/operation.forecasts.mach/${DateDebut}1500_002
ListeVersionsGEM="operation.forecasts.mach"
ListeEspeces="O3 N2 AF TT"
ListeNiveaux="76696048"
ListeJours="15 16 17 18 19 20 21 22"
ListePasse="00 12"
ListeHeures="002 003 004 005 006 007"
################# Extraction#############
for VersionGEM in  ${ListeVersionsGEM}
do
FileOut1=${PathOut}/${VersionGEM}/${Tag1}.${DateDebut}_${DateFin}_${Grille}.fst
if [  ${FileOut1}  ]; then
rm -rf  ${FileOut1}
else
continue
fi
FileIn=${FichierTICTAC}
${editfst} -s ${FileIn} -d ${FileOut1} <<EOF
DESIRE(-1,['>>','^^'],-1,-1,-1,-1,-1)
EOF
for mois in ${ListeMois}
do
echo ${mois}
for jour in ${ListeJours}
do
for passe  in ${ListePasse}
do
for heure in ${ListeHeures}
do
echo ${heure}
FileIn1=${PathIn}/${VersionGEM}/${DateDebut}${jour}${passe}_${heure}
if [ ! ${FileIn1}  ]; then
continue
else
echo "-------------"
echo ${FileIn1} "file does exist"
fi
echo ${FileIn1}
for Espece in ${ListeEspeces}
do
if [ "$Espece" = "P0" ] || [ "$Espece" = "TCC" ] ; then
${editfst} -s ${FileIn1} -d ${FileOut1} <<EOF
DESIRE (-1,"$Espece",-1, -1, 0, -1, -1)
EOF
else
for niveau in  ${ListeNiveaux}
do
${editfst} -s ${FileIn1} -d ${FileOut1} <<EOF
DESIRE (-1,"$Espece",-1, -1, $niveau, -1, -1) 
EOF
done
fi
done
done
done
done
done
done
