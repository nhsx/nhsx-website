# Console Access

_Note_ The below assumes you have access to the dxw Dalmatian infrastructure,
and have `dalmatian-tools` installed. If you don't have access, and need to,
contact a member of the dxw ops team.

## Login to dalmatian

```bash
dalmatian login
```

And follow the onscreen prompts

## Access the container

```bash
dalmatian service container-access -i nhsx-website -s web -e ENVIRONMENT
```

(Where `ENVIRONMENT` is one of `prod` or `staging`)
