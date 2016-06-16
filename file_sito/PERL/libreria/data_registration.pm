#! /usr/bin/perl -w

###################################################
# Pacchetto di gestione del salvataggio dei dati
###################################################

package data_registration;

use strict;
use warnings;
use diagnostics;

use XML::LibXML;
use XML::Tidy;
use Template;
use Fcntl qw( :flock );

our $xml_file = 'libreria/travelshare_data_file.xml';

our $parser = XML::LibXML->new();





# Nota sull'eliminazione. riferimenti a utenti cancellati??????<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#argomenti: xpath, keyname, keyvalue, doc
sub verifica_presenza {
    my $xpath = shift @_;
    my $keyname = shift @_;
    my $keyvalue = shift @_;
    my $doc = shift @_;
    #my $q = "$xpath/[$keyname=$keyvalue]";
    my $q = join('',$xpath,'[',join ('=',$keyname,join('',"'",$keyvalue,"'")),']');
    print "$q\n";
    my @nodes = $doc->findnodes($q);
    my $numNodes = @nodes;
   return $numNodes;
}

sub serializzazione_apertura{
    open( my $fileHandle, "+<:encoding(UTF-8)", $xml_file )
        or die("Errore nell'apertura del file in lettura");
    my $flock = flock $fileHandle, LOCK_EX;
    if ( $flock != 1 ) {
        die("lock fallito.\n");
    }
    my $xml_string = do { local $/ = undef; <$fileHandle> };
    # print $xml_string;
    #####
    my $doc = $parser->parse_string($xml_string)
        or die("errore nel caricamento del documento dal parser");
    return {
        'doc' => $doc,
        'filehandle' => $fileHandle
    };
}

# argomenti: filehandle, doc
sub serializzazione_chiusura{
    my $fileHandle = shift @_;
    my $doc = shift @_;
    # abbellimento codice
    ###################################################################### per la prof: posso metterlo fuori dal lock?
    my $docString = $doc->toString();
    my $tidy_obj = XML::Tidy->new( 'xml' => $docString );
    $tidy_obj->tidy()
    ; # eventualmente come argomento accetta i caratteri da usare per l'identazione. def: 2 spazi.
    $docString = $tidy_obj->toString();
    seek $fileHandle, 0, 0;
    truncate $fileHandle, 0;
    print $fileHandle $docString;
    flock $fileHandle, LOCK_UN;
    close $fileHandle;
    return 0;
}

# argomenti: frammento xml da inserire, xpath.
sub serializzazione_inserimento {
    my $fragm = shift @_;
    my $xpath = shift @_;
    my $keyname = shift @_;
    my $keyvalue = shift @_;
    my $ris;
    #inizializzazione
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $fileHandle = $aux{'filehandle'};
    # Do stuff#############################################################################
    my $padre = $doc->findnodes($xpath)->get_node(1)->parentNode;
    if(verifica_presenza($xpath,$keyname,$keyvalue,$doc))
    {
        $ris = 0;
    }
    else
    {
        $padre->appendChild($fragm);
        $ris = 1;
    }
    # end writing
    serializzazione_chiusura($fileHandle,$doc);
    return ris;
}



#requisito:passare un array in cui siano presenti tutti i parametri
#domanda? array associativo o semplice e ci fidiamo dell'ordine??
# ID è valore numerico dei caratteri dell'email

sub inserisci_nuovo_utente {
    my %array_argom = shift @_;
    # calcolo chiave
    my $emailinchars = '';
    for $char ( split //, $array_argom{'Email'} ) {
        print ord($char);
    }
    ############à PROBLEMA SINTESI CHIAVE

    $array_argom{'IDUte'} = $emailinchars;
    my @parametri   = (
        'IDUte',
        'Email',       'Nome',     'Cognome', 'Sesso',
        'AnnoNascita', 'Telefono', 'Password'
    );
    my $output = "<Utente>\n";
    foreach my $element (@parametri) {
        my $new_chunck = "<$element>$array_argom{$element}</$element>";
        $output = join( "\n", $output, $new_chunck );
    }
    my $ultima_parte = "<Profilo>
    <NumFeedbRicevuti>0</NumFeedbRicevuti>
	<NumPassaggiOff>0</NumPassaggiOff>
    <NumPassaggiPart>0</NumPassaggiPart>
	<Valutazione>
	<PunteggioMedio>0</PunteggioMedio>
    <Compagnia>0</Compagnia>
	<Puntualita>0</Puntualita>
    <Pulizia>0</Pulizia>
	<Guida>0</Guida>
    </Valutazione>
    <Preferenze>
    <Chiacchiere>2</Chiacchiere>
	<Musica>2</Musica>
    <Animali>2</Animali>
	<Fumatore>2</Fumatore>
    </Preferenze>
    </Profilo>";
    $output = join( "\n", $output, $ultima_parte );
    $output = join( "\n", $output, "</Utente>\n" );

    my %componenti = ("inizio" => "<Utente>\n" , "fine" => join '', $ultima_parte, "</Utente>\n" );
    my $fragm = $parser->parse_balanced_chunk($output);

#comincia a contare da 1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

   # if( !serializzazione_inserimento( $fragm, "//Utente", "Email", $array_argom{"Email"}))
    if( !serializzazione_inserimento( $fragm, "//Utente", "Email", $array_argom{"Email"}))
    {
        print "Valore già presente\n";
    }
}

sub inserisci_nuovo_viaggio   { }
sub inserisci_nuovo_messaggio { }

sub modifica_utente { }

#sub modifica_utente{}
sub modifica_messaggio { }

sub elimina_utente    { }
sub elimina_viaggio   { }
sub elimina_messaggio { }

1;
