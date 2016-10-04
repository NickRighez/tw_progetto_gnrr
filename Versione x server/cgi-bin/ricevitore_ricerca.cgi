#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI ;
use CGI::Session;
#use CGI::Cookie;
use CGI::Carp qw(fatalsToBrowser);
#use lib "../libreria";
use libreria::data_registration;
#use lib "libreria";
use libreria::sessione;

my $q = new CGI;
my @s = sessione::creaSessione();
my $session = $s[0];

my %problems = (empty => 'yes');
my %old_input;

if($q->param('partenza') eq '') {
    $problems{PARTENZA_ERR} = 'Luogo di partenza mancante';
    $problems{empty} = 'no';
}
elsif (!($q->param('partenza')=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0030}-\x{0039}]|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/)) {
    $problems{PARTENZA_ERR} = 'Luogo di partenza non valido';
    $problems{empty} = 'no';
}
else {
    $old_input{PARTENZA} = $q->param('partenza');
}

if($q->param('arrivo') eq '') {
    $problems{ARRIVO_ERR} = 'Luogo di partenza mancante';
    $problems{empty} = 'no';
}
elsif (!($q->param('arrivo')=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0030}-\x{0039}]|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/)) {
    $problems{ARRIVO_ERR} = 'Luogo di arrivo non valido';
    $problems{empty} = 'no';
}
else {
    $old_input{ARRIVO} = $q->param('arrivo');
}

if($q->param('data') eq '') {
    $problems{DATA_ERR} = 'Data di partenza mancante';
    $problems{empty} = 'no';
}
elsif (!($q->param('data')=~m/^[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}$/)) {
    $problems{DATA_ERR} = "Data di partenza non valida. Inserire una data in formato gg-mm-aaaa oppure g-m-aaaa";
    $problems{empty} = 'no';
}
else {
    $old_input{DATA} = $q->param('data');
}


if($problems{'empty'} eq 'yes') {
    my @data_arr = split /-/, $q->param('data');
    my %Ricerca = (
        partenza =>  $q->param('partenza'),
        arrivo => $q->param('arrivo'),
        data => $q->param('data')
        );
    $session->param('ricerca_prec', \%Ricerca);
    if (length($data_arr[1])  == 1) {$data_arr[1] = "0".$data_arr[1];}
    if (length($data_arr[0]) == 1) {$data_arr[0] = "0".$data_arr[0];}
    my $data = $data_arr[2]."-".$data_arr[1]."-".$data_arr[0];
    print $session->header(-location => "risultati_ricerca.cgi?partenza=".$q->param('partenza')."&arrivo=".$q->param('arrivo')."&data=$data");
}
else {
    $session->param('problems',\%problems);
    $session->param('old_input',\%old_input);
    print $session->header(-location => "home.cgi");
}
