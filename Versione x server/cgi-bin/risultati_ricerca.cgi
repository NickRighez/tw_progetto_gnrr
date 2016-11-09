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
binmode(STDOUT, ":utf8");
use utf8;

my $q = new CGI;
my @s = sessione::creaSessione();
my $session = $s[0];

if(!($q->param('partenza')=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/) ||
        !($q->param('arrivo')=~m/^(\x{0027}|\x{002C}|\x{002D}|\x{002F}|[\x{0041}-\x{005A}]|[\x{0061}-\x{007A}]|[\x{00C0}-\x{024F}]|\s)+$/) ||
        !($q->param('data')=~m/^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}$/) ){
    my %problems=(
      DESCRIZIONE_ERRORE => "I valori inseriti per la ricerca non sono validi."
      );
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
else {
    ############################################################################ valori appesi alla stringa URL
    my $partenza=$q->param('partenza');
    my $arrivo=$q->param('arrivo');
    my $data=$q->param('data');
    my $doc = data_registration::get_xml_doc();

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
	print "Content-Type: text/html\n\n\n";
    print $foglio;
}

