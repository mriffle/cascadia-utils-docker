FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    pyteomics \
    numpy \
    lxml \
    pandas

# copy in scripts to be run
COPY create_fasta_from_ssl.py /usr/local/bin/
COPY fix_scan_numbers.py /usr/local/bin/

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
