#! /usr/bin/perl
use XML::LibXML;
use XML::LibXSLT;
use XML::Tidy;
use strict;
use warnings;
use libreria::data_registration;


our $xml_file = '/home/nick/Documenti/progetto_tw/tw_progetto_gnrr/file_sito/provaXML.xml';

sub segna_letto{
  my $mitt = shift @_;
  my $send = shift @_; #proprietario della SESSIONE
  my $parser = XML::LibXML->new();
  open( my $fh, "+<:encoding(UTF-8)", $xml_file ) or die("Errore nell'apertura del file in lettura");
  my $xml_string = do { local $/ = undef; <$fh> };
          # print $xml_string;
          #####
  my $doc = $parser->parse_string($xml_string) or die("errore nel caricamento del documento dal parser");
  my $root = $doc->documentElement;
  #dovrebbe essere 1 vero??????
  my @conv = $root->findnodes("SetMessaggi/Conversazione[\@User1=\"$mitt\" and \@User2=\"$send\"] | SetMessaggi/Conversazione[\@User1=\"$send\" and \@User2=\"$mitt\"]");
  foreach my $messaggio( @conv){
    my @nodes = $messaggio->findnodes("Messaggio[Mittente=\'$mitt\' and \@Letto=\'no\']" );
    #print scalar @nodes;
    foreach my $elem (@nodes){
      $elem->setAttribute(Letto => 'si');
    }
  }
  #print scalar @conv;

  my $docString = $doc->toString();
  my $tidy_obj = XML::Tidy->new( 'xml' => $docString );
  $tidy_obj->tidy()
  ; # eventualmente come argomento accetta i caratteri da usare per l'identazione. def: 2 spazi.
  $docString = $tidy_obj->toString();
  seek $fh, 0, 0;
  truncate $fh, 0;
  print $fh $docString;
  close $fh;


}


segna_letto('u2','u1');
