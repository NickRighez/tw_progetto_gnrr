#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Carp qw(fatalsToBrowser);
use libreria::research;
use libreria::data_registration;
use CGI::Session;
use libreria::sessione;
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";
use utf8;

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
    print "Content-Type: text/html; charset=UTF-8\n\n";
    my $username=$session->param('username');
    my $contenuto;
    my $doc=data_registration::get_xml_doc();
    my @conv=$doc->findnodes("//SetMessaggi/Conversazione[\@User1='$username' or \@User2='$username']");
    my $num=@conv;
    my %Messaggi = ( UTENTE => $username);
    $contenuto = research::query_messaggi(\%Messaggi);

    my %hash_keys = (
        NOME_UTENTE => $username,
        CONTENUTO => $contenuto,
        NUM_NOTIFICHE => research::conta_notifiche($username, $doc),
        NUM_CONVERSAZIONI => $num
        );


    my $file = "../data/HTML_TEMPLATE/messaggi.html";
    my $template_parser = Template->new({ ENCODING => 'utf8' });
    open my $fh, '<:encoding(UTF-8)', $file;
    my $foglio = '';
    $template_parser->process($fh,\%hash_keys,\$foglio);

    my %hash_index = (INDEX => 9 );
    my $foglio_def = '';
    $template_parser->process(\$foglio,\%hash_index,\$foglio_def);
    print $foglio_def;

    if(defined($session->param('problems'))) {
        $session->clear(['problems']);
    }
}
