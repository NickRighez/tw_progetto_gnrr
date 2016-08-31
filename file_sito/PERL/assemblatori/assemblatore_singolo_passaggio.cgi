#! /usr/bin/perl -w
#print "Content-type: text/html\n\n\n";
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
my $contenuto = "";
my $doc = data_registration::get_xml_doc();
my %hash_keys;
if(defined($session->param('problems'))) {
      my $prob = $session->param('problems');
      my %prob_hash = %$prob;
      while( my( $key, $value ) = each %prob_hash ){
        $hash_keys{$key}="$value";
    }
}
my $pass = $q->param('passaggio'), ; 
my $part =$q->param('part');
my $arr = $q->param('arr');
my %Pass=(
	VIAGGIO => $pass,   
	NUM_PARTENZA =>$part,
	NUM_ARRIVO => $arr,
	#PREZZO => $q->param('prezzo'),
	#POSTI => $q->param('posti'),
	#CONDUCENTE => $q->param('cond')
	);
my %Bacheca =(
    VIAGGIO => $q->param('passaggio'),
    NUM_PARTENZA =>$q->param('part'),
    NUM_ARRIVO => $q->param('arr'),
    #PREZZO => $q->param('prezzo'),
    #POSTI => $q->param('posti'),
    #CONDUCENTE => $q->param('cond')
    );

$contenuto = research::query_viaggio(\%Pass);


if(defined($session->param('loggedin'))) {
  my $username = $session->param('username');
  my $conducente = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$pass']/Conducente");
  $Bacheca{UTENTE} = $username;
  if($conducente ne $username) {
    $session->param('Passaggio',\%Pass);
    $contenuto = $contenuto."\n 
    <a href=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/ricevitori/ricevitore_richiesta_prenotazione.cgi?passaggio=$pass&partenza=$part&arrivo=$arr\" >Prenota</a>"."\n";
  }
  $contenuto = $contenuto."\n 
    <h2>Bacheca dei messaggi</h2>  \n
      <div class=\"contenitore\">
      \n".research::query_bacheca_viaggio(\%Bacheca)."\n";
  if($conducente ne $username) {
    $contenuto = $contenuto."  
      <div class=\"contenitore\" id=\"NuovaConversazione\"> \n
       <form action=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/ricevitori/ricevitore_messaggio_pubblico.cgi\" method=\"POST\" >
        <p>Inizia una nuova conversazione con il proprietario del viaggio!</p><br /> \n
        <input type=\"hidden\" name=\"mittente\" value=\"$username\"></input>
        <input type=\"hidden\" name=\"destinatario\" value=\"".$q->param('cond')."\"></input>
        <input type=\"hidden\" name=\"passaggio\" value=\"".$q->param('passaggio')."\"></input>
        <input type=\"hidden\" name=\"partenza\" value=\"".$q->param('part')."\"></input>
        <input type=\"hidden\" name=\"arrivo\" value=\"".$q->param('arr')."\"></input>
        <input type=\"hidden\" name=\"prezzo\" value=\"".$q->param('prezzo')."\"></input>
        <input type=\"hidden\" name=\"posti\" value=\"".$q->param('posti')."\"></input>
        <input type=\"hidden\" name=\"conducente\" value=\"".$q->param('cond')."\"></input>
        <textarea rows=\"\" cols=\"\" name=\"messaggio\"></textarea> \n
        
        <div><input type=\"submit\" value=\"Invia\"></input></div> \n";
  }    

  $contenuto = $contenuto."</div> \n ";
  my $file = "TravelShare/singoloViaggioLog.html";
  $hash_keys{USERNAME} = $username;
  $hash_keys{CONTENUTO} = $contenuto;  
  my $template_parser = Template->new;
  my $foglio = '';
  $template_parser->process($file,\%hash_keys,\$foglio);
  print $foglio;
}
else {
  $Bacheca{UTENTE} = "";
  $contenuto = $contenuto."\n 
    <h2>Bacheca dei messaggi</h2>  \n
     <div class=\"contenitore\">
      \n".research::query_bacheca_viaggio(\%Bacheca)."\n";

  my $file = "TravelShare/singoloViaggio.html";
  $hash_keys{CONTENUTO} = $contenuto;  
  my $template_parser = Template->new;
  my $foglio = '';
  $template_parser->process($file,\%hash_keys,\$foglio);
  print $foglio;
}

if(defined($session->param('problems'))) {
  $session->clear(['problems']);
  } 
