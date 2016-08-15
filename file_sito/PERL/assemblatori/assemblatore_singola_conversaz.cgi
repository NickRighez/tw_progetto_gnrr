#! /usr/bin/perl -w

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
if(!defined($session->param('username'))) {
  die("not logged");
}

my $username = $session->param('username');

print("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">

<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"it\" lang=\"it\">
 <head>
  <title>Conversazione - Travel Share</title>
  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>
  <meta name=\"title\" content=\"...\" /> 
  <meta name=\"description\" content=\"...\" />
  <meta name=\"keywords\" content=\"messaggi, travel share, car pooling, passaggio, auto\" />
  <meta name=\"author\" content=\"Giovanni Sanna, Nicolò Rigato, Riccardo Ardossi, Riccardo Sagges\" />
  <meta name=\"language\" content=\"italian it\" />
  
  <meta name=\"viewport\" content=\"width=device-width\" /> 
  
  <link href=\"/screen.css\" rel=\"stylesheet\" type=\"text/css\" media=\"screen\" />
  <link href=\"print.css\" rel=\"stylesheet\" type=\"text/css\" media=\"print\" />
  
  <link rel=\"icon\" href=\"Immagini/TS_icon.png\" type=\"image/x-icon\" />
  <link rel=\"shortcut icon\" href=\"Immagini/TS_icon.png\" type=\"image/x-icon\" />
 </head>
 
 <body>
	
  <div id=\"header\">
   <a href=\"homeLog.html\" tabindex=\"\"><img src=\"Immagini/banner.png\" id=\"banner\" alt=\"Banner Travel Share - Link diretto alla Home\" /></a>
   <a id=\"bottoneMenu\" href=\"#menu\" tabindex=\"\">Men&ugrave;</a>
  </div>
  
  <div id=\"utente\">
   <p>Ciao $username</p>
   <p><a href=\"notifiche.html\">Notifiche (0)</a>  <a href=\"logout.cgi?operation=logout\" tabindex=\"\">Logout</a></p>
  </div>
	
  <div id=\"contenuto\">

	<h1>Conversazione con <a href=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_profilo.cgi?utente=$username\">",$session->param('ute'),"</a></h1>"); # da sostituire con parametri sessione

my %Conversazione=(     # Da sostituire con parametri sesisone
	UTENTE => $session->param('username'),
	MYSELF => $q->param('utente')
	);

print research::query_conversazione(\%Conversazione); 


print("
  <form action=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/ricevitori/ricevitore_messaggio_privato.cgi\" >
    <textarea rows=\"\" cols=\"\" name=\"messaggio\"></textarea>
    
    <div><input type=\"submit\" value=\"Invia\"></input></div>
</form>
  </div>
	<div id=\"menu\">
  <ul>
   <li><a href=\"homeLog.html\" tabindex=\"\">Cerca un passaggio <span class=\"frecceMenu\">&raquo;</span></a></li>
   <li><a href=\"offriLog.html\" tabindex=\"\">Offri un passaggio <span class=\"frecceMenu\">&raquo;</span></a></li>  
   <li><a href=\"profiloPubblicoLog.html\" tabindex=\"\">Gestisci il profilo <span class=\"frecceMenu\">&raquo;</span></a></li>
   <li><a href=\"viaggi.html\" tabindex=\"\">Viaggi<span class=\"frecceMenu\">&raquo;</span></a></li>
   <li><a href=\"infoLog.html\" tabindex=\"\">Informazioni su <span xml:lang=\"en\" lang=\"en\">Travel Share</span> <span class=\"frecceMenu\">&raquo;</span></a></li>
  </ul>
  </div>
	
  <div id=\"footer\">
   <a href=\"logout.cgi?operation=logout\" tabindex=\"\">Logout</a>
   <a href=\"#header\" tabindex=\"\">Torna su</a>
  </div>
  
  </body>
</html>");
