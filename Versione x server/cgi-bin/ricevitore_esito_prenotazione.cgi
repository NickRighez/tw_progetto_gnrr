#! /usr/bin/perl -w
#print "Content-Type: text/html; charset=UTF-8\n\n\n";

# parametri passati attraverso form di metodo post

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use libreria::data_registration;
use libreria::sessione;
use libreria::utility;
use utf8;
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";
use Encode qw(decode_utf8);

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
    my $pass =  decode_utf8 $q->param('passaggio');
    my $part =  decode_utf8 $q->param('partenza');
    my $arr =  decode_utf8 $q->param('arrivo');
    my $esito =  decode_utf8 $q->param('esito');

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
            Username =>  decode_utf8 $q->param('richiedente'),
            IDViaggio =>  decode_utf8 $q->param('passaggio'),
            NumTappaPartenza =>  decode_utf8 $q->param('partenza'),
            NumTappaArrivo =>  decode_utf8 $q->param('arrivo')
            );
        data_registration::incrementa("NumPassaggiPart",  decode_utf8 $q->param('richiedente'));
        data_registration::inserisci_prenotazione(\%Prenotazione);

        my %nota = ( nota => "Prenotazione registrata con successo.");
        $session->param('nota',\%nota);        
    }

    my $richiedente =  decode_utf8 $q->param('richiedente');
    my %Notifica = (
        Passaggio =>  decode_utf8 $q->param('passaggio'),
        Esito => $esito,
        Partenza =>  decode_utf8 $q->param('partenza'),
        Arrivo =>  decode_utf8 $q->param('arrivo')
        );
    data_registration::inserisci_notifica("EsitoPrenotaz",\%Notifica,$richiedente);

    if($doc->exists("//SetUtenti/Utente[Username='$username']/Notifiche/RichiestaPrenotaz[\@Mittente='". decode_utf8 $q->param('richiedente')."' and \@Passaggio='". decode_utf8 $q->param('passaggio')."' and \@Partenza='". decode_utf8 $q->param('partenza')."' and \@Arrivo='". decode_utf8 $q->param('arrivo')."']")) {
        data_registration::elimina_notifica($username,"RichiestaPrenotaz","\@Mittente='". decode_utf8 $q->param('richiedente')."' and \@Passaggio='". decode_utf8 $q->param('passaggio')."' and \@Partenza='". decode_utf8 $q->param('partenza')."' and \@Arrivo='". decode_utf8 $q->param('arrivo')."'");
    }
    print $session->header(-location => "notifiche.cgi");
}
