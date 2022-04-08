# pre-commit sample-config > .pre-commit-config.yaml
pre-commit install

# ************************
# https://pypi.org/project/commitizen/
# Add commitizen
# ************************
# - repo: https://github.com/commitizen-tools/commitizen
#    rev: master
#    hooks:
#      - id: commitizen
#        stages: [commit-msg]
pre-commit install --hook-type commit-msg
