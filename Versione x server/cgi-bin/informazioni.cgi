#! /usr/bin/perl -w
print "Content-type: text/html\n\n\n";
use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use Template;
#use lib "../libreria";
use libreria::sessione;
use libreria::data_registration;
use libreria::research;
my $cgi = new CGI;
my @s = sessione::creaSessione();
my $session = $s[0];
my $doc = data_registration::get_xml_doc();
my %hash_keys;

if(defined($session->param('username'))) {
    $hash_keys{LOGGEDIN} = 'yes';
    $hash_keys{NOME_UTENTE} =  $session->param('username');
    $hash_keys{NUM_NOTIFICHE} = research::conta_notifiche($session->param('username'), $doc);
    $hash_keys{INDEX} = 9;
}
else {
    $hash_keys{LOGGEDIN} = 'no';
    $hash_keys{INDEX} = 6;
}

my $file = "../data/HTML_TEMPLATE/info.html";
my $template_parser = Template->new;
open my $fh, '<:encoding(UTF-8)', $file;
my $foglio = '';
$template_parser->process($fh,\%hash_keys,\$foglio) or die($template_parser->error());
print $foglio;
