#! /usr/bin/perl -w
#print "Content-type: text/html\n\n";

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
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
        my %Feedback;
        $Feedback{IDMitt} = $session->param('username');
        $Feedback{IDDest} = $q->param('G');
        $Feedback{Passaggio} = $q->param('passaggio');
        $Feedback{Compagnia} = $q->param('_CompagniaG');
        $Feedback{Puntualita} = $q->param('_PuntualitaG');
        $Feedback{Guida} = $q->param('_Guida');
        $Feedback{Pulizia} = $q->param('_Pulizia');
        
        if($q->param('_commentoG') ne "Commento facoltativo" && $q->param('_commentoG') ne "") {
            my $comm = encode_entities($q->param('_commentoG'),'<>&"\'');
            $Feedback{Commento} = $comm;
        }
        my $punt_medio=($q->param('_CompagniaG') + $q->param('_PuntualitaG') + $q->param('_Guida') + $q->param('_Pulizia'))/4;
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
             my %Feedback;
            $Feedback{IDMitt} = $session->param('username');
            $Feedback{IDDest} = $q->param('P'.$i);
            $Feedback{Passaggio} = $q->param('passaggio');
            $Feedback{Compagnia} = $q->param('_CompagniaP'.$i);
            $Feedback{Puntualita} = $q->param('_PuntualitaP'.$i);
    
            if($q->param('_commentoP'.$i) ne "Commento facoltativo" && $q->param('_commentoP'.$i) ne "") {
                my $comm = encode_entities($q->param('_commentoP'.$i),'<>&"\'');
                $Feedback{Commento} = $comm;
            }
            my $punt_medio=($q->param('_CompagniaP'.$i) + $q->param('_PuntualitaP'.$i))/2;
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
