#!/bin/bash

# Add lang="ts" to all Svelte components
find src -name "*.svelte" -type f | while read -r file; do
  if ! grep -q "<script lang=\"ts\">" "$file"; then
    # Replace existing script tag or add new one
    if grep -q "<script>" "$file"; then
      sed -i 's/<script>/<script lang="ts">/' "$file"
    else
      # Insert at beginning of file
      sed -i '1i<script lang="ts">\n<\/script>\n' "$file"
    fi
    echo "Converted: $file"
  fi
done

echo "✅ All components converted to TypeScript!"
