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

my @s = sessione::creaSessione();
my $session = $s[0];

my $q=CGI->new;
my $contenuto_passaggio = "";
my $contenuto_bacheca = "";
my $doc = data_registration::get_xml_doc();
my %hash_keys;

if(defined($session->param('problems'))) {
    my $prob = $session->param('problems');
    my %prob_hash = %$prob;
    while( my( $key, $value ) = each %prob_hash ){
        $hash_keys{$key}="$value";
    }
}
my $pass = $q->param('passaggio');
my $part =$q->param('part');
my $arr = $q->param('arr');
my @passaggi = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$pass']/Itinerario[*/\@Numero='$part']/*[\@Numero='$arr']");
my $num = @passaggi;
if($num==0 or $part==$arr) {
    my %problems = ( DESCRIZIONE_ERRORE => "Si e' tentato di visualizzare un passaggio non valido.").
    print $session->header(-location => "home.cgi");
}
else {
    my %Pass=(
        VIAGGIO => $pass,
        NUM_PARTENZA =>$part,
        NUM_ARRIVO => $arr
        );

    $contenuto_passaggio = research::query_viaggio(\%Pass);

    if(defined($session->param('ricerca_prec'))) {
        my $aux = $session->param('ricerca_prec');
        my %ricerca = %$aux;
        $hash_keys{URL_RICERCA} = "<a class=\"linkSottoH\" href=\"ricevitore_ricerca?partenza=".$ricerca{'partenza'}."&arrivo=".$ricerca{'arrivo'}."&data=".$ricerca{'data'}."\" tabindex=\"7\">Torna ai risultati</a>";
        $session->clear(['ricerca_prec']);
    }

    if(defined($session->param('loggedin'))) {
        my $username = $session->param('username');
        $hash_keys{NUM_NOTIFICHE} = research::conta_notifiche($username, $doc);;
        $hash_keys{LOGGEDIN} = 'yes';
        $hash_keys{NOME_UTENTE} = $username;
        my $conducente = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$pass']/Conducente");

        if($conducente ne $username) {
            $hash_keys{NUOVA_CONVERSAZIONE} = 'yes';
            $hash_keys{CONDUCENTE} = $conducente;
            $hash_keys{PASSAGGIO} = $pass;
            $hash_keys{PARTENZA} = $part;
            $hash_keys{ARRIVO} = $arr;
        }

        if($doc->exists("//SetPassaggi/Passaggio[IDViaggio=\"$pass\" and \@Passato=\"si\"]")) {
            $hash_keys{MOTIVAZIONE} = "Passaggio non prenotabile, in quanto gi&agrave; avvenuto";
        }
        elsif($conducente eq $username){
            $hash_keys{MOTIVAZIONE} = "Passaggio non prenotabile, in quanto ne sei il conducente";
        }
        elsif($doc->exists("//SetPassaggi/Passaggio[IDViaggio=\"$pass\"]/Itinerario/*[\@Numero>=$part and \@Numero<=$arr]/Prenotazioni[Utente=\"$username\"]")){
            $hash_keys{MOTIVAZIONE} = "Passaggio non prenotabile, in quanto esiste gi&agrave; una prenotazione per esso";
        }
        elsif($doc->exists("//SetUtenti/Utente[Username='$conducente']/Notifiche/RichiestaPrenotaz[ \@Mittente='$username' and \@Passaggio='$pass' ]")) {
            $hash_keys{MOTIVAZIONE} = "Passaggio non prenotabile, in quanto esiste gi&agrave; una richiesta di prenotazione per esso";
        }
        elsif(utility::calcola_posti_disponibili($part, $arr, $pass) == 0){
            $hash_keys{MOTIVAZIONE} = "Passaggio non prenotabile, posti disponibili esauriti";
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


    if(defined($session->param('problems'))) {
        $session->clear(['problems']);
    }
}

