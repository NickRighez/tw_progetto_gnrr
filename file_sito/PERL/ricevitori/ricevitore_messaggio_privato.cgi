#! /usr/bin/perl -w
print "Content-type: text/html\n\n";

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use lib "../libreria";
use data_registration;

my $q=CGI->new;

my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
$year=$year+1900;
$mon=$mon+1;
if (length($mon)  == 1) {$mon = "0$mon";}
if (length($mday) == 1) {$mday = "0$mday";}
if (length($hour) == 1) {$hour = "0$hour";}
if (length($min)  == 1) {$min = "0$min";}
if (length($sec)  == 1) {$sec = "0$sec";}
my $d = $year."-".$mon."-".$mday;
my $o = $hour.":".$min.":".$sec;

my %Messaggio=(
	Mittente => $q->param('Mittente'),
	Destinatario => $q->param('Destinatario'),
	Data => $d,
	Ora => $o,
	Testo => $q->param('messaggio')
);

#  CHECK INPUT Testo PER CODE INJECTION

data_registration::inserisci_nuovo_messaggio_singolo(\%Messaggio);
