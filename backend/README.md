# Backend

## Run API Server
```bash
uv run uvicorn app.main:app --reload
```

## Run Knowledge Generator
```bash
# Generate for specific domains
uv run python -m generator.run_generator --domains MATH PHYSICS --target 100

# Generate for all domains
uv run python -m generator.run_generator --all-domains --target 200

# Load seed definitions only
uv run python -m generator.run_generator --seed-only

# Dry run (in-memory, no database)
uv run python -m generator.run_generator --dry-run --all-domains
```

