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
binmode(STDOUT, ":utf8");
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

    my $username=$session->param('username');
    my ($messaggi, $feedback, $richieste, $esito) = research::query_notifiche_utente($username, data_registration::get_xml_doc());
    my @messaggi_list = @$messaggi;
    my @feedback_list = @$feedback;
    my @richieste_list = @$richieste;
    my @esito_list = @$esito;
    my $file = "../data/HTML_TEMPLATE/notifiche.html";
    my %hash_keys = (
        NOME_UTENTE => $username,
        MESSAGGI_LIST => \@messaggi_list,
        FEEDBACK_LIST => \@feedback_list,
        RICHIESTE_LIST => \@richieste_list,
        ESITO_LIST => \@esito_list,
        NUM_NOTIFICHE => research::conta_notifiche($username, data_registration::get_xml_doc()),
        INDEX => 10
        );

    if(defined($session->param('nota'))) {
        my $aux = $session->param('nota');
        my %nota = %$aux;
        $hash_keys{NOTA} = $nota{'nota'};
        $session->clear(['nota']);
    }
    
    my $template_parser = Template->new({ ENCODING => 'utf8' });
    my $foglio = '';
    open my $fh, '<:encoding(UTF-8)', $file;
    $template_parser->process($fh,\%hash_keys,\$foglio);
print "Content-Type: text/html\n\n\n";
    print $foglio;
}
