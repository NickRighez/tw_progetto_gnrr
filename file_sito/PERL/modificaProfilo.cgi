#!/usr/bin/perl
use strict;
use warnings;

use CGI qw/:standard/;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);

my $cgi = new CGI;

my $session=new CGI::Session;
$session->load();
if(!defined($session->param('username'))) {
  die('not logge');
}


my $username=$session->param('username');
print("
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">

<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"it\" lang=\"it\">
 <head>
  <title>Gestisci il profilo - Travel Share</title>
  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>
  <meta name=\"title\" content=\"...\" /> 
  <meta name=\"description\" content=\"...\" />
  <meta name=\"keywords\" content=\"profilo, travel share, car pooling, passaggio, auto\" />
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
   <a href=\"homeLog.html\" tabindex=\"\"><img src=\"Immagini/banner.png\" id=\"banner\" alt=\"Banner Travel Share - Link diretto alla Home\" /></a>
   <a id=\"bottoneMenu\" href=\"#menu\" tabindex=\"\">Men&ugrave;</a>
  </div>
  
  <div id=\"utente\">
   <p>Ciao $username</p>
   <p><a href=\"notifiche.html\">Notifiche (0)</a>  <a href=\"logout.cgi?operation=logout\" tabindex=\"\">Logout</a></p>
  </div>
  
  <div id=\"contenuto\">
  <h1>Modifica il profilo</h1> 
  <form action=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/ricevitori/ricevitore_modifica.cgi\" method=\"post\">
  <fieldset><legend></legend>
  <label for=\"nome\">Nome:</label>
    <input type=\"text\" id=\"nome\" name=\"nome\" value=\"Nome\" tabindex=\"\"></input><br class=\"acapo\" />
  
  <label for=\"cognome\">Cognome:</label>
    <input type=\"text\" id=\"cognome\" name=\"cognome\" value=\"Cognome\" tabindex=\"\"></input><br class=\"acapo\" />
  
  <label for=\"email\"><span xml:lang=\"en\" lang=\"en\">Email:</span></label>
    <input type=\"text\" id=\"email\" name=\"email\" value=\"Email\" tabindex=\"\"></input><br class=\"acapo\" />
  
  <!--<p>lo mettimo?</p>
    <label for=\"vecchiaPassword\">Vecchia <span xml:lang=\"en\" lang=\"en\">Password:</span></label>
    <input type=\"password\" id=\"vecchiaPassword\" name=\"vecchiaPassword\" tabindex=\"\"></input><br class=\"acapo\" />
    <label for=\"nuovaPassword\">Nuova <span xml:lang=\"en\" lang=\"en\">Password:</span></label>
    <input type=\"password\" id=\"nuovaPassword\" name=\"nuovaPassword\" tabindex=\"\"></input><br class=\"acapo\" />-->
   
    <p>Sesso:
  <input type=\"radio\" name=\"sesso\" id=\"maschio\" value=\"maschio\" checked=\"checked\"></input><label  for=\"maschio\">Maschio</label>
    <input type=\"radio\" name=\"sesso\" id=\"femmina\" value=\"femmina\"></input><label  for=\"femmina\">Femmina</label><br class=\"acapo\" /> 
    </p> 
  
    <label for=\"anno\">Anno di nascita:</label>
    <input type=\"text\" id=\"anno\" name=\"anno\" value=\"Anno\" tabindex=\"\"></input><br class=\"acapo\" />
  
  <label for=\"descrizioneForm\">Descrizione:</label>
  <textarea id=\"descrizioneForm\" rows=\"\" cols=\"\" name=\"descrizioneForm\"> </textarea > 
  
  <label for=\"annoPatente\">Anno di rilascio della patente:</label>
    <input type=\"text\" id=\"annoPatente\" name=\"annoPatente\" value=\"\" tabindex=\"\"></input><br class=\"acapo\" />
    
  <label for=\"auto\">Auto:</label>
    <input type=\"text\" id=\"auto\" name=\"auto\" value=\"\" tabindex=\"\"></input><br class=\"acapo\" />
    
  <div id=\"preferenze\">
  <h2>Preferenze</h2>
  
  <p>Chiacchiere:</p> <!--manca il checked=\"checked\"-->
  <div class=\"preferenzeGroup\">
  <input type=\"radio\" name=\"chiacchiere\" id=\"chiacchiere0\" class=\"radioNascosto\" value=\"0\"></input>
  <label for=\"chiacchiere0\"><img class=\"preferenzeImg marginRadioNascosto\" src=\"Immagini/BLA0.png\" alt=\"Silenzioso\"></img></label>
  <input type=\"radio\" name=\"chiacchiere\" id=\"chiacchiere1\" class=\"radioNascosto\" value=\"1\" ></input>
  <label for=\"chiacchiere1\"><img class=\"preferenzeImg marginRadioNascosto\" src=\"Immagini/BLA1.png\" alt=\"Poche chiacchiere\"></img></label>
  <input type=\"radio\" name=\"chiacchiere\" id=\"chiacchiere2\" class=\"radioNascosto\" value=\"2\"></input>
  <label for=\"chiacchiere2\"><img class=\"preferenzeImg marginRadioNascosto\" src=\"Immagini/BLA2.png\" alt=\"Chiacchierone\"></img></label>
  </div>
  
  <p>Musica:</p>
  <div class=\"preferenzeGroup\">
  <input type=\"radio\" name=\"musica\" id=\"musica0\" class=\"radioNascosto\" value=\"0\"></input>
  <label for=\"musica0\"><img class=\"preferenzeImg marginRadioNascosto\" src=\"Immagini/musica0.png\" alt=\"\"></img></label>
  <input type=\"radio\" name=\"musica\" id=\"musica1\" class=\"radioNascosto\" value=\"1\" ></input>
  <label for=\"musica1\"><img class=\"preferenzeImg marginRadioNascosto\" src=\"Immagini/musica1.png\" alt=\"\"></img></label>
  <input type=\"radio\" name=\"musica\" id=\"musica2\" class=\"radioNascosto\" value=\"2\"></input>
  <label for=\"musica2\"><img class=\"preferenzeImg marginRadioNascosto\" src=\"Immagini/musica2.png\" alt=\"\"></img></label>
  </div>
  
  <p>Animali:</p>
  <div class=\"preferenzeGroup\">
  <input type=\"radio\" name=\"animali\" id=\"animali0\" class=\"radioNascosto\" value=\"0\"></input>
  <label for=\"animali0\"><img class=\"preferenzeImg marginRadioNascosto\" src=\"Immagini/animali0.png\" alt=\"\"></img></label>
  <input type=\"radio\" name=\"animali\" id=\"animali1\" class=\"radioNascosto\" value=\"1\" ></input>
  <label for=\"animali1\"><img class=\"preferenzeImg marginRadioNascosto\" src=\"Immagini/animali1.png\" alt=\"\"></img></label>
  </div>
  
  <p>Fumatori:</p>
  <div class=\"preferenzeGroup\">
  <input type=\"radio\" name=\"fumatori\" id=\"fumatori0\" class=\"radioNascosto\" value=\"0\"></input>
  <label for=\"fumatori0\"><img class=\"preferenzeImg marginRadioNascosto\" src=\"Immagini/fumo0.png\" alt=\"\"></img></label>
  <input type=\"radio\" name=\"fumatori\" id=\"fumatori1\" class=\"radioNascosto\" value=\"1\" ></input>  
  <label for=\"fumatori1\"><img class=\"preferenzeImg marginRadioNascosto\" src=\"Immagini/fumo1.png\" alt=\"\"></img></label>
  </div>
  
  </div>
  
  <input type=\"submit\" value=\"Invia\" tabindex=\"\"></input>
  </fieldset>
  </form>
  
  </div>


 ");


print("
  <div id=\"menu\">
      <ul id=\"menuLista\">
       <li><a href=\"offriLog.html\" tabindex=\"\">Offri un passaggio <span class=\"frecceMenu\">&raquo;</span></a></li>  
       <li><a href=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_profilo.cgi?utente=$username\" tabindex=\"\">Gestisci il profilo <span class=\"frecceMenu\">&raquo;</span></a></li>
       <li><a href=\"viaggi.html\" tabindex=\"\">Viaggi<span class=\"frecceMenu\">&raquo;</span></a></li>
       <li><a href=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_conversazioni.cgi\" tabindex=\"\">Messaggi <span class=\"frecceMenu\">&raquo;</span></a></li>
       <li><a href=\"infoLog.html\" tabindex=\"\">Informazioni su <span xml:lang=\"en\" lang=\"en\">Travel Share</span> <span class=\"frecceMenu\">&raquo;</span></a></li>
      </ul>
      </div>
  <div id=\"footer\">
   <a href=\"#header\" tabindex=\"\">Torna su</a>
  </div>
  
  </body>
</html>
  ");

