#! /usr/bin/perl -w
use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use Template;
use libreria::sessione;
use libreria::research;
use libreria::data_registration;
use libreria::date_time;
use utf8;
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";

my $q = new CGI;
my @s = sessione::creaSessione();
my $session = $s[0];

if(!defined($session->param('ricerca'))) {
     my %problems=(
      DESCRIZIONE_ERRORE => "Tentativo di visualizzare i risultati di una ricerca con una modalit&agrave; non permessa."
      );
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
else {
    my $ricerca_ref = $session->param('ricerca');
    my %ricerca = %$ricerca_ref;
    my $partenza=$ricerca{'partenza'};
    my $arrivo=$ricerca{'arrivo'};
    my $data=$ricerca{'data'};
    my $doc = data_registration::get_xml_doc();
    $session->clear(['ricerca']);
    my @viaggi_list = research::query_ricerca($partenza, $arrivo, $data, $doc);
    my $empty = "false";
    my $num_viaggi = @viaggi_list;
    if($num_viaggi == 0){
        $empty = "true";
    }
   # my %hash_keys;

    my %hash_keys = (
        VIAGGI_LIST => \@viaggi_list,
        EMPTY_LIST => $empty,
        PARTENZA => ucfirst  $partenza,
        ARRIVO => ucfirst $arrivo,
        DATA => date_time::formatta_data($data)
    );

    ##################!!!!!!!!!!!!!!!!!!!!!!!

    if(defined($session->param('username'))) {
        $hash_keys{LOGGEDIN} = 'yes';
        $hash_keys{NOME_UTENTE} = $session->param('username');
        $hash_keys{NUM_NOTIFICHE} = research::conta_notifiche($session->param('username'), $doc);
        $hash_keys{INDEX} = 9;
    }
    else {
        $hash_keys{LOGGEDIN} = 'no';
        $hash_keys{INDEX} = 6;
    }

    my $file = "../data/HTML_TEMPLATE/risultati.html";
    my $template_parser = Template->new({ ENCODING => 'utf8' });
    open my $fh, '<:encoding(UTF-8)', $file;
    my $foglio = '';
    $template_parser->process($fh,\%hash_keys,\$foglio);
	print "Content-Type: text/html; charset=UTF-8\n\n\n";
    print $foglio;
}
