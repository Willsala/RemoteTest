#!usr/bin/perl -w
use strict;
use File::Copy;

my $dir;
my $str;
my $file_tag = "PCINshift";
my $i;
my $temp;
my $j=0;
my @task_num_list = (85,116,2,17,15,1,4,12,13,14,2,21,130,10,25,2,9,14,23,3,16,1,2,23,17,20,19,8,16,2,18,1,4,1,1,90,17,5,128,1,9,8,20,23,2,10,9,15,18,20,4,17,16,2,1,11,114,6,13,3,20,3,11,17,25,30,12,2,2,4,97,3,84,3,122,6,2,3,14,10,6,94,13,12,119,4,20,20,8,12,1,1,11,21,123,2,12,10,1,6);
#my @task_num_list = (85,116,2,118,15,1,4,12,130,14,2,135,130,10,25,2,9,118,23,31,16,1,100,23,17,20,19,8,16,2,18,1,4,1,1,90,17,5,128,1,9,8,20,23,2,10,9,15,18,20);
foreach $i (31..80){
	$dir ="./user_$i";
	mkdir($dir);
	$dir ="./user_$i/Bugs";
	mkdir($dir);
	open FD,">$dir/tfo_demo.tfo";
	$dir = "./user_$i/Bugs/PCINshift";
	mkdir($dir);
	
	$str = "<TFO name = \"tfo_demo\" path = \"E:/accu1/\" comment = \"1\" author = \"xy\" date = \"2018/04/08\">
\t<LBF type = \"LB0101\">
\t<LIST>
\t\t<DUT name = \"1\" type = \"LX200\">\n";
	print FD $str;
	$str = "\t\t<TEST name = \"PCINshift\" path = \"./PCINshift\">
\t\t\t<DWM name = \"SelectMAP32\"/>
\t\t\t<ITM name = \"PCINshift\"/>
\t\t\t<PIO name = \"PCINshift\"/>
\t\t\t<BIT name = \"PCINshift\"/>
\t\t\t<VCD name = \"PCINshift\"/>
\t\t\t<UCF name = \"PCINshift\"/>
\t\t\t<RPT name = \"PCINshift\"/>
\t\t\t<ATF name = \"PCINshift\"/>
\t\t\t<WAV name = \"PCINshift\" type = \"\" compare = \"yes\"/>
\t\t</TEST>\n";
	foreach $j (1..$task_num_list[$i-31]){		
		print FD $str;
	}
	# mkdir($dir);
	
	#copy("./PCINshift/PCINshift.ptn",$dir."/PCINshift.ptn");	
	$str = "\t</LIST>
</TFO>";
	print FD $str;
	close FD;
}

1;