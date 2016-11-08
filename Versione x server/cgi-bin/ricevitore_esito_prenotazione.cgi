#! /usr/bin/perl -w
#print "Content-type: text/html\n\n\n";

# parametri passati attraverso form di metodo post

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
#use lib "../libreria";
use libreria::data_registration;
#use lib "libreria";
use libreria::sessione;
use libreria::utility;

my $q=new CGI;
my @s = sessione::creaSessione();
my $session = $s[0];
my $doc = data_registration::get_xml_doc();


if (!($q->request_method() eq 'POST')) {
    my %problems=(
      DESCRIZIONE_ERRORE => "Tentativo di inoltrare un esito di prenotazione con una modalit&agrave; non permessa."
      );
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
else {
    my $username = $session->param('username');
    my $pass = $q->param('passaggio');
    my $part = $q->param('partenza');
    my $arr = $q->param('arrivo');
    my $esito = $q->param('esito');

    if($esito eq "Rifiutata"){
        my %nota = ( nota => "Prenotazione rifiutata con successo.");
        $session->param('nota',\%nota);
    }
    elsif($doc->exists("//SetPassaggi/Passaggio[IDViaggio=\"$pass\"]/Itinerario/*[\@Numero>=$part and \@Numero<$arr]/Prenotazioni[Utente=\"$username\"]")) {
        $esito = "Rifiutata";
        my %nota = ( nota => "Prenotazione rifiutata,in quanto &egrave; presente una prenotazione da parte dell utente $username.");
        $session->param('nota',\%nota);
    }
    elsif ($doc->exists("//SetPassaggi/Passaggio[IDViaggio=\"$pass\" and \@Passato=\"si\"]")){
        $esito = "Rifiutata";
        my %nota = ( nota => "Prenotazione rifiutata, il viaggio &egrave; gi&agrave; avvenuto.");
        $session->param('nota',\%nota);
    }
    elsif (utility::calcola_posti_disponibili($part, $arr, $pass, $doc) == 0){
        $esito = "Rifiutata";
        my %nota = ( nota => "Prenotazione rifiutata, posti disponibili esauriti.");
        $session->param('nota',\%nota);
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

        my %nota = ( nota => "Prenotazione registrata con successo.");
        $session->param('nota',\%nota);        
    }

    my $richiedente = $q->param('richiedente');
    my %Notifica = (
        Passaggio => $q->param('passaggio'),
        Esito => $esito,
        Partenza => $q->param('partenza'),
        Arrivo => $q->param('arrivo')
        );
    data_registration::inserisci_notifica("EsitoPrenotaz",\%Notifica,$richiedente);

    if($doc->exists("//SetUtenti/Utente[Username='$username']/Notifiche/RichiestaPrenotaz[\@Mittente='".$q->param('richiedente')."' and \@Passaggio='".$q->param('passaggio')."' and \@Partenza='".$q->param('partenza')."' and \@Arrivo='".$q->param('arrivo')."']")) {
        data_registration::elimina_notifica($username,"RichiestaPrenotaz","\@Mittente='".$q->param('richiedente')."' and \@Passaggio='".$q->param('passaggio')."' and \@Partenza='".$q->param('partenza')."' and \@Arrivo='".$q->param('arrivo')."'");
    }
    print $session->header(-location => "notifiche.cgi");
}
