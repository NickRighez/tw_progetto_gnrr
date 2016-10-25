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
use libreria::utility;

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
    my $richiedente = $session->param('username');
    my $pass = $q->param('passaggio');
    my $part = $q->param('partenza');
    my $arr = $q->param('arrivo');
    my %problems;
    my $conducente = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio=\"$pass\"]/Conducente")->get_node(1)->textContent;
#*******************************************************************************************************************************************************

####       Controllare se pass, part e arr corrispondono a un passaggio esistente?   ##############################################à    
    if($doc->exists("//SetPassaggi/Passaggio[IDViaggio=\"$pass\"]/Itinerario/*[\@Numero>=$part and \@Numero<=$arr]/Prenotazioni[Utente=\"$richiedente\"]")) {
        $problems{ERR_PRENOTAZIONE} = "<p class=\"errore\"> Esiste già una prenotazione per questo passaggio</p>";
    }
    if($doc->exists("//SetUtenti/Utente[Username='$conducente']/Notifiche/RichiestaPrenotaz[ \@Mittente='$richiedente' and \@Passaggio='$pass' ]")) { # DA VALUTARE
        $problems{ERR_RICHIESTA} = "<p class=\"errore\"> Esiste una richiesta di prenotazione per questo viaggio</p>";
    }
    if($conducente eq $richiedente) {
        $problems{ERR_CONDUCENTE} = "<p class=\"errore\"> Il conducente non può prenotare un proprio viaggio</p>";
    }
    if($doc->exists("SetPassaggi/Passaggio[IDViaggio=\"$pass\" and \@Passato=\"si\"]")){
        $problems{ERR_PASSATO} = "<p class=\"errore\"> Tentativo di richiedere una prenotazione per un viaggio passato </p>";
    }
    if(utility::calcola_posti_disponibili($part, $arr, $pass, $doc) == 0){
        $problems{ERR_POSTI} = "<p class=\"errore\"> Tentativo di richiedere una prenotazione per un viaggio senza posti disponibili </p>";
    }

    if(!%problems){
        my %Prenotazione=(
            Mittente => $richiedente,
            Passaggio => $pass,
            Partenza => $part,
            Arrivo => $arr
        );

        if(data_registration::inserisci_notifica("RichiestaPrenotaz", \%Prenotazione, $conducente)) {
            print $session->header(-location => "viaggi.cgi");
        }
    }
    else {
        $session->param('problems',\%problems);
        print $session->header(-location => "singolo_passaggio.cgi?passaggio=$pass&part=$part&arr=$arr");

    }
}
