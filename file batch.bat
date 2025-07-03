@echo off

::set DURATION=20
::set OUTPUT=D:\WiresharkAnalyzer\secondaprova.pcap

tshark -i 4 -l -T fields -e ip.src -e ip.dst -e frame.time_epoch -e _ws.col.Protocol -e eth.src -e frame.len -e eth.dst -E separator=,
::-a duration:%DURATION% -w %OUTPUT%

pause