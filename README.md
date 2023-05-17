# Huggingface Space Deployer 🤗🚀

Deploy any arbitrary folder to a [Huggingface Space](https://huggingface.co/docs/hub/spaces).

## How to use

This command deploys the current directory to a Huggingface Space:

```sh
HF_SPACE_ID="username/myspace"
HF_TOKEN="hf_xxx"
docker run -it --rm -v .:/src samalba/hugginface-space-deploy \
    --repo-id $HF_SPACE_ID \
    --access-token $HF_TOKEN \
    /src \
    --ignore-patterns 'venv/*'
```

**Notes:**

1. The Huggingface Space must exist prior deploying.
2. this example assumes that the `./venv` directory contains a Python virtual env.
3. `.gitignore` is ignore so you need to specify what to ignore via `--ignore-patterns`.
4. The `.git` folder is automatically ignored.
