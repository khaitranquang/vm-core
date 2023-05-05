  #!/usr/bin/env bash
ssh -o StrictHostKeyChecking=no root@54.169.243.60 << 'ENDSSH'
 cd /django-rest-base
 docker login -u $REGISTRY_USER -p $CI_BUILD_TOKEN $CI_REGISTRY
 docker pull registry.gitlab.com/khaitranquang/django-rest-base:latest
 docker-compose up -d
ENDSSH