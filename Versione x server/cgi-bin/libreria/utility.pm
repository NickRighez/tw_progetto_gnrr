#! /usr/bin/perl -w

package utility;

use strict;
use warnings;
use diagnostics;
#use Switch;
use CGI;

use XML::LibXML;

our $q = new CGI;

#argomenti: xpath, keyname, keyvalue, doc
# verifica la presenza di elementi che abbiano valori delle chiavi indicati
sub verifica_presenza {
    my $xpath = shift @_;
    my $doc = shift @_;
    my @nodes = $doc->findnodes($xpath);
    my $numNodes = @nodes;
    return $numNodes;
}

# Funzione che verifica la presenza degli input necessari a memorizzare una Tappa (Luogo, Data e Ora), 
#   e restituisce il corrispondente hash con le informazionni da memorizzare
sub check_presenza_param_tappa {
    my $tag= shift @_; # $tag = 'Partenza', 'Tappa1', 'Tappa2', 'Tappa3', 'Arrivo'
    # Luogo, Data e Ora di Partenza e Arrivo sono obbligatori -> !($tag=~"/Tappa/")
    if(!($tag=~"/Tappa/") or $q->param('luogo'.$tag) ne '' or $q->param('data'.$tag) ne '' or $q->param('ora'.$tag) ne '') {
        if($q->param('luogo'.$tag) eq '') {
            die("Luogo $tag mancante");
        }
        if($q->param('data'.$tag) eq '') {
            die("Data $tag mancante");
        }
        if($q->param('ora'.$tag) eq '') {
            die("Ora di ritrovo $tag mancante");
        }
    }
    my %hash_tappa= ();
    $hash_tappa{Luogo}=$q->param('luogo'.$tag);
    $hash_tappa{Data}=$q->param('data'.$tag);
    $hash_tappa{Ora}=$q->param('ora'.$tag).":00";
    $hash_tappa{PostiDisp}=$q->param('postiDisp');
    return %hash_tappa;
}

# Crea il codice XML della tappa specificata dall hash $t 
sub CreaTappa {
    my $tag = shift @_; # valori: Partenza, Tappa, Arrivo
    my $num_t = shift @_; # Numero della tappa
    my $t = shift @_; # hash con le informazioni della tappa (PostiDisp, Data, Ora, Luogo)
    my $node="<$tag Numero=\"$num_t\"> \n";
    my %tappa = %$t; 
    my @parametri=('PostiDisp', 'Data', 'Ora', 'Luogo');
    foreach my $elemento (@parametri) {
        my $new = "<$elemento>$tappa{$elemento}</$elemento> \n";
        $node = $node.$new;
    }                        
    $node = $node."<Prenotazioni></Prenotazioni>\n</$tag> \n";     
}

sub controllo_tappa {
    my $t = shift @_;
    my %tappa=%$t;
    if($tappa{'Data'} =~ m/^[2][0-1][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$/ &&  # controllo che il viaggio avvenga entro un anno
        $tappa{'Ora'} =~ m/^[0-1][0-9]:[0-5][0-9]:00|[2][0-3]:[0-5][0-9]:00$/) {
        return 1;
    }
    else {
        return 0;
    }      
}


sub calcola_posti_disponibili {
    my $part= shift @_;
    my $arr = shift @_;
    my $id_p = shift @_;
    my $doc= shift @_;
    my $min = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$id_p']/Itinerario/*[\@Numero='$part']/PostiDisp")->get_node(1)->textContent();
    for(my $i=$part+1;$i<$arr;$i++) {
        my @nodes = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$id_p']/Itinerario/*[\@Numero=$i]");
        if(@nodes != 0) {
            my $pd = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$id_p']/Itinerario/*[\@Numero=$i]/PostiDisp")->get_node(1)->textContent();
            if($pd < $min) {
            $min=$pd;
            }
        }      
    }
    return $min;
}




1;