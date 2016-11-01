# Intro
Checks for common known magic bytes in the first 1024 bytes of a file. Magic
bytes are kept in python list in signatures.py for easy editing. Algorithm
converts this to a trie at runtime so that the program can scale to large
signature lists!

To avoid noise, this doesn't print one-byte headers by default. To get this
functionality use option --short_headers or -sh

# Usage
python shibboleth.py [-sh | --short_headers] file

# On the Name
This script was inspired by Ange Albertini's abuse of file formats. I decided
that I wanted a little utility to scan for common magic bytes at the beginning
of a file. Albertini's Corkami project often generates "polyglot files" -- files
which can be said to speak more than one language since they are valid files for
more than one file type specification.

The word shibboleth is an ancient, hard to pronounce word that tribes would use
to determine if a person was a member of the tribe. The theory was that people
who weren't native to that tribe's language (hebrew) would mispronounce
shibboleth and give away their foreign background.

Similarly, this program can be used to identify polyglot files -- files which
appear to be one file, but are actually another. It's not a perfect metaphor,
but I wrote this after midnight, give me a break.

Have fun :)
