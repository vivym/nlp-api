# Build variables
VERSION ?= $(shell git describe --tags --exact-match 2>/dev/null || git symbolic-ref -q --short HEAD)
COMMIT_HASH ?= $(shell git rev-parse --short HEAD 2>/dev/null)
DATE_FMT = +%FT%T%z
ifdef SOURCE_DATE_EPOCH
    BUILD_DATE ?= $(shell date -u -d "@$(SOURCE_DATE_EPOCH)" "$(DATE_FMT)" 2>/dev/null || date -u -r "$(SOURCE_DATE_EPOCH)" "$(DATE_FMT)" 2>/dev/null || date -u "$(DATE_FMT)")
else
    BUILD_DATE ?= $(shell date "$(DATE_FMT)")
endif

REGISTRY_URL = registry.cn-beijing.aliyuncs.com/public-api/
IMAGE_NAME = nlp-api
IMAGE_VER = ${VERSION}-${COMMIT_HASH}
IMAGE_FULL_NAME = ${REGISTRY_URL}${IMAGE_NAME}:${IMAGE_VER}


.PHONY: docker-login
docker-login:
	@echo building $(shell date "$(DATE_FMT)")
	@docker login --username=${REGISTRY_USERNAME} --password=${REGISTRY_PASSWORD} ${REGISTRY_URL}
	@echo done $(shell date "$(DATE_FMT)")


.PHONY: release
release:
	@mkdir build

	@echo
	@echo ---------------------------------------------------------------
	@echo - `date "+%H:%M:%S"` [1] building docker image
	@echo ---------------------------------------------------------------
	@docker build -t ${IMAGE_NAME}:${IMAGE_VER} .
	@docker tag ${IMAGE_NAME}:${IMAGE_VER} ${IMAGE_FULL_NAME}

	@echo
	@echo ---------------------------------------------------------------
	@echo - `date "+%H:%M:%S"` [2] pushing docker image
	@echo ---------------------------------------------------------------
	@docker push ${IMAGE_FULL_NAME}

	@echo
	@echo ---------------------------------------------------------------
	@echo - `date "+%H:%M:%S"` [3] create k8s deployment.yaml
	@echo ---------------------------------------------------------------
	@sed 's#__IMAGE_FULL_NAME__#${IMAGE_FULL_NAME}#g;s#__SENTRY_DSN__#${SENTRY_DSN}#g' deployment.yaml > deployment.yaml

	@echo
	@echo ---------------------------------------------------------------
	@echo - `date "+%H:%M:%S"` [4] done
	@echo ---------------------------------------------------------------
