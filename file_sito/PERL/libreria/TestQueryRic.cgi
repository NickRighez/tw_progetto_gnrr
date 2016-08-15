#!/usr/bin/perl
use strict;
use warnings;
use diagnostics;
use CGI::Carp qw(fatalsToBrowser);
use lib "libreria";
use data_registration;
use research;
#use libreria::data_registration; can t locate utility.pm in libreria/data_registration
#our $xml_file = '/var/www/html/cgi-bin/tw_progetto_gnrr/file_sito/provaXML.xml';
our $parser = XML::LibXML->new();


my $q=CGI->new;


print "Content-type: text/html\n\n";
print "<html><head></head><body>";
	

	my %RegUte= (
		Username => 'unbbvvbnmm',
		Email => 'pepddmvvme@hot.it',
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
	NUM_ARRIVO => '4'
  	);
	
   #print research::query_viaggi(\%RicPassag);

   my %InsMessBach= (
   		Mittente => 'u2',
   		Destinatario =>'',  #  SE IL MITTENTE E' IL CONDUCENTE, DEVE ESISTERE IL DESTINATARIO!!!!
   		Data => '1999-11-11',
   		Ora => '12:00:00',
   		Testo => ' soma text '
   	);

   my %InsMessBach2= (
   		Mittente => 'u1',
   		Destinatario =>'u2',
   		Data => '1999-11-11',
   		Ora => '12:00:00',
   		Testo => ' soma text inviato da conducente'
   	);

   my %InsMessBach3= (
   		Mittente => 'eeenees',
   		Destinatario =>'',
   		Data => '1999-11-11',
   		Ora => '12:00:00',
   		Testo => ' soma text '
   	);


 print data_registration::inserisci_nuovo_messaggio_bacheca('v2',\%InsMessBach);
 print data_registration::inserisci_nuovo_messaggio_bacheca('v2',\%InsMessBach2);
 print data_registration::inserisci_nuovo_messaggio_bacheca('v2',\%InsMessBach3);
	print "</body></html>";