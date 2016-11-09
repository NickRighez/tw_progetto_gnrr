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
use HTML::Entities;
use utf8;
use Encode qw(decode_utf8);
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";

my $q=new CGI;;
my @s = sessione::creaSessione();
my $session = $s[0];

my $doc = data_registration::get_xml_doc();

if($q->request_method() ne "POST") {
     my %problems=(
      DESCRIZIONE_ERRORE => "Tentativo di modifica del profilo con una modalit&agrave; non permessa."
      );
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
else {
    my %problems = ( empty => 'yes' );
    my %old_input;

    my $username = $session->param('username');

    my %Modifica=(
        Username => $session->param('username'), # username dell utente che modifica il profilo
        Sesso =>  decode_utf8 $q->param('sesso')
        );
	$old_input{SESSO}= decode_utf8 $q->param('sesso');

    if( decode_utf8 $q->param('nome') ne '') {
        if(!( decode_utf8 $q->param('nome')=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0030}-\x{0039}]|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/)) {
            $problems{NOME_ERR}="Nome utente non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola";
            $problems{empty}="no";
        }
        else {
            $old_input{NOME}= decode_utf8 $q->param('nome');
        }
        $Modifica{Nome}= decode_utf8 $q->param('nome');
    }

    if( decode_utf8 $q->param('cognome') ne '') {
        if(!( decode_utf8 $q->param('cognome')=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0030}-\x{0039}]|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/)) {
            $problems{COGNOME_ERR}="Cognome utente non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola";
            $problems{empty}="no";
        }
        else {
            $old_input{COGNOME}= decode_utf8 $q->param('cognome');
        }
        $Modifica{Cognome}= decode_utf8 $q->param('cognome');
    }

    if( decode_utf8 $q->param('email') ne '') {
        if(!( decode_utf8 $q->param('email')=~m/^([a-zA-Z0-9_\.-]+)@([a-z]+)\.([a-z]{2,6})$/)) {
            $problems{EMAIL_ERR}="Indirizzo email non valido";
            $problems{empty}="no";
        }
        else {
            my @email = $doc->findnodes("//SetUtenti/Utente[Email='". decode_utf8 $q->param('email')."']");
            my $num = @email;
            if($num!=0 and  decode_utf8 $q->param('email') ne $email[0]->findnodes("Email")->get_node(1)->textContent) {
                $problems{EMAIL_ERR}="Indirizzo email già esistente";
                $problems{empty}="no";
            }
            else {
                $old_input{EMAIL}= decode_utf8 $q->param('email');
            }
        }

        $Modifica{Email}= decode_utf8 $q->param('email');
    }

    if( decode_utf8 $q->param('anno') ne '') {
        if(!( decode_utf8 $q->param('anno')=~m/^[1-2][0-9][0-9][0-9]$/)) {
            $problems{ANNO_ERR}="Anno di nascita non valida, inserire l'anno in formato 'aaaa'";
            $problems{empty}="no";
        }
        else {
            my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
            $year=$year+1900-18;
            if(( decode_utf8 $q->param('anno'))>$year) {
                $problems{ANNO_ERR}="Possono registrarsi solo utenti maggiorenni";
                $problems{empty}="no";
            }
            else {
                $old_input{ANNO}= decode_utf8 $q->param('anno');
            }
        }

        $Modifica{AnnoNascita}= decode_utf8 $q->param('anno');
    }

    if( decode_utf8 $q->param('password') ne '') {
        if (length( decode_utf8 $q->param('password'))<8 or length( decode_utf8 $q->param('password')>16)){
            $problems{PASSWORD_ERR} = "La password dev essere compresa fra 8 e 16 caratteri";
            $problems{empty}="no";
        }
        elsif(!( decode_utf8 $q->param('password')=~m/^[A-Za-z0-9_\.-]{8,16}$/)) {
            $problems{PASSWORD_ERR} = "Password non valida, sono permesse lettere maiuscole o minuscole, e i caratteri underscore, hyphen o punto";
            $problems{empty}="no";
        }
        elsif( decode_utf8 $q->param('password') ne  decode_utf8 $q->param('conferma')) {
            $problems{CONFERMA_ERR} = "Password non coincidenti";
            $problems{empty}="no";
        }
        else {
            $old_input{PASSWORD}= decode_utf8 $q->param('password');
        }

        $Modifica{Password}= decode_utf8 $q->param('password');
    }

    my $descr =  decode_utf8 $q->param('descrizioneForm');
    $descr =~ s/^\s*(.*?)\s*$/$1/;
    $descr =encode_entities($descr,'<>&"\'');
    $old_input{DESCRIZIONEFORM}=$descr;
    $Modifica{DescrizionePers}=$descr;



    if( decode_utf8 $q->param('annoPatente') ne '' or  decode_utf8 $q->param('auto') ne '' or  decode_utf8 $q->param('chiacchiere') ne '' or  decode_utf8 $q->param('musica') ne '' or  decode_utf8 $q->param('animali') ne '' or  decode_utf8 $q->param('fumatori') ne '') {
        if( decode_utf8 $q->param('annoPatente') eq '' or  decode_utf8 $q->param('auto') eq '' or  decode_utf8 $q->param('chiacchiere') eq '' or  decode_utf8 $q->param('musica') eq '' or  decode_utf8 $q->param('animali') eq '' or  decode_utf8 $q->param('fumatori') eq '') {
            $problems{INFO_CONDUC_ERR}="Le informazioni necessarie per offrire un passaggio devono essere tutte presenti, o nessuna.";
            $problems{empty}="no";
        }
        elsif(!( decode_utf8 $q->param('annoPatente')=~m/^[1-2][0-9][0-9][0-9]$/)) {
            $problems{ANNOPATENTE_ERR}="Anno di rilascio della patente non valido, inserire l anno in formato 'aaaa'";
            $problems{empty}="no";
        }
        else {
            $old_input{ANNOPATENTE}= decode_utf8 $q->param('annoPatente');
        }

        if(!( decode_utf8 $q->param('auto')=~m/^[A-Za-z0-9,\s-]+$/)) {
            $problems{AUTO_ERR}="Auto non valida, inserire solo lettere, numeri, spazi o virgola.";
            $problems{empty}="no";
        }
        else {
            $old_input{AUTO}= decode_utf8 $q->param('auto');
        }
        $Modifica{Patente}= decode_utf8 $q->param('annoPatente');
        $Modifica{Auto}= decode_utf8 $q->param('auto');
        $Modifica{Chiacchiere}= decode_utf8 $q->param('chiacchiere');
        $Modifica{Musica}= decode_utf8 $q->param('musica');
        $Modifica{Animali}= decode_utf8 $q->param('animali');
        $Modifica{Fumatore}= decode_utf8 $q->param('fumatori');
    }

    my $chiacc = "CHECKED_C". decode_utf8 $q->param('chiacchiere');
    my $mus = "CHECKED_M". decode_utf8 $q->param('musica');
    my $anim = "CHECKED_A". decode_utf8 $q->param('animali');
    my $fum = "CHECKED_F". decode_utf8 $q->param('fumatori');

    $old_input{$chiacc} = "checked='checked'";
    $old_input{$mus} = "checked='checked'";
    $old_input{$anim} = "checked='checked'";
    $old_input{$fum} = "checked='checked'";

    if($problems{'empty'} eq "no") {
        $session->param('problems',\%problems);
        $session->param('old_input',\%old_input);
        print $session->header(-location => "modificaProfilo.cgi");
    }
    elsif(data_registration::inserisci_modifica_profilo(\%Modifica)) {
        print $session->header(-location => "profilo.cgi?utente=$username");
    }
}
