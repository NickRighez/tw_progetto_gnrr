#! /usr/bin/perl -w
#print "Content-type: text/html\n\n";

use strict;
use warnings;
use CGI qw(-utf8);
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use libreria::data_registration;
use libreria::sessione;
use HTML::Entities;
my $q=new CGI;

my @s = sessione::creaSessione();
my $session = $s[0];

if($q->request_method eq 'POST') {
    my $mitt = $session->param('username');
    # campi 'hidden':
    my $dest=$q->param('destinatario');
    my $pas = $q->param('passaggio');
    my $part = $q->param('partenza');
    my $arr = $q->param('arrivo');

    my $doc=data_registration::get_xml_doc();

    # se si deve confrontare una stringa proveniente da un nodo, &egrave; NECESSARIO TextContent

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

    my $mess = $q->param('messaggio');
    $mess =encode_entities($mess,'>');
    $mess = encode_entities($mess, '<');
    my %Messaggio=(
        Mittente => $mitt,
        Destinatario => $dest,
        Data => $d,
        Ora => $o,
        Testo => $mess
        );

    if(data_registration::inserisci_nuovo_messaggio_bacheca($pas,\%Messaggio)) {
        print $q->redirect("singolo_passaggio.cgi?passaggio=$pas&part=$part&arr=$arr");
    }
}
else{
     my %problems=(
          DESCRIZIONE_ERRORE => "Tentativo di inserire un messaggio in modalit&agrave; non permessa."
     );
     $session->param('problems',\%problems);
    print $q->redirect("home.cgi");
}
