#!/usr/bin/perl -w
print "\nEach array contains the following values: \n";

@arrayA = ( 1, 4, 9, 16, 25, 36 ); # List of Numbers
@arrayB = ( 1 .. 6); # Range of values
@arrayC = (13, 23,"Berlin", 34);# Mixed values
@arrayD = @arrayC;

print "ArrayA: @arrayA\n";
print "ArrayB: @arrayB\n";
print "ArrayC: @arrayC\n";
print "ArrayD: @arrayD\n";