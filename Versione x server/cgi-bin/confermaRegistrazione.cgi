#! /usr/bin/perl -w
use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use Template;
use libreria::sessione;
use libreria::data_registration;
binmode(STDOUT, ":utf8");
use utf8;


my $cgi = new CGI;
my @s = sessione::creaSessione();
my $session = $s[0];
my $doc = data_registration::get_xml_doc();

if(!defined($session->param('username'))) {
    my %problems=(
        LOGIN_ERR => "Utente non loggato, pagina inaccessibile"
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "login.cgi");
}
else {
print "Content-type: text/html\n\n\n";
    my $username = $session->param('username');
    my $file = "../data/HTML_TEMPLATE/confermaRegistrazione.html";
    my %hash_keys = (
        NOME_UTENTE => $username,
        NUM_NOTIFICHE => research::conta_notifiche($username, $doc)
        );
    my $template_parser = Template->new({ ENCODING => 'utf8' });
    my $foglio = '';
    open my $fh, '<:encoding(UTF-8)', $file;
    $template_parser->process($fh,\%hash_keys,\$foglio);
    print $foglio;

}
