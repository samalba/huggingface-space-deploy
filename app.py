#!/usr/bin/env python

import argparse
import time

import requests
from huggingface_hub import HfApi, SpaceStage


def fetch_build_logs(repo_id: str, access_token: str):
    # -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'authorization: Bearer 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'
    headers = {
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Authorization": f"Bearer {access_token}",
    }
    r = requests.get(f"https://huggingface.co/api/spaces/{repo_id}/logs/build?isHtml=true", headers=headers)
    return r.text


def hf_upload_to_space(repo_id: str, access_token: str, source_path: str, target_path: str, ignore_patterns: list[str] or None, timeout: int) -> str:
    api = HfApi(token=access_token)

    url = api.upload_folder(folder_path=source_path,
                            path_in_repo=target_path,
                            repo_id=repo_id,
                            repo_type="space",
                            ignore_patterns=ignore_patterns)

    started_build = False
    last_printed_logs = 0
    # timeout is 3 min
    for i in range(0, timeout):
        build_logs = fetch_build_logs(repo_id, access_token)
        if len(build_logs) > last_printed_logs:
            print(build_logs[last_printed_logs:], flush=True)
            last_printed_logs = len(build_logs)

        runtime = api.get_space_runtime(repo_id)
        if runtime.stage in [
            SpaceStage.RUNNING_BUILDING,
            SpaceStage.BUILDING]:
            if started_build is False:
                print(f"Build started on Space: {repo_id}")
                started_build = True
            continue

        if started_build is True and runtime.stage in [
            SpaceStage.BUILD_ERROR,
            SpaceStage.CONFIG_ERROR,
            SpaceStage.RUNNING]:
            print(f"Build completed with status: {runtime.stage}")
            return url

        time.sleep(1.0)

    print("Timeout reached, space might still be building in the background.")
    return url


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_path", help="local path of the source to upload")
    parser.add_argument("target_path", default="", nargs="?", help="target path of the destination")
    parser.add_argument("--repo-id", required=True, help="Ignore patterns")
    parser.add_argument("--access-token", required=True)
    parser.add_argument("--ignore-patterns", nargs="*")
    parser.add_argument("--timeout", type=int, default=300, help="Set timeout to wait for the deploy to complete (default: 5 min)")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    folder_url = hf_upload_to_space(args.repo_id,
                                    args.access_token,
                                    args.source_path,
                                    args.target_path,
                                    args.ignore_patterns,
                                    args.timeout)
    print(f"Deployed code to space {args.repo_id} at location {folder_url}")
