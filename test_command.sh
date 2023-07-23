# Use the `wait-for-it` script (https://github.com/vishnubob/wait-for-it) to
# test that the datastore-emulator is ready by testing against its host and
# port. Otherwise, if tests run before it's ready they will fail.

wait-for-it postgres:5432 --strict --timeout=30 -- \
# wait-for-it datastore:8814 --strict --timeout=30 -- \
# wait-for-it gcloud-tasks-emulator:8123 --strict --timeout=30 -- \
wait-for-it default:8080 --strict --timeout=30 -- \
python -m scripts.setup_local && \
pytest -s --junitxml=pytest-report.xml --cov=app --cov-report \
xml:coverage-report.xml app/tests
