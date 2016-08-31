#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI ;
use CGI::Session;
#use CGI::Cookie;
use CGI::Carp qw(fatalsToBrowser);  
use lib "../libreria";
use data_registration;
use lib "libreria";
use sessione;

 my $q = new CGI;
 my @s = sessione::creaSessione();  
 my $session = $s[0];

my %problems = (empty => 'yes');
my %old_input;

 if($q->param('partenza') eq '') {
  $problems{ERR_PARTENZA} = 'Luogo di partenza mancante';
  $problems{empty} = 'no';
}
elsif (!($q->param('partenza')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.-]+$/)) {
  $problems{ERR_PARTENZA} = 'Luogo di partenza non valido';
  $problems{empty} = 'no';
}
else {
  $old_input{PARTENZA} = $q->param('partenza');
}

if($q->param('arrivo') eq '') {
  $problems{ERR_ARRIVO} = 'Luogo di partenza mancante';
  $problems{empty} = 'no';
}
elsif (!($q->param('arrivo')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.-]+$/)) {
  $problems{ERR_ARRIVO} = 'Luogo di arrivo non valido';
  $problems{empty} = 'no';
}
else {
  $old_input{ARRIVO} = $q->param('arrivo');
}

if($q->param('data') eq '') {
  $problems{ERR_DATA} = 'Data di partenza mancante';
  $problems{empty} = 'no';
}
elsif (!($q->param('data')=~m/^[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}$/)) { # aggiungere condizione date_time::valida_data
  $problems{ERR_DATA} = "Data di partenza non valida. Inserire una data in formato gg-mm-aaaa oppure g-m-aaaa";
  $problems{empty} = 'no';
}
else {
  $old_input{DATA} = $q->param('data');
}

 # verificare che la data di partenza sia futura?

if($problems{'empty'} eq 'yes') {
  my @data_arr = split /-/, $q->param('data');
  if (length($data_arr[1])  == 1) {$data_arr[1] = "0".$data_arr[1];}
  if (length($data_arr[0]) == 1) {$data_arr[0] = "0".$data_arr[0];}
  my $data = $data_arr[2]."-".$data_arr[1]."-".$data_arr[0];
  print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_risultati_ricerca.cgi?partenza=".$q->param('partenza')."&arrivo=".$q->param('arrivo')."&data=$data");
}
else {
	$session->param('problems',\%problems);
	$session->param('old_input',\%old_input);
	print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_home.cgi");
}


