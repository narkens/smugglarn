# Smugglarn
A simple project to discover path traversals from known paths in a web 
application. The common usecase is to discover when path parameters (not to be
confused with query params) are used in subsequent requests towards a backend
and path normalization occurs in between.

## Squibbly squib
With the default mode, smugglarn tries to query the same endpoint specified in
the path-list, using simple path traversals, i.e. if the path is /squibbly/squib
, smugglarn will try to access the endpoint using /squibbly/../squibbly/squib,
/squibbly/..%2fsquibbly/squib etc.

If a known backend endpoint is known, this can be specified using the -e flag,
for example -e /super/secret/path will instead of requesting the path in the
paths file look for URLs like /squibbly/squib/../../super/secret/path.

## Usage
´´´
-u <base_url>   : specify the base URL of the target
-p <paths_file> : specify the file in which you have your paths
-e <endpoint>   : super special endpoint you like to grab
-H <header>     : headers in curl-syntax
-x <proxy>      : proxy to use in curl syntax (buggy)
´´´
