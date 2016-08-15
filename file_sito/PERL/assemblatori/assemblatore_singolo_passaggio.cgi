#! /usr/bin/perl -w
print "Content-type: text/html\n\n";

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use lib "../libreria";
use research;

my $q=CGI->new;
my $session=new CGI::Session;
$session->load();

print("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">  \n

<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"it\" lang=\"it\"> \n
 <head> \n
  <title>Dettagli del viaggio - Travel Share</title> \n
  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/> \n
  <meta name=\"title\" content=\"...\" />  \n
  <meta name=\"description\" content=\"...\" /> \n
  <meta name=\"keywords\" content=\"messaggi, travel share, car pooling, passaggio, auto\" /> \n
  <meta name=\"author\" content=\"Giovanni Sanna, Nicolò Rigato, Riccardo Ardossi, Riccardo Sagges\" /> \n
  <meta name=\"language\" content=\"italian it\" /> \n
  
  <meta name=\"viewport\" content=\"width=device-width\" />  \n
  
  <link href=\"/screen.css\" rel=\"stylesheet\" type=\"text/css\" media=\"screen\" /> \n
  <link href=\"print.css\" rel=\"stylesheet\" type=\"text/css\" media=\"print\" /> \n
  
  <link rel=\"icon\" href=\"Immagini/TS_icon.png\" type=\"image/x-icon\" /> \n
  <link rel=\"shortcut icon\" href=\"Immagini/TS_icon.png\" type=\"image/x-icon\" /> \n
 </head>
 
 <body> \n
	
  <div id=\"header\"> \n
   <a href=\"homeLog.html\" tabindex=\"\"><img src=\"Immagini/banner.png\" id=\"banner\" alt=\"Banner Travel Share - Link diretto alla Home\" /></a>
   <a id=\"bottoneMenu\" href=\"#menu\" tabindex=\"\">Men&ugrave;</a> \n
  </div> \n
  ");


  
if(defined($session->param('loggedin'))) {
  my $username = $session->param('username');
  print("<div id=\"utente\"> \n
   <p>Ciao my $username </p>
   <p><a href=\"notifiche.html\">Notifiche (0)</a>  <a href=\"logout.cgi?operation=logout\" tabindex=\"\">Logout</a></p>
  </div>
  ");
}
print("<div id=\"contenuto\">");





my %Pass=(
	VIAGGIO => $q->param('passaggio'),   
	NUM_PARTENZA =>$q->param('part'),
	NUM_ARRIVO => $q->param('arr'),
	PREZZO => $q->param('prezzo'),
	POSTI => $q->param('posti'),
	CONDUCENTE => $q->param('cond')
	);
  
print research::query_viaggio(\%Pass);

if(defined($session->param('loggedin'))) {
  my $username = $session->param('username');
  my $pass = $q->param('passaggio'), ; 
  my $part =$q->param('part');
  my $arr = $q->param('arr');

  print "<a href=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/ricevitori/ricevitore_prenotazione.cgi?passaggio=$pass&part=$part&arr=$arr\" >Prenota</a>";

  my %Bacheca =(
    VIAGGIO => $q->param('passaggio'),
    UTENTE => $username
    );

    print("<h2>Bacheca dei messaggi</h2>  \n
     <a class=\"linkSottoH\" href=\"#NuovaConversazione\">Scrivi un messaggio</a> \n
     <div class=\"contenitore\"> \n
      ");
    print research::query_bacheca_viaggio(\%Bacheca);

    print("
      <div class=\"contenitore\" id=\"NuovaConversazione\"> \n
       
        <p>Inizia una nuova conversazione con il proprietario del viaggio!</p><br /> \n
       
        <textarea rows=\"\" cols=\"\" name=\"messaggio\"></textarea> \n
        
        <div><input type=\"submit\" value=\"Invia\"></input></div> \n
      
      </div> \n ");
    }


 print("  
  </div> \n

	<div id=\"menu\"> \n
  <ul> \n
   <li><a href=\"homeLog.html\" tabindex=\"\">Cerca un passaggio <span class=\"frecceMenu\">&raquo;</span></a></li> \n
   <li><a href=\"offriLog.html\" tabindex=\"\">Offri un passaggio <span class=\"frecceMenu\">&raquo;</span></a></li>   \n
   <li><a href=\"profiloPubblicoLog.html\" tabindex=\"\">Gestisci il profilo <span class=\"frecceMenu\">&raquo;</span></a></li> \n
   <li><a href=\"viaggi.html\" tabindex=\"\">Viaggi<span class=\"frecceMenu\">&raquo;</span></a></li> \n
   <li><a href=\"infoLog.html\" tabindex=\"\">Informazioni su <span xml:lang=\"en\" lang=\"en\">Travel Share</span> <span class=\"frecceMenu\">&raquo;</span></a></li>
  </ul> \n
  </div> \n
	
  <div id=\"footer\">  \n
   <a href=\"logout.cgi?operation=logout\" tabindex=\"\">Logout</a> \n
   <a href=\"#header\" tabindex=\"\">Torna su</a> \n
  </div> \n
  
  </body> \n
</html>");


 
