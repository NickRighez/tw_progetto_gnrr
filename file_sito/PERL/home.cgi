#!/usr/bin/perl
use strict;
use warnings;
use diagnostics;
#use CGI::Cookie;             
 use CGI;                 
 use CGI::Session;                
 use CGI::Carp qw(fatalsToBrowser);                       
 my $cgi = new CGI;                       
 
 #my $sid = $cgi->cookie('CGISESSID') || $cgi->param('CGISESSID') || undef;                                      
 my $session = new CGI::Session;#load CGI::Session(undef, $sid, {Directory=>'/var/www/html/cgi-bin'});   
 $session->load();
 #my @arr=$session->param;
  print "Content-type: text/html\n\n";                      
print("
 	<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">

<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"it\" lang=\"it\">
 <head>
  <title>Home - Travel Share</title>
  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>
  <meta name=\"title\" content=\"...\" /> 
  <meta name=\"description\" content=\"...\" />
  <meta name=\"keywords\" content=\"home, travel share, car pooling, passaggio, auto\" />
  <meta name=\"author\" content=\"Giovanni Sanna, Nicolò Rigato, Riccardo Ardossi, Riccardo Saggese\" />
  <meta name=\"language\" content=\"italian it\" />
  
  <meta name=\"viewport\" content=\"width=device-width\" /> 
  
  <link href=\"/screen.css\" rel=\"stylesheet\" type=\"text/css\" media=\"screen\" />
  <link href=\"print.css\" rel=\"stylesheet\" type=\"text/css\" media=\"print\" />
  
  <link rel=\"icon\" href=\"Immagini/TS_icon.png\" type=\"image/x-icon\" />
  <link rel=\"shortcut icon\" href=\"Immagini/TS_icon.png\" type=\"image/x-icon\" />
 </head>
 
 <body>
	
  <div id=\"header\">
   <a href=\"home.html\" tabindex=\"\"><img src=\"Immagini/banner.png\" id=\"banner\" alt=\"Banner Travel Share - Link diretto alla Home\" /></a>
   <a id=\"bottoneMenu\" href=\"#menu\" tabindex=\"\">Men&ugrave;</a>
  </div>
	
	
  <div id=\"contenuto\">
	
	<h1>Cerca un passaggio!</h1> 
	
	<form action=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_risultati_ricerca.cgi\" method=\"get\">
	<fieldset><legend></legend>
	<label for=\"partenza\">Partenza</label><br class=\"acapo\" />
	<input type=\"text\" id=\"partenza\" name=\"partenza\" tabindex=\"\"></input><br class=\"acapo\" />
	<p class=\"errore\">ERRORE</p>
	<label for=\"arrivo\">Arrivo</label><br class=\"acapo\" />
	<input type=\"text\" id=\"arrivo\" name=\"arrivo\" tabindex=\"\"></input><br class=\"acapo\" />
	<p class=\"errore\">ERRORE</p>
	<label for=\"data\">Data</label><br class=\"acapo\" />
	<input type=\"text\" id=\"data\" name=\"data\" tabindex=\"\"></input><br class=\"acapo\" />
	<p class=\"errore\">ERRORE: inserire una data valida secondo il formato gg/mm/aa</p>
	<input type=\"submit\" value=\"Cerca\" tabindex=\"\"></input>
	</fieldset>
	</form>

  </div>
	"); 



if(defined($session->param('loggedin'))) {
	my $username=$session->param('username');
	print("
		<p> LOGGED </p>
		<div id=\"menu\">
		  <ul id=\"menuLista\">
		   <li><a href=\"offriLog.html\" tabindex=\"\">Offri un passaggio <span class=\"frecceMenu\">&raquo;</span></a></li>  
		   <li><a href=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_profilo.cgi?utente=$username\" tabindex=\"\">Gestisci il profilo <span class=\"frecceMenu\">&raquo;</span></a></li>
		   <li><a href=\"viaggi.html\" tabindex=\"\">Viaggi<span class=\"frecceMenu\">&raquo;</span></a></li>
		   <li><a href=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_conversazioni.cgi\" tabindex=\"\">Messaggi <span class=\"frecceMenu\">&raquo;</span></a></li>
		   <li><a href=\"infoLog.html\" tabindex=\"\">Informazioni su <span xml:lang=\"en\" lang=\"en\">Travel Share</span> <span class=\"frecceMenu\">&raquo;</span></a></li>
		  </ul>
		  </div>
		");
	}
else {
	print("
		<p> NOT LOGGED </p>
		<div id=\"menu\">
		  <ul id=\"menuLista\">
		   <li><a href=\"offri.html\" tabindex=\"\">Offri un passaggio <span class=\"frecceMenu\">&raquo;</span></a></li>  
		   <li><a href=\"http://localhost/iscriviti.html\" tabindex=\"\">Iscriviti <span class=\"frecceMenu\">&raquo;</span></a></li>
		   <li><a href=\"http://localhost/accedi.html\" tabindex=\"\">Accedi <span class=\"frecceMenu\">&raquo;</span></a></li>
		   <li><a href=\"info.html\" tabindex=\"\">Informazioni su <span xml:lang=\"en\" lang=\"en\">Travel Share</span> <span class=\"frecceMenu\">&raquo;</span></a></li>
		  </ul>
		  </div>
		");
}

print("
	<div id=\"footer\">
   <a href=\"#header\" tabindex=\"\">Torna su</a>
  </div>
  
  </body>
</html>
	");