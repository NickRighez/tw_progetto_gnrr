#! /usr/bin/perl -w

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

if(!defined($session->param('username'))) {
    my %problems=(
        LOGIN_ERR => "<p class=\"errore\">Utente non loggato, pagina inaccessibile</p>"
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "login.cgi");
}
else {
    my %hash_keys;

    my $ute= $q->param('utente'); # usernaem dell utente appeso alla stringa URL
    my $doc=data_registration::get_xml_doc();
    if(!$doc->exists("//SetUtenti/Utente[Username=\"$ute\"]")) {
        my %problems=(
            DESCRIZIONE_ERRORE => "<div class=\"descrizione_errore\"><p>Tentativo di visualizzazione di un profilo inesistente</p></div>"
        );
        $session->param('problems',\%problems);
        print $session->header(-location => "home.cgi");
    }
    else {
        $hash_keys{NOME} = $doc->findnodes("//SetUtenti/Utente[Username=\"$ute\"]/Nome")->get_node(1)->textContent;
        $hash_keys{COGNOME} = $doc->findnodes("//SetUtenti/Utente[Username=\"$ute\"]/Cognome")->get_node(1)->textContent;
        
        my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
        $year = $year+1900;
        my %Ute=(
            UTENTE => $q->param('utente'),
            ANNO_C => $year
        );

        my $file = "../data/HTML_TEMPLATE/profiloPubblico.html";
        $hash_keys{NUM_NOTIFICHE} = research::conta_notifiche($session->param('username'), $doc);
        $hash_keys{LOGGEDIN} = 'yes';
        $hash_keys{NOME_UTENTE}=$session->param('username');
        $hash_keys{NOME_PROFILO} = $ute;
        $hash_keys{CONTENUTO} = research::query_users(\%Ute);
        print $q->header();
        my $template_parser = Template->new;
        open my $fh, '<', $file;
        my $foglio = '';
        $template_parser->process($fh,\%hash_keys,\$foglio);
        print $foglio; 
    }    
}
