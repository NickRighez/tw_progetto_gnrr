#! /usr/bin/perl -w
#print "Content-Type: text/html; charset=UTF-8\n\n";

use strict;
use warnings;
use CGI qw(-utf8);
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use libreria::data_registration;
use libreria::sessione;
use HTML::Entities;
use utf8;
use Encode qw(decode_utf8);
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";

my $q=new CGI;

my @s = sessione::creaSessione();
my $session = $s[0];

if($q->request_method ne 'POST') {
    my %problems=(
          DESCRIZIONE_ERRORE => "Tentativo di inserire un messaggio in modalit&agrave; non permessa."
     );
     $session->param('problems',\%problems);
    print $q->redirect("home.cgi");
}
elsif (decode_utf8($q->param('messaggio')) eq ""){
    my %problems=(
          DESCRIZIONE_ERRORE => "Tentativo di inserire un messaggio vuoto."
     );
     $session->param('problems',\%problems);
    print $q->redirect("singolo_passaggio.cgi?passaggio=".$q->param('passaggio')."&part=".$q->param('partenza')."&arr=".$q->param('arrivo'));
}
else{

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

    my $mess =  decode_utf8($q->param('messaggio'));
    $mess =encode_entities($mess,'<>&"\'');

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
