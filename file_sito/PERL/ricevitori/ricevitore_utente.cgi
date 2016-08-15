#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI::Carp qw(fatalsToBrowser);
#use File::Spec;
#use lib File::Spec->catdir($FindBin::Bin, '..' ,'libreria');
#use FindBin;
use lib "../libreria";
use data_registration;
use utility;
my $q = CGI->new;

#  ******  TESTARE CHE IL METODO DELLA FORM SIA 'POST' *************  #
# ******** (per la ricerca il metodo è get) ******** #

if ($q->request_method eq 'POST') {

	if(!($q->param('Username')=~m/^[A-Za-z0-9_-]{5,18}$/)) {
		die("Username non valido");
	}

	if(!($q->param('email')=~m/^([a-z0-9_\.-]+)@([a-z]+)\.([a-z]{2,6})$/)) {
		die("indirizzo email non valido");
	}

	if(!($q->param('nome')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.-]+$/)) {
		die("nome utente non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola");
	}

	if(!($q->param('cognome')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.-]+$/)) {
		die("cognome utente non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola");
	}

	# non viene fatto controllo sul valore di 'sesso' in quanto i valori possibili sono dati dalla form

	if(!($q->param('anno')=~m/^[1-2][0-9][0-9][0-9]$/)) {
		die("Anno di nascita non valida, inserire l anno in formato 'aaaa'");
	}
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
	if(($q->param('anno'))>($year+1900-18)) {
		die("Possono registrarsi solo utenti maggiorenni");
	}

	if(!($q->param('password')=~m/^[A-Za-z0-9_\.-]{8,16}$/)) {
		die("Password non valida, sono permesse lettere maiuscole o minuscole, e i caratteri underscore, hyphen o punto");
	}

	my %ute = (
			Username => $q->param('Username'),
	        Email => $q->param('email'),       
	        Nome => $q->param('nome'),     
	        Cognome => $q->param('cognome'), 
	        Sesso =>$q->param('sesso'),
	        AnnoNascita => $q->param('anno'), 
	        Password => $q->param('password')
			);

	if($q->param('descr_pers') ne '') {
		$ute{'DescrizionePers'}=$q->param('descr_pers');
	}

	if(data_registration::inserisci_nuovo_utente(\%ute)) {
		print $q->redirect("http://localhost/accedi.html");
	}

}

