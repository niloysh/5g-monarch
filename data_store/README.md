# Data Store
S3 object storage using MinIO for usage with Thanos.
MongoDB for storing configuration and metadata.

# Installation

## minio
### install

Use the community [Helm Charts](https://github.com/minio/minio/tree/master/helm/minio).

```
helm install minio -f minio-values.yaml minio/minio -n minio
```

### minio client (optional)
The minio client can be used to interact with the minio server.
 
See the [documentation](https://min.io/docs/minio/linux/reference/minio-mc.html).
```
mc alias set minio https://minioserver.example.net ACCESS_KEY SECRET KEY

## mongodb

### install
Deploy using Kustomize.