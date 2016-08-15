#!/usr/bin/perl
use strict;
use warnings;
use diagnostics;
use CGI::Carp qw(fatalsToBrowser);
use lib "libreria";
use data_registration;
use libreria::research;
#use Time::localtime;
#use libreria::data_registration; can t locate utility.pm in libreria/data_registration
#our $xml_file = '/var/www/html/cgi-bin/tw_progetto_gnrr/file_sito/provaXML.xml';
our $parser = XML::LibXML->new();


my $q=CGI->new;


print "Content-type: text/html\n\n";
print "<html><head></head><body>";
		
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
		print $d."<br>".$o;
	my %aux=data_registration::serializzazione_apertura();
	my $doc = $aux{'doc'};
	my $fileHandle = $aux{'filehandle'};
	#print(data_registration::elimina_notifica("u1","NuovoMessaggioBacheca","\@Mittente=\"u2\" and \@Passaggio=\"v2\"",$doc));
	#print data_registration::elimina_info_auto('u1',$doc);
    #data_registration::serializzazione_chiusura($fileHandle,$doc);

	my %RegUte= (
		Username => 'unmm',
		Email => 'pevvme@hot.it',
		Nome => 'mario',
		Cognome => 'rossi',
		Sesso =>'M',
		AnnoNascita => '1990',
		Password => 'cdcfvfrr'
		);

	#print(data_registration::inserisci_nuovo_utente(\%RegUte));


#my $fragm="<Utente>u1</Utente>";
#$fragm = $parser->parse_balanced_chunk($fragm);
#data_registration::serializzazione_inserimento($fragm,'//x','//Passaggio[IDViaggio=\'v3\']/Itinerario/Partenza/Prenotazioni');

 	my %RicUte=(UTENTE => 'u1');
 	#print research::query_users(\%RicUte);

 	my %RicPassag= (
  	VIAGGIO => 'v2',
	NUM_PARTENZA => '0',
	NUM_ARRIVO => '4',
	PREZZO => '33',
	POSTI => '4',
	BAGAGLI => 'piccolo',
	CONDUCENTE => 'u1'
  	);
	
   #print research::query_viaggio(\%RicPassag);

   my %Mess=( UTENTE => 'u1', MYSELF => 'u2');
   #print research::query_conversazione(\%Mess);

   my %Bac=(
   	VIAGGIO => 'v1',
   	UTENTE => 'u1'
   	);

   print research::query_bacheca_viaggio(\%Bac);
	print "</body></html>";