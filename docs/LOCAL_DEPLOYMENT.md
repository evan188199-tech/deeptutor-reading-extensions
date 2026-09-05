# Local deployment on port 3782

The plugin needs a host with the provider-management integration from
[DeepTutor PR #1233](https://github.com/HKUDS/DeepTutor/pull/1233).
Installing a wheel in an older image alone cannot add the settings page.
The screenshots in this repository were captured from an upgraded local Docker
service; the existing data mount and EPUB paging changes were retained.

## Upgrade the host once

Build an integrated source checkout into a local image. For a clean trial:

```sh
git clone https://github.com/HKUDS/DeepTutor.git DeepTutor-reading
cd DeepTutor-reading
git fetch origin pull/1233/head
git switch --detach FETCH_HEAD
docker build --target development -t deeptutor-local:reading-providers .
```

For an existing customized deployment, merge the integration into an isolated
copy of its source before building. Preserve its current image tag for rollback.
Do not replace an existing checkout containing uncommitted work with the trial
checkout. The example uses the repository's development image; a production
image can be built with `--target production` instead.

In the directory of the existing Compose deployment, create a small override:

```yaml
services:
  deeptutor:
    image: deeptutor-local:reading-providers
    pull_policy: never
```

Use that override with the deployment's existing Compose file, environment file,
project name and **complete data mount**. In the default layout:

```sh
docker compose --env-file data/user/settings/docker.env -p deeptutor \
  -f docker-compose.ghcr.yml -f compose.reading.local.yml \
  up -d --no-deps deeptutor
```

The existing settings should retain frontend port 3782 and backend port 8001.
Verify `http://127.0.0.1:8001/health/ready`, then open
`http://127.0.0.1:3782/settings#reading-extensions` with an administrator account.

## Install and select only the providers you need

Use Settings → Reading extensions, or run commands inside the backend container:

```sh
docker exec --user deeptutor deeptutor python -m deeptutor_cli.main \
  plugin reading update --package deeptutor-reading-vocabulary
docker exec --user deeptutor deeptutor python -m deeptutor_cli.main \
  plugin reading provider vocabulary --package deeptutor-reading-vocabulary
docker restart deeptutor
```

Repeat only for the desired actions. `read-aloud` supplies the `read_aloud` slot;
`vocabulary` supplies `vocabulary`; `quiz` supplies `quiz`. The dictionary example
also supplies `vocabulary`, so select it explicitly when testing its three sample
entries. It is not selected automatically and is not a production dictionary.

Packages and selections persist beneath the runtime home's
`data/system/reading-providers`; the convenience bundle uses
`data/system/reading-plugins`. Retain the full data volume across container
recreation. Restart all workers after install, removal or provider selection.

## Roll back

Set the override back to the previous image tag and recreate only the app
service using the same data mount. Do not run `down -v` or delete runtime data.
An older host ignores the provider-manager files. To undo only a provider choice,
select Default provider and restart; other installed packages remain available.
