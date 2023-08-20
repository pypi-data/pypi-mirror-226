from setuptools import setup
from setuptools.extension import Extension

def main():
    setup(name="cwhois",
          version="1.0.2",
          description="Python interface for executing rfc1036 whois",
          author="Mariusz Krzyzok, Marco d'Itri",
          url="http://github.com/damemay/cwhois/",
          license="GPL-2.0",
          ext_modules=[Extension(
              "cwhois",
              sources=['utils.c', 'whois.c'],
              )],
          # packages=["cwhois"],
          keywords=["whois", "tld", "domain", "registrar",],
          python_requires=">=3.5",
          platforms="All")

if __name__ == "__main__":
    main()
