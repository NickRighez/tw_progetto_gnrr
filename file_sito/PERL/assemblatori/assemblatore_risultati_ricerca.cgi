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

if($q->param('partenza') eq '') {
  die("partenza mancante");
}
if($q->param('arrivo') eq '') {
  die("arrivo mancante");
}
if($q->param('data') eq '') {
  die("data di partenza mancante");
}
if(!($q->param('data')=~m/^[1-2][0-9][0-9][0-9]-[0-3][0-9]-[0-3][0-9]$/)) {
    die("data partenza non valida, inserire l anno in formato 'aaaa'");
}
 # verificare che la data di partenza sia futura?


my $partenza=$q->param('partenza');
my $arrivo=$q->param('arrivo');
my $data=$q->param('data');

my $session = new CGI::Session;
$session->load();

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
  ");

if(defined($session->param('loggedin'))) {
  my $username = $session->param('username');
  print("<div id=\"utente\"> \n
   <p>Ciao my $username </p>
   <p><a href=\"notifiche.html\">Notifiche (0)</a>  <a href=\"logout.cgi?operation=logout\" tabindex=\"\">Logout</a></p>
  </div>");
  }

print("<div id=\"contenuto\">");

my %aux = data_registration::serializzazione_apertura();
my $doc = $aux{'doc'};
my $filehandle = $aux{'filehandle'};
my @itiner=$doc->findnodes("//SetPassaggi/Passaggio/Itinerario[*[Data='$data']]");
my $num_it=@itiner;
for(my $i=0;$i<$num_it;$i++) {
  for(my $j=0;$j<5;$j++) {
      my @tappa=$itiner[$i]->findnodes("*[\@Numero=$j]");
      my $num = @tappa;
      if($num!=0) {
        my $luogo = $itiner[$i]->findnodes("*[\@Numero=$j]/Luogo")->get_node(1);
        if (index($luogo, $partenza) != -1 && $itiner[$i]->findnodes("*[\@Numero=$j]/PostiDisp")->get_node(1)->textContent() > 0) {
          for(my $k=$j+1;$k<5;$k++) {
            my @tappe_s=$itiner[$i]->findnodes("*[\@Numero=$k]");
            my $num = @tappe_s;
            if($num!=0) {
              if($itiner[$i]->findnodes("*[\@Numero=$j]/PostiDisp")->get_node(1)->textContent() == 0) {
                $k==5;
                $j==5;
              } 
              else {
                my $luog = $itiner[$i]->findnodes("*[\@Numero=$k]/Luogo")->get_node(1);
                if (index($luog, $arrivo) != -1) {
                  my $ora=$itiner[$i]->findnodes("*[\@Numero=0]/Ora")->get_node(1)->textContent();
                  my $part = $itiner[$i]->findnodes("*[\@Numero=$j]/Luogo")->get_node(1)->textContent();
                  my $arr = $itiner[$i]->findnodes("*[\@Numero=$k]/Luogo")->get_node(1)->textContent();
                  my $idv = $itiner[$i]->findnodes("../IDViaggio")->get_node(1)->textContent();
                  my $prezzo = '10'; # da sostituire con funzione che calcola il prezzo
                  my $posti = utility::calcola_posti_disponibili($j,$k,$idv,$doc);
                  my $conduc = $itiner[$i]->findnodes("../Conducente")->get_node(1)->textContent();
                  my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
                  my $eta=$year + 1900 - ($doc->findnodes("//SetUtenti/Utente[Username='$conduc']/AnnoNascita")->get_node(1)->textContent() ) ;
                  print("
                  <div class=\"risultato\">
                     <a href=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_singolo_passaggio.cgi?passaggio=$idv&part=$j&arr=$k&prezzo=$prezzo&posti=$posti&cond=$conduc\"><span class=\"partenza\">$part</span> &#8594; <span class=\"arrivo\">$arr</span></a>
                     
                     <p>Ora: $ora</p>
                     
                     <p>Posti: $posti<span class=\"destra\">$prezzo&euro; </span></p>
                     
                     <p>$conduc <span class=\"destra\">$eta anni</span></p>
            
                  </div> ");
                  
              }
            }
          }
          }
                 
        } 
      }

  }
}	
data_registration::serializzazione_chiusura($filehandle,$doc);
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


 
