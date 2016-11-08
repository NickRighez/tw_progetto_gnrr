#! /usr/bin/perl -w

use utf8;
use strict;
use CGI qw(-utf8);
#use CGI::Carp qw(fatalsToBrowser); # manda un header non utf8
use libreria::research;
use libreria::data_registration;
use CGI::Session;
use libreria::sessione;
binmode(STDOUT, ":utf8");



my @s = sessione::creaSessione(); 
my $session = $s[0];
my $q=CGI->new;
my $doc=data_registration::get_xml_doc();

if(!defined($session->param('username'))) {
    my %problems=(
        LOGIN_ERR => "Utente non loggato, pagina inaccessibile."
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "login.cgi");
}
elsif(!($q->param('utente')=~m/^[A-Za-z0-9_-]{5,18}$/) ||
        !($doc->exists("//SetUtenti/Utente[Username=\"".$q->param('utente')."\"]"))){  ####à   AGGIUNGERE MATCHING CON ESPRESSIONE REGOLARE!
    my %problems=(
        DESCRIZIONE_ERRORE => "Tentativo di visualizzazione di un profilo inesistente."
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");    
}
else {
    my %hash_keys;

    my $ute= $q->param('utente'); # usernaem dell utente appeso alla stringa URL
    my $doc=data_registration::get_xml_doc();

    $hash_keys{NOME} = $doc->findnodes("//SetUtenti/Utente[Username='$ute']/Nome")->get_node(1)->textContent;
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

print "Content-Type: text/html\n\n\n";

    my $template_parser = Template->new({ ENCODING => 'utf8' });
    open my $fh, '<:encoding(UTF-8)', $file;
    my $foglio = '';
    $template_parser->process($fh,\%hash_keys,\$foglio);
    print $foglio; 
}
