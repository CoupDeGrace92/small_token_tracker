Designed to track token usage for Google's Gemeni and their API.  It tracks and stores the token data in the log file specified by the global log 
file variable at the top of the file.  Not a complex utility but easily importable for any utility that is going to be consuming tokens to place
internal guardrails on programs calling AI APIs (in this case Google's).  For other API's, you will potentially have to adjust depending on how
they track token usage.
