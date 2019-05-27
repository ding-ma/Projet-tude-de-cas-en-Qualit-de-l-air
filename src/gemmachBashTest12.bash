#!/bin/bash
PathOut=/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest
PathIn=/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach
DateDebut=201901
DateFin=201901
ListeMois="01"
Annee=2019
Tag1=TEST
editfst=/fs/ssm/eccc/mrd/rpn/utils/16.2/ubuntu-14.04-amd64-64/bin/editfst
Type=species
Grille=regeta
FichierTICTAC=/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/operation.forecasts.mach/${DateDebut}0212_000
ListeVersionsGEM="operation.forecasts.mach"
ListeEspeces="O3"
ListeNiveaux="93423264 76696048"
ListeJours="02 03"
ListePasse="12"
ListeHeures="000 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022 023 024 025 026 027 028"
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
