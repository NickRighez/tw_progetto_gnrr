#! /usr/bin/perl -w
print "Content-type: text/html\n\n";

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use lib "../libreria";
use research;
use data_registration;
use CGI::Session;

my $q=CGI->new;

my $session=new CGI::Session;
$session->load();
if(!defined($session->param('username'))) {
  die("not logged");
}

my $username=$session->param('username');
print("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">

<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"it\" lang=\"it\">
 <head>
  <title>Messaggi - Travel Share</title>
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
	
	<h1>Messaggi</h1> <!--LA DATA?-->");

my %aux=data_registration::serializzazione_apertura();
my $doc=$aux{'doc'};
my $filehandle=$aux{'filehandle'};

my @conv=$doc->findnodes("//SetMessaggi/Conversazione[\@User1='$username' or \@User2='$username']");

if(@conv == 0) {
  print "<p>Non ci sono conversazioni con altri utenti </p>";
}
else {
  for(my $i=0;$i<@conv;$i++) {
    my $ute;
    if($conv[$i]->findnodes("./\@User1")->get_node(1)->textContent eq $username) {
      $ute = $conv[$i]->findnodes("./\@User2")->get_node(1)->textContent;
    }
    else {
      $ute = $conv[$i]->findnodes("./\@User1")->get_node(1)->textContent;
    }
    my $data=$conv[$i]->findnodes("./Messaggio[1]/Data")->get_node(1)->textContent;
    my $ora=$conv[$i]->findnodes("./Messaggio[1]/Ora")->get_node(1)->textContent;
    my $testo=$conv[$i]->findnodes("./Messaggio[1]/Testo")->get_node(1)->textContent;
    my @nodes = $conv[$i]->findnodes("./Messaggio[Mittente='$ute' and \@Letto='no']");
    if(@nodes != 0) {
        print "<div class=\"conversazione nuova\">
                <a href=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_singola_conversaz.cgi?utente=$ute\" title=\"Nuovo messaggio\" class=\"\">$ute <span class=\"data\">$data $ora</span></a> <!--nota: lo span toglie la sottolineatura-->
                <p class=\"ultimoMessaggio\">$testo</p>
              </div>";
    }
    else {
        print "<div class=\"conversazione\">
                  <a href=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_singola_conversaz.cgi?utente=$ute\" title=\"Messaggio letto\" class=\"\">$ute <span class=\"data\">$data $ora</span></a> <!--nota: lo span toglie la sottolineatura-->
                  <p class=\"ultimoMessaggio\">$testo</p>
              </div>";
    } 
  }
}
    

print("
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


