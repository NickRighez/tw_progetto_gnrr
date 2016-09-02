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
use lib "../libreria";
use sessione;
use lib "../libreria";
use date_time;
use XML::LibXML;
use Scalar::Util;

my $parser =  XML::LibXML->new();
my $q=new CGI;

my @s = sessione::creaSessione();  
 my $session = $s[0];
my %problems = ( empty => 'yes' );
my %old_input;

my %Passaggio;

if(!defined($session->param('username'))) {
  my %problems=(
     not_logged => "Utente non loggato, pagina inaccessibile"
     );
  $session->param('problems',\%problems);
  print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/accedi.cgi");
} 

my $username = $session->param('username');

if($q->param('partenza') eq "") {
	$problems{ERR_PARTENZA} = "Luogo di partenza mancante";
	$problems{empty} = 'no';
}
elsif (!($q->param('partenza')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð,-.\s]+$/)) {
	$problems{ERR_PARTENZA} = "Luogo di partenza non valido, inserire lettere o i caratteri: ',' '-' '.'";
	$problems{empty} = 'no';
}
else {
	$old_input{PARTENZA} = $q->param('partenza');
}


if($q->param('arrivo') eq "") {
	$problems{ERR_ARRIVO} = "Luogo di arrivo mancante";
	$problems{empty} = 'no';
}
elsif (!($q->param('arrivo')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð,-.\s]+$/)) {
	$problems{ERR_ARRIVO} = "Luogo di arrivo non valido, inserire lettere o i caratteri: ',' '-' '.'";
	$problems{empty} = 'no';
}
else {
	$old_input{ARRIVO} = $q->param('arrivo');
}

if($q->param('tappa1') ne "" and !($q->param('tappa1')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð,-.\s]+$/)) {
	$problems{ERR_TAPPA1} = "Luogo della tappa 1 non valido, inserire lettere o i caratteri: ',' '-' '.'";
	$problems{empty} = 'no';
}
else {
	$old_input{TAPPA1} = $q->param('tappa1');
} 

if($q->param('tappa2') ne "" and !($q->param('tappa2')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð,-.\s]+$/)) {
	$problems{ERR_TAPPA2} = "Luogo della tappa 2 non valido, inserire lettere o i caratteri: ',' '-' '.'";
	$problems{empty} = 'no';
} 
else {
	$old_input{TAPPA2} = $q->param('tappa2');
} 

if($q->param('tappa3') ne "" and !($q->param('tappa3')=~m/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð,-.\s]+$/)) {
	$problems{ERR_TAPPA3} = "Luogo della tappa 3 non valido, inserire lettere o i caratteri: ',' '-' '.'";
	$problems{empty} = 'no';
} 
else {
	$old_input{TAPPA3} = $q->param('tappa3');
} 

if($q->param('tappa3') ne "" ) {
	if($q->param('tappa2') eq "" ) {
		$problems{ERR_TAPPA2} = "Per inserire la terza tappa, è necessario inserire le tappe precedenti";
		$problems{empty} = 'no';
	}
	if($q->param('tappa1') eq "" ) {
		$problems{ERR_TAPPA1} = "Per inserire la terza tappa, è necessario inserire le tappe precedenti";
		$problems{empty} = 'no';
	}
}

if($q->param('tappa2') ne "" ) {
	if($q->param('tappa1') eq "" ) {
		$problems{ERR_TAPPA1} = "Per inserire la seconda tappa, è necessario inserire la tappa precedente";
		$problems{empty} = 'no';
	}
}

my ($sec,$min,$hour,$mday, $mon, $year ,$wday,$yday,$isdst) = localtime();
$year = $year + 1900;
my @dataP = split /-/, $q->param('dataP');
my @oraP = split /:/, $q->param('oraP');
my @dataA = split /-/, $q->param('dataA');
my @oraA = split /:/, $q->param('oraA');

if($q->param('dataP') eq "") {
	$problems{dataP_err} = "Data di partenza mancante";
	$problems{empty} = 'no';
}
elsif (!($q->param('dataP')=~m/^[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}$/)) { # aggiungere condizione date_time::valida_data
	$problems{dataP_err} = "Data di partenza non valida. Inserire una data in formato gg-mm-aaaa oppure g-m-aaaa";
	$problems{empty} = 'no';
}
else {
	$old_input{DATA_P} = $q->param('dataP');
}

if($q->param('oraP') eq "") {
	$problems{ERR_ORA_P} = "Ora di partenza mancante";
	$problems{empty} = 'no';
}
elsif (!($q->param('oraP')=~m/^(([0-1][0-9])|([2][0-3])):[0-5][0-9]$/)) {
	$problems{ERR_ORA_P} = "Ora di partenza non valida. Inserire un ora in formato hh:mm";
	$problems{empty} = 'no';
}
else {
	$old_input{ORA_P} = $q->param('oraP');
}

if(!defined($problems{'dataP_err'}) and !defined($problems{'ERR_ORA_P'}) ) { # controllo che la data di partenza sia futura
	#my @dataP = split /-/, $q->param('dataP');
	#my @oraP = split /:/, $q->param('oraP');
	# $oraP[0] - 1 => questo permette di obbligare l utente a inserire un passaggio $mon = $mon +1;che inizi almeno tra un ora, non prima 
	if(date_time::confronto_dataora($mday, $mon, $year, $hour, $min, $dataP[0], $dataP[1]-1, $dataP[2], $oraP[0]-1, $oraP[1])) {
		# la data di partenza è (correttamente) futura, quindi di passa a controllare la data di arrivo
		if($q->param('dataA') eq "") {
			$problems{dataA_err} = "Data di arrivo mancante";
			$problems{empty} = 'no';
		}
		elsif (!($q->param('dataA')=~m/^[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}$/)) { # aggiungere condizione date_time::valida_data
			$problems{dataA_err} = "Data di arrivo non valida. Inserire una data in formato gg-mm-aaaa oppure g-m-aaaa";
			$problems{empty} = 'no';
		}
		else {
			$old_input{DATA_A} = $q->param('dataA');
		}
		
		if($q->param('oraA') eq "") {
			$problems{ERR_ORA_A} = "Ora di arrivo mancante";
			$problems{empty} = 'no';
		}
		elsif (!($q->param('oraP')=~m/^(([0-1][0-9])|([2][0-3])):[0-5][0-9]$/)) {
			$problems{ERR_ORA_A} = "Ora di arrivo non valida. Inserire un ora in formato hh:mm";
			$problems{empty} = 'no';
		}
		else {
			$old_input{ORA_A} = $q->param('oraA');
		} 

		if(!defined($problems{'dataA_err'}) and !defined($problems{'ERR_ORA_A'}) ) { # le date sono corrette. Ora si controlla che l arrivo sia successivo alla partenza
			if(!(date_time::confronto_dataora($dataP[0], $dataP[1]-1, $dataP[2], $oraP[0], $oraP[1], $dataA[0], $dataA[1]-1, $dataA[2], $oraA[0], $oraA[1]))) {
				$old_input{DATA_A} = "";
				$old_input{ORA_A} =  "";
				$problems{dataA_err} = "la data/ora di partenza dev essere successiva alla data/ora d arrivo";
				$problems{ERR_ORA_A} = "la data/ora di partenza dev essere successiva alla data/ora d arrivo";
				$problems{empty} = 'no';				
			}			
		}
	}
	else { # ramo in cui la data di partenza è corretta, ma non è futura
		$problems{dataP_err} = "la data/ora di partenza dev essere almeno di un ora nel futuro";
		$problems{ERR_ORA_P} = "la data/ora di partenza dev essere almeno di un ora nel futuro";
		$problems{empty} = 'no';
	}
}

if($q->param('prezzo') eq "") {
	$problems{ERR_PREZZO} = "Prezzo mancante";
	$problems{empty} = 'no';
}
else {
	my $prezzo = $q->param('prezzo');
	$prezzo =~ tr/,/./;
	if(Scalar::Util::looks_like_number($prezzo) and $prezzo>0) {
		$old_input{PREZZO} = $prezzo;
	}	
	else {
		$problems{ERR_PREZZO} = "Prezzo non valido. Inserire un prezzo positivo valido";
		$problems{empty} = 'no';
	} 
}

if($q->param('posti') eq "") {
	$problems{ERR_POSTI} = "Posti disponibili mancante";
	$problems{empty} = 'no';
}
elsif (!($q->param('posti')=~m/^[0-9]{1,2}$/)) {
	$problems{ERR_POSTI} = "Numero di posti disponibili non valido, inserire un valore intero positivo minore di 99";
	$problems{empty} = 'no';
}
else {
	$old_input{POSTI} = $q->param('posti');
}

$old_input{descrizioneViaggio}= $q->param('descrizioneViaggio');  # code injection

if($q->param('bagagli') eq "piccolo") {
	$old_input{BAGAGLIP} = "selected=\"selected\"";
}
if($q->param('bagagli') eq "medio") {
	$old_input{BAGAGLIM} = "selected=\"selected\"";
}
if($q->param('bagagli') eq "grande") {
	$old_input{BAGAGLIG} = "selected=\"selected\"";
}
###############################################################################
if($problems{'empty'} eq "no") {
	$session->param('problems',\%problems);
	$session->param('old_input',\%old_input);
	print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_offerta_passaggio.cgi");
}
else {
	if (length($dataP[1])  == 1) {$dataP[1] = "0$dataP[1]";}
	if (length($dataP[0]) == 1) {$dataP[0] = "0$dataP[0]";}
	if (length($dataA[1])  == 1) {$dataA[1] = "0$dataA[1]";}
	if (length($dataA[0]) == 1) {$dataA[0] = "0$dataA[0]";}
	
	my %Partenza = (
	Luogo => $q->param('partenza'),
	Data => $dataP[2]."-".$dataP[1]."-".$dataP[0],
	Ora => $q->param('oraP').":00",
	PostiDisp => $q->param('posti')
	);
	my %Arrivo = (
		Luogo => $q->param('arrivo'),
		Data => $dataA[2]."-".$dataA[1]."-".$dataA[0],
		Ora => $q->param('oraA').":00",
		PostiDisp => $q->param('posti')
	);

	if($q->param('descrizioneViaggio') ne "") {
		$Passaggio{Dettagli}=$q->param('descrizioneViaggio');
	}
	$Passaggio{PrezzoTot} = $q->param('prezzo');
	$Passaggio{PostiDisp} = $q->param('posti');
	$Passaggio{Conducente} = $username;
	$Passaggio{Partenza} = \%Partenza;
	$Passaggio{Arrivo} = \%Arrivo;

	my @data_ora_tappe;
	#my @dataP = split /-/, $q->param('dataP');
	#my @oraP = split /:/, $q->param('oraP');
	#my @dataA = split /-/, $q->param('dataA');
	#my @oraA = split /:/, $q->param('oraA');

	if($q->param('tappa3') ne "") {
		 @data_ora_tappe = date_time::calcola_tappe($dataP[0], $dataP[1], $dataP[2], $oraP[0], $oraP[1], $dataA[0], $dataA[1], $dataA[2], $oraA[0], $oraA[1],5);
		 my @data_ora_tappa1 = split / /,$data_ora_tappe[1];
		 my @data_ora_tappa2 = split / /,$data_ora_tappe[2];
		 my @data_ora_tappa3 = split / /,$data_ora_tappe[3];
		 my %Tappa1 = (
		 	Luogo => $q->param('tappa1'),
			Data => $data_ora_tappa1[0],
			Ora => $data_ora_tappa1[1],
			PostiDisp => $q->param('posti')
		 );
		 my %Tappa2 = (
		 	Luogo => $q->param('tappa2'),
			Data => $data_ora_tappa2[0],
			Ora => $data_ora_tappa2[1],
			PostiDisp => $q->param('posti')
		 );
		 my %Tappa3 = (
		 	Luogo => $q->param('tappa3'),
			Data => $data_ora_tappa3[0],
			Ora => $data_ora_tappa3[1],
			PostiDisp => $q->param('posti')
		 );
		 $Passaggio{Tappa1} = \%Tappa1;
		 $Passaggio{Tappa2} = \%Tappa2;
		 $Passaggio{Tappa3} = \%Tappa3;
	}
	elsif ($q->param('tappa2') ne "") {
		@data_ora_tappe = date_time::calcola_tappe($dataP[0], $dataP[1], $dataP[2], $oraP[0], $oraP[1], $dataA[0], $dataA[1], $dataA[2], $oraA[0], $oraA[1],4);
		 my @data_ora_tappa1 = split / /,$data_ora_tappe[1];
		 my @data_ora_tappa2 = split / /,$data_ora_tappe[2];
		 my %Tappa1 = (
		 	Luogo => $q->param('tappa1'),
			Data => $data_ora_tappa1[0],
			Ora => $data_ora_tappa1[1],
			PostiDisp => $q->param('posti')
		 );
		 my %Tappa2 = (
		 	Luogo => $q->param('tappa2'),
			Data => $data_ora_tappa2[0],
			Ora => $data_ora_tappa2[1],
			PostiDisp => $q->param('posti')
		 );
		 $Passaggio{Tappa1} = \%Tappa1;
		 $Passaggio{Tappa2} = \%Tappa2;
	}
	elsif ($q->param('tappa1') ne "") {
		@data_ora_tappe = date_time::calcola_tappe($dataP[0], $dataP[1], $dataP[2], $oraP[0], $oraP[1], $dataA[0], $dataA[1], $dataA[2], $oraA[0], $oraA[1],3);
		 my @data_ora_tappa1 = split / /,$data_ora_tappe[1];
		 my %Tappa1 = (
		 	Luogo => $q->param('tappa1'),
			Data => $data_ora_tappa1[0],
			Ora => $data_ora_tappa1[1],
			PostiDisp => $q->param('posti')
		 );
		 $Passaggio{Tappa1} = \%Tappa1;
	}



	if(data_registration::inserisci_nuovo_viaggio(\%Passaggio)) {
		data_registration::incrementa("NumPassaggiOff", $username);
		print $q->redirect("http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_profilo.cgi?utente=$username");
	}
}


