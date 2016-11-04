#! /usr/bin/perl -w

###################################################
# Pacchetto di gestione delle ricerche nel file XML
###################################################

package research;

use XML::LibXML;
use XML::LibXSLT;
use Template;
use Cwd;
use libreria::date_time;


use strict;
use warnings;
use diagnostics;
use utf8;
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
    #my $min_index = $vars{'INDEX'};
    #delete $vars{'INDEX'};
    my $xml_parser = XML::LibXML->new( );
    my $xslt_parser = XML::LibXSLT->new( );
    my $template_parser = Template->new({RELATIVE => 1,});
    #({ABSOLUTE => 1,});
    my $foglio_di_stile_con_parametri = '';
    $template_parser->process($style_file,\%vars,\$foglio_di_stile_con_parametri);#or die $template_parser->error();
    (length $foglio_di_stile_con_parametri) or die("ERRORE 1: foglio xslt vuoto\n".$style_file . '    '. getcwd);

    my $style_oggetto_xml = $xml_parser->parse_string($foglio_di_stile_con_parametri);
    my $style_oggetto_xsl = $xslt_parser->parse_stylesheet( $style_oggetto_xml );
    my $file_oggetto_xml = $xml_parser->parse_file( $xml_file );
    my $html_output_1 = $style_oggetto_xsl->transform( $file_oggetto_xml);
    (length $html_output_1) or die("ERRORE 2: output HTML vuoto\n".$style_file  . '    '. getcwd);
    #open my $f, '>prova_html_1.txt';
     #   print $f $html_output_1;
    #my $html_output = '';
    #$template_parser->process(\$html_output_1,{INDEX => $min_index},\$html_output) or die $template_parser->error();
    #(length $html_output) or die("ERRORE 1.1: foglio xslt vuoto\n" . '    '. getcwd);

    $html_output_1 =~ s/<\?xml\ version\=\"1\.0\"\?>//;
   # return $html_output;
   return $html_output_1;
}

sub query_users
{
    my $lista = shift @_;
    if(! exists $lista->{"UTENTE"})
    {
        die "Non esiste la chiave UTENTE nella query users\n";
    }
    if(! exists $lista->{"ANNO_C"})
    {
        die "Non esiste la chiave ANNO_C nella query users\n";
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
# Il contenuto và sostituito con il tag RISULTATI_LIST, una lista di hash, ognuno della forma:
#       { href => $link_passaggio, partenza => $partenza, arrivo => $arrivo, ora => $ora, posti => $posti,
# conducente => $user_conduc, eta => $conduc_eta, punteggio => $conduc_punteg, auto => $conduc_auto, start_index => $tab_index }

# Inoltre è necessario passare un tag PARTENZA (la partenza inserita nella ricerca), ARRIVO (l arrivo inserito nella ricerca) e la DATA
    my $partenza = shift @_;
    my $arrivo=shift @_;
    my $data=shift @_;
    my $doc = shift @_;
    my $contenuto= "";
    my @viaggi_list;
    my @itiner=$doc->findnodes("//SetPassaggi/Passaggio/Itinerario[*[Data='$data']]");
    my $num_it=@itiner;
    for(my $i=0;$i<$num_it;$i++) {
        for(my $j=0;$j<5;$j++) {
            my @tappa=$itiner[$i]->findnodes("*[\@Numero=$j]");
            my $num = @tappa;
            if($num!=0) {
                my $luogo = $itiner[$i]->findnodes("*[\@Numero=$j]/Luogo")->get_node(1);
                if (index(lc $luogo, lc $partenza) != -1 && $itiner[$i]->findnodes("*[\@Numero=$j]/PostiDisp")->get_node(1)->textContent() > 0) {
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
                                if (index(lc $luog, lc $arrivo) != -1) {
                                    my $ora=$itiner[$i]->findnodes("*[\@Numero=0]/Ora")->get_node(1)->textContent();
                                    my $part = $itiner[$i]->findnodes("*[\@Numero=$j]/Luogo")->get_node(1)->textContent();
                                    my $arr = $itiner[$i]->findnodes("*[\@Numero=$k]/Luogo")->get_node(1)->textContent();
                                    my $idv = $itiner[$i]->findnodes("../IDViaggio")->get_node(1)->textContent();
                                    my $prezzo = utility::calcola_prezzo($j,$k,$idv,$doc);
                                    my $posti = utility::calcola_posti_disponibili($j,$k,$idv,$doc);
                                    my $conduc = $itiner[$i]->findnodes("../Conducente")->get_node(1)->textContent();
                                    my $auto = $doc->findnodes("//SetUtenti/Utente[Username='$conduc']/Profilo/Auto")->get_node(1)->textContent;
                                    my $punteggio = $doc->findnodes("//SetUtenti/Utente[Username='$conduc']/Profilo/Valutazione/PunteggioMedio")->get_node(1)->textContent;
                                    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
                                    my $eta=$year + 1900 - ($doc->findnodes("//SetUtenti/Utente[Username='$conduc']/AnnoNascita")->get_node(1)->textContent() ) ;
                                    push @viaggi_list, {
                                                  href => "singolo_passaggio.cgi?passaggio=$idv&part=$j&&arr=$k", partenza => $part, arrivo => $arr,
                                                  ora => date_time::formatta_ora($ora), posti => $posti, prezzo => $prezzo, conducente => $conduc,
                                                  eta => $eta, punteggio => $punteggio, auto => $auto };

                                }
                            }
                        }
                    }

                }
            }

        }
    }
    return @viaggi_list;
}

sub query_viaggi_attivi_utente {
    ### RICORDARSI DI GESTIRE IL CASO NON CI SIA NESSUN VIAGGIO ATTIVO O NESSUN PASSAGGIO DA RECENSIRE (aggiungere all hash una key 'empty => $bool'?) ###

# Il CONTENUTO viene sostituito da una lista, di nome VIAGGI_LIST, di hash (uno per ogni viaggio attivo) ognuno della forma:
#   { href => $link_passaggio, partenza => $partenza, arrivo => $arrivo, posti => $posti, prezzo => $prezzo, data => $data, ora => $ora }
# NOTA: includere nei viaggi attivi anche quelli di cui l utente è conducente.

# Inoltre dev venire restituito anche una lista, di nome FEEDB_RECENS, di hash (uno per ogni viaggio da recensire) ognuno della forma:
#   { href => $link_passaggio_da_recensire, partenza => $partenza, arrivo => $arrivo, data => $data}

    my $utente=shift @_;
    my $doc = shift @_;

    my @viaggi_list;

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

        push @viaggi_list, {href => "singolo_passaggio.cgi?passaggio=$idv&part=0&arr=4",
            partenza => $partenza,
            arrivo => $arrivo,
            prezzo => $prezzo,
            posti => $posti,
            data => date_time::formatta_data($data),
            ora => date_time::formatta_ora($ora)};
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


        push @viaggi_list, {
            href => "singolo_passaggio.cgi?passaggio=$idv&part=$num_p&arr=$num_a",
            partenza => $partenza,
            arrivo => $arrivo,
            prezzo => $prezzo,
            posti => $posti,
            data => date_time::formatta_data($data),
            ora => date_time::formatta_ora($ora)};
    }


    return @viaggi_list;
}

sub query_viaggi_recensire_utente {
    my $utente=shift @_;
    my $doc = shift @_;
    my @feed_da_ril = $doc->findnodes("//SetUtenti/Utente[Username='$utente']/Notifiche/FeedDaRilasciare");
    my $num = @feed_da_ril;
    my @viaggi_list;
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
          push @viaggi_list, {
                                href => "viaggio_recensire.cgi?passaggio=$idv",
                                partenza => $partenza,
                                arrivo => $arrivo,
                                data => date_time::formatta_data($data)
                            }
        }
    return @viaggi_list;
}

sub query_notifiche_utente {
# Per le notifiche dei nuovi messaggi viene richiesto un tag MESSAGGI_LIST, una lista di hash, ognuno della forma:
#       { href => $link_singola_conversazione, mittente => $user_mittente, start_index => $tab_index }

# Per le notifiche sui viaggi da recensire viene richiesto un tag VIAGGI_RECENS_LIST, una lista di hash, ognuno della forma:
#       { href => $link_viaggio_recensire, start_index => $tab_index }

# Per le notifiche sulle richieste di prenotazione, viene usato un tag RICHIESTE_LIST, una lista di hash, ognuno della forma:
#       { richiedente => $user_richied, passaggio => $passaggio, partenza => $partenza, arrivo => $arrivo, start_index => $tab_index }

# Per le notifiche sull esito delle prenotazioni, viene usato un tag ESITI_LIST, una lista di hash, ognuno della forma:
#       { passaggio => $passaggio, esito => $esito, start_index => $tab_index }

# NOTA: è necessario passare un tag CONTATORE, che indica il numero totale di notifiche presenti. Attraverso un costrutto condizionale bisogna
#        testare se esso è uguale a 0.

    my $ute = shift @_;
    my $doc = shift @_;
    my @messaggi_list;
    my @feedback_list;
    my @richieste_list;
    my @esito_list;

    my @notifiche_mess = $doc->findnodes("//SetUtenti/Utente[Username='$ute']/Notifiche/NuovoMessaggio");
    my $size =@notifiche_mess;
    for(my $i=0; $i<$size; $i++) {
        my $mittente = $notifiche_mess[$i]->findnodes("\@Mittente")->get_node(1)->textContent;
        push @messaggi_list, { href => "singola_conversaz.cgi?utente=$mittente", mittente => $mittente};
    }

    my @notifiche_feedbd = $doc->findnodes("//SetUtenti/Utente[Username='$ute']/Notifiche/FeedDaRilasciare");
    my $size =@notifiche_feedbd;
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
            push @feedback_list, { href => "viaggio_recensire.cgi?passaggio=$passaggio" };
        }
    }

    my @notifiche_richiesta_prenot = $doc->findnodes("//SetUtenti/Utente[Username='$ute']/Notifiche/RichiestaPrenotaz");
    my $size =@notifiche_richiesta_prenot;
    for(my $i=0; $i<$size; $i++) {
        my $richiedente = $notifiche_richiesta_prenot[$i]->findnodes("\@Mittente");
        my $passaggio = $notifiche_richiesta_prenot[$i]->findnodes("\@Passaggio");
        my $partenza = $notifiche_richiesta_prenot[$i]->findnodes("\@Partenza");
        my $arrivo = $notifiche_richiesta_prenot[$i]->findnodes("\@Arrivo");
        push @richieste_list, { richiedente => $richiedente, passaggio => $passaggio, partenza => $partenza, arrivo => $arrivo };
        # PER RICCARDO : MANCANO TABINDEX
    }

    my @notifiche_esito_prenot = $doc->findnodes("//SetUtenti/Utente[Username='$ute']/Notifiche/EsitoPrenotaz");
    my $size =@notifiche_esito_prenot;
    for(my $i=0; $i<$size; $i++) {
        my $passaggio = $notifiche_esito_prenot[$i]->findnodes("\@Passaggio");
        my $esito = $notifiche_esito_prenot[$i]->findnodes("\@Esito");
        push @esito_list, { href => "ricevitore_esito_visualizz.cgi?passaggio=$passaggio", esito => $esito };
    }
    return (\@messaggi_list, \@feedback_list, \@richieste_list, \@esito_list);
}

sub conta_notifiche {
    my $ute = shift @_;
    my $doc = shift @_;
    my $count = 0;

    my @notifiche_mess = $doc->findnodes("//SetUtenti/Utente[Username='$ute']/Notifiche/NuovoMessaggio");
    my $size = @notifiche_mess;
    $count = $count + $size;

    my @notifiche_feedbd = $doc->findnodes("//SetUtenti/Utente[Username='$ute']/Notifiche/FeedDaRilasciare");
    my $num_feedb =@notifiche_feedbd;
    my @aux;
    for(my $i=0; $i<$num_feedb; $i++) {
        my $presenza = 0;
        my $passaggio = $notifiche_feedbd[$i]->findnodes("\@Passaggio")->get_node(1)->textContent;
        my $size= @aux;
        for(my $j=0; $j<$size; $j++) {
            if($aux[$j] eq $passaggio) { $presenza = 1; }
        }
        if(!$presenza) {
            push @aux, $passaggio;
            $count = $count + 1;
        }
    }


    my @notifiche_richiesta_prenot = $doc->findnodes("//SetUtenti/Utente[Username='$ute']/Notifiche/RichiestaPrenotaz");
    my $size =@notifiche_richiesta_prenot;
    $count = $count + $size;

    my @notifiche_esito_prenot = $doc->findnodes("//SetUtenti/Utente[Username='$ute']/Notifiche/EsitoPrenotaz");
    my $size =@notifiche_esito_prenot;
    $count = $count + $size;

    return $count;

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

sub query_feedback_da_rilasciare_viaggio
{
    my $username = shift @_;
    my $passaggio = shift @_;
    my @feedback_list;
    my $doc=data_registration::get_xml_doc();
    my $conducente = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$passaggio']/Conducente")->get_node(1)->textContent;
    my @destinatari = $doc->findnodes("//SetUtenti/Utente[Username='$username']/Notifiche/FeedDaRilasciare[\@Passaggio='$passaggio']/\@Destinatario");
    my $num = @destinatari;
    my $ind = 1;

    for(my $i=0; $i<$num; $i++){
        my $dest = $destinatari[$i]->textContent;
        my $nome = $doc->findnodes("//SetUtenti/Utente[Username='$dest']/Nome")->get_node(1)->textContent;
        my $cognome = $doc->findnodes("//SetUtenti/Utente[Username='$dest']/Cognome")->get_node(1)->textContent;
        if($conducente eq $dest) {
            utf8::encode($nome);
            utf8::encode($cognome);
            utf8::encode($dest);
            push @feedback_list, { passaggio => $passaggio, username => $dest, nome => $nome, cognome => $cognome, index => 0 };
        }
        else {
            utf8::encode($nome);
            utf8::encode($cognome);
            utf8::encode($dest);
            push @feedback_list, { passaggio => $passaggio, username => $dest, nome => $nome, cognome => $cognome, index => $ind };
            $ind++;
        }
    }
    return @feedback_list;
}

sub utenti_prenotati {
my $viaggio = shift @_;
my $doc=data_registration::get_xml_doc();
my $userNodesP = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio=\"$viaggio\"]/Itinerario/Partenza/Prenotazioni/Utente");
my $userNodesA = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio=\"$viaggio\"]/Itinerario/Arrivo/Prenotazioni/Utente");
my $userNodesT = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio=\"$viaggio\"]/Itinerario/Tappa/Prenotazioni/Utente");
my @userList = ();
my $numA = $userNodesA->size();
my $numP = $userNodesP->size();
my $numT = $userNodesT->size();
for(my $i =1;$i<=$numP;$i++){
  my $nome = $userNodesP->get_node($i)->textContent;
  my $m = grep { $nome } @userList;
  if(!$m){
    push @userList, $nome;
  }
}
for(my $i =1;$i<=$numA;$i++){
  my $nome = $userNodesA->get_node($i)->textContent;
  my $m = grep { $nome } @userList;
  if(!$m){
    push @userList, $nome;
  }
}
for(my $i =$1;$i<=$numT;$i++){
  my $nome = $userNodesT->get_node($i)->textContent;
  my $m = grep { $nome } @userList;
  if(!$m){
    push @userList, $nome;
  }
}

return @userList;
}



1;
