#!/usr/bin/env python3
"""Load .env and export to environment, then run cognee commands."""
import os, sys, subprocess

# Change to cognee-mcp directory
os.chdir(os.path.expanduser("~/projects/cognee/cognee-mcp"))

# Parse .env file manually
env_path = os.path.join(os.getcwd(), ".env")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip()
        # Strip surrounding quotes if present
        if val.startswith(("{", '"', "'")) and val.endswith(("}", '"', "'")):
            # Keep JSON as-is
            pass
        else:
            val = val.strip("\"'")
        os.environ[key] = val

print("=== Environment loaded ===")
for k in ["LLM_PROVIDER", "LLM_ENDPOINT", "LLM_MODEL", "EMBEDDING_PROVIDER",
          "EMBEDDING_ENDPOINT", "EMBEDDING_MODEL", "EMBEDDING_DIMENSIONS",
          "VECTOR_DB_PROVIDER", "GRAPH_DATABASE_PROVIDER"]:
    print(f"  {k}={os.environ.get(k, '(not set)')}")

# Now run the command passed as args
if len(sys.argv) > 1:
    cmd = " ".join(sys.argv[1:])
    print(f"\n=== Running: {cmd} ===")
    result = subprocess.run(cmd, shell=True, env=os.environ, capture_output=False)
    sys.exit(result.returncode)
