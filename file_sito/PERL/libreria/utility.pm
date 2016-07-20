#! /usr/bin/perl -w

package utility;

use strict;
use warnings;
use diagnostics;
use Switch;
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


sub crea_itinerario {
    my $tag = shift @_; # tag = Partenza, Arrivo, Tappa1, Tappa2, Tappa3 (stringa)
    my $node;
    switch($tag) {
        case "Partenza" { $node="<Partenza Numero=\"0\"> \n"; }
        case "Tappa1" { $node="<Tappa Numero=\"1\"> \n"; }
        case "Tappa2" { $node="<Tappa Numero=\"2\"> \n"; }
        case "Tappa3" { $node="<Tappa Numero=\"3\"> \n"; }
        case "Arrivo" { $node="<Arrivo Numero=\"4\"> \n"; }
        else { die("Tag Errato"); }
    }
    my %tappa= (
                PostiDisp => $q->param("postiDisp"),    
                Data => $q->param("data$tag"),
                Ora => $q->param("ora$tag"),
                Provincia => $q->param("prov$tag"),
                Comune => $q->param("com$tag")
                );
    if(ControlloTappa(\%tappa)==1) {
        my @parametri=('PostiDisp', 'Data', 'Ora', 'Provincia', 'Comune');
        foreach my $elemento (@parametri) {
            my $new = "<$elemento>$tappa{$elemento}</$elemento> \n";
            $node = $node.$new;
        }
        if($tag eq "Tappa1" | $tag eq "Tappa2" | $tag eq "Tappa3" ) { 
            $node = $node."</Tappa>"; 
        }
        else { $node = $node."</$tag> \n"; }
        return $node;
    }
    else {
        return 0;
    }
}

sub CreaTappa {
    my $tag = shift @_;
    my $num_t = shift @_;
    my $t = shift @_;
    my $node="<$tag Numero=\"$num_t\"> \n";
    my %tappa = %$t;
    if(ControlloTappa(\%tappa)==1) {  ############          CONTROLLO TAPPA DEV ESSERE GIA STATO FATTO 
        my @parametri=('PostiDisp', 'Data', 'Ora', 'Provincia', 'Comune');
        foreach my $elemento (@parametri) {
            my $new = "<$elemento>$tappa{$elemento}</$elemento> \n";
            $node = $node.$new;
        }                        
        $node = $node."</$tag> \n"; 
    }
}

sub ControlloTappa {
    my $t = shift @_;
    my %tappa=%$t;
    if($tappa{'Provincia'} =~ m/^[A-Z][a-z]+(\s[a-z]+[à|ò|ì]*)*$/ &&
    $tappa{'Comune'} =~ m/^[A-Z][a-z]+(\s[a-z]+[à|ò|ì]*)*$/ &&
    $tappa{'Data'} =~ m/^[2][0-1][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$/ &&  # controllo che il viaggio avvenga entro un anno
    $tappa{'Ora'} =~ m/^[0-1][0-9]:[0-5][0-9]|[2][0-3]:[0-5][0-9]$/) {
        return 1;
    }
    else {
        return 0;
    }      
}


1;
