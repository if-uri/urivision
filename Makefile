.PHONY: doctor-setup test matrix native-matrix native-probe confidence docker-matrix docker-linux-x11 docker-wayland docker-contract zip

doctor-setup:
	python3 -m pip install -e ".[test]"

test:
	PYTHONPATH=src:. python3 -m unittest discover -s tests -v

matrix:
	PYTHONPATH=src:. python3 tools/run_backend_matrix.py --out artifacts/backend-matrix.json --markdown artifacts/backend-matrix.md

native-matrix:
	PYTHONPATH=src:. python3 tools/run_native_lab_matrix.py --out artifacts/native-lab-matrix.json --markdown artifacts/native-lab-matrix.md --confidence artifacts/native-confidence-gate.md

native-probe:
	PYTHONPATH=src:. python3 tools/probe_native_host.py --out artifacts/native-host-probe.json

confidence:
	PYTHONPATH=src:. python3 tools/check_confidence_gate.py artifacts/native-lab-matrix.json

docker-matrix:
	docker compose -f docker/docker-compose.yml run --rm uri-runtime-matrix

docker-linux-x11:
	docker compose -f docker/docker-compose.yml --profile linux-x11 up --build --abort-on-container-exit

docker-wayland:
	docker compose -f docker/docker-compose.yml --profile linux-wayland up --build --abort-on-container-exit

docker-contract:
	docker compose -f docker/docker-compose.yml --profile contract up --build --abort-on-container-exit

zip:
	cd .. && zip -qr urivision_native_test_lab.zip urivision -x 'urivision/venv/*' -x 'urivision/.git/*'
