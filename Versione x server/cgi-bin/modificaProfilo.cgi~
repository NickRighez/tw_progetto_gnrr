#! /usr/bin/perl -w
print "Content-type: text/html\n\n\n";
use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use Template;
#use lib "../libreria";    
use libreria::sessione;
#use lib "../libreria";    
use libreria::data_registration;

 my $cgi = new CGI;                       
 my @s = sessione::creaSessione();  
 my $session = $s[0]; 
 my $doc = data_registration::get_xml_doc();

if(!defined($session->param('username'))) {
 	my %problems=(
     LOGIN_ERR => "Utente non loggato, pagina inaccessibile"
     );
  	$session->param('problems',\%problems);
  	print $session->header(-location => "login.cgi");
 }	 
else {
  my $username = $session->param('username');
  
  my $file = "../data/HTML_TEMPLATE/modificaProfilo.html";
  my %hash_keys = ( NOME_UTENTE => $session->param('username'));

  if(defined($session->param('problems'))) {
      my $prob = $session->param('problems');
      my %prob_hash = %$prob;
      while( my( $key, $value ) = each %prob_hash ){
        $hash_keys{$key}="$value";
    }
  }

    if(defined($session->param('old_input'))) {
      my $old = $session->param('old_input');
      my %old_hash = %$old;
      while( my( $key, $value ) = each %old_hash ){
        $hash_keys{$key}="$value";
    }
    }
    else {
      my $ute = $doc->findnodes("//SetUtenti/Utente[Username=\"$username\"]")->get_node(1);
      print "//SetUtenti/Utente[Username=\"$username\"]";
      $hash_keys{NOME} = $ute->findnodes("Nome")->get_node(1)->textContent;
      $hash_keys{COGNOME} = $ute->findnodes("Cognome")->get_node(1)->textContent;
      $hash_keys{EMAIL} = $ute->findnodes("Email")->get_node(1)->textContent;
      $hash_keys{ANNO} = $ute->findnodes("AnnoNascita")->get_node(1)->textContent;
      if($ute->exists("DescrizionePers")) {
        $hash_keys{DESCRIZIONEFORM} = $ute->findnodes("DescrizionePers")->get_node(1)->textContent;
      }
      if($ute->exists("Profilo/Auto"))  {
        $hash_keys{AUTO} = $ute->findnodes("Profilo/Auto")->get_node(1)->textContent;
      }
      if($ute->exists("Profilo/Patente"))  {
        $hash_keys{ANNOPATENTE} = $ute->findnodes("Profilo/Patente")->get_node(1)->textContent;
      }   
      if($ute->exists("Profilo/Preferenze"))  {
        my $chiac = $ute->findnodes("Profilo/Preferenze/Chiacchiere")->get_node(1)->textContent;
        my $key = "CHECKED_C".$chiac;
        $hash_keys{$key} = "checked=\"checked\"";

        my $musica = $ute->findnodes("Profilo/Preferenze/Musica")->get_node(1)->textContent;
        $key = "CHECKED_M".$musica;
        $hash_keys{$key} = "checked=\"checked\"";

        my $anim = $ute->findnodes("Profilo/Preferenze/Animali")->get_node(1)->textContent;
        $key = "CHECKED_A".$anim;
        $hash_keys{$key} = "checked=\"checked\"";

        my $fumat = $ute->findnodes("Profilo/Preferenze/Fumatore")->get_node(1)->textContent;
        $key = "CHECKED_F".$fumat;
        $hash_keys{$key} = "checked=\"checked\"";
      }

    }
my $cont = research::query_notifiche_utente($username, $doc);
  $hash_keys{NUM_NOTIFICHE} = @$cont[1];
    my $template_parser = Template->new;
    my $foglio = '';
    open my $fh, '<', $file;
    $template_parser->process($fh,\%hash_keys,\$foglio);
    #print $q->header();
    print $foglio;


  if(defined($session->param('problems'))) {
    $session->clear(['problems']);
  }
  if(defined($session->param('old_input'))) {
    $session->clear(['old_input']);
  }   
}
 
