#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use lib "../libreria";
use data_registration;
use Scalar::Util qw(looks_like_number);

#  SERVE LA SESSIONE PER ESTRARRE IL CONDUCENTE ( UTENTE CHE STA INSERENDO IL VIAGGIO )

my $q = CGI->new;
print "Content-type: text/html\n\n";

my %Passaggio=();
my %Partenza=();
my %Tappa1=();
my %Tappa2=();
my %Tappa3=();
my %Arrivo=();


if(!looks_like_number($q->param('prezzo')) or
    $q->param('prezzo')<0) {
        die("E obbligatorio inserire un prezzo valido");
    }
$Passaggio{PrezzoTot}=$q->param('prezzo');

if(!looks_like_number($q->param('postiDisp')) or
    $q->param('postiDisp')<0) {
        die("E obbligatorio inserire un numero di posti disponibili valido");
    }
$Passaggio{PostiDisp}=$q->param('postiDisp');

if($q->param('dettagli') ne '') {
    $Passaggio{Dettagli}=$q->param('dettagli');
}

# E davvero necessario?
%Partenza=utility::check_presenza_param_tappa("Partenza");
if(!(utility::controllo_tappa(\%Partenza))) {
    print("Partenza non valida");
}
$Passaggio{Partenza}=\%Partenza;

%Arrivo=utility::check_presenza_param_tappa("Arrivo");
if(!(utility::controllo_tappa(\%Arrivo))) {
    print("Arrivo non valido");
}
$Passaggio{Arrivo}=\%Arrivo;

if($q->param('AbilitaT1') eq 'Abilita tappa 1') {
    %Tappa1=utility::check_presenza_param_tappa("Tappa1");
    if(!(utility::controllo_tappa(\%Tappa1))) {
        print("Tappa 1 non valida");
    }
    $Passaggio{Tappa1}=\%Tappa1;
}

if($q->param('AbilitaT2') eq 'Abilita tappa 2') {
    %Tappa2=utility::check_presenza_param_tappa("Tapp21");
    if(!(utility::controllo_tappa(\%Tappa2))) {
        print("Tappa 2 non valida");
    }
    $Passaggio{Tappa1}=\%Tappa1;
}

if($q->param('AbilitaT3') eq 'Abilita tappa 3') {
    %Tappa3=utility::check_presenza_param_tappa("Tappa3");
    if(!(utility::controllo_tappa(\%Tappa3))) {
        print("Tappa 3 non valida");
    }
    $Passaggio{Tappa1}=\%Tappa1;
}

print data_registration::inserisci_nuovo_viaggio(\%Passaggio);





