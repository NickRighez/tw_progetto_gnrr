#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use lib "../libreria";
use research;
use data_registration;
use CGI::Session;
use lib "../libreria";    
use sessione;

my @s = sessione::creaSessione();  
my $session = $s[0]; 
my $q=CGI->new;
my %hash_keys;
if(defined($session->param('problems'))) {
	    my $prob = $session->param('problems');
	    my %prob_hash = %$prob;
	    while( my( $key, $value ) = each %prob_hash ){
	    	$hash_keys{$key}="$value";
		}
 	}

  	if(defined($session->param('old_input'))) {
	    my $old = $session->param('old_input');
	    my %old_hash = %$old;
	    while( my( $key, $value ) = each %old_hash ){
	    	$hash_keys{$key}="$value";
		}
  	}

my $file = "TravelShare/iscriviti.html";
my $template_parser = Template->new;
my $foglio = '';
$template_parser->process($file,\%hash_keys,\$foglio);
print $foglio;

if(defined($session->param('problems'))) {
	$session->clear(['problems']);
}
if(defined($session->param('old_input'))) {
	$session->clear(['old_input']);
}