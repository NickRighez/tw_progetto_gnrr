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
use data_registration;

my $q=CGI->new;

my $session = new CGI::Session;#load CGI::Session(undef, $sid, {Directory=>'/tmp'});   
$session->load();

print("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">

<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"it\" lang=\"it\">
 <head>
  <title>Profilo utente - Travel Share</title>
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
  
  <div id=\"contenuto\">
  
  <h1> 
");   

my %aux=data_registration::serializzazione_apertura();
my $ute= $q->param('utente'); # usernaem dell utente appeso alla stringa URL
my $doc=$aux{'doc'};
my $filehandle=$aux{'filehandle'};
my $nome = $doc->findnodes("//SetUtenti/Utente[Username=\"$ute\"]/Nome")->get_node(1)->textContent;
my $cognome = $doc->findnodes("//SetUtenti/Utente[Username=\"$ute\"]/Cognome")->get_node(1)->textContent;
data_registration::serializzazione_chiusura($filehandle,$doc);

print("$nome $cognome</h1>");

# SE L UTENTE E' LOGGATO:
# - Inserire i link per scrivere messaggio privato e per modificare il profilo ( se l utente loggato sta visualizzando il proprio profilo)
# - inoltre : (print sottostante)
if(defined($session->param('username'))) {
  if($session->param('username') eq $ute) {
    print("<a class=\"linkSottoH\" href=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/modificaProfilo.cgi\">Modifica</a>");
  }
  else {
    $session->param('ute',$ute);
    print("<a class=\"linkSottoH\" href=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_singola_conversaz.cgi?utente=$ute\">Scrivi un messaggio privato</a> ");
  }  
  print("</p>
   <p><a href=\"notifiche.html\">Notifiche (0)</a>  <a href=\"logout.cgi?operation=logout\" tabindex=\"\">Logout</a></p>
  </div>");
}

	
  print "<br>",$session->param('username'),"<br>";

my %Ute=(
	UTENTE => $session->param('username')   # VA SOSTIUITO CON L USERNAME DELL UTENTE DELLA SESSIONE CORRENTE
	);

print research::query_users(\%Ute);

print("
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

 
