#!/usr/bin/env perl
use strict;
use warnings;

use FindBin qw($Bin);
use lib ($Bin,"$Bin/lib");
use readtsv;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";

my @colnames;
my @filenames;
my $robust;
foreach my $arg (@ARGV) { 
    if($arg =~ m/^-r$/) {
        $robust = 1;
    } elsif($arg =~ m/\.(csv|tsv|txt)$/) {
        push @filenames, $arg;
    } else {
        push @colnames, $arg;
    }
}
if (@filenames == 0) { push @filenames, "-"; }

foreach my $fn (@filenames) { 
    print "READ: $fn\n";
    my $in = new readtsv($fn,map { $_, $_ } @colnames);
    $in->{robust} = $robust;
    while( my $row = $in->getln() ) {
        print join("\t",map $row->{$_},@colnames),"\n";
    }
}
