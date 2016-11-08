#! /usr/bin/perl -w
#print "Content-type: text/html\n\n\n";
use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
#use lib "../libreria";
use libreria::research;
use libreria::data_registration;
use CGI::Session;
#use lib "../libreria";
use libreria::sessione;
#use libreria::utility;

my @s = sessione::creaSessione();
my $session = $s[0];

my $q=CGI->new;
my $contenuto_passaggio = "";
my $contenuto_bacheca = "";
my $doc = data_registration::get_xml_doc();
my %hash_keys;

my $pass = $q->param('passaggio');
my $part =$q->param('part');
my $arr = $q->param('arr');

if(!($pass=~m/^v[0-9]+$/) || !($part=~m/^[0-4]$/) || !($arr=~m/^[0-4]$/)){
    my %problems = ( DESCRIZIONE_ERRORE => "Si e' tentato di visualizzare un passaggio non valido.");
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
elsif(!$doc->exists("//SetPassaggi/Passaggio[IDViaggio='$pass']/Itinerario[*/\@Numero='$part' and */\@Numero='$arr']") or $part==$arr) {
    my %problems = ( DESCRIZIONE_ERRORE => "Si e' tentato di visualizzare un passaggio non valido.");
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
else {
    my %Pass=(
        VIAGGIO => $pass,
        NUM_PARTENZA => $part,
        NUM_ARRIVO => $arr,
        PREZZO => utility::calcola_prezzo($part,$arr,$pass,$doc)
        );

    $hash_keys{PASSAGGIO} = $pass;
    $hash_keys{PARTENZA} = ucfirst $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$pass']/Itinerario/*[\@Numero='$part']/Luogo");
    $hash_keys{ARRIVO} = ucfirst $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$pass']/Itinerario/*[\@Numero='$arr']/Luogo");
    $hash_keys{NUM_PARTENZA} = $part;
    $hash_keys{NUM_ARRIVO} = $arr;

    $contenuto_passaggio = research::query_viaggio(\%Pass);

    if(defined($session->param('ricerca'))) {
        my $aux = $session->param('ricerca');
        my %ricerca = %$aux;
        $hash_keys{RICERCA_PREC} = "yes";
    }

    if(defined($session->param('nota'))) {
        my $aux = $session->param('nota');
        my %nota = %$aux;
        $hash_keys{NOTA} = $nota{'nota'};
        $session->clear(['nota']);
    }

    if(defined($session->param('problems'))) {
        my $aux = $session->param('problems');
        my %prob = %$aux;
        $hash_keys{DESCRIZIONE_ERRORE} = $prob{'DESCRIZIONE_ERRORE'};
        $session->clear(['prob']);
    }

    if(defined($session->param('loggedin'))) {
        my $username = $session->param('username');
        $hash_keys{NUM_NOTIFICHE} = research::conta_notifiche($username, $doc);;
        $hash_keys{LOGGEDIN} = 'yes';
        $hash_keys{NOME_UTENTE} = $username;
        $hash_keys{INDEX} = 10;
        my $conducente = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$pass']/Conducente");

        if($conducente ne $username && !$doc->exists("//SetPassaggi/Passaggio[IDViaggio='$pass']/Bacheca/ConversazioneBacheca[\@User1='$username']")) {
            $hash_keys{NUOVA_CONVERSAZIONE} = 'yes';
            $hash_keys{CONDUCENTE} = $conducente;
        }

         if($conducente eq $username){
            my @user_ref = research::utenti_prenotati($hash_keys{PASSAGGIO},$part,$arr);
            $hash_keys{LISTA_UTENTI} = \@user_ref;
        }
        elsif($doc->exists("//SetPassaggi/Passaggio[IDViaggio=\"$pass\" and \@Passato=\"si\"]")) {
            $hash_keys{MOTIVAZIONE} = "Passaggio non prenotabile, in quanto gi&agrave; avvenuto";
        }
        elsif($doc->exists("//SetPassaggi/Passaggio[IDViaggio=\"$pass\"]/Itinerario/*[\@Numero>=$part and \@Numero<=$arr]/Prenotazioni[Utente=\"$username\"]")){
            $hash_keys{MOTIVAZIONE} = "Passaggio non prenotabile, hai gi&agrave; effettuato una prenotazione.";
        }
        elsif($doc->exists("//SetUtenti/Utente[Username='$conducente']/Notifiche/RichiestaPrenotaz[ \@Mittente='$username' and \@Passaggio='$pass' ]")) {
            $hash_keys{MOTIVAZIONE} = "Passaggio non prenotabile, hai gi&agrave; una richiesta di prenotazione pendente.";
        }
        elsif (utility::calcola_posti_disponibili($part, $arr, $pass, $doc) == 0){
            $hash_keys{MOTIVAZIONE} = "Passaggio non prenotabile, posti disponibili esauriti.";
        }
        else {
            $hash_keys{PRENOTAZIONE} = 'yes';
        }

        my %Bacheca = (
            VIAGGIO => $pass,
            NUM_PARTENZA =>$part,
            NUM_ARRIVO => $arr,
            UTENTE => $username
            );
        $contenuto_bacheca =research::query_bacheca_viaggio(\%Bacheca)."\n";
    }
    else {
        $hash_keys{LOGGEDIN} = 'no';

        my %Bacheca = (
            VIAGGIO => $pass,
            NUM_PARTENZA =>$part,
            NUM_ARRIVO => $arr,
            UTENTE => ""
            );
        $contenuto_bacheca = research::query_bacheca_viaggio(\%Bacheca)."\n" ;
    }

    my $file = "../data/HTML_TEMPLATE/singoloViaggio.html";
    $hash_keys{CONTENUTO_PASSAGGIO} = $contenuto_passaggio;
    $hash_keys{CONTENUTO_BACHECA} = $contenuto_bacheca;
    my $template_parser = Template->new;
    open my $fh, '<', $file;
    my $foglio = '';
    $template_parser->process($fh,\%hash_keys,\$foglio);
    print $q->header();

    print $foglio;
}
