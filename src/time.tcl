#!/bin/bash
# : - \
exec /fs/ssm/eccc/cmo/cmoe/apps/SPI_7.12.0_all/tclsh "$0" "$@"
package require TclData

set Path /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/ProjetRepo/rarc/operation.scribeMat.mist.aq/
set bashFST 2014030100_mist_anal
set FileOut [open times.csv w+]
set FileIn [ lsort -dictionary [ glob $Path$bashFST ] ]
fstdfile open 1 read  $FileIn
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
set convTime [exec date -d @$arr($element) +%Y%m%d%H]
set cmctime [exec r.date -n -S $convTime]
set hour [string rang $convTime 8 end]
if { $hour < 10} {
set timePre10 [ string rang $hour 1 end]
puts $FileOut "$cmctime,$convTime,$timePre10 "
} else {
puts $FileOut "$cmctime,$convTime,$hour"
}
}
fstdfile close 1
close $FileOut


