#!/usr/bin/env perl
while(my $ln = <STDIN>) {
  @cols = split /\t/, $ln;
  $cols[-1] =~ s/\s+$//gs;
  $cols[0] =~ s/^#//
    if $. == 1;
  print("|".join("|",@cols)."|\n");
  print("|".join("|",map "---",@cols)."|\n")
    if $. == 1;
}
