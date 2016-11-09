#! /usr/bin/perl -w
#print "Content-Type: text/html; charset=UTF-8\n\n\n";
use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use libreria::data_registration;
use libreria::sessione;
use libreria::utility;
use utf8;
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";

my $q=new CGI;
my @s = sessione::creaSessione();
my $session = $s[0];
my $doc = data_registration::get_xml_doc();

if (!($q->request_method() eq "POST") ) {
    my %problems=(
          DESCRIZIONE_ERRORE => "Tentativo di inoltrare una richiesta di prenotazione con una modalit&agrave; non permessa."
     );
     $session->param('problems',\%problems);
     print $session->header(-location => "home.cgi");
}
else {
  my $doc = data_registration::get_xml_doc();
  my $richiedente = $session->param('username');
  my $pass = $q->param('passaggio');
  my $part = $q->param('partenza');
  my $arr = $q->param('arrivo');

  my $conducente = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio=\"$pass\"]/Conducente")->get_node(1)->textContent;

  my %Prenotazione=(
    Mittente => $richiedente,
    Passaggio => $pass,
    Partenza => $part,
    Arrivo => $arr
  );

  data_registration::inserisci_notifica("RichiestaPrenotaz", \%Prenotazione, $conducente);
  my %nota = ( nota => "Richiesta di prenotazione inoltrata con successo.");
  $session->param('nota',\%nota);       
  print $session->header(-location => "singolo_passaggio.cgi?passaggio=$pass&part=$part&arr=$arr");
}
