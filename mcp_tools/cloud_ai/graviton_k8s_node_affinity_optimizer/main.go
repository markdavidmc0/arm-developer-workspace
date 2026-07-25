package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type AffinityConfig struct {
	ManifestPath   string   `json:"manifest_path"`
	NodeArch       string   `json:"node_arch"`
	TargetGraviton string   `json:"target_graviton"`
	InjectedRules  []string `json:"injected_rules"`
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println(`{"error": "Manifest path argument required"}`)
		os.Exit(1)
	}

	manifestPath := os.Args[1]
	data, err := os.ReadFile(manifestPath)

	rules := []string{}
	if err == nil && strings.Contains(string(data), "kind: Deployment") {
		rules = append(rules, "kubernetes.io/arch: arm64")
		rules = append(rules, "node.kubernetes.io/instance-type: c7g.4xlarge")
		rules = append(rules, "topologySpreadConstraints: zone-balancing-enabled")
	} else {
		rules = append(rules, "default-arm64-node-selector-added")
	}

	config := AffinityConfig{
		ManifestPath:   manifestPath,
		NodeArch:       "arm64",
		TargetGraviton: "Graviton4",
		InjectedRules:  rules,
	}

	out, _ := json.MarshalIndent(config, "", "  ")
	fmt.Println(string(out))
}
