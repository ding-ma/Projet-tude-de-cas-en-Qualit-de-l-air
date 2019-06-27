#!/bin/bash
# : - \
exec /fs/ssm/eccc/cmo/cmoe/apps/SPI_7.12.0_all/tclsh "$0" "$@"
package require TclData

set Path /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/ProjetRepo/rarc/operation.scribeMat.mist.aq/
set bashFST 2014030100_mist_anal
set FileOut [open times.csv w+]
set FileIn [ lsort -dictionary [ glob $Path$bashFST ] ]
fstdfile open 1 read  $FileIn
#gives list in epoch
set eticket [fstdfile info 1 DATEV]
set output [split $eticket " "]
set output_list [lsort $output]
set i 0
foreach line $output_list {
   set arr($i) $line
   incr i
}
set listOfNames [lsort [array names arr]]
foreach element $listOfNames {
#puts $arr($element)
#puts "element $element = $arr($element)"
set convTime [exec date -d @$arr($element) +%Y%m%d%H]
set cmctime [exec r.date -n -S $convTime]
puts $convTime
set hour [string rang $convTime 8 end]
puts "hour: $hour"
if { $hour < 10} {
set timePre10 [ string rang $hour 1 end]
puts $FileOut "$cmctime,$convTime,$timePre10 "
set fieldinfoPre10 [fstdfield find 1 -1 "" -1 $timePre10 -1 "" "S2" ]
puts $fieldinfoPre10 
} else {
puts $FileOut "$cmctime,$convTime,$hour"
set fieldinfoPost10 [fstdfield find 1 -1 "" -1 $hour -1 "" "S2" ]
puts $fieldinfoPost10 
}
puts $cmctime
puts "---" 

}

fstdfile close 1
close $FileOut
#foreach index [array names arr]
#set convTime [exec date -d @$arr($element) +%Y%m%d%H]
#set cmctime [exec r.date -n -S $convTime]
# [fstdfield find 1 -1 "" -1 $timePre10 -1 O3 "" ]

