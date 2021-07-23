# Restoring a dump from prod/staging

_Note_ The below assumes you have access to the dxw Dalmatian infrastructure,
and have `dalmatian-tools` installed. If you don't have access, and need to,
contact a member of the dxw ops team.

## Creating the dump

Access the container as described in [Console Access](./console-access.md) and
run the following command:

```bash
./manage.py dumpdata --natural-foreign --indent 2 \
    -e contenttypes -e auth.permission -e postgres_search.indexentry \
    -e wagtailcore.groupcollectionpermission \
    -e wagtailcore.grouppagepermission -e wagtailimages.rendition \
    -e sessions > /tmp/$(date +%Y%m%d).json
```

## Copying the file from the live environment

List the EC2 instances in your chosen environment (where `ENV` is one of `prod`
or `staging`):

```bash
dalmatian ecs ec2-access -i nhsx-website -e ENV -l
```

Access the EC2 instance (where `INSTANCE_ID` is the ID of the instance you
want to connect to):

```bash
dalmatian ecs ec2-access -i nhsx-website -e ENV -I INSTANCE_ID
```

Switch to Sudo:

```bash
sudo bash
```

List the containers to get the name of your container:

```bash
docker ps
```

Copy the file from the relevant container:

```bash
docker cp CONTAINER_NAME:/tmp/$(date +%Y%m%d).json /tmp/$(date +%Y%m%d).json
```

Upload the file to S3 (where `ENVIRONMENT` is one of `staging` or `prod`)

```bash
aws s3 cp /tmp/$(date +%Y%m%d).json s3://nhsx-website-ecs-ENVIRONMENT-dalmatian-transfer/
```

Exit the EC2 instance and run the following locally:

```bash
dalmatian aws exec -i dalmatian-1 s3 cp s3://nhsx-website-ecs-prod-dalmatian-transfer/$(date +%Y%m%d).json app/$(date +%Y%m%d).json
```

Restore the data to your development environment like so:

```bash
script/manpy flush
script/manpy migrate
script/manpy loaddata $(date +%Y%m%d).json
```
