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
our $xml_file = '../data/TravelShare.xml';


#parametri: nome file xml

sub generic_xslt_query
{
    my ($style_file,  $lista_filtri );
    $style_file  = shift @_;
    $lista_filtri = shift @_;
    my %vars= %$lista_filtri;
    my $xml_parser = XML::LibXML->new( );
    my $xslt_parser = XML::LibXSLT->new( );
    my $template_parser = Template->new({RELATIVE => 1,});
    #({ABSOLUTE => 1,});
    my $foglio_di_stile_con_parametri = '';
    $template_parser->process($style_file,\%vars,\$foglio_di_stile_con_parametri); #or die $template_parser->error()
    (length $foglio_di_stile_con_parametri) or die("ERRORE 1: foglio xslt vuoto\n".$style_file . '    '. getcwd);
    my $style_oggetto_xml = $xml_parser->parse_string($foglio_di_stile_con_parametri);
    my $style_oggetto_xsl = $xslt_parser->parse_stylesheet( $style_oggetto_xml );
    my $file_oggetto_xml = $xml_parser->parse_file( $xml_file );
    my $html_output = $style_oggetto_xsl->transform( $file_oggetto_xml);
    (length $html_output) or die("ERRORE 2: output HTML vuoto\n".$style_file  . '    '. getcwd);
    $html_output =~ s/<\?xml\ version\=\"1\.0\"\?>//;
    return $html_output;
}

sub query_users
{
    my $lista = shift @_;
    if(! exists $lista->{"UTENTE"})
    {
        die "Non esiste la chiave UTENTE nella query users\n";
    }

    return generic_xslt_query('../data/xslt_files/users.xsl',\%$lista);
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
    if(! exists $lista->{"NUM_PARTENZA"})
    {
        die "Non esiste la chiave NUM_PARTENZA nella query viaggi\n";
    }
    if(! exists $lista->{"NUM_ARRIVO"})
    {
        die "Non esiste la chiave NUM_ARRIVO nella query viaggi\n";
    }
    return generic_xslt_query('../data/xslt_files/bachecaviaggio.xsl',\%$lista);
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
    return generic_xslt_query('../data/xslt_files/singoloviaggio.xsl',\%$lista);
}

sub query_ricerca
{
    my $partenza = shift @_;
    my $arrivo=shift @_;
    my $data=shift @_;
    my $doc = shift @_;
    my $contenuto= "";
    my @itiner=$doc->findnodes("//SetPassaggi/Passaggio/Itinerario[*[Data='$data']]");
    my $num_it=@itiner;
    for(my $i=0;$i<$num_it;$i++) {
        for(my $j=0;$j<5;$j++) {
            my @tappa=$itiner[$i]->findnodes("*[\@Numero=$j]");
            my $num = @tappa;
            if($num!=0) {
                my $luogo = $itiner[$i]->findnodes("*[\@Numero=$j]/Luogo")->get_node(1);
                if (index($luogo, $partenza) != -1 && $itiner[$i]->findnodes("*[\@Numero=$j]/PostiDisp")->get_node(1)->textContent() > 0) {
                    for(my $k=$j+1;$k<5;$k++) {
                        my @tappe_s=$itiner[$i]->findnodes("*[\@Numero=$k]");
                        my $num = @tappe_s;
                        if($num!=0) {
                            if($itiner[$i]->findnodes("*[\@Numero=$j]/PostiDisp")->get_node(1)->textContent() == 0) {
                                $k=5;
                                $j=5;
                            }
                            else {
                                my $luog = $itiner[$i]->findnodes("*[\@Numero=$k]/Luogo")->get_node(1);
                                if (index($luog, $arrivo) != -1) {
                                    my $ora=$itiner[$i]->findnodes("*[\@Numero=0]/Ora")->get_node(1)->textContent();
                                    my $part = $itiner[$i]->findnodes("*[\@Numero=$j]/Luogo")->get_node(1)->textContent();
                                    my $arr = $itiner[$i]->findnodes("*[\@Numero=$k]/Luogo")->get_node(1)->textContent();
                                    my $idv = $itiner[$i]->findnodes("../IDViaggio")->get_node(1)->textContent();
                                    my $prezzo = '10'; # da sostituire con funzione che calcola il prezzo
                                    my $posti = utility::calcola_posti_disponibili($j,$k,$idv,$doc);
                                    my $conduc = $itiner[$i]->findnodes("../Conducente")->get_node(1)->textContent();
                                    my $auto = $doc->findnodes("//SetUtenti/Utente[Username='$conduc']/Profilo/Auto")->get_node(1)->textContent;
                                    my $punteggio = $doc->findnodes("//SetUtenti/Utente[Username='$conduc']/Profilo/Valutazione/PunteggioMedio")->get_node(1)->textContent;
                                    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
                                    my $eta=$year + 1900 - ($doc->findnodes("//SetUtenti/Utente[Username='$conduc']/AnnoNascita")->get_node(1)->textContent() ) ;
                                    $contenuto = $contenuto."\n
                     <div class=\"risultato\">
     <p><a href=\"singolo_passaggio.cgi?passaggio=$idv&part=$j&arr=$k\" class=\"linkMobileRisultati\"><span class=\"partenza\">$part</span> &#8594; <span class=\"arrivo\">$arr</span>
        <span class=\"linkDesktop destra\">Vai al viaggio &raquo;</span></a></p>

     <p>Ora: $ora</p>

     <p>Posti: $posti<span class=\"destra\">$prezzo&euro; <!--&#8364;--></span></p>

     <hr />

     <p>$conduc <!-- <span class=\"destra\">33 anni</span> --></p>

     <p>Voto medio: $punteggio/5</p>

     <p>Auto: $auto</p>

    </div> ";
                                }
                            }
                        }
                    }

                }
            }

        }
    }
    if($contenuto eq "") {
        $contenuto = "<div class=\"contenitore\"><p>Nessun passaggio corrisponde ai criteri di ricerca</p></div>";
    }
    return $contenuto;
}

sub query_viaggi_utente {
    my $utente=shift @_;
    my $doc = shift @_;
    my $contenuto;
    my ($sec,$min,$hour,$mday, $mon, $year ,$wday,$yday,$isdst) = localtime();
    $year = $year + 1900;
    # viaggi attivi di cui l utente &egrave; conducente
    my @viaggi_cond = $doc->findnodes("//SetPassaggi/Passaggio[Conducente='$utente' and \@Passato='no']");
    my $num = @viaggi_cond;
    for(my $i=0;$i<$num;$i++) {
        my $idv = $viaggi_cond[$i]->findnodes("IDViaggio")->get_node(1)->textContent;
        my $partenza = $viaggi_cond[$i]->findnodes("Itinerario/Partenza/Luogo")->get_node(1)->textContent;
        my $arrivo = $viaggi_cond[$i]->findnodes("Itinerario/Arrivo/Luogo")->get_node(1)->textContent;
        my $data = $viaggi_cond[$i]->findnodes("Itinerario/Partenza/Data")->get_node(1)->textContent;
        my $ora = $viaggi_cond[$i]->findnodes("Itinerario/Partenza/Ora")->get_node(1)->textContent;
        my $prezzo = utility::calcola_prezzo('0','4',$idv,$doc); # funzione che calcola il prezzo
        my $posti = utility::calcola_posti_disponibili('0','4',$idv,$doc);
        $contenuto = $contenuto."\n
        <div class=\"viaggio\">
        <a class='linkMobileViaggi' href=\"singolo_passaggio.cgi?passaggio=$idv&part=0&arr=4&prezzo=$prezzo&posti=$posti&cond=$utente\"><span class=\"partenza\">$partenza</span> &#8594; <span class=\"arrivo\">$arrivo</span></a>
        <p>Data: $data</p>
        <p>Ora: $ora <a href=\"singolo_passaggio.cgi?passaggio=$idv&part=0&arr=4&prezzo=$prezzo&posti=$posti&cond=$utente\" class=\"linkDesktop destra\">Vai al viaggio &raquo;</a></p> 
        <p>Posti liberi: $posti</p>
        <p>Prezzo: $prezzo</p>
        <br />
        </div> ";
    }

    # viaggi attivi di cui il conducente &egrave; partecipante
    my @viaggi_att = $doc->findnodes("//SetPassaggi/Passaggio[\@Passato='no' and Itinerario/*/Prenotazioni/Utente='$utente']");
    my $num = @viaggi_att;
    for(my $i=0;$i<$num;$i++) {
        my $idv = $viaggi_att[$i]->findnodes("IDViaggio")->get_node(1)->textContent;
        my $cond = $viaggi_att[$i]->findnodes("Conducente")->get_node(1)->textContent;
        my $partenza = $viaggi_att[$i]->findnodes("Itinerario/*[Prenotazioni/Utente='$utente']/Luogo")->get_node(1)->textContent;
        my $num_p = $viaggi_att[$i]->findnodes("Itinerario/*[Prenotazioni/Utente='$utente']/\@Numero")->get_node(1)->textContent;
        my $data = $viaggi_att[$i]->findnodes("Itinerario/*[Prenotazioni/Utente='$utente']/Data")->get_node(1)->textContent;
        my $ora = $viaggi_att[$i]->findnodes("Itinerario/*[Prenotazioni/Utente='$utente']/Ora")->get_node(1)->textContent;
        my $arrivo;
        my $num_a;
        for(my $j=4;$j>0;$j--) {
            my @tappa = $viaggi_att[$i]->findnodes("Itinerario/*[Prenotazioni/Utente='$utente' and \@Numero='$j']");
            my $num = @tappa;
            if($num!=0) {
                $arrivo=$tappa[0]->findnodes("Luogo")->get_node(1)->textContent;
                $num_a=$tappa[0]->findnodes("\@Numero")->get_node(1)->textContent;
                $j=0;
            }
        }
        my $prezzo = utility::calcola_prezzo($num_p,$num_a,$idv,$doc); # funzione che calcola il prezzo
        my $posti = utility::calcola_posti_disponibili($num_p,$num_a,$idv,$doc);
        $contenuto = $contenuto."\n
        <div class=\"viaggio\">
        <a href=\"singolo_passaggio.cgi?passaggio=$idv&part=$num_p&arr=$num_a\"><span class=\"partenza\">$partenza</span> &#8594; <span class=\"arrivo\">$arrivo</span></a>
        <p>Data: $data</p>
        <p>Ora: $ora <a href=\"singolo_passaggio.cgi?passaggio=$idv&part=$num_p&arr=$num_a\" class=\"linkDesktop destra\">Vai al viaggio &raquo;</a></p>
        <p>Posti liberi: $posti</p>
        <p>Prezzo: $prezzo</p>
        <br />
        </div> ";
    }

    $contenuto = $contenuto."\n<h2>Viaggi passati da recensire</h2>";

    my @feed_da_ril = $doc->findnodes("//SetUtenti/Utente[Username='$utente']/Notifiche/FeedDaRilasciare");
    my $num = @feed_da_ril;
    if($num==0) {
        $contenuto = $contenuto."\n<div class=\"contenitore\"><p>Nessun passaggio da recensire</p></div>";
    }
    else {
        my @passag_da_rec;
        # popola @pass_da_rec, array con l insieme dei passaggi di cui c'&egrave; almeno un utente da recensire
        for(my $i=0;$i<$num;$i++) {
            my $idv = $feed_da_ril[$i]->findnodes("\@Passaggio")->get_node(1)->textContent;
            my $num = @passag_da_rec;
            my $presenza = 0;
            for(my $j=0;$j<$num && $presenza==0;$j++) {
                if($passag_da_rec[$j] eq $idv) {
                    $presenza = 1;
                }
            }
            if($presenza==0) {
                push @passag_da_rec, $idv;
            }
        }

        my $num_pas = @passag_da_rec;
        for(my $k=0; $k<$num_pas; $k++) {
            my $idv = $passag_da_rec[$k];
            my $partenza = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$idv']/Itinerario/Partenza/Luogo")->get_node(1)->textContent;
            my $arrivo = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$idv']/Itinerario/Arrivo/Luogo")->get_node(1)->textContent;
            my $data = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$idv']/Itinerario/Partenza/Data")->get_node(1)->textContent;
            $contenuto = $contenuto."\n
                <div class=\"viaggio\">
                    <a href=\"viaggio_recensire.cgi?passaggio=$idv\"><span class=\"partenza\">$partenza</span> &#8594; <span class=\"arrivo\">$arrivo</span><span class=\"data\">$data</span></a>
                </div>
                ";
        }
    }
    return $contenuto;
}

sub query_notifiche_utente {
    my $ute = shift @_;
    my $doc = shift @_;
    my $contenuto="";
    my $numNotifiche = 0;
    my $contatore=4; # per tabindex
    my @notifiche_mess = $doc->findnodes("//SetUtenti/Utente[Username='$ute']/Notifiche/NuovoMessaggio");
    my $size =@notifiche_mess;
    $numNotifiche = $numNotifiche + $size;
    for(my $i=0; $i<$size; $i++) {
        my $mittente = $notifiche_mess[$i]->findnodes("\@Mittente")->get_node(1)->textContent;
        $contenuto = $contenuto."\n
            <div class=\"notifica\">
                <p>Hai un nuovo messaggio da $mittente<br class=\"aCapoMobile\"/> <a href=\"singola_conversaz.cgi?utente=$mittente\" class=\"destraDesktop\" tabindex=\"$contatore\">Vai ai messaggi</a></p>
            </div>";
        $contatore++;
    }

    my @notifiche_feedbd = $doc->findnodes("//SetUtenti/Utente[Username='$ute']/Notifiche/FeedDaRilasciare");
    my $size =@notifiche_feedbd;
    $numNotifiche = $numNotifiche + $size;
    my @aux;
    for(my $i=0; $i<$size; $i++) {
        my $presenza = 0;
        my $passaggio = $notifiche_feedbd[$i]->findnodes("\@Passaggio")->get_node(1)->textContent;
        my $size= @aux;
        for(my $j=0; $j<$size; $j++) {
            if($aux[$j] eq $passaggio) { $presenza = 1; }
        }
        if(!$presenza) {
            push @aux, $passaggio;
            $contenuto = $contenuto."\n
            <div class=\"notifica\">
                <p>Hai un nuovo viaggio da recensire <br class=\"aCapoMobile\"/> <a href=\"viaggio_recensire.cgi?passaggio=$passaggio\" class=\"destraDesktop\" tabindex=\"$contatore\">Inserisci i <span xml:lang=\"en\" lang=\"en\">feedback</span></a></p>
            </div>";
            $contatore++;
        }
    }

    my @notifiche_richiesta_prenot = $doc->findnodes("//SetUtenti/Utente[Username='$ute']/Notifiche/RichiestaPrenotaz");
    my $size =@notifiche_richiesta_prenot;
    $numNotifiche = $numNotifiche + $size;
    for(my $i=0; $i<$size; $i++) {
        my $richiedente = $notifiche_richiesta_prenot[$i]->findnodes("\@Mittente");
        my $passaggio = $notifiche_richiesta_prenot[$i]->findnodes("\@Passaggio");
        my $partenza = $notifiche_richiesta_prenot[$i]->findnodes("\@Partenza");
        my $arrivo = $notifiche_richiesta_prenot[$i]->findnodes("\@Arrivo");
        # PER RICCARDO : MANCANO TABINDEX
        $contenuto = $contenuto."\n
        <div class=\"notifica\">
        <p>Hai una nuova richiesta di prenotazione da parte di $richiedente:</p>
            <form action=\"ricevitore_esito_prenotazione.cgi\" method=\"post\" >
                <fieldset>
                    <legend>Richiesta prenotazione da $richiedente per il passaggio $passaggio</legend>
                    <div class=\"test\">
                    <input type=\"radio\" name=\"esito\" id=\"accetta\" value=\"Accettata\"></input>
                    <label for=\"accetta\">Accetta</label>
                    <span class=\"paddingSpan\"></span>
                    <input type=\"radio\" name=\"esito\" id=\"rifiuta\" value=\"Rifiutata\"></input>
                    <label for=\"rifiuta\">Rifiuta</label>
                    </div>
                    <input type=\"hidden\" name=\"richiedente\" value=\"$richiedente\"></input>
                    <input type=\"hidden\" name=\"passaggio\" value=\"$passaggio\"></input>
                    <input type=\"hidden\" name=\"partenza\" value=\"$partenza\"></input>
                    <input type=\"hidden\" name=\"arrivo\" value=\"$arrivo\"></input>
                    <input type=\"submit\" value=\"Invia\"></input>
                </fieldset>
            </form>
            </div>
        ";
    }

    my @notifiche_esito_prenot = $doc->findnodes("//SetUtenti/Utente[Username='$ute']/Notifiche/EsitoPrenotaz");
    my $size =@notifiche_esito_prenot;
    $numNotifiche = $numNotifiche + $size;
    for(my $i=0; $i<$size; $i++) {
        my $passaggio = $notifiche_esito_prenot[$i]->findnodes("\@Passaggio");
        my $esito = $notifiche_esito_prenot[$i]->findnodes("\@Esito");
        $contenuto = $contenuto."\n
                <div class=\"notifica\">
                    <p>La tua richiesta di prenotazione &egrave; stata $esito <br class=\"aCapoMobile\"/> <a href=\"ricevitore_esito_visualizz.cgi?passaggio=$passaggio\" class=\"destraDesktop\" tabindex=\"$contatore\">Elimina esito</a></p>
                </div>
            ";
        $contatore++;
    }
    if($numNotifiche==0) {
        $contenuto = "\n<div class=\"contenitore\"><p>Nessuna notifica presente</p></div>";
    }
    return [$contenuto, $numNotifiche, $contatore];
}


sub query_messaggi
{
    my $lista = shift @_;
    if(! exists $lista->{"UTENTE"})
    {
        die "Non esiste la chiave Utente nella query messaggi";
    }
    return generic_xslt_query('../data/xslt_files/messaggi.xsl',\%$lista);
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
    return generic_xslt_query('../data/xslt_files/singolaconversazione.xsl',\%$lista);
}




1;
