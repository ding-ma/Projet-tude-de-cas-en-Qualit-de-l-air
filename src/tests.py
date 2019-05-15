#! bin/env python3
import os
#
# PathOut = "/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma$"
# PathIn = "/space/hall1/sitestore/eccc/oth/airq_central/rio001/Requete_ETS/DonneesBrutes"
#
# DateDebut = "201502"
# DateFin = "201502"
# ListeMois = "12"
# Tag1 = "TEST"
#
# editfst = "/fs/ssm/eccc/mrd/rpn/utils/16.2/ubuntu-14.04-amd64-64/bin/editfst"
# Type = "species"
# Grille = "regeta"
# FichierTICTAC = "/space/hall1/sitestore/eccc/oth/airq_central/rio001/Requete_ETS/DonneesBrutes/operation.forecasts.regeta/" + DateDebut + "2200_000"
#
# ListeVersionsGEM = "operation.forecasts.regeta"
# ListeEspeces = "TT"
#
# # ListeNiveaux="12000 11950 11850 11733 11606 11467 11316 11151 10973 10780 10571 10346 10104 9845 9567 9272 8959 8646 8337 8034 7737 7446 7161 6883 6612 6348 6091 5843 5602 5369 5144 4928 4721 4522 4331 4149 3976 3812 3667 3541 3431 3334 3248 3172  3104 3044 2990 2941 2897 2852 2795 2720 2625 2508 2374 2233 2102 2000"
#
# ListeJours = "22 23 24 25 26 27 28"
#
# ListePasse = "00 06 12 18"
# ListeHeures = "000 001 002 003 004 005"
#
# for VersionGEM in ListeVersionsGEM:
#     FileOut1 = PathOut + "/" + VersionGEM + "/" + Tag1 + "." + DateDebut + "_" + DateFin + "_" + Grille + ".fst"
#     if FileOut1 is True:  # never going to be true
#         os.system("rm -rf" + FileOut1)
#     FileIn = FichierTICTAC
#     os.system(editfst + " -s " + FileIn + " -d " +FileOut1 + "<< EOF")
#     os.system("DESIRE(-1,['>>','^^'],-1,-1,-1,-1,-1)")
#     os.system("EOF")
#     for mois in ListeMois:
#         print(mois)
#         for jour in ListeJours:
#             for passse in ListePasse:
#                 for heure in ListeHeures:
#                     print(heure)
#                     FileIn1 = PathIn + "/" + VersionGEM + "/" + DateDebut + jour + passse + "_" + heure
#                     if FileIn1 is True:  # same here
#                         print("-------------")
#                         print(FileIn1 + " file does exist")
#                     print(FileIn1)
#                     for espece in ListeEspeces:
#                         if espece == "P0" or espece == "TCC":
#                             os.system(editfst + "-s" + FileIn1 + "-d" + FileOut1 + "<<EOF")
#                             os.system("DESIRE (-1," + espece + ",-1, -1, 0, -1, -1) ")
#                             os.system("EOF")
#
# # EOF
#/space/hall1/sitestore/eccc/cmod/prod/../rarc_tmp/big_tmpdir/sair001_544254

file = open("Extract_species_Meteo_AvecP0.bash", "r")
a=file.read()
print(a)
