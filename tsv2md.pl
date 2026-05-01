#!/usr/bin/env perl
use strict;
# one way to use this:
# pipe a tsv through it
# copy the output
# open in vscode
# hit ctrl-k then m, tell vscode it's markdown
# then ctrl-shift-v to see a formatted preview
# then you can paste that wherever
while(my $ln = <STDIN>) {
  @cols = split /\t/, $ln;
  $cols[-1] =~ s/\s+$//gs;
  $cols[0] =~ s/^#//
    if $. == 1;
  print("|".join("|",@cols)."|\n");
  print("|".join("|",map "---",@cols)."|\n")
    if $. == 1;
}
