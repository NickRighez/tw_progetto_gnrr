#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use libreria::data_registration;
use libreria::sessione;

use utf8;
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";

use Encode qw(decode_utf8);

my $q = new CGI;
my @s = sessione::creaSessione();
my $session = $s[0];

if($q->request_method() ne "POST") {
     my %problems=(
      DESCRIZIONE_ERRORE => "Tentativo di ricerca passaggio con una modalit&agrave; non permessa."
      );
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
else{
    my %problems = (empty => 'yes');
    my %old_input;

    my $partenza = decode_utf8($q->param('partenza'));

    if($partenza eq '') {
        $problems{PARTENZA_ERR} = 'Luogo di partenza mancante';
        $problems{empty} = 'no';
    }
    elsif (! $partenza =~ m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|è|é|à|ù|ò|ì|\s)+$/) {
        $problems{PARTENZA_ERR} = 'Luogo di partenza non valido';
        $problems{empty} = 'no';
    }
    else {
        $old_input{PARTENZA} = decode_utf8($partenza);
    }

my $arrivo = decode_utf8($q->param('arrivo'));
    if($arrivo eq '') {
        $problems{ARRIVO_ERR} = 'Luogo di partenza mancante';
        $problems{empty} = 'no';
    }
    elsif (!$arrivo=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[àèéìòù]|\s)+$/) {
        $problems{ARRIVO_ERR} = 'Luogo di arrivo non valido';
        $problems{empty} = 'no';
    }
    else {
        $old_input{ARRIVO} = decode_utf8($arrivo);
    }

my $dataInput = $q->param('data');
    if($dataInput eq '') {
        $problems{DATA_ERR} = 'Data di partenza mancante';
        $problems{empty} = 'no';
    }
    elsif (!$dataInput=~m/^[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}$/) {
        $problems{DATA_ERR} = "Data di partenza non valida. Inserire una data in formato gg-mm-aaaa oppure g-m-aaaa";
        $problems{empty} = 'no';
    }
    else {
        $old_input{DATA} = $dataInput;
    }


    if($problems{'empty'} eq 'yes') {
        my @data_arr = split /-/, $dataInput;
        if (length($data_arr[1])  == 1) {$data_arr[1] = "0".$data_arr[1];}
        if (length($data_arr[0]) == 1) {$data_arr[0] = "0".$data_arr[0];}
        my $data = $data_arr[2]."-".$data_arr[1]."-".$data_arr[0];

        my %Ricerca = (
            partenza =>  $partenza,
            arrivo => $arrivo,
            data => $data
            );
            $session->param('ricerca',\%Ricerca);
        print $session->header(-location => "risultati_ricerca.cgi");
    }
    else {
        $session->param('problems',\%problems);
        $session->param('old_input',\%old_input);
        print $session->header(-location => "home.cgi");
    }
}
