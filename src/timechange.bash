#!/bin/bash
PathOut=/fs/site1/dev/eccc/oth/airq_central/sair001/Ding_Ma/ProjetRepo/bash
PathIn=/fs/site1/dev/eccc/oth/airq_central/sair001/Ding_Ma/ProjetRepo/rarc
DateDebut=20140301
DateFin=20140301
ListeMois="03"
Annee=2014
Tag1=UMOSmist00
editfst=/fs/ssm/eccc/mrd/rpn/utils/16.2/ubuntu-14.04-amd64-64/bin/editfst
Type=species
Grille=regeta
FichierTICTAC=/fs/site1/dev/eccc/oth/airq_central/sair001/Ding_Ma/ProjetRepo/rarc/operation.scribeMat.mist.aq/${DateDebut}00_mist_anal
ListeVersionsGEM="operation.scribeMat.mist.aq"
ListeEspeces="O3 N2 AF"
ListeNiveaux="-1"
ListeJours="-1"
ListePasse="-1"
ListeHeures="-1"
################# Extraction#############
./time.tcl
declare -a my_array=()

for VersionGEM in  ${ListeVersionsGEM}
do
FileOut1=${PathOut}/${Tag1}.${DateDebut}_${DateFin}_${Grille}.fst
if [  ${FileOut1}  ]; then
rm -rf  ${FileOut1}
else
continue
fi
FileIn=${FichierTICTAC}
${editfst} -s ${FileIn} -d ${FileOut1} <<EOF
DESIRE(-1,['>>','^^'],-1,-1,-1,-1,-1)
ZAP(-1,-1,'CAPAMIST',-1,-1,-1,-1)
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
FileIn1=${PathIn}/${VersionGEM}/${DateDebut}00_mist_anal
if [ ! ${FileIn1}  ]; then
continue
else
echo "-------------"
echo ${FileIn1} "file does exist"
fi
echo ${FileIn1}
for Espece in ${ListeEspeces}
do
for niveau in  ${ListeNiveaux}
do

readarray -t eCollection0 < <(cut -d, -f1 times.csv)
readarray -t eCollection1 < <(cut -d, -f2 times.csv)
readarray -t eCollection2 < <(cut -d, -f3 times.csv)
len=${#eCollection0[@]}
for (( i=0; i<$len; i++ ))
do
echo $i
${editfst} -s ${FileIn1} -d ${FileOut1} <<EOF
DESIRE(-1,"$Espece",-1,-1,-1,${eCollection2[$i]},-1)
ZAP(-1,"$Espece",'CAPAMIST',${eCollection0[$i]}, -1,${eCollection2[$i]},-1)
EOF

done
done
done
done
done
done
done
done
echo "+++++++++++++++++++++++++++++++"

