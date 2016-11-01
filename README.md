Checks for common known magic bytes in the first 1024 bytes of a file. Magic
bytes are kept in python list in signatures.py for easy editing. Algorithm
converts this to a trie at runtime so that the program can scale to large
signature lists!

To avoid noise, doesn't print one-byte headers by default. To get this
functionality use option --short_headers or -sh

Functionality:
python shibboleth.py [-sh | --short_headers] file

Have fun :)
