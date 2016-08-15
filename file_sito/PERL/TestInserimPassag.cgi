#!/usr/bin/perl
use CGI;
use CGI ':standard';
use libreria::utility;
use libreria::data_registration;
use strict;
use warnings;
use diagnostics;

use XML::LibXML;
use XML::Tidy;
use Template;
use Fcntl qw( :flock );

our $xml_file = 'libreria/travelshare_data_file.xml';

#our $parser = XML::LibXML->new();

my $q=new CGI;
my $parser = XML::LibXML->new;
my $doc = $parser->parse_file($xml_file);
my $root = $doc->documentElement;
my @passaggi =$root->findnodes("SetPassaggi/Passaggio");
my $max = 0;
foreach my $node (@passaggi) {
      my $idv = $node->findvalue("IDViaggio");
      $idv = substr($idv,1);
      if($idv > $max) {
            $max = $idv;
      } 
}
$max = $max+1;
my $idv = "v".$max;

# ESTRAZIONE USERNAME DA SESSIONE ###################################
my $output="<Passaggio>
      <IDViaggio>$idv</IDViaggio>
      <Conducente>u1</Conducente>   
      <PrezzoTot>15</PrezzoTot>
      <PostiTot>4</PostiTot>
      <Dettagli>Max un bagaglio medio</Dettagli>
      <Itinerario> \n";
 ###################################################################           


print "Content-type: text/html\n\n";
print "<html><head></head><body>";

my $new = utility::crea_itinerario("Partenza");
$output = $output.$new;

if(param("AbilitaT1") eq "Abilita tappa 1")
{
      $new = utility::crea_itinerario("Tappa1");
      $output = $output.$new;
}
if(param("AbilitaT2") eq "Abilita tappa 2")
{
      if(!(param("AbilitaT1") eq "Abilita tappa 1") {
            die("Inserire tappa 1");
      }
      $new = utility::crea_itinerario("Tappa2");
      $output = $output.$new;      
}
if(param("AbilitaT3") eq "Abilita tappa 3")
{
      if(!(param("AbilitaT1") eq "Abilita tappa 1" && param("AbilitaT2") eq "Abilita tappa 2")) {
            die("Inserire tappe precedenti");
      }
      $new = utility::crea_itinerario("Tappa3");
      $output = $output.$new;
}
$new = utility::crea_itinerario("Arrivo");
$output = $output.$new;
$output = $output."</Itinerario>\n</Passaggio>";
print "</body></html>";
my $fragm = $parser->parse_balanced_chunk($output); # or die ****************************************
data_registration::serializzazione_inserimento( $fragm, "//Passaggio[IDViaggio=\"$idv\"]", "//SetPassaggi[1]");

    

