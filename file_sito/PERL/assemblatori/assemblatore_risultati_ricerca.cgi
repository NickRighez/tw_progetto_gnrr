#! /usr/bin/perl -w
print "Content-type: text/html\n\n\n";
use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use Template;
use lib "../libreria";    
use sessione;
use lib "../libreria";
use research;
use lib "../libreria";
use data_registration;

 my $q = new CGI;                       
 my @s = sessione::creaSessione();  
 my $session = $s[0]; 

my $partenza=$q->param('partenza');
my $arrivo=$q->param('arrivo');
my $data=$q->param('data');
my $doc = data_registration::get_xml_doc();
my $contenuto = research::query_ricerca($partenza, $arrivo, $data, $doc);


my %hash_keys = (
  CONTENUTO => $contenuto,
  PARTENZA => $partenza,
  ARRIVO => $arrivo,
  DATA => $data
  );

if(!defined($session->param('username'))) {
  my $file = "TravelShare/risultati.html";
  my $template_parser = Template->new;
  my $foglio = '';
  $template_parser->process($file,\%hash_keys,\$foglio);
  #print $q->header();
  print $foglio;
 }
else {
  print "$partenza - $arrivo - $data";
  my $file = "TravelShare/risultatiLog.html";
  $hash_keys{UTENTE} = $session->param('username');
  my $template_parser = Template->new;
  my $foglio = '';
  $template_parser->process($file,\%hash_keys,\$foglio);
  #print $q->header();
  print $foglio;
}


 
