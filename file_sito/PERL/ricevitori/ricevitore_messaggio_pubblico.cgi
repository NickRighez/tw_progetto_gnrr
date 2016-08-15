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

my $mitt = $q->param('Mittente');
my $dest = $q->param('Destinatario');
my $pas = $q->param('Passaggio');
my %aux=data_registration::serializzazione_apertura();
my $doc=$aux{'doc'};
my $filehandle=$aux{'filehandle'};

# se si deve confrontare una stringa proveniente da un nodo, è NECESSARIO TextContent
my $conduc=$doc->findnodes("//SetPassaggi/Passaggio[IDViaggio=\"$pas\"]/Conducente")->get_node(1)->textContent();
if($q->param('Mittente') eq $conduc) {
	my @conver = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio=\"$pas\"]/Bacheca/ConversazioneBacheca[\@User1=\"$dest\" and \@User2=\"$mitt\"]");
	my $num_conv = @conver;
	if($num_conv eq 0) {
		die("Il conducente non può avviare una conversazione per un suo passaggio");
	}
}
elsif ($q->param('Destinatario') ne $conduc) {
	die("Una conversazione bacheca deve avvenire fra il conducente e un altro utente");
}
data_registration::serializzazione_chiusura($filehandle,$doc);


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
print data_registration::inserisci_nuovo_messaggio_bacheca($q->param('Passaggio'),\%Messaggio);
