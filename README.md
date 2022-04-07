# ASEW
## ASEW is a Simple Exploitable Web Application
Built to test and explot SQL Injection, Credential Stuffing and XSS vulnerabilities.
ASEW also has a mitigated version (run app_fixed.py) that prevents SQLi and XSS.

## To Run - 
1. If running for the first time, directly run.
2. If you wish to reset the application, delete both database files.
3. run python app.py
4. An example passwords file can be downloaded from [here](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/500-worst-passwords.txt). Warning: may contain explicit words.

### Precaution
While running Intruder code for testing XSS, the index page may get populated with lot of posts and javascript.
It is advised to clear databases after the attack.
