#! /usr/bin/perl -w
#print "Content-type: text/html\n\n";

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use lib "../libreria";
use data_registration;
use lib "libreria";
use sessione;

my $q=new CGI;;
my @s = sessione::creaSessione();  
 my $session = $s[0];
my %problems = ( empty => 'yes' );
my %old_input;

#  ******  TESTARE CHE IL METODO DELLA FORM SIA 'POST' *************  #
# ******** (per la ricerca il metodo è get) ******** #

if ($q->request_method eq 'POST') {

	if($q->param('username') eq "") {
		$problems{username_err} = "Username mancante";
		$problems{empty} = "no";
	}
	elsif(!($q->param('username')=~m/^[A-Za-z0-9_-]{5,18}$/)) {
		$problems{username_err} = "Username non valido, caratteri ammessi: lettere, numeri, '_', '-'";
		$problems{empty} = "no";
	}
	else {
		$old_input{username} = $q->param('Username');
	} 

	if($q->param('email') eq "") {
		$problems{email_err} = "E-mail mancante";
		$problems{empty} = "no";
	}
	elsif(!($q->param('email')=~m/^([a-z0-9_\.-]+)@([a-z]+)\.([a-z]{2,6})$/)) {
		$problems{email_err}="indirizzo email non valido";
		$problems{empty}="no";
	}
	else {		
		my $doc = data_registration::get_xml_doc();
		my @email = $doc->findnodes("//SetUtenti/Utente[Email='".$q->param('email')."']");
		my $num = @email;
		if($num!=0) {
			$problems{email_err}="indirizzo email già esistente";
			$problems{empty}="no";
		}
		else {
			$old_input{email}=$q->param('email');
		}
	}
		

	if($q->param('nome') eq "") {
		$problems{nome_err} = "Nome utente mancante";
		$problems{empty} = "no";
	}
	elsif(!($q->param('nome')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð'\'']+$/)) {
		$problems{nome_err}="nome utente non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola";
		$problems{empty}="no";
	}
	else {
		$old_input{nome}=$q->param('nome');
	}

	if($q->param('cognome') eq "") {
		$problems{cognome_err} = "Cognome utente mancante";
		$problems{empty} = "no";
	}
	elsif(!($q->param('cognome')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð]+$/)) {
		$problems{cognome_err}="cognome utente non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola";
		$problems{empty}="no";
	}
	else {
		$old_input{cognome}=$q->param('cognome');
	}

	# non viene fatto controllo sul valore di 'sesso' in quanto i valori possibili sono dati dalla form

	if($q->param('anno') eq "") {
		$problems{anno_err}="Anno di nascita mancante";
		$problems{empty}="no";
	}
	elsif(!($q->param('anno')=~m/^[1-2][0-9][0-9][0-9]$/)) {
		$problems{anno_err}="Anno di nascita non valida, inserire l anno in formato 'aaaa'";
		$problems{empty}="no";
	}
	else {
		my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
		$year=$year+1900-18;
		if(($q->param('anno'))>$year) {
			$problems{anno_err}="Possono registrarsi solo utenti maggiorenni";
			$problems{empty}="no";
		}
		else {
			$old_input{anno}=$q->param('anno');
		}
	} 

	if($q->param('password') eq "") {
		$problems{password_err} = "Password mancante";
		$problems{empty}="no";
	}
	elsif (length($q->param('password'))<8 or length($q->param('password')>16)){
		$problems{password_err} = "La password dev essere compresa fra 8 e 16 caratteri";
		$problems{empty}="no";
	}		
	elsif(!($q->param('password')=~m/^[A-Za-z0-9_\.-]{8,16}$/)) {
		$problems{password_err} = "Password non valida, sono permesse lettere maiuscole o minuscole, e i caratteri underscore, hyphen o punto";
		$problems{empty}="no";
	}
	elsif($q->param('password') ne $q->param('conferma')) {
			$problems{conferma_err} = "Password non coincidenti";
			$problems{empty}="no";
	}

	

	my %ute = (
			Username => $q->param('username'),
	        Email => $q->param('email'),       
	        Nome => $q->param('nome'),     
	        Cognome => $q->param('cognome'), 
	        Sesso =>$q->param('sesso'),
	        AnnoNascita => $q->param('anno'), 
	        Password => $q->param('password')
			);

	#if($q->param('descr_pers') ne '') {
	#	$ute{'DescrizionePers'}=$q->param('descr_pers');
	#}
	if($problems{'empty'} eq 'yes') {
		if(data_registration::inserisci_nuovo_utente(\%ute)) {
			print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_login.cgi");
		}
	}
	else {
		$session->param('problems', \%problems);
		$session->param('old_input', \%old_input);
		print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_iscrizione.cgi");
	} 
}	



