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
        LOGIN_ERR => "Utente non loggato, pagina inaccessibile"
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "login.cgi");
}
else {
    print "Content-type: text/html\n\n";
    my $username=$session->param('username');
    my $cont = research::query_notifiche_utente($username, data_registration::get_xml_doc());
    my $contenuto = @$cont[0];
    my $file = "../data/HTML_TEMPLATE/notifiche.html";
    my %hash_keys = (
        NOME_UTENTE => $username,
        CONTENUTO => $contenuto,
        NUM_NOTIFICHE => @$cont[1]
        );
    my $template_parser = Template->new;
    my $foglio = '';
    open my $fh, '<', $file;
    $template_parser->process($fh,\%hash_keys,\$foglio);
    print $foglio;
}
