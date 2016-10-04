#! /usr/bin/perl -w
#print "Content-type: text/html\n\n";

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
#use lib "../libreria";
use libreria::data_registration;
#use lib "../libreria";
use libreria::sessione;
my $q=new CGI;

my @s = sessione::creaSessione();
my $session = $s[0];

if(!defined($session->param('username'))) {
    my %problems=(
        LOGIN_ERR => "Utente non loggato, pagina inaccessibile"
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "login.cgi");
}
else {
    my $username = $session->param('username');
    my $doc = data_registration::get_xml_doc();
    my $passaggio = $q->param('passaggio');
    if($doc->exists("//SetUtenti/Utente[Username='$username']/Notifiche/EsitoPrenotaz[\@Passaggio='$passaggio']")) {
    	data_registration::elimina_notifica($username,"EsitoPrenotaz","\@Passaggio='$passaggio'");
    	print $session->header(-location => "notifiche.cgi");
    }
    else {
    	#########################  AGGIUNGERE ERRORE ALLA HOME
    	my %problems=(
        	DESCRIZIONE_ERRORE => "<div class=\"descrizione_errore\"><p>Errore eliminazione notifica di un esito di prenotazione. Notifica inesistente.</p></div>"
        );
	    $session->param('problems',\%problems);
	    print $session->header(-location => "home.cgi");
    }
}