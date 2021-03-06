#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use Template;
use libreria::sessione;
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";
use utf8;


my $cgi = new CGI;
my @s = sessione::creaSessione();
my $session = $s[0];

if(defined($session->param('loggedin'))) {   
     my %problems=(
      DESCRIZIONE_ERRORE => "Tentativo di visualizzare una pagina per soli utenti non loggati."
      );
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
else {
    my %hash_keys;

    my %prob_hash;
    if(defined($session->param('problems'))) {
        my $prob = $session->param('problems');
        %prob_hash = %$prob;
        while( my( $key, $value ) = each %prob_hash ){
            $hash_keys{$key}="$value";
        }
    }

    my %old_hash;
    if(defined($session->param('old_input'))) {
        my $old = $session->param('old_input');
        %old_hash = %$old;
        while( my( $key, $value ) = each %old_hash ){
            $hash_keys{$key}="$value";
        }
    }



    my $file = "../data/HTML_TEMPLATE/accedi.html";
    open my $fh, '<:encoding(UTF-8)', $file;
    my $template_parser = Template->new({ ENCODING => 'utf8' });
    my $foglio = '';
    $template_parser->process($fh,\%hash_keys,\$foglio) or die $!;
    print "Content-Type: text/html; charset=UTF-8\n\n\n";
    close $fh;
    print $foglio;

    if(defined($session->param('problems'))) {
        $session->clear(['problems']);
    }
    if(defined($session->param('old_input'))) {
        $session->clear(['old_input']);
    }

}
