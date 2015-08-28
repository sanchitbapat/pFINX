# pFINX
A reverse proxy that also performs input sanitization
Nginx acts as a reverse proxy to filter the incoming traffic and send it to an underlying python script.
A python script performs input sanitization on the request and forwards it to the intended server. The script redirects the reply to the nginx proxy which in turn redirects it to the end user.
