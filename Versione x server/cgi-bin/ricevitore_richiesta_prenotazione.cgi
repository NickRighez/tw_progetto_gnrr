#! /usr/bin/perl -w
#print "Content-type: text/html\n\n\n";
use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
#use lib "../libreria";
use libreria::data_registration;
#use lib "libreria";
use libreria::sessione;

my $q=new CGI;
my @s = sessione::creaSessione();
my $session = $s[0];

if(!defined($session->param('username'))) {
    my %problems=(
        not_logged => "Utente non loggato, pagina inaccessibile"
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "login.cgi");
}
else {
    my $doc = data_registration::get_xml_doc();
    my $username = $session->param('username');
    my $pass = $q->param('passaggio');
    my $part = $q->param('partenza');
    my $arr = $q->param('arrivo');
    my @prenotazioni = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio=\"$pass\"]/Itinerario/*[\@Numero>=$part and \@Numero<=$arr]/Prenotazioni[Utente=\"$username\"]");
    my $num = @prenotazioni;

    if($num!=0) {
        my %problems=(
            ERR_PRENOTAZIONE => "<p class=\"errore\"> Esiste già una prenotazione per questo passaggio</p>"
            );
        $session->param('problems',\%problems);
        print $session->header(-location => "singolo_passaggio.cgi?passaggio=$pass&part=$part&arr=$arr");
    }
    else {
        my $conducente = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio=\"$pass\"]/Conducente")->get_node(1)->textContent();
        my %Prenotazione=(
            Mittente => $session->param('username'),
            Passaggio => $q->param('passaggio'),
            Partenza => $q->param('partenza'),
            Arrivo => $q->param('arrivo')
            );

        if(data_registration::inserisci_notifica("RichiestaPrenotaz", \%Prenotazione, $conducente)) {
            print $session->header(-location => "viaggi.cgi");
        }
    }
}
