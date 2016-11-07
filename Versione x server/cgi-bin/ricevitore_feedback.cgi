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
#use lib "../libreria";
use libreria::sessione;
use XML::LibXML;
use HTML::Entities;
my $parser =  XML::LibXML->new();
my $q=new CGI;

my @s = sessione::creaSessione();
my $session = $s[0];

if($q->request_method() ne 'POST') {
    my %problems=(
          DESCRIZIONE_ERRORE => "Tentativo di inserire un feedback con una modalit&agrave; non permessa."
        );
        $session->param('problems',\%problems);
        print $session->header(-location => "home.cgi");
}
else {
    my $username = $session->param('username');
    if(defined($q->param('G'))) {
        my %Feedback= (
            IDMitt => $session->param('username'),
            IDDest => $q->param('G'),
            Passaggio => $q->param('passaggio'),
            Compagnia => $q->param('CompagniaG'),
            Puntualita => $q->param('PuntualitaG'),
            Guida => $q->param('Guida'),
            Pulizia => $q->param('Pulizia')
        );
        if($q->param('commentoG') ne "Commento facoltativo" && $q->param('commentoG') ne "") {
            $Feedback{'Commento'} = encode_entities($q->param('commentoG'));
        }
        my $punt_medio=($q->param('CompagniaG') + $q->param('PuntualitaG') + $q->param('Guida') + $q->param('Pulizia'))/4;
        $Feedback{PunteggioMedio}=$punt_medio;
        if(data_registration::inserisci_feedback(\%Feedback)) {
            data_registration::incrementa("NumFeedbRicevuti", $q->param('G'));
            data_registration::elimina_notifica("$Feedback{'IDMitt'}","FeedDaRilasciare","\@Destinatario=\"$Feedback{'IDDest'}\" and \@Passaggio=\"$Feedback{'Passaggio'}\"");
            data_registration::aggiorna_valutazione_utente(\%Feedback, $q->param('G'));

            my %nota = ( nota => "Passaggio recensito con successo!" );
            $session->param('nota',\%nota);
        }
    }

    my $doc = data_registration::get_xml_doc();
    my $username=$session->param('username');
    my $p=$q->param('passaggio');
    my @feed_da_rilas=$doc->findnodes("//SetUtenti/Utente[Username=\"$username\"]/Notifiche/FeedDaRilasciare[\@Passaggio=\"$p\"]");
    my $num_da_rilasc=@feed_da_rilas;
    for(my $i=1;$i<=$num_da_rilasc;$i++) {
        if(defined($q->param('P'.$i))) {
            my %Feedback= (
                IDMitt => $session->param('username'),
                IDDest => $q->param('P'.$i),
                Passaggio => $q->param('passaggio'),
                Compagnia => $q->param('CompagniaP'.$i),
                Puntualita => $q->param('PuntualitaP'.$i),
                Commento => $q->param('commentoP'.$i)
            );
            if($q->param('commentoP'.$i) ne "Commento facoltativo" && $q->param('commentoP'.$i) ne "") {
                $Feedback{'Commento'} = encode_entities($q->param('commentoG'));
            }
            my $punt_medio=($q->param('CompagniaP'.$i) + $q->param('PuntualitaP'.$i))/2;
            $Feedback{PunteggioMedio}=$punt_medio;

            if(data_registration::inserisci_feedback(\%Feedback)) {
                data_registration::incrementa("NumFeedbRicevuti", $q->param('P'.$i));
                data_registration::aggiorna_valutazione_utente(\%Feedback, $q->param('P'.$i));
                data_registration::elimina_notifica("$Feedback{'IDMitt'}","FeedDaRilasciare","\@Destinatario=\"$Feedback{'IDDest'}\" and \@Passaggio=\"$Feedback{'Passaggio'}\"",$doc);
            
                my %nota = ( nota => "Passaggio recensito con successo!" );
                $session->param('nota',\%nota);
            }
        }
    }
    print $session->header(-location => "notifiche.cgi");

}
