#! /usr/bin/perl -w
#print "Content-Type: text/html; charset=UTF-8\n\n";

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use libreria::data_registration;
use libreria::sessione;
use XML::LibXML;
use HTML::Entities;
use Encode qw(decode_utf8);

use utf8;
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";

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
    if(defined( decode_utf8 $q->param('G'))) {
        my %Feedback;
        $Feedback{IDMitt} = $session->param('username');
        $Feedback{IDDest} =  decode_utf8 $q->param('G');
        $Feedback{Passaggio} =  decode_utf8 $q->param('passaggio');
        $Feedback{Compagnia} =  decode_utf8 $q->param('_CompagniaG');
        $Feedback{Puntualita} =  decode_utf8 $q->param('_PuntualitaG');
        $Feedback{Guida} =  decode_utf8 $q->param('_Guida');
        $Feedback{Pulizia} =  decode_utf8 $q->param('_Pulizia');
        
        if( decode_utf8 $q->param('_commentoG') ne "Commento facoltativo" &&  decode_utf8 $q->param('_commentoG') ne "") {
            my $comm = encode_entities( decode_utf8 $q->param('_commentoG'),'<>&"\'');
            $Feedback{Commento} = $comm;
        }
        my $punt_medio=( decode_utf8 $q->param('_CompagniaG') +  decode_utf8 $q->param('_PuntualitaG') +  decode_utf8 $q->param('_Guida') +  decode_utf8 $q->param('_Pulizia'))/4;
        $Feedback{PunteggioMedio}=$punt_medio;

        if(data_registration::inserisci_feedback(\%Feedback)) {
            data_registration::incrementa("NumFeedbRicevuti",  decode_utf8 $q->param('G'));
            data_registration::elimina_notifica("$Feedback{'IDMitt'}","FeedDaRilasciare","\@Destinatario=\"$Feedback{'IDDest'}\" and \@Passaggio=\"$Feedback{'Passaggio'}\"");
            data_registration::aggiorna_valutazione_utente(\%Feedback,  decode_utf8 $q->param('G'));

            my %nota = ( nota => "Passaggio recensito con successo!" );
            $session->param('nota',\%nota);
        }
    }

    my $doc = data_registration::get_xml_doc();
    my $username=$session->param('username');
    my $p= decode_utf8 $q->param('passaggio');
    my @feed_da_rilas=$doc->findnodes("//SetUtenti/Utente[Username=\"$username\"]/Notifiche/FeedDaRilasciare[\@Passaggio=\"$p\"]");
    my $num_da_rilasc=@feed_da_rilas;
    for(my $i=1;$i<=$num_da_rilasc;$i++) {
        if(defined( decode_utf8 $q->param('P'.$i))) {
             my %Feedback;
            $Feedback{IDMitt} = $session->param('username');
            $Feedback{IDDest} =  decode_utf8 $q->param('P'.$i);
            $Feedback{Passaggio} =  decode_utf8 $q->param('passaggio');
            $Feedback{Compagnia} =  decode_utf8 $q->param('_CompagniaP'.$i);
            $Feedback{Puntualita} =  decode_utf8 $q->param('_PuntualitaP'.$i);
    
            if( decode_utf8 $q->param('_commentoP'.$i) ne "Commento facoltativo" &&  decode_utf8 $q->param('_commentoP'.$i) ne "") {
                my $comm = encode_entities( decode_utf8 $q->param('_commentoP'.$i),'<>&"\'');

                $Feedback{Commento} = $comm;
            }
            my $punt_medio=( decode_utf8 $q->param('_CompagniaP'.$i) +  decode_utf8 $q->param('_PuntualitaP'.$i))/2;
            $Feedback{PunteggioMedio}=$punt_medio;

            if(data_registration::inserisci_feedback(\%Feedback)) {
                data_registration::incrementa("NumFeedbRicevuti",  decode_utf8 $q->param('P'.$i));
                data_registration::aggiorna_valutazione_utente(\%Feedback,  decode_utf8 $q->param('P'.$i));
                data_registration::elimina_notifica("$Feedback{'IDMitt'}","FeedDaRilasciare","\@Destinatario=\"$Feedback{'IDDest'}\" and \@Passaggio=\"$Feedback{'Passaggio'}\"",$doc);
            
                my %nota = ( nota => "Passaggio recensito con successo!" );
                $session->param('nota',\%nota);
            }
        }
    }
    print $session->header(-location => "notifiche.cgi");

}
