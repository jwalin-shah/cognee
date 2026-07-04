#!/usr/bin/env python3
"""Delete all datasets and re-ingest them."""
import os, sys, asyncio

# Ensure we're in the right directory with env loaded
os.chdir(os.path.expanduser("~/projects/cognee/cognee-mcp"))

# Load .env
env_path = os.path.join(os.getcwd(), ".env")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip()
        os.environ[key] = val

print("=== Environment loaded ===")
for k in ["LLM_PROVIDER", "EMBEDDING_PROVIDER", "EMBEDDING_ENDPOINT",
          "EMBEDDING_MODEL", "EMBEDDING_DIMENSIONS"]:
    print(f"  {k}={os.environ.get(k, '(not set)')}")

import cognee

async def delete_all_datasets():
    print("\n=== Deleting all datasets ===")
    try:
        result = await cognee.datasets.delete_all()
        print(f"Delete result: {result}")
    except Exception as e:
        print(f"Error during delete_all: {e}")
        import traceback
        traceback.print_exc()

    remaining = await cognee.datasets.list_datasets()
    print(f"Remaining datasets: {len(remaining)}")
    return remaining

async def reingest_test_single():
    print("\n=== Re-ingesting test_single ===")
    try:
        test_data = "This is a test document for verifying the MLX embedding configuration."
        result = await cognee.add(test_data, dataset_name="test_single")
        print(f"Add result: {result}")

        # Verify dataset was created
        ds_list = await cognee.datasets.list_datasets()
        for ds in ds_list:
            if ds.name == "test_single":
                print(f"test_single dataset created: {ds.id}")
                return ds
        print("test_single not found after add!")
        return None
    except Exception as e:
        print(f"Error during re-ingest: {e}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    await delete_all_datasets()
    ds = await reingest_test_single()
    if ds:
        print("\n=== test_single ready for cognify! ===")
    else:
        print("\n=== FAILED to create test_single ===")

if __name__ == "__main__":
    asyncio.run(main())
