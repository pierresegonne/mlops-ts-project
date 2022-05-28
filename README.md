# mlops-ts-project

Cloud run URL https://mlops-ts-project-jfnx5klx2a-od.a.run.app


Can be queried with

```
curl -H \
"Authorization: Bearer $(gcloud auth print-identity-token)" \
https://mlops-ts-project-jfnx5klx2a-od.a.run.app
```

__set environment variables__

```
export EMAP_PROJECT_ID=tmrow-152415
export POSTGRES_DB=electricitymap
export POSTGRES_HOST=127.0.0.1
export POSTGRES_USER=readonly
export POSTGRES_PORT=5432
```


__run__

```
poetry run serve
```
### Blog post

The scripts for the blog post must be prefixed with `PYTHONPATH=.`


### Improvements

- better project separation to not have to share dependencies.
- `local-run` for training / to not have to write Dockerfile
