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



if(defined($q->param('CompagniaG'))) {
	my %Feedback= (
		IDMitt => $q->param('Mittente'),
		IDDest => $q->param('G'),
		Passaggio => $q->param('Passaggio'),
		Compagnia => $q->param('CompagniaG'),
		Puntualita => $q->param('PuntualitaG'),
		Guida => $q->param('Guida'),
		Pulizia => $q->param('Pulizia'),
		Commento => $q->param('commentoG')
	);
	my $punt_medio=($q->param('CompagniaG') + $q->param('PuntualitaG') + $q->param('Guida') + $q->param('Pulizia'))/4;
	$Feedback{PunteggioMedio}=$punt_medio;

	if(data_registration::inserisci_feedback(\%Feedback)) {
		# AGGIORNA PUNTEGGIO UTENTE DESTINATARIO
		data_registration::elimina_notifica("$Feedback{'IDMitt'}","FeedDaRilasciare","\@Destinatario=\"$Feedback{'IDDest'}\" and \@Passaggio=\"$Feedback{'Passaggio'}\"");
	}
}


my %aux = data_registration::serializzazione_apertura();
my $doc = $aux{'doc'};
my $fileHandle = $aux{'filehandle'};
my $m=$q->param('Mittente');
my $p=$q->param('Passaggio');
my @feed_da_rilas=$doc->findnodes("//SetUtenti/Utente[Username=\"$m\"]/Notifiche/FeedDaRilasciare[\@Passaggio=\"$p\"]");
my $num_da_rilasc=@feed_da_rilas;
data_registration::serializzazione_chiusura($fileHandle,$doc);

for(my $i=1;$i<=$num_da_rilasc;$i++) {
	my %Feedback= (
		IDMitt => $q->param('Mittente'),
		IDDest => $q->param('P'.$i),
		Passaggio => $q->param('Passaggio'),
		Compagnia => $q->param('CompagniaP'.$i),
		Puntualita => $q->param('PuntualitaP'.$i),
		Commento => $q->param('commentoP'.$i)
	);
	my $punt_medio=($q->param('CompagniaP'.$i) + $q->param('PuntualitaP'.$i))/2;
	$Feedback{PunteggioMedio}=$punt_medio;
	if(data_registration::inserisci_feedback(\%Feedback)) {
		# AGGIORNA PUNTEGGIO UTENTE DESTINATARIO
		data_registration::elimina_notifica("$Feedback{'IDMitt'}","FeedDaRilasciare","\@Destinatario=\"$Feedback{'IDDest'}\" and \@Passaggio=\"$Feedback{'Passaggio'}\"",$doc);
	}
}	

