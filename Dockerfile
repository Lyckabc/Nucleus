FROM python:3.11-slim
WORKDIR /app
RUN pip install psycopg2-binary
ARG BUILD_DATE
ARG BUILD_VERSION
LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.version=$BUILD_VERSION
COPY setup_db.py .
CMD ["python", "setup_db.py"]