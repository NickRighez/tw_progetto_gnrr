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
use libreria::data_registration;

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
	my $username = $session->param('username');
  my $cont = research::query_notifiche_utente($username, $doc);
	my $file = "../data/HTML_TEMPLATE/confermaRegistrazione.html";
  	my %hash_keys = (
		NOME_UTENTE => $username,
		NUM_NOTIFICHE => @$cont[1]
		);
	my $template_parser = Template->new;
    my $foglio = '';
    open my $fh, '<', $file;
    $template_parser->process($fh,\%hash_keys,\$foglio);
    #print $q->header();
    print $foglio;

}