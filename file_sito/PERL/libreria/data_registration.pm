#! /usr/bin/perl -w

###################################################
# Pacchetto di gestione del salvataggio dei dati
###################################################


########################################################
# TUTTI I COINTROLLI SUGLI INPUT DEVONO ESSERE GIA STATI FATTI AL MOMENTO IN CUI SI CHIAMA LA FUNZIONE
##########################################################

package data_registration;

use strict;
use warnings;
use diagnostics;
use Switch;
use XML::LibXML;
use XML::Tidy;
use Template;
use Fcntl qw( :flock );
use libreria::utility;

our $xml_file = 'libreria/travelshare_data_file.xml';

our $parser = XML::LibXML->new();

# Nota sull'eliminazione. riferimenti a utenti cancellati??????<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

sub serializzazione_apertura {
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
    return (
        'doc' => $doc,
        'filehandle' => $fileHandle
    );
}

# argomenti: filehandle, doc
sub serializzazione_chiusura {
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
sub serializzazione_inserimento {          ####################  MODIFICA ######################
    my $fragm = shift @_;
    my $xpath_presenza = shift @_;
    my $xpath_padre = shift @_;
    my $ris;
    #inizializzazione
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $root = $doc->documentElement;
    my $fileHandle = $aux{'filehandle'};
    if(utility::verifica_presenza($xpath_presenza,$doc))
    {
        $ris = 0;
    }
    else
    {
        print $xpath_padre, "\n";
        $doc->findnodes($xpath_padre)->get_node(1)->appendChild($fragm);
        $ris = 1;
    }
    # end writing
    serializzazione_chiusura($fileHandle,$doc);
    return $ris;
}

#requisito:passare un array in cui siano presenti tutti i parametri
#domanda? array associativo o semplice e ci fidiamo dell'ordine??
# ID è valore numerico dei caratteri dell'email

sub inserisci_nuovo_utente {
    my $array_argom_ref = shift @_;
    my %array_argom = %$array_argom_ref;   # tutorialspoint/perl/perl_references
    my @parametri   = (
        'Username',
        'Email',       'Nome',     'Cognome', 'Sesso',
        'AnnoNascita', 'Password'
    );
    my $output = "<Utente>\n";
    foreach my $element (@parametri) {
        my $new_chunck = "<$element>$array_argom{$element}</$element>";
        $output = join( "\n", $output, $new_chunck );
        ######################################################################
         if(($array_argom{$element} eq '')){
            print "elemento vuoto";
             die "$element vuoto";
         }
        #######################################################################
    }

    # ATTENZIONE : tenere aggiornata $ultima_parte secondo lo Schema ##################################
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
    </Profilo>
    <Notifiche>
    </Notifiche>";
    $output = join( "\n", $output, $ultima_parte );
    $output = join( "\n", $output, "</Utente>\n" );

    my $fragm = $parser->parse_balanced_chunk($output); # or die ****************************************

    return serializzazione_inserimento( $fragm, "//Utente[Username=\"$array_argom{'Username'}\"","//SetUtenti[1]");
}


#### IL RICEVITORE DEVE TESTARE LA CONSISTENZA DI DATA/ORA IN SUCCESSIONE FRA LE TAPPE DELL INTERO ITINERARIO
sub inserisci_nuovo_viaggio   {
    my $array_argom_ref = shift @_;
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $fileHandle = $aux{'filehandle'};
    my $root = $doc->documentElement;
    my @passaggi =$root->findnodes("SetPassaggi/Passaggio");

    #############  CREAZIONE ID VIAGGIO ########################
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
    serializzazione_chiusura($fileHandle,$doc);
    #################################################################

    # ESTRAZIONE USERNAME CONDUCENTE DA SESSIONE ###################################
    my $output="<Passaggio>
          <IDViaggio>$idv</IDViaggio>
          <Conducente>u1</Conducente>
          <PrezzoTot>15</PrezzoTot>
          <PostiTot>4</PostiTot>
          <Dettagli>Max un bagaglio medio</Dettagli>
          <Itinerario> \n";
     ###################################################################

    my %array_argom = %$array_argom_ref; #  hash di riferimenti a hash CHIAVI : Partenza, Arrivo, Tappa1, Tappa2, Tappa3
    ### CREAZIONE PARTENZA #############################################
    if(!defined($array_argom{'Partenza'})) {
        die("E obbligatorio inserire una partenza valida");
    }
    my $p = utility::CreaTappa("Partenza",0,$array_argom{'Partenza'});
    $output = $output.$p;
    ### CREAZIONE TAPPA 1 #############################################
    if(defined($array_argom{'Tappa1'})) {
        my $t1 = utility::CreaTappa("Tappa",1,$array_argom{'Tappa1'});
        $output = $output.$t1;
    }
    ### CREAZIONE TAPPA 2 #############################################
    if(defined($array_argom{'Tappa2'})) {
        if(!defined($array_argom{'Tappa1'})) {
            die("Per inserire la seconda tappa è obbligatorio inserire la prima");
        }
        my $t2 = utility::CreaTappa("Tappa",2,$array_argom{'Tappa2'});
        $output = $output.$t2;
    }
    ### CREAZIONE TAPPA3 #############################################
    if(defined($array_argom{'Tappa3'})) {
        if(!defined($array_argom{'Tappa1'}) or !defined($array_argom{'Tappa2'})) {
            die("Per inserire la terza tappa è obbligatorio inserire le tappe precedenti");
        }
        my $t3 = utility::CreaTappa("Tappa",3,$array_argom{'Tappa3'});
        $output = $output.$t3;
    }
    ### CREAZIONE ARRIVO #############################################
    my $a = utility::CreaTappa("Arrivo",4,$array_argom{'Arrivo'});
    $output = $output.$a;

    $output = $output."</Itinerario>\n</Passaggio>";
    my $fragm = $parser->parse_balanced_chunk($output); # or die ****************************************
    return serializzazione_inserimento( $fragm, "//Passaggio[IDViaggio=\"$idv\"]", "//SetPassaggi[1]");
}

sub inserisci_prenotazione {
    my $array_argom_ref = shift @_;
    my %array_argom = %$array_argom_ref; # CHIAVI : Username, IDViaggio, NumTappaPartenza, NumTappaArrivo
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $fileHandle = $aux{'filehandle'};
    for(my $i=$array_argom{'NumTappaPartenza'}; $i<=$array_argom{'NumTappaArrivo'}; $i++) {
        my $xpath_tappa="//Passaggio[IDViaggio=\"$array_argom{'IDViaggio'}\"]/Itinerario/*[\@Numero=\"$i\"]";
        if(utility::verifica_presenza($xpath_tappa,$doc)) {
            my $pd = $doc->findvalue($xpath_tappa."/PostiDisp");
            my $new_pd = $pd - 1;
            my $new_node = "<PostiDisp>$new_pd</PostiDisp>";
            $new_node = $parser->parse_balanced_chunk($new_node);
            my $old_node = $doc->findnodes($xpath_tappa."/PostiDisp")->get_node(1);
            $old_node->replaceNode($new_node);
            my $prenot = "";
            if(utility::verifica_presenza($xpath_tappa."/Prenotazioni",$doc)) {
                my $parent = $doc->findnodes($xpath_tappa."/Prenotazioni")->get_node(1);
                $prenot = $parser->parse_balanced_chunk("<Utente>$array_argom{'Username'}</Utente>");
                $parent->appendChild($prenot);
            }
            else {
                my $parent = $doc->findnodes($xpath_tappa)->get_node(1);
                my $output ="<Prenotazioni>
                                <Utente>$array_argom{'Username'}</Utente>
                             </Prenotazioni>";
                $prenot = $parser->parse_balanced_chunk($output);
                $parent->appendChild($prenot);
            }
        }
    }
    serializzazione_chiusura($fileHandle,$doc);

}

sub inserisci_nuovo_messaggio_singolo {
    my $array_argom_ref = shift @_;  # DEVE CONTENERE CHIAVI : Mittente, Destinatario, Data, Ora, Testo
    my %array_argom = %$array_argom_ref;
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $fileHandle = $aux{'filehandle'};
    my $output = "";
    my $root = $doc->documentElement;
    my @conv = $root->findnodes("SetMessaggi/Conversazione[\@User1=\"$array_argom{'Mittente'}\" and \@User2=\"$array_argom{'Destinatario'}\"] | SetMessaggi/Conversazione[\@User1=\"$array_argom{'Destinatario'}\" and \@User2=\"$array_argom{'Mittente'}\"]");
    my $numNodes = @conv;
    if($numNodes == 0) {
        $output = $output."<Conversazione User1=\"$array_argom{'Mittente'}\" User2=\"$array_argom{'Destinatario'}\">
                                <Messaggio Letto=\"no\">
                                    <Mittente>$array_argom{'Mittente'}</Mittente>
                                    <Data>$array_argom{'Data'}</Data>
                                    <Ora>$array_argom{'Ora'}</Ora>
                                    <Testo>$array_argom{'Testo'}</Testo>
                                </Messaggio>
                            </Conversazione>";
        serializzazione_chiusura($fileHandle,$doc);
        my $fragm = $parser->parse_balanced_chunk($output);
        if(serializzazione_inserimento($fragm,"//SetMessaggi/Conversazione[User1=\"$array_argom{'Mittente'}\" and User2=\"$array_argom{'Destinatario'}\"] | //SetMessaggi/Conversazione[User1=\"$array_argom{'Mittente'}\" and User2=\"$array_argom{'Destinatario'}\"]","//SetMessaggi[1]")) {
            my %attr = (
                    Mittente => "$array_argom{'Mittente'}"
                );
            inserisci_notifica("NuovoMessaggio", \%attr, $array_argom{'Destinatario'});
            return 1;
        }
        else {
            return 0;
        }
    }
    else {
        $output = $output."<Messaggio>
                                    <Mittente>$array_argom{'Mittente'}</Mittente>
                                    <Data>$array_argom{'Data'}</Data>
                                    <Ora>$array_argom{'Ora'}</Ora>
                                    <Testo>$array_argom{'Testo'}</Testo>
                                </Messaggio>";
        serializzazione_chiusura($fileHandle,$doc);
        my $fragm = $parser->parse_balanced_chunk($output);
        if(serializzazione_inserimento($fragm,"//x","/ts:TravelShare/SetMessaggi/Conversazione[\@User1=\'$array_argom{'Mittente'}\' and \@User2=\'$array_argom{'Destinatario'}\'] | /ts:TravelShare/SetMessaggi/Conversazione[\@User1=\'$array_argom{'Destinatario'}\' and \@User2=\'$array_argom{'Mittente'}\']")) {
            my %attr = (
                    Mittente => "$array_argom{'Mittente'}"
                );
            inserisci_notifica("NuovoMessaggio",\%attr,$array_argom{'Destinatario'});
            return 1;
        }
        else {
            return 0;
        }
    }
    # INVIO NOTIFICA A DESTINATARIO
}
sub inserisci_nuovo_messaggio_bacheca {
    my $idv = shift @_; # id del viaggio
    my $array_argom_ref = shift @_; # DEVE CONTENERE CHIAVI : Mittente, Data, Ora, Testo  ( il messaggio da inserire )
    my %array_argom = %$array_argom_ref;
    my $array_risp_ref = shift @_; # DEVE CONTENERE CHIAVI : Mittente, Data, Ora, Testo ( del messaggio di cui è risposta )
    if($array_risp_ref != undef) { # => il messaggio è una risposta di un messaggio in bacheca di $idv
        my %array_risp = %$array_risp_ref;
        my $output = "<MessaggioBacheca>
                        <Mittente>$array_argom{'Mittente'}</Mittente>
                        <Data>$array_argom{'Data'}</Data>
                        <Ora>$array_argom{'Ora'}</Ora>
                        <Testo>$array_argom{'Testo'}</Testo>
                        <Risposte>
                        </Risposte>
                    </MessaggioBacheca>";
    my $fragm = $parser->parse_balanced_chunk($output);
    return serializzazione_inserimento($fragm,"//x","//Passaggio[IDViaggio=\'$idv\']/Bacheca/MessaggioBacheca[Mittente=\'$array_risp{'Mittente'}\' and Data=\'$array_risp{'Data'}\' and Ora=\'$array_risp{'Ora'}\' and Testo=\'$array_risp{'Testo'}\']/Risposte");
    }
    else { # => nuovo messaggio della bacheca
        print "undefined";
    }
 }

sub inserisci_notifica {
    my $tag = shift @_; # tag = NuovoMessaggio, NuovoMessaggioBacheca, FeedDaRilasciare, RichiestaPrenotaz, AccettazionePrenotaz
    my $attr = shift @_; # hash di attributi con chiavi = Utente, Viaggio, Mittente
    my $user_destinat = shift @_;
    my %attributi = %$attr;
    my $fragm = "<$tag ";
    foreach (keys %attributi ) {
        $fragm = $fragm.$_."=\""."$attributi{$_}"."\" ";
    }
    $fragm = $fragm." /> \n";
    $fragm = $parser->parse_balanced_chunk($fragm);
    return serializzazione_inserimento($fragm,"//x","//Utente[Username=\'$user_destinat\']/Notifiche");
}

sub inserisci_feedback {
    my $array_argom_ref = shift @_;
    # CHIAVI : IDMitt, IDDest, Passaggio, Commento, PunteggioMedio, Compagnia, Puntualita. Nel
    #             caso il destinatario sia il conducente del viaggio, anche le chiavi Pulizia e Guida
    my %array_argom = %$array_argom_ref;
    my $output = "<Feedback IDMitt=\"$array_argom{'IDMitt'}\" IDDest=\"$array_argom{'IDDest'}\">
                              <Passaggio>$array_argom{'Passaggio'}</Passaggio>
                              <Commento>$array_argom{'Commento'}</Commento> \n";

    if(utility::verifica_presenza("//Passaggio[IDViaggio=\"$array_argom{'Passaggio'}\" and Conducente=\"$array_argom{'IDDest'}\"]")) {

        $output = $output."   <ValutazioneConduc>
                                <PunteggioMedio>$array_argom{'PunteggioMedio'}</PunteggioMedio>
                                <Compagnia>$array_argom{'Compagnia'}</Compagnia>
                                <Puntualita>$array_argom{'Puntualita'}</Puntualita>
                                <Pulizia>$array_argom{'Pulizia'}</Pulizia>
                                <Guida>$array_argom{'Guida'}</Guida>
                              </ValutazioneConduc> \n";
    }
    else {
        $output = $output."   <ValutazionePasseg>
                                <PunteggioMedio>$array_argom{'PunteggioMedio'}</PunteggioMedio>
                                <Compagnia>$array_argom{'Compagnia'}</Compagnia>
                                <Puntualita>$array_argom{'Puntualita'}</Puntualita>
                              </ValutazionePasseg> \n";
    }
    $output = $output."</Feedback> \n";
    my $fragm = $parser->parse_balanced_chunk($output);
    return serializzazione_inserimento($fragm,"//SetFeedback/Feedback[\@IDMitt=\"$array_argom{'IDMitt'}\" and \@IDDest=\"$array_argom{'IDDest'}\"]","//SetFeedback");
}

sub inserisci_info_auto {
    my $array_argom_ref = shift @_; # CHIAVI : Username, Marca, Modello, Tipologia
    my %array_argom = %$array_argom_ref;
    my $output = "<Auto>
                    <Marca>$array_argom{'Marca'}</Marca>
                    <Modello>$array_argom{'Modello'}</Modello>
                    <Tipologia>$array_argom{'Tipologia'}</Tipologia>
                  </Auto> \n";
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $root = $doc->documentElement;
    my $fileHandle = $aux{'filehandle'};
    my $fragm = $parser->parse_balanced_chunk($output);
    if(utility::verifica_presenza("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Auto",$doc)) {
        #elimina_info_auto($array_argom{'Username'},$doc);
        my $auto = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Auto")->get_node(1);
        $auto->replaceNode($fragm);
    }
    else {
        my $sibling_node = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Valutazione")->get_node(1);
        my $parent = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo")->get_node(1);
        $parent->insertAfter($fragm,$sibling_node);
    }
    serializzazione_chiusura($fileHandle,$doc);
    return 1;
}

sub inserisci_info_patente {
    my $array_argom_ref = shift @_; # CHIAVI :  Username, Patente
    my %array_argom = %$array_argom_ref;
    my $output = "<Patente DataRilascio=\"$array_argom{'Patente'}\" /> \n";
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $root = $doc->documentElement;
    my $fileHandle = $aux{'filehandle'};
    my $fragm = $parser->parse_balanced_chunk($output);
    if(utility::verifica_presenza("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Patente",$doc)) {
        #elimina_info_auto($array_argom{'Username'},$doc);
        my $pat = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Patente")->get_node(1);
        $pat->replaceNode($fragm);
    }
    else {
        my $sibling_node;
        if(utility::verifica_presenza("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Auto",$doc)) {
            $sibling_node = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Auto")->get_node(1);
        }
        else {
            $sibling_node= $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Valutazione")->get_node(1);
        }
        my $parent = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo")->get_node(1);
        $parent->insertAfter($fragm,$sibling_node);
    }
    serializzazione_chiusura($fileHandle,$doc);
    return 1;
}

sub elimina_info_auto {
    my $user = shift @_;
    my $doc = shift @_;
    if(utility::verifica_presenza("//Utente[Username=\"$user\"]/Profilo/Auto",$doc)) {
        my $auto = $doc->findnodes("//Utente[Username=\"$user\"]/Profilo/Auto")->get_node(1);
        my $patente = $doc->findnodes("//Utente[Username=\"$user\"]/Profilo/Patente")->get_node(1);
        my $prof = $doc->findnodes("//Utente[Username=\"$user\"]/Profilo")->get_node(1);
        $prof->removeChild($doc->findnodes("//Utente[Username=\"$user\"]/Profilo/Auto")->get_node(1));
        $prof->removeChild($doc->findnodes("//Utente[Username=\"$user\"]/Profilo/Patente")->get_node(1));
    }
    return 1;
}

sub inserisci_preferenze {
    my $array_argom_ref = shift @_; # CHIAVI : Username, Chiacchere, Musica, Animali, Fumatore
    my %array_argom = %$array_argom_ref;
    my $output = "<Preferenze>
                    <Chiacchiere>$array_argom{'Chiacchere'}</Chiacchiere>
                    <Musica>$array_argom{'Musica'}</Musica>
                    <Animali>$array_argom{'Animali'}</Animali>
                    <Fumatore>$array_argom{'Fumatore'}</Fumatore>
                </Preferenze>";
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $root = $doc->documentElement;
    my $fileHandle = $aux{'filehandle'};
    my $fragm = $parser->parse_balanced_chunk($output);
    if(utility::verifica_presenza("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Preferenze",$doc)) {
        #elimina_info_auto($array_argom{'Username'},$doc);
        my $pref = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Preferenze")->get_node(1);
        $pref->replaceNode($fragm);
    }
    else {
        my $parent = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo")->get_node(1);
        $parent->insertAfter($fragm,undef);
    }
    serializzazione_chiusura($fileHandle,$doc);
    return 1;
}


sub modifica_utente { }

sub elimina_utente    {
    my $id = shift @_;
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $fileHandle = $aux{'filehandle'};
    # do stuff

    ######
    serializzazione_chiusura($fileHandle,$doc);
    return;
}

sub elimina_viaggio   {
}

sub elimina_messaggio { # serve xpath un po' complesso
}

1;
