# fano-oss-py-sdk

This is a fork of minio-py.

## Difference

- Add `external_host` and `contextual_path` to `Minio` constructor.
- Add `is_external` to `presigned_get_object` and `presigned_put_object` method.


Following is an example code:
```
client = Minio(
    "192.168.4.19:9000",
    access_key="accesskey",
    secret_key="secretkey",
    secure=False,
    external_host="https://sample.fano.ai",
    contextual_path=True,
)

# For external link
result = client.presigned_get_object("example", "test", is_external=True)
# for internal link
result = client.presigned_get_object("example", "test")
```
