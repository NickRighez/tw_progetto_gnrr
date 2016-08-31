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

 my $cgi = new CGI;                       
 my @s = sessione::creaSessione();  
 my $session = $s[0]; 

my %hash_keys;

 my %prob_hash;
 if(defined($session->param('problems'))) {
    my $prob = $session->param('problems');
    %prob_hash = %$prob;
    while( my( $key, $value ) = each %prob_hash ){
    	$hash_keys{$key}="$value";
	}
 }

  my %old_hash;
  if(defined($session->param('old_input'))) {
    my $old = $session->param('old_input');
    %old_hash = %$old;
    while( my( $key, $value ) = each %old_hash ){
    	$hash_keys{$key}="$value";
	}
  } 



  my $file = "TravelShare/accedi.html";
  
  my $template_parser = Template->new;
  my $foglio = '';
  $template_parser->process($file,\%hash_keys,\$foglio);
	#print $q->header();
  print $foglio;

if(defined($session->param('problems'))) {
	$session->clear(['problems']);
}
if(defined($session->param('old_input'))) {
	$session->clear(['old_input']);
}