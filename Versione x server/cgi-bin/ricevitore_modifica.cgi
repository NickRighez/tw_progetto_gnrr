#! /usr/bin/perl -w
#print "Content-type: text/html\n\n";

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
#use lib "../libreria";
use libreria::data_registration;
#use lib "libreria";
use libreria::sessione;
use HTML::Entities;

my $q=new CGI;;
my @s = sessione::creaSessione();  
 my $session = $s[0];

if(!defined($session->param('username'))) {
  my %problems=(
     not_logged => "Utente non loggato, pagina inaccessibile"
     );
  $session->param('problems',\%problems);
  print $session->header(-location => "login.cgi");
} 
else {
	my %problems = ( empty => 'yes' );
	my %old_input;

	my $username = $session->param('username');

	my %Modifica=( 
		Username => $session->param('username'), # username dell utente che modifica il profilo
		Sesso => $q->param('sesso')
		);

	if($q->param('nome') ne '') {
		if(!($q->param('nome')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð]+$/)) {
			$problems{ERR_NOME}="Nome utente non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola";
			$problems{empty}="no";
		}
		else {
			$old_input{NOME}=$q->param('nome');
		}
		$Modifica{Nome}=$q->param('nome');
	}

	if($q->param('cognome') ne '') {
		if(!($q->param('cognome')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.-]+$/)) {
			$problems{ERR_COGNOME}="Cognome utente non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola";
			$problems{empty}="no";
		}
		else {
			$old_input{COGNOME}=$q->param('cognome');
		}
		$Modifica{Cognome}=$q->param('cognome');
	}

	if($q->param('email') ne '') {
		if(!($q->param('email')=~m/^([a-z0-9_\.-]+)@([a-z]+)\.([a-z]{2,6})$/)) {
			$problems{ERR_EMAIL}="Indirizzo email non valido";
			$problems{empty}="no";
		}
		else {		
			my $doc = data_registration::get_xml_doc();
			my @email = $doc->findnodes("//SetUtenti/Utente[Email='".$q->param('email')."']");
			my $num = @email;
			if($num!=0 and $q->param('email') ne $email[0]->findnodes("Email")->get_node(1)->textContent) {
				$problems{ERR_EMAIL}="Indirizzo email già esistente";
				$problems{empty}="no";
			}
			else {
				$old_input{EMAIL}=$q->param('email');
			}
		}
			
		$Modifica{Email}=$q->param('email');
	}

	if($q->param('anno') ne '') {
		if(!($q->param('anno')=~m/^[1-2][0-9][0-9][0-9]$/)) {
			$problems{ERR_ANNO}="Anno di nascita non valida, inserire l anno in formato 'aaaa'";
			$problems{empty}="no";
		}
		else {
			my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
			$year=$year+1900-18;
			if(($q->param('anno'))>$year) {
				$problems{ERR_ANNO}="Possono registrarsi solo utenti maggiorenni";
				$problems{empty}="no";
			}
			else {
				$old_input{ANNO}=$q->param('anno');
			}
		} 
		
		$Modifica{AnnoNascita}=$q->param('anno');
	}

	if($q->param('password') ne '') {
		if (length($q->param('password'))<8 or length($q->param('password')>16)){
			$problems{PASSWORD_ERR} = "La password dev essere compresa fra 8 e 16 caratteri";
			$problems{empty}="no";
		}		
		elsif(!($q->param('password')=~m/^[A-Za-z0-9_\.-]{8,16}$/)) {
			$problems{PASSWORD_ERR} = "Password non valida, sono permesse lettere maiuscole o minuscole, e i caratteri underscore, hyphen o punto";
			$problems{empty}="no";
		}
		elsif($q->param('password') ne $q->param('conferma')) {
				$problems{CONFERMA_ERR} = "Password non coincidenti";
				$problems{empty}="no";
		}
		else {
			$old_input{PASSWORD}=$q->param('password');
		}

		$Modifica{Password}=$q->param('password');
	}

	if($q->param('descrizioneForm') ne '') {
		my $mess = $q->param('descrizioneForm');
		$mess =encode_entities($mess,'>');
		$mess = encode_entities($mess, '<');
		$old_input{DESCRIZIONEFORM}=$q->param('descrizioneForm');
		$Modifica{DescrizionePers}=$q->param('descrizioneForm');
	}


		if($q->param('annoPatente') ne '' or $q->param('auto') ne '' or $q->param('chiacchiere') ne '' or $q->param('musica') ne '' or $q->param('animali') ne '' or $q->param('fumatori') ne '') {
			if($q->param('annoPatente') eq '' or $q->param('auto') eq '' or $q->param('chiacchiere') eq '' or $q->param('musica') eq '' or $q->param('animali') eq '' or $q->param('fumatori') eq '') {
				$problems{ERR_INFO_CONDUCENTE}="Le informazioni necessarie per offrire un passaggio devono essere tutte presenti, o nessuna";
				$problems{empty}="no";
			}
			elsif(!($q->param('annoPatente')=~m/^[1-2][0-9][0-9][0-9]$/)) {
				$problems{ERR_ANNOPATENTE}="Anno di rilascio della patente non valido, inserire l anno in formato 'aaaa'";
				$problems{empty}="no";
			}
				else {
					$old_input{ANNOPATENTE}=$q->param('annoPatente');
				}

			if(!($q->param('auto')=~m/^[a-z0-9A-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.-]+$/)) {
				$problems{ERR_AUTO}="Auto non valida, inserire solo lettere o numeri";
				$problems{empty}="no";
			}
			else {
				$old_input{AUTO}=$q->param('auto');
			}
			$Modifica{Patente}=$q->param('annoPatente');
			$Modifica{Auto}=$q->param('auto');
			$Modifica{Chiacchere}=$q->param('chiacchiere');
			$Modifica{Musica}=$q->param('musica');
			$Modifica{Animali}=$q->param('animali');
			$Modifica{Fumatore}=$q->param('fumatori');
		}

	my $chiacc = "CHECKED_C".$q->param('chiacchiere');
	my $mus = "CHECKED_M".$q->param('musica');
	my $anim = "CHECKED_A".$q->param('animali');
	my $fum = "CHECKED_F".$q->param('fumatori');

	$old_input{$chiacc} = "checked='checked'";
	$old_input{$mus} = "checked='checked'";
	$old_input{anim} = "checked='checked'";
	$old_input{fum} = "checked='checked'";

	if($problems{'empty'} eq "no") {
		$session->param('problems',\%problems);
		$session->param('old_input',\%old_input);
		print $session->header(-location => "modificaProfilo.cgi");
	}
	elsif(data_registration::inserisci_modifica_profilo(\%Modifica)) {
		print $session->header(-location => "profilo.cgi?utente=$username");
	}
}



