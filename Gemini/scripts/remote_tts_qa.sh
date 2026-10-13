#!/bin/bash
# --- DATE CALCULATION ---
if [ -n "$1" ]; then
    M=$(echo "$1" | awk '{print $1}')
    D=$(echo "$1" | awk '{print $2}')
    if [ ${#D} -eq 1 ]; then D="0$D"; fi
else
    M=$(date +%b)
    D=$(date +%d)
fi

# TTS QA Arguments
# $2: NOREN_PATH, $3: NEST_PATH, $4: ZERODHA_PATH, $5: HSM_SCRIP_PATH, $6: HSM_CSV_PATH, $7: EXT_PATH
NOREN_PATH=$(echo "$2" | tr ',' ' ')
NEST_PATH=$(echo "$3" | tr ',' ' ')
ZERODHA_PATH=$(echo "$4" | tr ',' ' ')
HSM_SCRIP_PATH=$(echo "$5" | tr ',' ' ')
HSM_CSV_PATH=$(echo "$6" | tr ',' ' ')
EXT_PATH=$(echo "$7" | tr ',' ' ')

echo "===DATA_START==="
echo "REMOTE_DATE: $(date)"
echo "MATCHING_DATE: $M $D"

# 1. External Files Count
count_files() {
    local dirs="$@"
    local total=0
    for dir in $dirs; do
        if [ -d "$dir" ]; then
            count=$(find "$dir" -maxdepth 1 -type f -printf "%b %d\n" 2>/dev/null | awk -v m="$M" -v d="$D" '
                $1 == m && $2 == d { count++ }
                END { print count }
            ')
            total=$((total + count))
        fi
    done
    echo $total
}
echo "EXTERNAL_FILES: $(count_files $EXT_PATH)"

# 2. Containers
CONT_COUNT=$(docker ps --format '{{.ID}}' | wc -l)
RESTART_COUNT=$(docker ps -a --filter "status=restarting" --format '{{.ID}}' | wc -l)
EXITED_NAMES=$(docker ps -a --filter "status=exited" --format '{{.Names}}' | tr '\n' ',' | sed 's/,$//')
echo "CONTAINERS: $CONT_COUNT"
echo "RESTARTING_CONTAINERS: $RESTART_COUNT"
echo "EXITED_CONTAINER_NAMES: $EXITED_NAMES"

# 3. Disk Usage
df -BG | awk 'NR>1 { p=$(NF-1); sub(/%/,"",p); avail=$4; sub(/G/,"",avail); mount=$NF; if (mount == "/" || mount == "/Data" || mount == "/data") { prefix = (mount == "/") ? "ROOT" : "DATA"; print prefix "_AVAIL: " avail; print prefix "_USED: " p; } }'

# 4. RAM Usage %
RAM_PCT=$(free | awk '/Mem:/ { printf("%.2f", $3/$2 * 100) }')
echo "RAM_USED_PCT: $RAM_PCT"

# 5. File Lists helper
get_files_in_sub() {
    local sub=$1
    shift
    local dirs="$@"
    for dir in $dirs; do
        target_dir="${dir%/}/$sub"
        if [ -d "$target_dir" ]; then
            ls -l --time-style=+"%b %d" "$target_dir" 2>/dev/null | awk -v m="$M" -v d="$D" '
                $1 ~ /^-/ && $6 == m && $7 == d {
                    printf "%s|%s|%s %s,", $NF, $5, $6, $7
                }
            '
        fi
    done
}

# Special for HSI Noren
echo "NOREN_INDEX_FILES: $(get_files_in_sub index-data $NOREN_PATH)"
echo "NOREN_INFO_FILES: $(get_files_in_sub info-data $NOREN_PATH)"
echo "NOREN_SCRIP_FILES: $(get_files_in_sub scrip-data $NOREN_PATH)"

# Special for HSI Nest
echo "NEST_INDEX_FILES: $(get_files_in_sub index-data $NEST_PATH)"
echo "NEST_INFO_FILES: $(get_files_in_sub info-data $NEST_PATH)"
echo "NEST_SCRIP_FILES: $(get_files_in_sub scrip-data $NEST_PATH)"

# Zerodha (No subfolders)
echo "ZERODHA_FILES: $(ls -l --time-style=+"%b %d" $ZERODHA_PATH 2>/dev/null | awk -v m="$M" -v d="$D" '$1 ~ /^-/ && $6 == m && $7 == d { printf "%s|%s|%s %s,", $NF, $5, $6, $7 }')"

# HSM Scrip Master
echo "HSM_SCRIP_INDEX_FILES: $(get_files_in_sub index-data $HSM_SCRIP_PATH)"
echo "HSM_SCRIP_INFO_FILES: $(get_files_in_sub info-data $HSM_SCRIP_PATH)"
echo "HSM_SCRIP_SCRIP_FILES: $(get_files_in_sub scrip-data $HSM_SCRIP_PATH)"

# HSM CSV Gen
echo "HSM_CSV_INDEX_FILES: $(get_files_in_sub index-data $HSM_CSV_PATH)"
echo "HSM_CSV_INFO_FILES: $(get_files_in_sub info-data $HSM_CSV_PATH)"
echo "HSM_CSV_SCRIP_FILES: $(get_files_in_sub scrip-data $HSM_CSV_PATH)"

echo "===DATA_END==="
