#!/bin/bash
source ../utils/cecho.sh
check_status() {
    component="$1"
    namespace="$2"
    
    if [ "$(helm status "$component" -n "$namespace" -o json 2>/dev/null | jq -r '.info.status')" = "deployed" ]; then
        cecho "GREEN" "Component $component is deployed."
        return
    fi
    cecho "RED" "Component $component is not deployed."
    

}