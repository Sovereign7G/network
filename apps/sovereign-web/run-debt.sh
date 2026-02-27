echo "Unused variables: $(grep -r "const .* = .*;" src --include="*.ts" --include="*.svelte" | grep -v "used" | wc -l) remaining"
echo "Unused imports: $(grep -r "import .* from" src --include="*.ts" --include="*.svelte" | grep -v "used" | wc -l) remaining"
echo "TODO comments: $(grep -r "TODO" src --include="*.svelte" --include="*.ts" | wc -l)"
echo "FIXME comments: $(grep -r "FIXME" src --include="*.svelte" --include="*.ts" | wc -l)"
