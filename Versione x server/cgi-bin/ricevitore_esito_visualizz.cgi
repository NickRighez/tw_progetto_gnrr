#! /usr/bin/perl -w
#print "Content-type: text/html\n\n";

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
#use lib "../libreria";
use libreria::data_registration;
#use lib "../libreria";
use libreria::sessione;
my $q=new CGI;

my @s = sessione::creaSessione();
my $session = $s[0];
my $doc = data_registration::get_xml_doc();

if(!defined($session->param('username'))) {
    my %problems=(
        LOGIN_ERR => "Utente non loggato, pagina inaccessibile"
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "login.cgi");
}
elsif (!($q->param('passaggio')=~m/^v[0-9]+$/) || 
        !($doc->exists("//SetUtenti/Utente[Username='".$session->param('username')."']/Notifiche/EsitoPrenotaz[\@Passaggio='".$q->param('passaggio')."']"))) {
    my %problems=(
        DESCRIZIONE_ERRORE => "Tentativo di eliminare una notifica con una modalit&agrave; non permessa."
    );
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
else {
    my $username = $session->param('username');

    # $q->param('passaggio') passato con GET (appeso alla stringa URL)
    my $passaggio = $q->param('passaggio');    

    data_registration::elimina_notifica($username,"EsitoPrenotaz","\@Passaggio='$passaggio'");
    my %nota = ( nota => "Notifica di esito prenotazione eliminato con successo.");
    $session->param('nota',\%nota);

    print $session->header(-location => "notifiche.cgi");
}
