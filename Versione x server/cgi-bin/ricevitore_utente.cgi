#! /usr/bin/perl -w
#print "Content-Type: text/html; charset=UTF-8\n\n";

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use libreria::data_registration;
use libreria::sessione;

use utf8;
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";
use Encode qw(decode_utf8);

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
    my $username = $q->param('username');
    if($username eq "") {
        $problems{USERNAME_ERR} = "Username mancante";
        $problems{empty} = "no";
    }
    elsif(!($username=~m/^[A-Za-z0-9_-]{5,18}$/)) {
        $problems{USERNAME_ERR} = "Username non valido, caratteri ammessi: lettere (non accentate), numeri, '_', '-'. Lunghezza: minimo 5 caratteri, massimo 18 caratteri.";
        $problems{empty} = "no";
    }
    else {
        $old_input{USERNAME} = $username;
    }

 my $email = $q->param('email');
    if($email eq "") {
        $problems{EMAIL_ERR} = "E-mail mancante";
        $problems{empty} = "no";
    }
    elsif(!$email=~m/^([a-zA-Z0-9_\.-]+)@([a-z]+)\.([a-z]{2,6})$/) {
        $problems{EMAIL_ERR}="Indirizzo email non valido";
        $problems{empty}="no";
    }
    else {
        my $doc = data_registration::get_xml_doc();
        my @email = $doc->findnodes("//SetUtenti/Utente[Email='".$email."']");
        my $num = @email;
        if($num!=0) {
            $problems{EMAIL_ERR}="Indirizzo email gi&agrave; esistente";
            $problems{empty}="no";
        }
        else {
            $old_input{EMAIL}=$email;
        }
    }

 my $nome = decode_utf8($q->param('nome'));
    if($nome eq "") {
        $problems{NOME_ERR} = "Nome utente mancante";
        $problems{empty} = "no";
    }
    elsif(!$nome=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0030}-\x{0039}]|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/) {
        $problems{NOME_ERR}="Nome utente non valido, inserire solo lettere, di cui, al pi&ugrave; la prima lettera pu&ograve; essere mauiscola";
        $problems{empty}="no";
    }
    else {
        $old_input{NOME}=decode_utf8($nome);
    }

 my $cognome = decode_utf8($q->param('cognome'));
    if($cognome eq "") {
        $problems{COGNOME_ERR} = "Cognome utente mancante";
        $problems{empty} = "no";
    }
    elsif(!$cognome =~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0030}-\x{0039}]|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/) {
        $problems{COGNOME_ERR}="Cognome utente non valido, inserire solo lettere, di cui, al pi&ugrave; la prima lettera pu&ograve; essere mauiscola";
        $problems{empty}="no";
    }
    else {
        $old_input{COGNOME}=decode_utf8($cognome);
    }

 my $anno = $q->param('anno');
    if($anno eq "") {
        $problems{ANNO_ERR}="Anno di nascita mancante";
        $problems{empty}="no";
    }
    elsif(!$anno =~ m/^[1-2][0-9][0-9][0-9]$/) {
        $problems{ANNO_ERR}="Anno di nascita non valida, inserire l anno in formato 'aaaa'";
        $problems{empty}="no";
    }
    else {
        my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
        $year=$year+1900-18;
        if($anno>$year) {
            $problems{ANNO_ERR}="Possono registrarsi solo utenti maggiorenni";
            $problems{empty}="no";
        }
        else {
            $old_input{ANNO}=$anno;
        }
    }

 my $password = $q->param('password');
    if($password eq "") {
        $problems{PASSWORD_ERR} = "Password mancante";
        $problems{empty}="no";
    }
    elsif (length($password)<8 or length($password)>16){
        $problems{PASSWORD_ERR} = "La password dev essere compresa fra 8 e 16 caratteri";
        $problems{empty}="no";
    }
    elsif(!($password =~m/^[A-Za-z0-9_\.-]{8,16}$/)) {
        $problems{PASSWORD_ERR} = "Password non valida, sono permesse lettere maiuscole o minuscole, e i caratteri underscore, hyphen o punto";
        $problems{empty}="no";
    }
    elsif($password ne $q->param('conferma')) {
        $problems{CONFERMA_ERR} = "Password non coincidenti";
        $problems{empty}="no";
    }

    #$nome= encode("utf-8",decode("iso-8859-2",$nome));
    my %ute = (
        Username => $username,
        Email => $email,
        Nome => $nome,
        Cognome => $cognome,
        Sesso => $q->param('sesso'),
        AnnoNascita => $anno,
        Password => $password,
	DescrizionePers => ''
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
