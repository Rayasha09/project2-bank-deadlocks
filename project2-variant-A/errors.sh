
#!/bin/bash

files=("bank_state.txt" "bank_state2.txt")

total_lines=0
total_5xx=0
min_file=""
min_5xx=-1

for file in "${files[@]}"; do
    lines=$(wc -l < "$file")
    errors=$(grep -Eo '\b5[0-9]{2}\b' "$file" | wc -l)

    echo "Файл: $file"
    echo "Количество строк: $lines"
    echo "Количество ошибок 5xx: $errors"
    echo

    total_lines=$((total_lines + lines))
    total_5xx=$((total_5xx + errors))

    if [ "$min_5xx" -eq -1 ] || [ "$errors" -lt "$min_5xx" ]; then
        min_5xx=$errors
        min_file="$file"
    fi
done

echo "Общее количество строк: $total_lines"
echo "Общее количество ошибок 5xx: $total_5xx"
echo "Файл с минимальным количеством 5xx: $min_file ($min_5xx)"
