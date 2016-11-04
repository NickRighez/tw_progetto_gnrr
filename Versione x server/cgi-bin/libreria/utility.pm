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



# Crea il codice XML della tappa specificata dall hash $t
sub CreaTappa {
    my $tag = shift @_; # valori: Partenza, Tappa, Arrivo
    my $num_t = shift @_; # Numero della tappa
    my $t = shift @_; # hash con le informazioni della tappa (PostiDisp, Data, Ora, Luogo)
    my $node="<$tag Numero=\"$num_t\"> \n";
    my %tappa = %$t;
    foreach my $el (%tappa){
        utf8::encode($el);
    }
    my @parametri=('PostiDisp', 'Data', 'Ora', 'Luogo');
    foreach my $elemento (@parametri) {
        my $new = "<$elemento>$tappa{$elemento}</$elemento> \n";
        $node = $node.$new;
    }
    $node = $node."<Prenotazioni></Prenotazioni>\n</$tag> \n";
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

sub calcola_prezzo {
    my $part= shift @_;
    my $arr = shift @_;
    my $id_p = shift @_;
    my $doc= shift @_;
    my $prezzoTot = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$id_p']/PrezzoTot")->get_node(1)->textContent();
    my @tappeTot = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$id_p']/Itinerario/*");
    my $numTappeTot = @tappeTot;
    my @tappeCorrenti = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$id_p']/Itinerario/*[\@Numero>='$part' and \@Numero<='$arr']");
    my $numTappeCorrenti = @tappeCorrenti;
    my $prezzo = ($prezzoTot/$numTappeTot)*$numTappeCorrenti;
    return sprintf("%.2f",$prezzo);
}




1;
