import os
import re
import shutil


def run():
    molecules = ["o3"]
    for m in molecules:
        os.system("cmcarc -x 2019060400_054_GM_north@america@gemmach_I_GEMMACH_"+m+"@sfc@001.* -f "+os.getcwd()+ "/rarc/operation.images.chronos/2019060400_north@america@gemmach")
        # convert -delay 35 -loop 0 *.png aa.gif
        # convert -delay 35 -loop 0 2019060400_054_GM_north@america@gemmach_I_GEMMACH_o3@sfc@001* D55.gif
        # cmcarc -x 2019060400_054_GM_north@america@gemmach_I_GEMMACH_o3@sfc@.* -f 2019060400_north@america@gemmach
        def purge(dir, pattern):
            for f in os.listdir(dir):
                if re.search(pattern, f):
                    shutil.move(f, os.getcwd()+"/imgTemp")

        print("Sorting")
        purge(os.getcwd(),"2019060400_054_GM_north@america@gemmach_I_GEMMACH_"+m+"@sfc@001")
        print("generating gif")
        os.system("convert -delay 35 -loop 0 "+os.getcwd()+"/imgTemp/2019060400_054_GM_north@america@gemmach_I_GEMMACH_"+m+"@sfc@001* /fs/site1/dev/eccc/oth/airq_central/sair001/Ding_Ma/ProjetQA/output/"+m+"D55.gif")
        # shutil.rmtree("imgTemp")
        # os.mkdir("imgTemp")
        print("remaking dir")

