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
#use lib "libreria";
use libreria::sessione;

my $q=new CGI;;
my @s = sessione::creaSessione();
my $session = $s[0];


my %problems = ( empty => 'yes' );
my %old_input;

#  ******  TESTARE CHE IL METODO DELLA FORM SIA 'POST' *************  #
# ******** (per la ricerca il metodo &egrave; get) ******** #
if (!($q->request_method() eq 'POST')) {
    my %problems=(
      DESCRIZIONE_ERRORE => "Tentativo di inserire un nuovo utente con una modalit&agrave; non permessa."
      );
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
else {

    if($q->param('username') eq "") {
        $problems{USERNAME_ERR} = "Username mancante";
        $problems{empty} = "no";
    }
    elsif(!($q->param('username')=~m/^[A-Za-z0-9_-]{5,18}$/)) {
        $problems{USERNAME_ERR} = "Username non valido, caratteri ammessi: lettere (non accentate), numeri, '_', '-'. Lunghezza: minimo 5 caratteri, massimo 18 caratteri.";
        $problems{empty} = "no";
    }
    else {
        $old_input{USERNAME} = $q->param('username');
    }

    if($q->param('email') eq "") {
        $problems{EMAIL_ERR} = "E-mail mancante";
        $problems{empty} = "no";
    }
    elsif(!($q->param('email')=~m/^([a-z0-9_\.-]+)@([a-z]+)\.([a-z]{2,6})$/)) {
        $problems{EMAIL_ERR}="Indirizzo email non valido";
        $problems{empty}="no";
    }
    else {
        my $doc = data_registration::get_xml_doc();
        my @email = $doc->findnodes("//SetUtenti/Utente[Email='".$q->param('email')."']");
        my $num = @email;
        if($num!=0) {
            $problems{EMAIL_ERR}="indirizzo email gi&agrave; esistente";
            $problems{empty}="no";
        }
        else {
            $old_input{EMAIL}=$q->param('email');
        }
    }


    if($q->param('nome') eq "") {
        $problems{NOME_ERR} = "Nome utente mancante";
        $problems{empty} = "no";
    }
    elsif(!($q->param('nome')=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0030}-\x{0039}]|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/)) {
        $problems{NOME_ERR}="nome utente non valido, inserire solo lettere, di cui, al pi&ugrave; la prima lettera pu&ograve; essere mauiscola";
        $problems{empty}="no";
    }
    else {
        $old_input{NOME}=$q->param('nome');
    }

    if($q->param('cognome') eq "") {
        $problems{COGNOME_ERR} = "Cognome utente mancante";
        $problems{empty} = "no";
    }
    elsif(!($q->param('cognome')=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0030}-\x{0039}]|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/)) {
        $problems{COGNOME_ERR}="cognome utente non valido, inserire solo lettere, di cui, al pi&ugrave; la prima lettera pu&ograve; essere mauiscola";
        $problems{empty}="no";
    }
    else {
        $old_input{COGNOME}=$q->param('cognome');
    }

    if($q->param('anno') eq "") {
        $problems{ANNO_ERR}="Anno di nascita mancante";
        $problems{empty}="no";
    }
    elsif(!($q->param('anno')=~m/^[1-2][0-9][0-9][0-9]$/)) {
        $problems{ANNO_ERR}="Anno di nascita non valida, inserire l anno in formato 'aaaa'";
        $problems{empty}="no";
    }
    else {
        my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
        $year=$year+1900-18;
        if(($q->param('anno'))>$year) {
            $problems{ANNO_ERR}="Possono registrarsi solo utenti maggiorenni";
            $problems{empty}="no";
        }
        else {
            $old_input{ANNO}=$q->param('anno');
        }
    }

    if($q->param('password') eq "") {
        $problems{PASSWORD_ERR} = "Password mancante";
        $problems{empty}="no";
    }
    elsif (length($q->param('password'))<8 or length($q->param('password'))>16){
        $problems{PASSWORD_ERR} = "La password dev essere compresa fra 8 e 16 caratteri";
        $problems{empty}="no";
    }
    elsif(!($q->param('password')=~m/^[A-Za-z0-9_\.-]{8,16}$/)) {
        $problems{PASSWORD_ERR} = "Password non valida, sono permesse lettere maiuscole o minuscole, e i caratteri underscore, hyphen o punto";
        $problems{empty}="no";
    }
    elsif($q->param('password') ne $q->param('conferma')) {
        $problems{CONFERMA_ERR} = "Password non coincidenti";
        $problems{empty}="no";
    }

    #$nome= encode("utf-8",decode("iso-8859-2",$nome));
    my %ute = (
        Username => $q->param('username'),
        Email => $q->param('email'),
        Nome => $q->param('nome'),
        Cognome => $q->param('cognome'),
        Sesso =>$q->param('sesso'),
        AnnoNascita => $q->param('anno'),
        Password => $q->param('password')
        );

   
    if($problems{'empty'} eq 'yes') {
        data_registration::inserisci_nuovo_utente(\%ute);
        $session->param('nuova_regis',\%ute);
        print $session->header(-location => "ricevitore_login.cgi");

    }
    else {
        $session->param('problems', \%problems);
        $session->param('old_input', \%old_input);
        print $session->header(-location => "iscrizione.cgi");
    }
}
