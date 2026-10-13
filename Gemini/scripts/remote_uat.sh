# #!/bin/bash
#!/usr/bin/env bash

# ============================================================
# DATA FETCHER
# Optimized Version (Part 1)
# ============================================================
# ------------------------------------------------------------
# Date
# ------------------------------------------------------------
if [[ -n "${1:-}" ]]; then
    read -r M D <<< "$1"
else
    M=$(date +%b)
    D=$(date +%e)
fi

# ------------------------------------------------------------
# Path Arrays
# ------------------------------------------------------------
IFS=',' read -ra INTERACTIVE_PATH <<< "${2:-}"
IFS=',' read -ra BROADCAST_PATH <<< "${3:-}"
IFS=',' read -ra BROADCAST_CSV_PATH <<< "${4:-}"
IFS=',' read -ra COMMON_PATH <<< "${5:-}"

# Ensure required variables are set
INFO_PATH=${INFO_PATH:-/data/ttsvolume/hscommonvol/data/exch_scrip_master/info-data/}
SCRIP_PATH=${SCRIP_PATH:-/data/ttsvolume/hscommonvol/data/exch_scrip_master/scrip-data/}
PATTERN=${PATTERN:-'"MTFStatus": "1"'}

echo "===DATA_START==="
echo "REMOTE_DATE: $(date)"
echo "MATCHING_DATE: $M $D"

# ============================================================
# Count files inside a subdirectory
# ============================================================

count_files() {

    local suffix="$1"
    shift

    local total=0

    for dir in "$@"
    do
        local target_dir="${dir%/}/$suffix"

        [[ -d "$target_dir" ]] || continue

        local count

        count=$(
            ls -l "$target_dir" 2>/dev/null |
            grep -Ec "$M +$D"
        )

        ((total+=count))
    done

    echo "$total"
}

EXT_COUNT=$(count_files exchangefiles "${COMMON_PATH[@]}")

echo "EXTERNAL_FILES: $EXT_COUNT"

# ============================================================
# 2. Containers (Optimized)
# ============================================================

CONT_COUNT=$(docker ps -q | wc -l)
RESTART_COUNT=$(docker ps -aq --filter status=restarting | wc -l)
EXITED_NAMES=$(docker ps -a --filter status=exited --format '{{.Names}}' | paste -sd "," -)

echo "CONTAINERS: $CONT_COUNT"
echo "RESTARTING_CONTAINERS: $RESTART_COUNT"
echo "EXITED_CONTAINER_NAMES: $EXITED_NAMES"

IN_RANGE_CONTAINERS=""
OUT_OF_RANGE_CONTAINERS=""

while IFS='|' read -r name status
do
    # --------------------------------------------------------
    # Handle exited containers
    # --------------------------------------------------------
    if [[ "$status" == *"Exited"* ]]; then

        if [[ "$name" == *"exch-json-gen-noren"* || \
              "$name" == *"exch-csv-gen"* || \
              "$name" == *"exch-scrip-master"* ]]; then
            continue
        fi

        OUT_OF_RANGE_CONTAINERS+="$name (Exited),"
        continue
    fi

    # --------------------------------------------------------
    # Parse uptime
    # --------------------------------------------------------
    uptime=$(echo "$status" | sed 's/^Up //' | sed 's/ (.*)//')

    # -----------------------------------
    # ✅ Normalize uptime (handle "About")
    # -----------------------------------
    if [[ "$uptime" == About* ]]; then
        if [[ "$uptime" == *"hour"* ]]; then
            value1=1
            unit1="hour"
        elif [[ "$uptime" == *"minute"* ]]; then
            value1=1
            unit1="minute"
        else
            value1=1
            unit1="second"
        fi
        value2=0
        unit2=""
    else
        value1=$(echo "$uptime" | awk '{print $1}')
        unit1=$(echo "$uptime" | awk '{print $2}')
        value2=$(echo "$uptime" | awk '{print $3}')
        unit2=$(echo "$uptime" | awk '{print $4}')
    fi

    # -----------------------------------
    # ✅ Ensure numeric defaults (CRITICAL)
    # -----------------------------------
    [[ "$value1" =~ ^[0-9]+$ ]] || value1=0
    [[ "$value2" =~ ^[0-9]+$ ]] || value2=0

    seconds=0

    # First unit
    case "$unit1" in
        second* ) seconds=$value1 ;;
        minute* ) seconds=$((value1 * 60)) ;;
        hour*   ) seconds=$((value1 * 3600)) ;;
        day*    ) seconds=$((value1 * 86400)) ;;
        *       ) seconds=0 ;;   # ✅ fallback
    esac

    # Second unit
    case "$unit2" in
        second* ) seconds=$((seconds + value2)) ;;
        minute* ) seconds=$((seconds + value2 * 60)) ;;
        hour*   ) seconds=$((seconds + value2 * 3600)) ;;
    esac

    if [[ "$value2" =~ ^[0-9]+$ && -n "$unit2" ]]; then
        readable_time="${value1}${unit1:0:1} ${value2}${unit2:0:1}"
    else
        readable_time="${value1}${unit1:0:1}"
    fi

    if (( seconds > 20 && seconds < 20000 )); then
        IN_RANGE_CONTAINERS+="$name (${readable_time}),"
    else
        OUT_OF_RANGE_CONTAINERS+="$name (${readable_time}),"
    fi

done < <(docker ps -a --format '{{.Names}}|{{.Status}}')

IN_RANGE_CONTAINERS="${IN_RANGE_CONTAINERS%,}"
OUT_OF_RANGE_CONTAINERS="${OUT_OF_RANGE_CONTAINERS%,}"

echo "IN_RANGE_CONTAINERS: $IN_RANGE_CONTAINERS"
echo "OUT_OF_RANGE_CONTAINERS: $OUT_OF_RANGE_CONTAINERS"

# ============================================================
# 3. Disk Usage (Optimized)
# ============================================================

df -BG | awk '
NR == 1 { next }

{
    used = $(NF-1)
    gsub(/%/, "", used)

    avail = $4
    gsub(/G/, "", avail)

    mount = $NF

    if (mount == "/") {
        prefix = "ROOT"
    }
    else if (mount == "/data") {
        prefix = "DATA"
    }
    else if (used > 75) {
        prefix = mount
        gsub(/[^[:alnum:]]/, "_", prefix)
    }
    else {
        next
    }

    print prefix "_AVAIL: " avail
    print prefix "_USED: " used
}'

# ============================================================
# 4. RAM Usage
# ============================================================

RAM_PCT=$(
    free -b | awk '
    /^Mem:/ {
        printf "%.2f", ($3 / $2) * 100
    }'
)

echo "RAM_USED_PCT: $RAM_PCT"

# ============================================================
# 5. Specific File Lists (Optimized)
# ============================================================

get_files_in_sub() {
    local sub="$1"
    shift

    local dir
    local target_dir

    for dir in "$@"; do
        target_dir="${dir%/}/$sub"

        if [[ -d "$target_dir" ]]; then
            ls -l --time-style=+"%b %e" "$target_dir" 2>/dev/null |
            awk -v m="$M" -v d="$D" '
                $1 ~ /^-/ && $6 == m && $7 + 0 == d + 0 {
                    printf "%s|%s|%s %s,", $NF, $5, $6, $7
                }
            '
        fi
    done
}

echo "INTERACTIVE_INDEX_FILES: $(get_files_in_sub index-data "${INTERACTIVE_PATH[@]}")"
echo "INTERACTIVE_INFO_FILES: $(get_files_in_sub info-data "${INTERACTIVE_PATH[@]}")"
echo "INTERACTIVE_SCRIP_FILES: $(get_files_in_sub scrip-data "${INTERACTIVE_PATH[@]}")"

echo "BROADCAST_MASTER_INDEX_FILES: $(get_files_in_sub index-data "${BROADCAST_PATH[@]}")"
echo "BROADCAST_MASTER_INFO_FILES: $(get_files_in_sub info-data "${BROADCAST_PATH[@]}")"
echo "BROADCAST_MASTER_SCRIP_FILES: $(get_files_in_sub scrip-data "${BROADCAST_PATH[@]}")"

echo "BROADCAST_CSV_INDEX_FILES: $(get_files_in_sub index-data "${BROADCAST_CSV_PATH[@]}")"
echo "BROADCAST_CSV_INFO_FILES: $(get_files_in_sub info-data "${BROADCAST_CSV_PATH[@]}")"
echo "BROADCAST_CSV_SCRIP_FILES: $(get_files_in_sub scrip-data "${BROADCAST_CSV_PATH[@]}")"

echo "COMMON_MASTER_INDEX_FILES: $(get_files_in_sub index-data "${COMMON_PATH[@]}")"
echo "COMMON_MASTER_INFO_FILES: $(get_files_in_sub info-data "${COMMON_PATH[@]}")"
echo "COMMON_MASTER_SCRIP_FILES: $(get_files_in_sub scrip-data "${COMMON_PATH[@]}")"

echo "BASE_MAP_DETAILS: $(
    ls -ld /data/ttsvolume/hscommonvol/data/exch_scrip_master/base-map 2>/dev/null |
    awk '{print $1 "|" $3 "|" $4}'
)"

echo "BASE_MAP_FILES: $(get_files_in_sub base-map "${COMMON_PATH[@]}")"

# ============================================================
# 6. MTF Counts
# ============================================================

MTF_NSE_CM_INFO=$(grep -c "$PATTERN" "$INFO_PATH/nse_cm.json" 2>/dev/null || echo 0)
MTF_BSE_CM_INFO=$(grep -c "$PATTERN" "$INFO_PATH/bse_cm.json" 2>/dev/null || echo 0)

MTF_NSE_CM_SCRIP=$(grep -c "$PATTERN" "$SCRIP_PATH/nse_cm.json" 2>/dev/null || echo 0)
MTF_BSE_CM_SCRIP=$(grep -c "$PATTERN" "$SCRIP_PATH/bse_cm.json" 2>/dev/null || echo 0)

echo "MTF_NSE_CM_INFO: $MTF_NSE_CM_INFO"
echo "MTF_BSE_CM_INFO: $MTF_BSE_CM_INFO"
echo "MTF_NSE_CM_SCRIP: $MTF_NSE_CM_SCRIP"
echo "MTF_BSE_CM_SCRIP: $MTF_BSE_CM_SCRIP"

echo "===DATA_END==="