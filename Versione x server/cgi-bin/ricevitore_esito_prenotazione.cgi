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
my $doc = data_registration::get_xml_doc();

if(!defined($session->param('username'))) {
    my %problems=(
        LOGIN_ERR => "Utente non loggato, pagina inaccessibile"
        );

    $session->param('problems',\%problems);
    print $q->header(-location => "login.cgi");
}
else {
    my $username = $session->param('username');
    if($q->request_method() eq 'POST') {
        my $username = $session->param('username');
        my $pass = $q->param('passaggio');
        my $part = $q->param('partenza');
        my $arr = $q->param('arrivo');
        my $esito = $q->param('esito');
        my @prenotazioni = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio=\"$pass\"]/Itinerario/*[\@Numero>=$part and \@Numero<=$arr]/Prenotazioni[Utente=\"$username\"]");
        my $num = @prenotazioni;
        if($num!=0) {
            $esito = "Rifiutata";
        }
        if($esito eq 'Accettata') {
            my %Prenotazione=(
                Username => $q->param('richiedente'),
                IDViaggio => $q->param('passaggio'),
                NumTappaPartenza => $q->param('partenza'),
                NumTappaArrivo => $q->param('arrivo')
                );
            data_registration::incrementa("NumPassaggiPart", $q->param('richiedente'));
            data_registration::inserisci_prenotazione(\%Prenotazione);
         
        }
         my $richiedente = $q->param('richiedente');
            my %Notifica = (
                Passaggio => $q->param('passaggio'),
                Esito => $esito
                );
        data_registration::inserisci_notifica("EsitoPrenotaz",\%Notifica,$richiedente);
        if($doc->exists("//SetUtenti/Utente[Username='$username']/Notifiche/RichiestaPrenotaz[\@Mittente='".$q->param('richiedente')."' and \@Passaggio='".$q->param('passaggio')."' and \@Partenza='".$q->param('partenza')."' and \@Arrivo='".$q->param('arrivo')."']")) {
            data_registration::elimina_notifica($username,"RichiestaPrenotaz","\@Mittente='".$q->param('richiedente')."' and \@Passaggio='".$q->param('passaggio')."' and \@Partenza='".$q->param('partenza')."' and \@Arrivo='".$q->param('arrivo')."'");
        }
    }    
    print $session->header(-location => "notifiche.cgi");
}
