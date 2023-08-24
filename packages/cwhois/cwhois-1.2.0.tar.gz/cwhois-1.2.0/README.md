rfc1036's (Marco d'Itri) Intelligent WHOIS client fork extended in C for parsing and Python usage.

# python usage

```python
import cwhois

print(cwhois.query('example.com'))
```

## install

`python -m pip install cwhois`

# c usage

```c
#include "whois.h"

int main(int argc, char** argv)
{
    if(argc > 1) {
        // Queries WHOIS and saves output to C-string
        char* q = query_whois(argv[1]);
        puts(q);

        // Parse output into simple struct
        domain* d = parse_whois(q);

        if(d->created)          printf("Created: %s\n", d->created);
        if(d->expires)          printf("Expires: %s\n", d->expires);
        if(d->updated)          printf("Updated: %s\n", d->updated);
        if(d->status)           printf("Status: %s\n", d->status);
        if(d->registrar)        printf("Registrar: %s\n", d->registrar);

        // Free all resources
        domain_free(d);
        free(q);
    } else {
        printf("usage: %s <domain>\n", argv[0]);
    }

    return 0;
}
```
