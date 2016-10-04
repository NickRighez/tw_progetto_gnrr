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
#use lib "../libreria";
use libreria::research;
#use lib "../libreria";
use libreria::data_registration;

 my $q = new CGI;                       
 my @s = sessione::creaSessione();  
 my $session = $s[0]; 

my $partenza=$q->param('partenza');
my $arrivo=$q->param('arrivo');
my $data=$q->param('data');
my $doc = data_registration::get_xml_doc();
my $contenuto = research::query_ricerca($partenza, $arrivo, $data, $doc);
my %hash_keys;

my %hash_keys = (
  CONTENUTO => $contenuto,
  PARTENZA => $partenza,
  ARRIVO => $arrivo,
  DATA => $data
);

  
  ##################!!!!!!!!!!!!!!!!!!!!!!!
  
 
  
if(defined($session->param('username'))) {
  my $cont = research::query_notifiche_utente($session->param('username'), $doc);
  $hash_keys{LOGGEDIN} = 'yes';
  $hash_keys{NOME_UTENTE} = $session->param('username');
    $hash_keys{NUM_NOTIFICHE} = @$cont[1];
}
else {
  $hash_keys{LOGGEDIN} = 'no';
}


my $file = "../data/HTML_TEMPLATE/risultati.html";
  my $template_parser = Template->new;
  open my $fh, '<', $file;
  my $foglio = '';
  $template_parser->process($fh,\%hash_keys,\$foglio);
  #print $q->header();
  print $foglio;
