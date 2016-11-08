#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Carp qw(fatalsToBrowser);
use libreria::research;
use libreria::data_registration;
use CGI::Session;
use libreria::sessione;
use HTML::Entities;
binmode(STDOUT, ":utf8");
use utf8;

use Cwd;

my @s = sessione::creaSessione();
my $session = $s[0];
my $q=CGI->new;

if(defined($session->param('loggedin'))) {
    my %problems=(
        DESCRIZIONE_ERRORE => "Tentativo di visualizzare una pagina per soli utenti non loggati."
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
else {
     print "Content-Type: text/html\n\n\n";
    my %hash_keys;

    # 
    if(defined($session->param('problems'))) {
        my $prob = $session->param('problems');
        
        my %prob_hash = %$prob;
        while( my( $key, $value ) = each %prob_hash ){
            $hash_keys{$key}="$value";
        }
    }

    if(defined($session->param('old_input'))) {
        my $old = $session->param('old_input');
        my %old_hash = %$old;
        while( my( $key, $value ) = each %old_hash ){
            $hash_keys{$key}="$value";
        }
    }

    my $file = "../data/HTML_TEMPLATE/iscriviti.html";
    my $template_parser = Template->new({ ENCODING => 'utf8' });
    open my $fh, '<:encoding(UTF-8)', $file;
    my $foglio = '';
    $template_parser->process($fh,\%hash_keys,\$foglio) or die "Errore nella templatizzazione:  $!   ";
    print $foglio;

    if(defined($session->param('problems'))) {
        $session->clear(['problems']);
    }
    if(defined($session->param('old_input'))) {
        $session->clear(['old_input']);
    }
}
