# Check user environment variable
if [[ -z "${SERVICE_NAME}" ]]; then
  echo "Missing SERVICE_NAME environment variable" >&2
  exit 1
fi

# Use the `wait-for-it` script (https://github.com/vishnubob/wait-for-it) to
# test that the datastore-emulator is ready by testing against its host and
# port. Otherwise, if tests run before it's ready they will fail.
# wait-for-it datastore:8814 --strict --timeout=30 -- \
# wait-for-it pubsub:8171 --strict --timeout=30 -- \
# wait-for-it gcloud-tasks-emulator:8123 --strict --timeout=30 -- \

# call scripts.setup_local to setup necessary infrastructure based on your
# requirements, i.e., topic subscribers, message publishers, etc

python -m scripts.setup_local && \
gunicorn --log-level debug --bind 0.0.0.0:8080 --reuse-port --workers 1 \
-k uvicorn.workers.UvicornWorker \
--timeout 3600 --graceful-timeout 50 \
app.services.${SERVICE_NAME}.api:app \
--reload

