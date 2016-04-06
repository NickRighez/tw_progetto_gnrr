#! /usr/bin/perl

use strict;
use warnings;
use XML::LibXML;
use XML::LibXSLT;
#use CGI;
use Template;

my $style_file = "style.xsl";
my $xml_file = "test.xml";
my $xml_parser = XML::LibXML->new( );
my $xslt_parser = XML::LibXSLT->new( );
my $template_parser = Template->new();
my %vars=('FILTRO1' => 'anno &gt; 2000');    #,'FILTRO2' => "autore = 'King'");
my $foglio_di_stile_con_parametri = '';
# inserisce il contenuto del file style come stringa all'interno della variabile (vuota)
# foglio_di_stile_con_parametri passata per riferimento
$template_parser->process($style_file,\%vars,\$foglio_di_stile_con_parametri);
my $style_oggetto_xml = $xml_parser->parse_string($foglio_di_stile_con_parametri);
my $style_oggetto_xsl = $xslt_parser->parse_stylesheet( $style_oggetto_xml );
my $file_oggetto_xml = $xml_parser->parse_file( $xml_file );
my $html_output = $style_oggetto_xsl->transform( $file_oggetto_xml);
print "Content-type: text/html\r\n\r\n";
print $style_oggetto_xsl->output_string( $html_output );
