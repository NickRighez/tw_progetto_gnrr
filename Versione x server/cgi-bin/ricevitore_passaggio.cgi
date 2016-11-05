#! /usr/bin/perl -w
#print "Content-type: text/html\n\n";

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use lib "libreria";
use data_registration;
use libreria::sessione;
use libreria::date_time;
use XML::LibXML;
use Scalar::Util;
use HTML::Entities;

my $parser =  XML::LibXML->new();
my $q=new CGI;

my @s = sessione::creaSessione();
my $session = $s[0];
my %problems = ( empty => 'yes' );
my %old_input;

my %Passaggio;

if($q->request_method() ne "POST") {
     my %problems=(
      DESCRIZIONE_ERRORE => "Tentativo di inserire un nuovo passaggio con una modalit&agrave; non permessa."
      );
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
else {
    my $username = $session->param('username');

    if($q->param('partenza') eq "") {
        $problems{PARTENZA_ERR} = "Luogo di partenza mancante";
        $problems{empty} = 'no';
    }
    elsif (!($q->param('partenza')=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0030}-\x{0039}]|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/)) {
        $problems{PARTENZA_ERR} = "Luogo di partenza non valido, inserire lettere o i caratteri: ',' '-' '.'";
        $problems{empty} = 'no';
    }
    else {
        $old_input{PARTENZA} = $q->param('partenza');
    }


    if($q->param('arrivo') eq "") {
        $problems{ARRIVO_ERR} = "Luogo di arrivo mancante";
        $problems{empty} = 'no';
    }
    elsif (!($q->param('arrivo')=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0030}-\x{0039}]|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/)) {
        $problems{ARRIVO_ERR} = "Luogo di arrivo non valido, inserire lettere o i caratteri: ',' '-' '.'";
        $problems{empty} = 'no';
    }
    else {
        $old_input{ARRIVO} = $q->param('arrivo');
    }

    if($q->param('tappa1') ne "" and !($q->param('tappa1')=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0030}-\x{0039}]|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/)) {
        $problems{TAPPA1_ERR} = "Luogo della tappa 1 non valido, inserire lettere o i caratteri: ',' '-' '.'";
        $problems{empty} = 'no';
    }
    else {
        $old_input{TAPPA1} = $q->param('tappa1');
    }

    if($q->param('tappa2') ne "" and !($q->param('tappa2')=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0030}-\x{0039}]|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/)) {
        $problems{TAPPA2_ERR} = "Luogo della tappa 2 non valido, inserire lettere o i caratteri: ',' '-' '.'";
        $problems{empty} = 'no';
    }
    else {
        $old_input{TAPPA2} = $q->param('tappa2');
    }

    if($q->param('tappa3') ne "" and !($q->param('tappa3')=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0030}-\x{0039}]|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/)) {
        $problems{TAPPA3_ERR} = "Luogo della tappa 3 non valido, inserire lettere o i caratteri: ',' '-' '.'";
        $problems{empty} = 'no';
    }
    else {
        $old_input{TAPPA3} = $q->param('tappa3');
    }

    if($q->param('tappa3') ne "" ) {
        if($q->param('tappa2') eq "" ) {
            $problems{TAPPA2_ERR} = "Per inserire la terza tappa, &egrave; necessario inserire le tappe precedenti";
            $problems{empty} = 'no';
        }
        if($q->param('tappa1') eq "" ) {
            $problems{TAPPA1_ERR} = "Per inserire la terza tappa, &egrave; necessario inserire le tappe precedenti";
            $problems{empty} = 'no';
        }
    }

    if($q->param('tappa2') ne "" ) {
        if($q->param('tappa1') eq "" ) {
            $problems{TAPPA1_ERR} = "Per inserire la seconda tappa, &egrave; necessario inserire la tappa precedente";
            $problems{empty} = 'no';
        }
    }

    my ($sec,$min,$hour,$mday, $mon, $year ,$wday,$yday,$isdst) = localtime();
    $year = $year + 1900;
    my @dataP = split /-/, $q->param('dataP');
    my @oraP = split /:/, $q->param('oraP');
    my @dataA = split /-/, $q->param('dataA');
    my @oraA = split /:/, $q->param('oraA');

    if($q->param('dataP') eq "") {
        $problems{DATAP_ERR} = "Data di partenza mancante";
        $problems{empty} = 'no';
    }
    elsif (!($q->param('dataP')=~m/^[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}$/)) { # aggiungere condizione date_time::valida_data
        $problems{DATAP_ERR} = "Data di partenza non valida. Inserire una data in formato gg-mm-aaaa oppure g-m-aaaa";
        $problems{empty} = 'no';
    }
    else {
        if(!(date_time::valida_data($dataP[0], $dataP[1], $dataP[2]))) {
            $problems{DATAP_ERR} = "Data di partenza non valida.";
            $problems{empty} = 'no';
        }
        else {
            $old_input{DATAP} = $q->param('dataP');
        }       
    }

    if($q->param('oraP') eq "") {
        $problems{ORAP_ERR} = "Ora di partenza mancante";
        $problems{empty} = 'no';
    }
    elsif (!($q->param('oraP')=~m/^(([0-1][0-9])|([2][0-3])):[0-5][0-9]$/)) {
        $problems{ORAP_ERR} = "Ora di partenza non valida. Inserire un ora in formato hh:mm";
        $problems{empty} = 'no';
    }
    else {
        $old_input{ORAP} = $q->param('oraP');
    }

    if(!(defined($problems{'DATAP_ERR'})) and !(defined($problems{'ORAP_ERR'})) ) { # controllo che la data di partenza sia futura
       if(date_time::confronto_dataora($mday, $mon, $year, $hour, $min, $dataP[0], $dataP[1]-1, $dataP[2], $oraP[0]-1, $oraP[1])) {
            # la data di partenza &egrave; (correttamente) futura, quindi di passa a controllare la data di arrivo
            if($q->param('dataA') eq "") {
                $problems{DATAA_ERR} = "Data di arrivo mancante";
                $problems{empty} = 'no';
            }
            elsif (!($q->param('dataA')=~m/^[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}$/)) { # aggiungere condizione date_time::valida_data
                $problems{DATAA_ERR} = "Data di arrivo non valida. Inserire una data in formato gg-mm-aaaa oppure g-m-aaaa";
                $problems{empty} = 'no';
            }
            elsif(!(date_time::valida_data($dataA[0], $dataA[1], $dataA[2]))) {
                    $problems{DATAA_ERR} = "Data di arrivo non valida.";
                    $problems{empty} = 'no';                 
            }

            if($q->param('oraA') eq "") {
                $problems{ORAA_ERR} = "Ora di arrivo mancante";
                $problems{empty} = 'no';
            }
            elsif (!($q->param('oraP')=~m/^(([0-1][0-9])|([2][0-3])):[0-5][0-9]$/)) {
                $problems{ORAA_ERR} = "Ora di arrivo non valida. Inserire un ora in formato hh:mm";
                $problems{empty} = 'no';
            }
            

            if(!defined($problems{'DATAA_ERR'}) and !defined($problems{'ORAA_ERR'}) ) { # le date sono corrette. Ora si controlla che l arrivo sia successivo alla partenza
                if(!(date_time::confronto_dataora($dataP[0], $dataP[1]-1, $dataP[2], $oraP[0], $oraP[1], $dataA[0], $dataA[1]-1, $dataA[2], $oraA[0], $oraA[1]))) {
                    $problems{DATAA_ERR} = "la data/ora di partenza dev essere successiva alla data/ora d arrivo";
                    $problems{ORAA_ERR} = "la data/ora di partenza dev essere successiva alla data/ora d arrivo";
                    $problems{empty} = 'no';
                }
                else {
                    $old_input{DATAA} = $q->param('dataA');
                    $old_input{ORAA} = $q->param('oraA');
                }
            }
        }
        else { # ramo in cui la data di partenza &egrave; corretta, ma non &egrave; futura
            $problems{DATAP_ERR} = "la data/ora di partenza dev essere almeno di un ora nel futuro";
            $problems{ORAP_ERR} = "la data/ora di partenza dev essere almeno di un ora nel futuro";
            $problems{empty} = 'no';
        }
    }

    if($q->param('prezzo') eq "") {
        $problems{PREZZO_ERR} = "Prezzo mancante";
        $problems{empty} = 'no';
    }
    else {
        my $prezzo = $q->param('prezzo');
        $prezzo =~ tr/,/./;
        if(Scalar::Util::looks_like_number($prezzo) and $prezzo>0) {
            $old_input{PREZZO} = $prezzo;
        }
        else {
            $problems{PREZZO_ERR} = "Prezzo non valido. Inserire un prezzo positivo valido";
            $problems{empty} = 'no';
        }
    }

    if($q->param('posti') eq "") {
        $problems{POSTI_ERR} = "Posti disponibili mancante";
        $problems{empty} = 'no';
    }
    elsif (!($q->param('posti')=~m/^[0-9]{1,2}$/)) {
        $problems{POSTI_ERR} = "Numero di posti disponibili non valido, inserire un valore intero positivo minore di 99";
        $problems{empty} = 'no';
    }
    else {
        $old_input{POSTI} = $q->param('posti');
    }

    $old_input{DESCRIZIONEVIAGGIO}= $q->param('descrizioneViaggio');  


    ###############################################################################
    if($problems{'empty'} eq "no") {
        $session->param('problems',\%problems);
        $session->param('old_input',\%old_input);
        print $session->header(-location => "offerta_passaggio.cgi");
    }
    else {
        if (length($dataP[1])  == 1) {$dataP[1] = "0$dataP[1]";}
        if (length($dataP[0]) == 1) {$dataP[0] = "0$dataP[0]";}
        if (length($dataA[1])  == 1) {$dataA[1] = "0$dataA[1]";}
        if (length($dataA[0]) == 1) {$dataA[0] = "0$dataA[0]";}

        my %Partenza = (
            Luogo => $q->param('partenza'),
            Data => $dataP[2]."-".$dataP[1]."-".$dataP[0],
            Ora => $q->param('oraP').":00",
            PostiDisp => $q->param('posti')
            );
        my %Arrivo = (
            Luogo => $q->param('arrivo'),
            Data => $dataA[2]."-".$dataA[1]."-".$dataA[0],
            Ora => $q->param('oraA').":00",
            PostiDisp => 0
            );

        if($q->param('descrizioneViaggio') ne "") {
            my $descr = $q->param('descrizioneViaggio');
            $descr =encode_entities($descr,'>');
            $descr = encode_entities($descr, '<');
            $Passaggio{Dettagli}=$descr;
        }
        $Passaggio{PrezzoTot} = $q->param('prezzo');
        $Passaggio{PostiDisp} = $q->param('posti');
        $Passaggio{Conducente} = $username;
        $Passaggio{Partenza} = \%Partenza;
        $Passaggio{Arrivo} = \%Arrivo;

        my @data_ora_tappe;

        if($q->param('tappa3') ne "") {
            @data_ora_tappe = date_time::calcola_tappe($dataP[0], $dataP[1], $dataP[2], $oraP[0], $oraP[1], $dataA[0], $dataA[1], $dataA[2], $oraA[0], $oraA[1],5);
            my @data_ora_tappa1 = split / /,$data_ora_tappe[1];
            my @data_ora_tappa2 = split / /,$data_ora_tappe[2];
            my @data_ora_tappa3 = split / /,$data_ora_tappe[3];
            my %Tappa1 = (
                Luogo => $q->param('tappa1'),
                Data => $data_ora_tappa1[0],
                Ora => $data_ora_tappa1[1],
                PostiDisp => $q->param('posti')
                );
            my %Tappa2 = (
                Luogo => $q->param('tappa2'),
                Data => $data_ora_tappa2[0],
                Ora => $data_ora_tappa2[1],
                PostiDisp => $q->param('posti')
                );
            my %Tappa3 = (
                Luogo => $q->param('tappa3'),
                Data => $data_ora_tappa3[0],
                Ora => $data_ora_tappa3[1],
                PostiDisp => $q->param('posti')
                );
            $Passaggio{Tappa1} = \%Tappa1;
            $Passaggio{Tappa2} = \%Tappa2;
            $Passaggio{Tappa3} = \%Tappa3;
        }
        elsif ($q->param('tappa2') ne "") {
            @data_ora_tappe = date_time::calcola_tappe($dataP[0], $dataP[1], $dataP[2], $oraP[0], $oraP[1], $dataA[0], $dataA[1], $dataA[2], $oraA[0], $oraA[1],4);
            my @data_ora_tappa1 = split / /,$data_ora_tappe[1];
            my @data_ora_tappa2 = split / /,$data_ora_tappe[2];
            my %Tappa1 = (
                Luogo => $q->param('tappa1'),
                Data => $data_ora_tappa1[0],
                Ora => $data_ora_tappa1[1],
                PostiDisp => $q->param('posti')
                );
            my %Tappa2 = (
                Luogo => $q->param('tappa2'),
                Data => $data_ora_tappa2[0],
                Ora => $data_ora_tappa2[1],
                PostiDisp => $q->param('posti')
                );
            $Passaggio{Tappa1} = \%Tappa1;
            $Passaggio{Tappa2} = \%Tappa2;
        }
        elsif ($q->param('tappa1') ne "") {
            @data_ora_tappe = date_time::calcola_tappe($dataP[0], $dataP[1], $dataP[2], $oraP[0], $oraP[1], $dataA[0], $dataA[1], $dataA[2], $oraA[0], $oraA[1],3);
            my @data_ora_tappa1 = split / /,$data_ora_tappe[1];
            my %Tappa1 = (
                Luogo => $q->param('tappa1'),
                Data => $data_ora_tappa1[0],
                Ora => $data_ora_tappa1[1],
                PostiDisp => $q->param('posti')
                );
            $Passaggio{Tappa1} = \%Tappa1;
        }

        data_registration::inserisci_nuovo_viaggio(\%Passaggio);
        data_registration::incrementa("NumPassaggiOff", $username);
        print $session->header(-location => "viaggi.cgi");
    }


}
