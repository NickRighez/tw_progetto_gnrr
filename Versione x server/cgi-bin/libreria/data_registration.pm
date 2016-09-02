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
#use lib "libreria";
#use utility;
use libreria::utility;
#use Switch;
use XML::LibXML;
use XML::Tidy;my ($sec,$min,$hour,$mday, $mon, $year ,$wday,$yday,$isdst) = localtime();
$year = $year + 1900;
use Template;
use libreria::date_time;

use Fcntl qw( :flock );

our $xml_file = '../data/TravelShare.xml';

our $parser = XML::LibXML->new();

# Nota sull'eliminazione. riferimenti a utenti cancellati??????<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

sub get_xml_doc {
    open( my $fileHandle, "<:encoding(UTF-8)", $xml_file )
        or die("Errore nell'apertura del file in lettura:  $!");
        my $xml_string = do { local $/ = undef; <$fileHandle> };
    my $doc = $parser->parse_string($xml_string)
        or die("errore nel caricamento del documento dal parser");
    return $doc;
}

sub serializzazione_apertura{
    open( my $fileHandle, "+<:encoding(UTF-8)", $xml_file )
        or die("Errore nell'apertura del file in lettura : $!");
    my $flock = flock $fileHandle, LOCK_EX;
    if ( $flock != 1 ) {
        die("lock fallito.\n");
    }
    my $xml_string = do { local $/ = undef; <$fileHandle> };
    # print $xml_string;
    #####
    my $doc = $parser->parse_string($xml_string)
        or die("errore nel caricamento del documento dal parser  : $!");
    return (
        'doc' => $doc,
        'filehandle' => $fileHandle
    );
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
    my $xpath_presenza = shift @_; 
    my $xpath_padre = shift @_;
    my $ris;
    #inizializzazione
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $fileHandle = $aux{'filehandle'};
    if(utility::verifica_presenza($xpath_presenza,$doc))
    {
        $ris = 0;
    }
    else
    {
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
        'Email',       'Nome',     'Cognome', 'DescrizionePers', 'Sesso',
        'AnnoNascita', 'Password'
    );
    my $output = "<Utente>\n";
    foreach my $element (@parametri) {
        if(defined($array_argom{$element})) {
            my $new_chunck = "<$element>$array_argom{$element}</$element>";
            $output = join( "\n", $output, $new_chunck );
         # eliminato il controllo per elemento vuoto
        }       
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
    return serializzazione_inserimento( $fragm, "//Utente[Username=\"$array_argom{'Username'}\"]","//SetUtenti[1]");
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
    my %array_argom = %$array_argom_ref; #  hash di riferimenti a hash CHIAVI : Partenza, Arrivo, Tappa1, Tappa2, Tappa3
    # ESTRAZIONE USERNAME CONDUCENTE DA SESSIONE ###################################
    my $output="<Passaggio Passato=\"no\">
          <IDViaggio>$idv</IDViaggio>
          <Conducente>$array_argom{'Conducente'}</Conducente>   
          <PrezzoTot>$array_argom{'PrezzoTot'}</PrezzoTot>
          <PostiTot>$array_argom{'PostiDisp'}</PostiTot>\n";
    if(defined($array_argom{'Dettagli'})) {
        $output=$output."<Dettagli>$array_argom{'Dettagli'}</Dettagli>\n";
    }
    $output=$output."<Itinerario> \n";
     ###################################################################   
    
    ### CREAZIONE PARTENZA #############################################
    my $p = utility::CreaTappa("Partenza",0,$array_argom{'Partenza'});
    $output = $output.$p;
   
    ### CREAZIONE TAPPA 1 #############################################
    if(defined($array_argom{'Tappa1'})) {
        my $t1 = utility::CreaTappa("Tappa",1,$array_argom{'Tappa1'});
        $output = $output.$t1;
    }
   
    ### CREAZIONE TAPPA 2 #############################################
    if(defined($array_argom{'Tappa2'})) {
        my $t2 = utility::CreaTappa("Tappa",2,$array_argom{'Tappa2'});
        $output = $output.$t2;
    }
   
    ### CREAZIONE TAPPA3 #############################################
    if(defined($array_argom{'Tappa3'})) {
        my $t3 = utility::CreaTappa("Tappa",3,$array_argom{'Tappa3'});
        $output = $output.$t3;
    }
    ### CREAZIONE ARRIVO #############################################
    my $a = utility::CreaTappa("Arrivo",4,$array_argom{'Arrivo'});
    $output = $output.$a;

    $output = $output."</Itinerario>\n<Bacheca></Bacheca></Passaggio>";
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
        my @nodes = $doc->findnodes("//Passaggio[IDViaggio=\"$array_argom{'IDViaggio'}\"]/Itinerario/*[\@Numero=\"$i\"]");
        if(@nodes != 0) {
            my $pd = $doc->findvalue($xpath_tappa."/PostiDisp");
            my $new_pd = $pd - 1;
            my $new_node = "<PostiDisp>$new_pd</PostiDisp>";
            $new_node = $parser->parse_balanced_chunk($new_node);
            my $old_node = $doc->findnodes($xpath_tappa."/PostiDisp")->get_node(1);
            $old_node->replaceNode($new_node);
            my $prenot = "";
            my $parent = $doc->findnodes($xpath_tappa."/Prenotazioni")->get_node(1);
            $prenot = $parser->parse_balanced_chunk("<Utente>$array_argom{'Username'}</Utente>");
            $parent->appendChild($prenot);
        }
    }    
    serializzazione_chiusura($fileHandle,$doc);
    return 1;
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
        if(serializzazione_inserimento($fragm,"//x","//SetMessaggi[1]")) {
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
        $output = $output."<Messaggio Letto=\"no\">
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

# da valutare a chi inviare una notifica dopo l inserimento di un messaggio in bacheca
# un 
sub inserisci_nuovo_messaggio_bacheca {
    my $idv = shift @_; # id del viaggio
    my $array_argom_ref = shift @_; # DEVE CONTENERE CHIAVI : Mittente, Destinatario, Data, Ora, Testo  ( il messaggio da inserire ) 
    my %array_argom = %$array_argom_ref;
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $fileHandle = $aux{'filehandle'};
    my $root = $doc->documentElement;
    my $output;
    my $conducente= $root->findnodes("//SetPassaggi/Passaggio[IDViaggio=\"$idv\"]/Conducente")->get_node(1)->textContent();
    # caso 1: il conducente(Mittente) risponde un messaggio, quindi deve esistere una conversazione con l utente $array_argom{'Destinatario'}
    if($array_argom{'Mittente'} eq $conducente) { 
        my @conv = $root->findnodes("//SetPassaggi/Passaggio[IDViaggio=\"$idv\"]/Bacheca/ConversazioneBacheca[\@User1=\"$array_argom{'Destinatario'}\" and \@User2=\"$conducente\"]");  
        $output = $output."<Messaggio>
                                    <Mittente>$array_argom{'Mittente'}</Mittente>
                                    <Data>$array_argom{'Data'}</Data>
                                    <Ora>$array_argom{'Ora'}</Ora>
                                    <Testo>$array_argom{'Testo'}</Testo>
                            </Messaggio>";
        serializzazione_chiusura($fileHandle,$doc);
        my $fragm = $parser->parse_balanced_chunk($output);
        if(serializzazione_inserimento($fragm,"//x","/ts:TravelShare/SetPassaggi/Passaggio[IDViaggio=\"$idv\"]/Bacheca/ConversazioneBacheca[\@User1=\"$array_argom{'Destinatario'}\" and \@User2=\"$conducente\"]")) {
            my %attr = (
                    Mittente => "$array_argom{'Mittente'}",
                    Passaggio => "$idv"
                );
            #inserisci_notifica("NuovoMessaggioBacheca",\%attr,$array_argom{'Destinatario'});
            return 1;
        } 
        else {
            return 0;
        } 
    }
     # caso 2 : il mittente è un utente (diverso dal conducente del viaggio in cui si vuole inserire un messaggio)
    else {
        my @conv = $root->findnodes("//SetPassaggi/Passaggio[IDViaggio=\"$idv\"]/Bacheca/ConversazioneBacheca[\@User1=\"$array_argom{'Mittente'}\" and \@User2=\"$conducente\"]");  
        my $numNodes = @conv;
        # se non esiste una conversazione tra i due utenti, crea la nuova conversazione 
        if($numNodes == 0) {
            $output = $output."<ConversazioneBacheca User1=\"$array_argom{'Mittente'}\" User2=\"$conducente\"> 
                                    <Messaggio>
                                        <Mittente>$array_argom{'Mittente'}</Mittente>
                                        <Data>$array_argom{'Data'}</Data>
                                        <Ora>$array_argom{'Ora'}</Ora>
                                        <Testo>$array_argom{'Testo'}</Testo>
                                    </Messaggio>
                                </ConversazioneBacheca>";
            serializzazione_chiusura($fileHandle,$doc);
            my $fragm = $parser->parse_balanced_chunk($output);
            if(serializzazione_inserimento($fragm,"//x","//SetPassaggi/Passaggio[IDViaggio=\"$idv\"]/Bacheca")) {
                my %attr = (
                        Mittente => "$array_argom{'Mittente'}",
                        Passaggio => "$idv"
                    );
                #inserisci_notifica("NuovoMessaggioBacheca", \%attr, $conducente);
                return 1;
            }
            else {
                return 0;
            }
        }
        # esiste già una conversazione tra i due utenti, inserisce il messaggio all interno di essa
        else {
            $output = $output."<Messaggio>
                                        <Mittente>$array_argom{'Mittente'}</Mittente>
                                        <Data>$array_argom{'Data'}</Data>
                                        <Ora>$array_argom{'Ora'}</Ora>
                                        <Testo>$array_argom{'Testo'}</Testo>
                                    </Messaggio>";
            serializzazione_chiusura($fileHandle,$doc);
            my $fragm = $parser->parse_balanced_chunk($output);
            if(serializzazione_inserimento($fragm,"//x","/ts:TravelShare/SetPassaggi/Passaggio[IDViaggio=\"$idv\"]/Bacheca/ConversazioneBacheca[\@User1=\"$array_argom{'Mittente'}\" and \@User2=\"$conducente\"]")) {
                my %attr = (
                        Mittente => "$array_argom{'Mittente'}",
                        Passaggio => "$idv"
                    );
                #inserisci_notifica("NuovoMessaggioBacheca",\%attr,$conducente);
                return 1;
            } 
            else {
                return 0;
            } 
        }
    }
    
 }

sub inserisci_notifica{
    my $tag = shift @_; # tag = NuovoMessaggio, NuovoMessaggioBacheca, FeedDaRilasciare, RichiestaPrenotaz, AccettazionePrenotaz 
    my $attr = shift @_; # hash di attributi con chiavi = Destinatario, Passaggio, Mittente, Esito, Partenza, Arrivo
    my $user_destinat = shift @_;
    my %attributi = %$attr;
    my $fragm;
    if($tag eq 'NuovoMessaggio') {
        $fragm = "<NuovoMessaggio Mittente=\"".$attributi{'Mittente'}."\"/> \n";
    }
    if($tag eq 'FeedDaRilasciare') {
        $fragm = "<FeedDaRilasciare Destinatario=\"".$attributi{'Destinatario'}."\" Passaggio=\"".$attributi{'Passaggio'}."\" /> \n";
    }
    if($tag eq 'RichiestaPrenotaz') {
        $fragm = "<RichiestaPrenotaz Mittente=\"".$attributi{'Mittente'}."\" Passaggio=\"".$attributi{'Passaggio'}."\" Partenza=\"".$attributi{'Partenza'}."\" Arrivo=\"".$attributi{'Arrivo'}."\" /> \n";
    }
    if($tag eq 'EsitoPrenotaz') {
        $fragm = "<EsitoPrenotaz Passaggio=\"".$attributi{'Passaggio'}."\" Esito=\"".$attributi{'Esito'}."\" /> \n";
    }
    
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
    my %aux=serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $fileHandle = $aux{'filehandle'};
    if(utility::verifica_presenza("//Passaggio[IDViaggio=\"$array_argom{'Passaggio'}\" and Conducente=\"$array_argom{'IDDest'}\"]",$doc)) {
        
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
    serializzazione_chiusura($fileHandle,$doc);
    $output = $output."</Feedback> \n";
    my $fragm = $parser->parse_balanced_chunk($output);
    return serializzazione_inserimento($fragm,"//SetFeedback/Feedback[\@IDMitt=\"$array_argom{'IDMitt'}\" and \@IDDest=\"$array_argom{'IDDest'}\"]","//SetFeedback");
}

sub inserisci_info_auto {
    my $array_argom_ref = shift @_; # CHIAVI : Username, Auto
    my %array_argom = %$array_argom_ref;
    my $output = "<Auto>$array_argom{'Auto'}</Auto> \n";
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $root = $doc->documentElement;
    my $fileHandle = $aux{'filehandle'};
    my $fragm = $parser->parse_balanced_chunk($output);
    if(utility::verifica_presenza("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Auto",$doc)) {
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
    my $output = "<Patente>$array_argom{'Patente'}<Patente/> \n";
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
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

sub elimina_notifica {
    my $user = shift @_;
    my $tag = shift @_;  # tag = NuovoMessaggio, NuovoMessaggioBacheca, FeedDaRilasciare, RichiestaPrenotaz, AccettazionePrenotaz 
    my $attr = shift @_;  # stringa di attributi che identificano la notifica da eliminare
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $fileHandle = $aux{'filehandle'};
    my $padre = $doc->findnodes("//Utente[Username=\"$user\"]/Notifiche")->get_node(1);
    print "<br>","//Utente[Username=\"$user\"]/Notifiche/".$tag."[$attr]","</br>";
    $padre->removeChild($doc->findnodes("//Utente[Username=\"$user\"]/Notifiche/".$tag."[$attr]")->get_node(1)); 
    serializzazione_chiusura($fileHandle,$doc);
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


sub inserisci_modifica_profilo { 
    my $array_argom_ref = shift @_; # CHIAVI : Username(del profilo da modificare), Nome, Cognome, Sesso, Email, AnnoNascita, Descrizione, Patente, Auto, Chiacchere, Animali, Musica, Fumatore
    my %array_argom = %$array_argom_ref;
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $fileHandle = $aux{'filehandle'};

    if(defined($array_argom{'Nome'})) {
        my $old_nome=$doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Nome")->get_node(1);
        $old_nome->replaceNode($parser->parse_balanced_chunk("<Nome>$array_argom{'Nome'}</Nome>"));
    }

    if(defined($array_argom{'Cognome'})) {
        my $old_cognome=$doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Cognome")->get_node(1);
        $old_cognome->replaceNode($parser->parse_balanced_chunk("<Cognome>$array_argom{'Cognome'}</Cognome>"));
    }

    if(defined($array_argom{'Sesso'})) {
        my $old_sesso=$doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Sesso")->get_node(1);
        $old_sesso->replaceNode($parser->parse_balanced_chunk("<Sesso>$array_argom{'Sesso'}</Sesso>"));
    }

    if(defined($array_argom{'Email'})) {
        my $old_email=$doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Email")->get_node(1);
        $old_email->replaceNode($parser->parse_balanced_chunk("<Email>$array_argom{'Email'}</Email>"));
    }

    if(defined($array_argom{'AnnoNascita'})) {
        my $old_nasc=$doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/AnnoNascita")->get_node(1);
        $old_nasc->replaceNode($parser->parse_balanced_chunk("<AnnoNascita>$array_argom{'AnnoNascita'}</AnnoNascita>"));
    }

    if(defined($array_argom{'Password'})) {
        my $old_nasc=$doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Password")->get_node(1);
        $old_nasc->replaceNode($parser->parse_balanced_chunk("<Password>$array_argom{'Password'}</Password>"));
    }

    if(defined($array_argom{'DescrizionePers'})) {
        my @old_desc=$doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/DescrizionePers");
        my $n = @old_desc;
        if($n != 0) {
            my $des = $old_desc[0]->findnodes(".")->get_node(1);
                $des->replaceNode($parser->parse_balanced_chunk("<DescrizionePers>$array_argom{'DescrizionePers'}</DescrizionePers>"));           
        }
        else {
            my $sibling_node = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Cognome")->get_node(1);
            my $parent = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]")->get_node(1);
            my $fragm = $parser->parse_balanced_chunk("<DescrizionePers>$array_argom{'DescrizionePers'}</DescrizionePers>");
            $parent->insertAfter($fragm,$sibling_node);        
        }
    }

    if(defined($array_argom{'Patente'})) { # se è definita la patente, allora lo sono anche Auto e Preferenze
        my @old_pat=$doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Patente");
        my $n = @old_pat;
        if($n != 0) {
            my $pat = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Patente")->get_node(1);
                $pat->replaceNode($parser->parse_balanced_chunk("<Patente>$array_argom{'Patente'}</Patente>"));
            my $auto=$doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Auto")->get_node(1);
                $auto->replaceNode($parser->parse_balanced_chunk("<Auto>$array_argom{'Auto'}</Auto>"));
            my $pref=$doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Preferenze")->get_node(1);
            my $new_pref="<Preferenze>
                        <Chiacchiere>$array_argom{'Chiacchiere'}</Chiacchiere>
                        <Musica>$array_argom{'Musica'}</Musica>
                        <Animali>$array_argom{'Animali'}</Animali>
                        <Fumatore>$array_argom{'Fumatore'}</Fumatore>
                    </Preferenze>";
                $pref->replaceNode($parser->parse_balanced_chunk($new_pref));
        }
        else {
            my $sibling_node = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Valutazione")->get_node(1);
            my $parent = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo")->get_node(1);
                $parent->insertAfter($parser->parse_balanced_chunk("<Auto>$array_argom{'Auto'}</Auto>"),$sibling_node);
                $sibling_node = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Auto")->get_node(1);
                $parent->insertAfter($parser->parse_balanced_chunk("<Patente>$array_argom{'Patente'}</Patente>"),$sibling_node);
                $sibling_node = $doc->findnodes("//Utente[Username=\"$array_argom{'Username'}\"]/Profilo/Patente")->get_node(1); 
            my $new_pref="<Preferenze>
                        <Chiacchiere>$array_argom{'Chiacchiere'}</Chiacchiere>
                        <Musica>$array_argom{'Musica'}</Musica>
                        <Animali>$array_argom{'Animali'}</Animali>
                        <Fumatore>$array_argom{'Fumatore'}</Fumatore>
                    </Preferenze>";
            $parent->insertAfter($parser->parse_balanced_chunk($new_pref),$sibling_node);
       
        }
    }

    
    serializzazione_chiusura($fileHandle,$doc);
    return 1;

}

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

sub aggiorna_feedback_da_rilasciare {
    my $doc = get_xml_doc;
    my @passaggi = $doc->findnodes("//SetPassaggi/Passaggio[\@Passato='no']");
    my $num_pas = @passaggi;
    for(my $i=0; $i<$num_pas; $i++) {
        my @data_pas = split /-/, $passaggi[$i]->findnodes("Itinerario/Arrivo/Data")->get_node(1)->textContent;
        my ($sec,$min,$hour,$mday, $mon, $year ,$wday,$yday,$isdst) = localtime();
        $year = $year + 1900;
        # cerca i passaggi con attributo Passato='no' ma con data passata. Queste condizioni indicano un viaggio che è temporalmente passato, ma di cui non sono
        #       state aggiornate le relative notifiche di rilascio feedback
        if(!(date_time::confronto_dataora($mday, $mon, $year, $hour, $min, $data_pas[2], $data_pas[1]-1, $data_pas[0], "23", "59"))) {
            my $pass = $passaggi[$i]->findnodes("IDViaggio")->get_node(1)->textContent;
            
            my %aux = serializzazione_apertura();
            my $doc2 = $aux{'doc'};
            my $fileHandle = $aux{'filehandle'};
            my $node = $doc2->findnodes("//SetPassaggi/Passaggio[IDViaggio='$pass']")->get_node(1)->setAttribute('Passato' ,'si');
            serializzazione_chiusura($fileHandle, $doc2);
            
            my @tappe = $passaggi[$i]->findnodes("Itinerario/*");
            my $num = @tappe;
            for(my $w=0; $w<$num; $w++) {
                my @partecipanti = ( $passaggi[$i]->findnodes("Conducente")->get_node(1)->textContent ); # il conducente è sicuramente un partecipante
                my @prenotaz = $tappe[$w]->findnodes("Prenotazioni/Utente");
                my $num_pr = @prenotaz;    
                for(my $x=0; $x<$num_pr; $x++) {
                    push @partecipanti, $prenotaz[$x]->findnodes(".")->get_node(1)->textContent; # creo un array di utenti che devono rilasciare il feedback fra ognumo di loro
                }
                my $num_p = @partecipanti;
                for(my $j=0; $j<$num_p; $j++) {
                    for(my $k=0; $k<$num_p; $k++) {
                        if($j != $k) {
                            my $mittente = $partecipanti[$j];
                            my $destinatario = $partecipanti[$k];
                            my $doc = get_xml_doc();
                            if(!($doc->exists("//SetUtenti/Utente[Username='$mittente']/Notifiche/FeedDaRilasciare[\@Destinatario='$destinatario' and \@Passaggio='$pass']"))) {
                                my %Notifica = (
                                    Destinatario => $destinatario,
                                    Passaggio => $pass
                                );
                                inserisci_notifica("FeedDaRilasciare",\%Notifica,$mittente);
                            }
                        }
                    }
                }           
            } 
        }
    }
    return 1;
}

sub aggiorna_valutazione_utente {
    my $array_argom_ref = shift @_; # hash del feedback appena rilasciato (nuovo)
    my $utente = shift @_;
    my %array_argom = %$array_argom_ref;
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $fileHandle = $aux{'filehandle'};
    my $utente = $array_argom{'IDDest'};  # utente di cui si sta aggiornando la valutazione
    print "//SetFeedback/Feedback[\@IDDest='$utente']/Guida";
    my @feed_cond = $doc->findnodes("//SetFeedback/Feedback[\@IDDest='$utente']/ValutazioneConduc");
    my $num_fb_cond = @feed_cond;
    print $num_fb_cond;
    my $feed_ric = $doc->findnodes("//SetUtenti/Utente[Username='$utente']/Profilo/NumFeedbRicevuti")->get_node(1)->textContent;
    my $old_punteg = $doc->findnodes("//SetUtenti/Utente[Username='$utente']/Profilo/Valutazione/PunteggioMedio")->get_node(1);
    my $old_comp = $doc->findnodes("//SetUtenti/Utente[Username='$utente']/Profilo/Valutazione/Compagnia")->get_node(1);
    my $old_punt = $doc->findnodes("//SetUtenti/Utente[Username='$utente']/Profilo/Valutazione/Puntualita")->get_node(1);
    my $old_puliz = $doc->findnodes("//SetUtenti/Utente[Username='$utente']/Profilo/Valutazione/Pulizia")->get_node(1);
    my $old_guida = $doc->findnodes("//SetUtenti/Utente[Username='$utente']/Profilo/Valutazione/Guida")->get_node(1);

    my $new_punteg = (($old_punteg->textContent*($feed_ric - 1)+$array_argom{'PunteggioMedio'}))/$feed_ric;
    my $new_punteg_node = "<PunteggioMedio>$new_punteg</PunteggioMedio>";
    $new_punteg_node = $parser->parse_balanced_chunk($new_punteg_node);
    $old_punteg->replaceNode($new_punteg_node);

    my $new_comp = (($old_comp->textContent*($feed_ric - 1)+$array_argom{'Compagnia'}))/$feed_ric;
    my $new_comp_node = "<Compagnia>$new_comp</Compagnia>";
    $new_comp_node = $parser->parse_balanced_chunk($new_comp_node);
    $old_comp->replaceNode($new_comp_node);

    my $new_punt = (($old_punt->textContent*($feed_ric - 1)+$array_argom{'Puntualita'}))/$feed_ric;
    my $new_punt_node = "<Puntualita>$new_punt</Puntualita>";
    $new_punt_node = $parser->parse_balanced_chunk($new_punt_node);
    $old_punt->replaceNode($new_punt_node);

    if(defined($array_argom{'Guida'}) and defined($array_argom{'Pulizia'})) {
        my $new_guida = (($old_guida->textContent*($num_fb_cond - 1)+$array_argom{'Guida'}))/$num_fb_cond;
        my $new_guida_node = "<Guida>$new_guida</Guida>";
        $new_guida_node = $parser->parse_balanced_chunk($new_guida_node);
        $old_guida->replaceNode($new_guida_node);

        my $new_puliz = (($old_puliz->textContent*($num_fb_cond - 1)+$array_argom{'Pulizia'}))/$num_fb_cond;
        my $new_puliz_node = "<Pulizia>$new_puliz</Pulizia>";
        $new_puliz_node = $parser->parse_balanced_chunk($new_puliz_node);
        $old_puliz->replaceNode($new_puliz_node);
    }



    serializzazione_chiusura($fileHandle, $doc);
    return 1;

}


sub incrementa {
    my $tag = shift @_; # NumFeedbRicev, NumPassaggiOff, NumPassaggiPart
    my $utente = shift @_;
    my %aux = serializzazione_apertura();
        my $doc = $aux{'doc'};
        my $fileHandle = $aux{'filehandle'};
        my $incrementa = $doc->findnodes("//SetUtenti/Utente[Username='$utente']/Profilo/$tag")->get_node(1)->textContent();
        $incrementa = $incrementa + 1;
        my $new_node = $parser->parse_balanced_chunk("<$tag>$incrementa</$tag>");
        $doc->findnodes("//SetUtenti/Utente[Username='$utente']/Profilo/$tag")->get_node(1)->replaceNode($new_node);
    serializzazione_chiusura($fileHandle, $doc);
    return 1;
}

sub aggiorna_messaggi_letti {
    my $utente = shift @_; #proprietario della SESSIONE
    my $conversatore = shift @_; 
    my %aux = serializzazione_apertura();
    my $doc = $aux{'doc'};
    my $fileHandle = $aux{'filehandle'};
    my $conv = $doc->findnodes("//SetMessaggi/Conversazione[\@User1=\"$utente\" and \@User2=\"$conversatore\"] | //SetMessaggi/Conversazione[\@User1=\"$conversatore\" and \@User2=\"$utente\"]")->get_node(1);
    my @nodes = $conv->findnodes("Messaggio[Mittente=\'$conversatore\' and \@Letto=\'no\']" );
    my $size= @nodes;
    for(my $j=0; $j<$size; $j++) {
        $nodes[$j]->setAttribute(Letto => 'si');
    }
    serializzazione_chiusura($fileHandle, $doc);
    my @notifiche_mess = $doc->findnodes("//SetUtenti/Utente[Username='$utente']/Notifiche/NuovoMessaggio[\@Mittente='$conversatore']");
    my $size = @notifiche_mess;
    for(my $i=0; $i<$size; $i++) {
        elimina_notifica($utente, "NuovoMessaggio", "\@Mittente='$conversatore'");
    }
    return 1;
}

1;
