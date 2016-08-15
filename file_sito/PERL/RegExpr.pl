#!/usr/bin/perl
use strict;
use warnings;
use diagnostics;

print "Content-type: text/html\n\n";
print "<html><head></head><body>";

	my $x="Piovì di salò";
	my $d="nnnnnnn";
	my $t="pepe\@iy.ij";

	if($x=~m/^[A-Za-z][a-zàèòùì]+(\s[a-zàèòùì]+)*$/) { print "<h2>YES</h2>"; }
	else { print "<h2>NO</h2>"; }

	if($d =~ m/^[A-Za-z0-9_-]{3,15}$/) { print "<h2>YES</h2>"; }
	else { print "<h2>NO</h2>"; }

	if($t =~ m/^([a-z0-9_\.-]+)@([a-z]+)\.([a-z]{2,6})$/) { print "<h2>YES</h2>"; }
	else { print "<h2>NO</h2>"; }
print "</body></html>";

