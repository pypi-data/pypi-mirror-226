from setuptools import setup
from setuptools.extension import Extension

def main():
    setup(name="cwhois",
          version="1.0.4",
          description="rfc1036's (Marco d'Itri) Intelligent WHOIS client fork extended for Python usage.",
          author="Mariusz Krzyzok, Marco d'Itri",
          url="http://github.com/damemay/cwhois/",
          license="GPL-2.0",
          ext_modules=[Extension(
              "cwhois",
              sources=['utils.c', 'whois.c'],
              )],
          keywords=["whois", "tld", "domain", "registrar",],
          python_requires=">=3.5",
          platforms="All")

if __name__ == "__main__":
    main()
