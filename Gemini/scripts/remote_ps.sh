#!/bin/bash
# --- DATE CALCULATION ---
if [ -n "$1" ]; then
    M=$(echo "$1" | awk '{print $1}')
    D=$(echo "$1" | awk '{print $2}')
else
    M=$(date +%b)
    D=$(date +%e)
fi

INTERACTIVE_PATH=$(echo "$2" | tr ',' ' ')
BROADCAST_PATH=$(echo "$3" | tr ',' ' ')
BROADCAST_CSV_PATH=$(echo "$4" | tr ',' ' ')
COMMON_PATH=$(echo "$5" | tr ',' ' ')

echo "===DATA_START==="
echo "REMOTE_DATE: $(date)"
echo "MATCHING_DATE: $M $D"

# 1. External Files Count
count_files() {
    local suffix=$1
    shift
    local dirs="$@"
    local total=0
    for dir in $dirs; do
        target_dir="${dir%/}/$suffix"
        if [ -d "$target_dir" ]; then
            # Use ls -l to match the user's manual check logic
            count=$(ls -l "$target_dir" 2>/dev/null | grep -Ec "$M +$D")
            total=$((total + count))
        fi
    done
    echo $total
}
EXT_COUNT=$(count_files "exchangefiles" $COMMON_PATH)
echo "EXTERNAL_FILES: $EXT_COUNT"

# 2. Containers
CONT_COUNT=$(docker ps --format '{{.ID}}' | wc -l)
RESTART_COUNT=$(docker ps -a --filter "status=restarting" --format '{{.ID}}' | wc -l)
EXITED_NAMES=$(docker ps -a --filter "status=exited" --format '{{.Names}}' | tr '\n' ',' | sed 's/,$//')
echo "CONTAINERS: $CONT_COUNT"
echo "RESTARTING_CONTAINERS: $RESTART_COUNT"
echo "EXITED_CONTAINER_NAMES: $EXITED_NAMES"

# 3. Disk Usage
df -BG | awk 'NR>1 { p=$(NF-1); sub(/%/,"",p); avail=$4; sub(/G/,"",avail); mount=$NF; if (mount == "/" || mount == "/data" || p > 75) { prefix = (mount == "/") ? "ROOT" : (mount == "/data" ? "DATA" : mount); gsub(/[^a-zA-Z0-9]/, "_", prefix); print prefix "_AVAIL: " avail; print prefix "_USED: " p; } }'

# 4. RAM Usage %
RAM_PCT=$(free | awk '/Mem:/ { printf("%.2f", $3/$2 * 100) }')
echo "RAM_USED_PCT: $RAM_PCT"

# 5. Specific File Lists
get_files_in_sub() {
    local sub=$1
    shift
    local dirs="$@"
    for dir in $dirs; do
        target_dir="${dir%/}/$sub"
        if [ -d "$target_dir" ]; then
            ls -l --time-style=+"%b %e" "$target_dir" 2>/dev/null | awk -v m="$M" -v d="$D" '
                $1 ~ /^-/ && $6 == m && $7 + 0 == d + 0 {
                    printf "%s|%s|%s %s,", $NF, $5, $6, $7
                }
            '
        fi
    done
}

echo "INTERACTIVE_INDEX_FILES: $(get_files_in_sub index-data $INTERACTIVE_PATH)"
echo "INTERACTIVE_INFO_FILES: $(get_files_in_sub info-data $INTERACTIVE_PATH)"
echo "INTERACTIVE_SCRIP_FILES: $(get_files_in_sub scrip-data $INTERACTIVE_PATH)"

echo "BROADCAST_MASTER_INDEX_FILES: $(get_files_in_sub index-data $BROADCAST_PATH)"
echo "BROADCAST_MASTER_INFO_FILES: $(get_files_in_sub info-data $BROADCAST_PATH)"
echo "BROADCAST_MASTER_SCRIP_FILES: $(get_files_in_sub scrip-data $BROADCAST_PATH)"

echo "BROADCAST_CSV_INDEX_FILES: $(get_files_in_sub index-data $BROADCAST_CSV_PATH)"
echo "BROADCAST_CSV_INFO_FILES: $(get_files_in_sub info-data $BROADCAST_CSV_PATH)"
echo "BROADCAST_CSV_SCRIP_FILES: $(get_files_in_sub scrip-data $BROADCAST_CSV_PATH)"

echo "COMMON_MASTER_INDEX_FILES: $(get_files_in_sub index-data $COMMON_PATH)"
echo "COMMON_MASTER_INFO_FILES: $(get_files_in_sub info-data $COMMON_PATH)"
echo "COMMON_MASTER_SCRIP_FILES: $(get_files_in_sub scrip-data $COMMON_PATH)"

echo "===DATA_END==="
