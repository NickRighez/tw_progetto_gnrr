#! /usr/bin/perl -w
#print "Content-Type: text/html; charset=UTF-8\n\n";

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Carp qw(fatalsToBrowser);
use libreria::data_registration;
use libreria::sessione;
use CGI::Session;
use HTML::Entities;
use utf8;
use Encode qw(decode_utf8);
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";

my @s = sessione::creaSessione();
my $session = $s[0];
my $q=CGI->new;

if($q->request_method() eq "POST") {

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

    my $mess =  decode_utf8 $q->param('messaggio');
    $mess =encode_entities($mess,'<>&"\'');


    my %Messaggio=(
        Mittente => $session->param('username'),
        Destinatario =>  decode_utf8 $q->param('destinatario'),
        Data => $d,
        Ora => $o,
        Testo => $mess
        );
    my $doc = data_registration::get_xml_doc();
    data_registration::inserisci_nuovo_messaggio_singolo(\%Messaggio);
    print $session->header(-location => "singola_conversaz.cgi?utente=". decode_utf8 $q->param('destinatario'));
    
}
else {
     my %problems=(
          DESCRIZIONE_ERRORE => "Tentativo di inserire un messaggio privato in modalit&agrave; non permessa."
     );
     $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
