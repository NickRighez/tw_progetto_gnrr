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
use lib '/usr/share/perl5';


#############################################
## Ricerche tramite XSLT
#############################################

# our === package variable, my === current scope variable
our $xml_file = 'libreria/travelshare_data_file.xml';


#parametri: nome file xml

sub generic_xslt_query
{
    my ($foglio_trasformazione,  @lista_filtri ) = @_;
    ###
    # Costruzione lista parametri
    my @lista_parentesi;
    foreach my $element (@lista_filtri){
        push @lista_parentesi, (join "", '['. $element . ']');
    }
    my $parametri = join('',@lista_parentesi);
    ###
    my $style_file = $foglio_trasformazione;

    my $xml_parser = XML::LibXML->new( );
    my $xslt_parser = XML::LibXSLT->new( );
    my $template_parser = Template->new();
    my %vars=('FILTRO' => $parametri);
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
    my @lista = @_;
    # controllo???? che in lista ci siano i parametri giusti??? secondo me no
    return generic_xslt_query('libreria/xslt_files/users.xsl',@lista);
}


sub query_viaggi
{
    my @lista = @_;
    return generic_xslt_query('libreria/xslt_files/viaggi.xsl',@lista);
}

sub query_messaggi
{
    my @lista = @_;
    return generic_xslt_query('libreria/slt_files/messaggi.xsl',@lista);
}

sub query_passaggi
{
    my @lista = @_;
    return generic_xslt_query('libreria/xslt_files/passaggi.xsl',@lista);
}

#############################################
## Ricerche tramite xpath semplice
#############################################

#
# è una cosa abbastanza a caso. devo vedere altri pezzi del progetto per capire come mi serve
# sia fatta la funzione.
#
#sub query_base_generic
#{
#    #my @lista = @_;
#    my $parser = XML::LibXML->new;
#    my $doc = $parser->parse_file($FILENAME);
#    my @nodes = $doc->findnodes($XPATH_EXPRESSION);
#    foreach my $node (@nodes) {
#        print $node->firstChild->data, "\n";
#    }
#}
#

sub generic_xpath_query
{
    my $parser = XML::LibXML->new(  );
    my $xml_doc = $parser->parse_file($xml_file);

}


sub query_usernamepw
{
    my ($username, $password) = @_;
    my @userlist = $XML_DOC->getElementsByTagName('Utente');
    #foreach my $utente (@userlist){
	#my ( $nome, $passwd );
	#$nome = $utente->find
}






1;