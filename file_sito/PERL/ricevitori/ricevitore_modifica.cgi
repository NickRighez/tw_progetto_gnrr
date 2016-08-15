#! /usr/bin/perl -w
print "Content-type: text/html\n\n";

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use lib "../libreria";
use data_registration;

my $q=CGI->new;

my %Modifica=( 
	Username => $q->param('Utente'), # username dell utente che modifica il profilo
	Sesso => $q->param('sesso')
	);

if($q->param('nome') ne 'Nome') {
	if(!($q->param('nome')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.-]+$/)) {
		die("nome utente non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola");
	}
	$Modifica{Nome}=$q->param('nome');
}

if($q->param('cognome') ne 'Cognome') {
	if(!($q->param('cognome')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.-]+$/)) {
		die("cognome utente non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola");
	}
	$Modifica{Cognome}=$q->param('cognome');
}

if($q->param('email') ne 'Email') {
	if(!($q->param('email')=~m/^([a-z0-9_\.-]+)@([a-z]+)\.([a-z]{2,6})$/)) {
		die("indirizzo email non valido");
	}
	# controllo email unica
	$Modifica{Email}=$q->param('email');
}

if($q->param('anno') ne 'Anno') {
	if(!($q->param('anno')=~m/^[1-2][0-9][0-9][0-9]$/)) {
		die("Anno di nascita non valida, inserire l anno in formato 'aaaa'");
	}
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
	$year=$year+1900-18;
	print $year,$q->param('anno');
	if(($q->param('anno'))>$year) {
		die("Possono registrarsi solo utenti maggiorenni");
	}
	$Modifica{AnnoNascita}=$q->param('anno');
}

if($q->param('descrizioneForm') ne '') {
	# controllo per code injection da fare
	$Modifica{DescrizionePers}=$q->param('descrizioneForm');
}

print $q->param('annoPatente')."<br>".$q->param('auto')."<br>".$q->param('chiacchiere')."<br>".$q->param('musica')."<br>".$q->param('animali')."<br>".$q->param('fumatori')."<br>";

if($q->param('annoPatente') ne '' or $q->param('auto') ne '' or $q->param('chiacchiere') ne '' or $q->param('musica') ne '' or $q->param('animali') ne '' or $q->param('fumatori') ne '') {
	if($q->param('annoPatente') eq '' or $q->param('auto') eq '' or $q->param('chiacchiere') eq '' or $q->param('musica') eq '' or $q->param('animali') eq '' or $q->param('fumatori') eq '') {
		die("Le informazioni necessarie per offrire un passaggio devono essere tutte presenti, o nessuna");
	}
	if(!($q->param('annoPatente')=~m/^[1-2][0-9][0-9][0-9]$/)) {
		die("Anno di rilascio della patente non valido, inserire l anno in formato 'aaaa'");
	}
	if(!($q->param('auto')=~m/^[a-z0-9A-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.-]+$/)) {
		die("auto non valida, inserire solo lettere o numeri");
	}
	$Modifica{Patente}=$q->param('annoPatente');
	$Modifica{Auto}=$q->param('auto');
	$Modifica{Chiacchere}=$q->param('chiacchiere');
	$Modifica{Musica}=$q->param('musica');
	$Modifica{Animali}=$q->param('animali');
	$Modifica{Fumatore}=$q->param('fumatori');
}

print data_registration::inserisci_modifica_profilo(\%Modifica);


