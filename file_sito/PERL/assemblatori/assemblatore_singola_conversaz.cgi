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

if(!defined($session->param('username'))) {
  my %problems=(
     NOT_LOGGED => "Utente non loggato, pagina inaccessibile"
     );
  $session->param('problems',\%problems);
  print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/accedi.cgi");
}
my $username = $session->param('username');
my $utente = $q->param('utente');
my $doc = data_registration::get_xml_doc();
my $node = $doc->findnodes("//SetUtenti")->get_node(1);
if(!($node->exists("Utente[Username=\"".$q->param('utente')."\"]"))) {
  my %problems=(
     conversazione_err => "<p class=\"errore\">Impossibile visualizzare la conversazione. Utente inesistente</p>"
     );
  $session->param('problems',\%problems);
  print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_conversazioni.cgi");
}
print "Content-type: text/html\n\n";
my $username=$session->param('username');
my $contenuto;
my %Conversazione=(    
	UTENTE => $utente,
	MYSELF => $username
	);
$contenuto = research::query_conversazione(\%Conversazione); 

if($doc->exists("//SetMessaggi/Conversazione[\@User1=\"$utente\" and \@User2=\"$username\"] | SetMessaggi/Conversazione[\@User1=\"$username\" and \@User2=\"$utente\"]")) {
  data_registration::aggiorna_messaggi_letti($username, $q->param('utente'));
}

my $file = "TravelShare/singolaConversazione.html";
my %hash_keys = (
  USERNAME => $username,
  CONTENUTO => $contenuto,
  destinatario_mess_p => $q->param('utente'),
  conversatore => $q->param('utente')
);  
my $template_parser = Template->new;
my $foglio = '';
$template_parser->process($file,\%hash_keys,\$foglio);
print $foglio;
