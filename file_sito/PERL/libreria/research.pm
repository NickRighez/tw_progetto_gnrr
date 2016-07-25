#! /usr/bin/perl -w

###################################################
# Pacchetto di gestione delle ricerche nel file XML
###################################################

package research;

use XML::LibXML;
use XML::LibXSLT;
use Template;


use strict;
use warnings;
use diagnostics;

#per il MIO server
#use lib '/usr/share/perl5';


#############################################
## Ricerche tramite XSLT
#############################################

# our === package variable, my === current scope variable
our $xml_file = 'libreria/travelshare_data_file.xml';


#parametri: nome file xml

sub generic_xslt_query
{
    my ($style_file,  $lista_filtri );
    $style_file  = shift @_;
    $lista_filtri = shift @_;
    ###
    # Costruzione lista parametri
#    my @lista_parentesi;
#    foreach my $element (@lista_filtri){
#        push @lista_parentesi, (join "", '['. $element . ']');
#    }
#    my $parametri = join('',@lista_parentesi);
    ###
    my %vars= %$lista_filtri;
    my $xml_parser = XML::LibXML->new( );
    my $xslt_parser = XML::LibXSLT->new( );
    my $template_parser = Template->new();

    my $foglio_di_stile_con_parametri = '';
    $template_parser->process($style_file,\%vars,\$foglio_di_stile_con_parametri);
	(length $foglio_di_stile_con_parametri) or die("ERRORE 1: foglio xslt vuoto\n".$style_file);
    my $style_oggetto_xml = $xml_parser->parse_string($foglio_di_stile_con_parametri);
    my $style_oggetto_xsl = $xslt_parser->parse_stylesheet( $style_oggetto_xml );
    my $file_oggetto_xml = $xml_parser->parse_file( $xml_file );
    my $html_output = $style_oggetto_xsl->transform( $file_oggetto_xml);
	(length $html_output) or die("ERRORE 2: output HTML vuoto\n".$style_file);
#print "checkpoint 1\n";
#print "--------- ". (length $html_output) . " ---------\n";
return $html_output;
   # print $style_oggetto_xsl->output_string( $html_output );
}

sub query_users
{
    my $lista = shift @_;
    # controllo che ci siano tutti i filtri necessari. else die
    if(! exists $lista->{"UTENTE"}){
        die "Non esiste la chiave UTENTE nella query users\n";
    }

    return generic_xslt_query('libreria/xslt_files/users.xsl',\%$lista);
}


sub query_viaggi
{
    my $lista = shift @_;
    if(! exists $lista->{"VIAGGIO"})
    {
        die "Non esiste la chiave VIAGGIO nella query viaggi\n";
    }
    if(! exists $lista->{"NUM_PARTENZA"})
    {
        die "Non esiste la chiave NUM_PARTENZA nella query viaggi\n";
    }
    if(! exists $lista->{"NUM_ARRIVO"})
    {
        die "Non esiste la chiave NUM_ARRIVO nella query viaggi\n";
    }
    return generic_xslt_query('libreria/xslt_files/singoloviaggio.xsl',\%$lista);
}

sub query_messaggi
{
    my $lista = shift @_;
    if(! exists $lista->{"UTENTE"})
    {
        die "Non esiste la chiave Utente nella query messaggi";
    }
    return generic_xslt_query('libreria/slt_files/messaggi.xsl',\%$lista);
}

sub query_conversazione
{
    my $lista = shift @_;
    if(! exists $lista->{"USER1"})
    {
        die "Non esiste la chiave user1 nella query conversazione\n";
    }
    if(! exists $lista->{"USER2"})
    {
        die "Non esiste la chiave USER2 nella query conversazione\n";
    }
    if(! exists $lista->{"MYSELF"})
    {
        die "Non esiste la chiave myself nella query conversazione\n";
    }
    if($lista->{"MYSELF"} ne $lista->{"USER1"} && $lista->{"MYSELF"} ne $lista->{"USER2"})
    {
        die "nella query conversazione myself non coincide nè con user1 nè con user2\n";
    }
    return generic_xslt_query('libreria/slt_files/singolaconversazione.xsl',\%$lista);
}


#############################################
## Ricerche tramite xpath semplice
#############################################



#sub generic_xpath_query
#{
#    my $parser = XML::LibXML->new(  );
#    my $xml_doc = $parser->parse_file($xml_file);

#}


sub query_usernamepw
{
    my $username = shift @_;
    my $password = shift @_;
    my $xml_parser = XML::LibXML->new( );
    my $XML_DOC = $xml_parser->parse_file( $xml_file );
    #my @userlist = $XML_DOC->getElementsByTagName('Utente');
    #foreach my $utente (@userlist){
	#my ( $nome, $passwd );
	#$nome = $utente->find
  my $path = "/ts:TravelShare/SetUtenti/Utente[Username='$username' and Password='$password']";
  my @nodes = $XML_DOC->findnodes($path);
  #print "$path\n";
  return scalar @nodes;
}



sub getNotifications(){
    my $username = shift @_;
    #cercare i dati e fare una lista delle chiavi
    my %messaggi;
    my %prenotazioni;
    my %bacheca;
    return ('messaggi' =>\%messaggi,  )
}


1;
