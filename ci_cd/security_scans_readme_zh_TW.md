# 安全掃描

## 執行的掃描項目：

- 針對 `./docs/` 的 Trivy 掃描 (高/危急/中)
- 針對 `./ui/` 的 Trivy 掃描 (高/危急/中)
- 針對 `Dockerfile.database` 的 Grype 掃描 (遇危急則失敗)
- 針對主要 `Dockerfile` 的 Grype 掃描 (遇危急則失敗)
- 針對主要 `Dockerfile` 的 Grype CVSS ≥ 4.0 掃描 (遇任何 CVSS ≥ 4.0 的弱點則失敗)
