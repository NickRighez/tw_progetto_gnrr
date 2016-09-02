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
     NOT_LOGGED => "Utente non loggato, pagina inaccessibile"
     );
  $session->param('problems',\%problems);
  print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/accedi.cgi");
}
print "Content-type: text/html\n\n";
my $username=$session->param('username');

data_registration::aggiorna_feedback_da_rilasciare();

my $doc=data_registration::get_xml_doc();
my $contenuto = research::query_viaggi_utente($username, $doc);

my $file = "../data/HTML_TEMPLATE/TravelShare/viaggi.html";
my %hash_keys = (
  USERNAME => $username,
  CONTENUTO => $contenuto
);  
my $template_parser = Template->new;
my $foglio = '';
$template_parser->process($file,\%hash_keys,\$foglio);
print $foglio;