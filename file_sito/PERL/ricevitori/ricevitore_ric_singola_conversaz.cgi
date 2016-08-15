#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use lib "../libreria";
use research;

my $q=CGI->new;

my %Conversaz=(
	UTENTE => 'u1',
	MYSELF => 'u2'
	);

research::query_conversazione(\%Conversaz); 
