#! /usr/bin/perl -w

###################################################
# Pacchetto di gestione delle ricerche nel file XML
###################################################

package research;

use XML::LibXML;
use XML::LibXSLT;
use Template;
use Cwd;


use strict;
use warnings;
use diagnostics;

#per il MIO server
#use lib '/usr/share/perl5';


#############################################
## Ricerche tramite XSLT
#############################################

# our === package variable, my === current scope variable
our $xml_file = '/var/www/html/cgi-bin/tw_progetto_gnrr/file_sito/provaXML.xml';


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
    my $template_parser = Template->new({
    ABSOLUTE => 1,
    });

    my $foglio_di_stile_con_parametri = '';
    $template_parser->process($style_file,\%vars,\$foglio_di_stile_con_parametri) ,"\n"; #or die $template_parser->error()
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
    if(! exists $lista->{"UTENTE"})
    {
        die "Non esiste la chiave UTENTE nella query users\n";
    }

    return generic_xslt_query('/var/www/html/cgi-bin/tw_progetto_gnrr/file_sito/PERL/libreria/xslt_files/users.xsl',\%$lista);
}

sub query_bacheca_viaggio
{
    my $lista = shift @_;
    if(! exists $lista->{"VIAGGIO"}) # passaggio che detiene la bacheca che si vuole visualizzare
    {
        die "Non esiste la chiave VIAGGIO nella query bacheca viaggio\n";
    }
    if(! exists $lista->{'UTENTE'}) { # utente che visualizza il passaggio che detiene la bacheca
        die "Non esiste la chiave UTENTE (che visualizza il passaggio) nella query bacheca viaggio"
    }
    return generic_xslt_query('/var/www/html/cgi-bin/tw_progetto_gnrr/file_sito/PERL/libreria/xslt_files/bachecaviaggio.xsl',\%$lista);
}

sub query_viaggio
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
    if(! exists $lista->{"PREZZO"})
    {
        die "Non esiste la chiave PREZZO nella query viaggi\n";
    }
    if(! exists $lista->{"POSTI"})
    {
        die "Non esiste la chiave POSTI nella query viaggi\n";
    }
    if(! exists $lista->{"CONDUCENTE"})
    {
        die "Non esiste la chiave CONDUCENTE nella query viaggi\n";
    }
    return generic_xslt_query('/var/www/html/cgi-bin/tw_progetto_gnrr/file_sito/PERL/libreria/xslt_files/singoloviaggio.xsl',\%$lista);
}

sub query_messaggi
{
    my $lista = shift @_;
    if(! exists $lista->{"UTENTE"})
    {
        die "Non esiste la chiave Utente nella query messaggi";
    }
    return generic_xslt_query('/var/www/html/cgi-bin/tw_progetto_gnrr/file_sito/PERL/libreria/xslt_files/messaggi.xsl',\%$lista);
}

sub query_conversazione
{
    my $lista = shift @_;
    if(! exists $lista->{"UTENTE"})
    {
        die "Non esiste la chiave utente nella query conversazione\n";
    }
    if(! exists $lista->{"MYSELF"})
    {
        die "Non esiste la chiave myself nella query conversazione\n";
    }
    if($lista->{"MYSELF"} eq $lista->{"UTENTE"})
    {
        die "nella query conversazione myself coincide con l altro utente di cui si ricerca la conversazione\n";
    }
    return generic_xslt_query('/var/www/html/cgi-bin/tw_progetto_gnrr/file_sito/PERL/libreria/xslt_files/singolaconversazione.xsl',\%$lista);
}

################### RICERCA NOTIFICHE PER UTENTE #######################################


#############################################
## Ricerche tramite xpath semplice
#############################################



sub generic_xpath_query
{
    my $parser = XML::LibXML->new(  );
    my $xml_doc = $parser->parse_file($xml_file);

}


sub query_usernamepwi {
    my ($username, $password) = @_;
   # my @userlist = $XML_DOC->getElementsByTagName('Utente');
    #foreach my $utente (@userlist){
	#my ( $nome, $passwd );
	#$nome = $utente->find
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