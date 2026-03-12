# LiteLLM Helm Chart

> [!IMPORTANT]
> 此項目由社群維護，若遇到 bug 請提交 issue。
> 我們建議在[生產環境部署中使用 Docker 或 Kubernetes](https://docs.litellm.ai/docs/proxy/prod)。

## 先決條件

- Kubernetes 1.21+
- Helm 3.8.0+

若使用 `db.deployStandalone`：

- 底層基礎設施需支援 PV provisioner

若使用 `db.useStackgresOperator`（尚未實作）：

- Kubernetes 叢集中必須已安裝 Stackgres Operator。若缺失，此 chart **不會**自動安裝該 operator。

## 參數 (Parameters)

### LiteLLM Proxy 部署設定

| 名稱                        | 描述                                                                                                                                                                                                                                   | 數值                     |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| `replicaCount`              | 要部署的 LiteLLM Proxy pod 數量                                                                                                                                                                                               | `1`                       |
| `masterkeySecretName`       | 包含 LiteLLM Master API Key 的 Kubernetes Secret 名稱。若未指定，則使用產生的 secret 名稱。                                                                                                              | N/A                       |
| `masterkeySecretKey`        | Kubernetes Secret 中包含 LiteLLM Master API Key 的鍵值 (key)。若未指定，預設使用 `masterkey`。                                                                                                              | N/A                       |
| `masterkey`                 | LiteLLM 的 Master API Key。若未指定，將隨機產生一個 `sk-...` 格式的金鑰。                                                                                                                                           | N/A                       |
| `environmentSecrets`        | 選用的 Secret 物件名稱陣列。這些 secret 中的鍵值對將作為環境變數提供給 LiteLLM proxy pod。範例請見下方 Secret 物件。                                                   | `[]`                      |
| `environmentConfigMaps`     | 選用的 ConfigMap 物件名稱陣列。這些 configmap 中的鍵值對將作為環境變數提供給 LiteLLM proxy pod。範例請見下方 Secret 物件。                                             | `[]`                      |
| `image.repository`          | LiteLLM Proxy 映像檔儲存庫 (repository)                                                                                                                                                                                 | `docker.litellm.ai/berriai/litellm` |
| `image.pullPolicy`          | LiteLLM Proxy 映像檔提取策略 (pull policy)                                                                                                                                                                                | `IfNotPresent`            |
| `image.tag`                 | 覆寫映像檔標籤 (tag)，預設為此 chart 發佈時 LiteLLM 的最新版本。                                                                                                                                     | `""`                      |
| `imagePullSecrets`          | LiteLLM 與 initContainer 映像檔的登錄 (registry) 憑證。                                                                                                                                                 | `[]`                      |
| `serviceAccount.create`     | 是否為此部署建立 Kubernetes Service Account。預設為 `false`，因為 LiteLLM 不需要存取 Kubernetes API。                                                                                   | `false`                   |
| `service.type`              | Kubernetes Service 類型（例如 `LoadBalancer`、`ClusterIP` 等）                                                                                                                                                                              | `ClusterIP`               |
| `service.port`              | Kubernetes Service 監聽的 TCP 連接埠。也是 Pod 內 proxy 監聽的 TCP 連接埠。                                                                                                                          | `4000`                    |
| `livenessProbe.*`           | LiteLLM 容器的存活探針 (Liveness probe) 設定（`path`、`periodSeconds`、`timeoutSeconds`、閾值及初始延遲）。                                                                                                                  | 請參閱 `values.yaml`         |
| `readinessProbe.*`          | LiteLLM 容器的就緒探針 (Readiness probe) 設定（`path`、`periodSeconds`、`timeoutSeconds`、閾值及初始延遲）。                                                                                                                 | 請參閱 `values.yaml`         |
| `startupProbe.*`            | LiteLLM 容器的啟動探針 (Startup probe) 設定（`path`、`periodSeconds`、`timeoutSeconds`、閾值及初始延遲）。                                                                                                                   | 請參閱 `values.yaml`         |
| `resources.*`               | LiteLLM 容器的 CPU/記憶體請求 (requests) 與限制 (limits)。                                                                                                                                                                                       | `{}`                      |
| `service.loadBalancerClass` | 選用的 LoadBalancer 實作類別（僅在 `service.type` 為 `LoadBalancer` 時使用）                                                                                                                                                  | `""`                      |
| `ingress.labels`            | Ingress 資源的額外標籤 (labels)                                                                                                                                                                                                    | `{}`                      |
| `ingress.*`                 | 設定範例請參閱 [values.yaml](./values.yaml)                                                                                                                                                                                         | N/A                       |
| `proxyConfigMap.create`     | 設定為 `true` 時，將根據 `.Values.proxy_config` 渲染並掛載 ConfigMap。                                                                                                                                                                     | `true`                    |
| `proxyConfigMap.name`       | 當 `create=false` 時，指定要掛載的現有 ConfigMap 名稱。                                                                                                                                                                                 | `""`                      |
| `proxyConfigMap.key`        | ConfigMap 中包含 proxy 設定檔的鍵值 (key)。                                                                                                                                                                                     | `"config.yaml"`           |
| `proxy_config.*`            | 預設設定請參閱 [values.yaml](./values.yaml)。僅在 `proxyConfigMap.create=true` 時渲染至 ConfigMap 的 `config.yaml`。配置範例請參閱 [example_config_yaml](../../../litellm/proxy/example_config_yaml/)。 | `N/A`                     |
| `extraContainers[]`         | 與 LiteLLM Proxy 一起作為 sidecars 部署的額外容器陣列。                                                                                                                                                     |
| `pdb.enabled`               | 為 LiteLLM proxy Deployment 啟用 PodDisruptionBudget (PDB)                                                                                                                                                                                 | `false`                   |
| `pdb.minAvailable`          | 在**自願性**中斷期間必須可用的最小 pod 數量/百分比（在 minAvailable/maxUnavailable 中選擇**其一**）                                                                                                     | `null`                    |
| `pdb.maxUnavailable`        | 在**自願性**中斷期間可以不可用的最大 pod 數量/百分比（在 minAvailable/maxUnavailable 中選擇**其一**）                                                                                                    | `null`                    |
| `pdb.annotations`           | 要新增至 PDB 的額外元資料註解 (annotations)                                                                                                                                                                                                  | `{}`                      |
| `pdb.labels`                | 要新增至 PDB 的額外元資料標籤 (labels)                                                                                                                                                                                                       | `{}`                      |

#### 根據 values 產生的範例 `proxy_config` ConfigMap（預設）：

```
proxyConfigMap:
  create: true
  key: "config.yaml"

proxy_config:
  general_settings:
    master_key: os.environ/PROXY_MASTER_KEY
  model_list:
    - model_name: gpt-3.5-turbo
      litellm_params:
        model: gpt-3.5-turbo
        api_key: eXaMpLeOnLy
```

#### 使用現有的 `proxyConfigMap` 而非新建的範例：

```
proxyConfigMap:
  create: false
  name: my-litellm-config
  key: config.yaml

# 在此模式下會忽略 proxy_config
```

#### 範例 `environmentSecrets` Secret

```
apiVersion: v1
kind: Secret
metadata:
  name: litellm-envsecrets
data:
  AZURE_OPENAI_API_KEY: TXlTZWN1cmVLM3k=
type: Opaque
```

### 資料庫設定 (Database Settings)

| 名稱                      | 描述                                                                                                                                                                                                                                                                               | 數值                                                                                      |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `db.useExisting`          | 使用現有的 Postgres 資料庫。必須存在包含連線憑證的 Kubernetes Secret 物件。下方提供範例 secret 物件定義。                                                                                                 | `false`                                                                                    |
| `db.endpoint`             | 若 `db.useExisting` 為 `true`，則為 Postgres 伺服器連線的 IP、主機名稱 (Hostname) 或 Service 名稱。                                                                                                                                                                             | `localhost`                                                                                |
| `db.database`             | 若 `db.useExisting` 為 `true`，則為要連線的現有資料庫名稱。                                                                                                                                                                                                           | `litellm`                                                                                  |
| `db.url`                  | 若 `db.useExisting` 為 `true`，可使用此值覆寫現有資料庫的連線 URL。                                                                                                                                                              | `postgresql://$(DATABASE_USERNAME):$(DATABASE_PASSWORD)@$(DATABASE_HOST)/$(DATABASE_NAME)` |
| `db.secret.name`          | 若 `db.useExisting` 為 `true`，則為包含憑證的 Kubernetes Secret 名稱。                                                                                                                                                                                               | `postgres`                                                                                 |
| `db.secret.usernameKey`   | 若 `db.useExisting` 為 `true`，則為 Kubernetes Secret 中保存 Postgres 驗證使用者名稱的鍵值 (key)。                                                                                                                                    | `username`                                                                                 |
| `db.secret.passwordKey`   | 若 `db.useExisting` 為 `true`，則為 Kubernetes Secret 中保存上述使用者密碼的鍵值 (key)。                                                                                                                                                   | `password`                                                                                 |
| `db.useStackgresOperator` | 尚未實作。                                                                                                                                                                                                                                                                      | `false`                                                                                    |
| `db.deployStandalone`     | 使用 Bitnami postgresql chart 部署獨立的單個 Postgres 實例。這適合快速入門，但不提供高可用性 (HA) 或（預設情況下）資料備份。                                                                                                  | `true`                                                                                     |
| `postgresql.*`            | 若 `db.deployStandalone` 為 `true`，則為傳遞給 Bitnami postgresql chart 的配置。完整配置細節請參閱 [Bitnami 文件](https://github.com/bitnami/charts/tree/main/bitnami/postgresql)。預設配置請參閱 [values.yaml](./values.yaml)。 | 請參閱 [values.yaml](./values.yaml)                                                           |
| `postgresql.auth.*`       | 若 `db.deployStandalone` 為 `true`，應注意確保**不**使用預設的 `password` 與 `postgres-password` 數值。                                                                                                                                                | `NoTaGrEaTpAsSwOrD`                                                                        |

#### Postgres `db.useExisting` Secret 範例

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres
data:
  # "postgres" 使用者的密碼
  postgres-password: <some secure password, base64 encoded>
  username: litellm
  password: <some secure password, base64 encoded>
type: Opaque
```

#### `environmentSecrets` 與 `environmentConfigMaps` 範例

```yaml
# 使用 config map 處理非機密的配置資料
apiVersion: v1
kind: ConfigMap
metadata:
  name: litellm-env-configmap
data:
  SOME_KEY: someValue
  ANOTHER_KEY: anotherValue
```

```yaml
# 使用 secrets 處理機密資料，如 API 金鑰、憑證等
# 將儲存在 Kubernetes Secret 中的數值進行 Base64 編碼：$ pbpaste | base64 | pbcopy
# --decode 旗標很方便：$ pbpaste | base64 --decode

apiVersion: v1
kind: Secret
metadata:
  name: litellm-env-secret
type: Opaque
data:
  SOME_PASSWORD: cDZbUGVXeU5e0ZW # base64 encoded
  ANOTHER_PASSWORD: AAZbUGVXeU5e0ZB # base64 encoded
```

來源：[GitHub Gist from troyharvey](https://gist.github.com/troyharvey/4506472732157221e04c6b15e3b3f094)

### 遷移作業 (Migration Job) 設定

遷移作業支援 ArgoCD 與 Helm hooks，以確保資料庫遷移在部署期間的適當時間執行。

| 名稱                                   | 描述                                                                                                          | 數值   |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------- |
| `migrationJob.enabled`                 | 啟用或停用結構描述 (schema) 遷移作業                                                                           | `true`  |
| `migrationJob.backoffLimit`            | 作業重試次數限制 (Backoff limit)                                                                                       | `4`     |
| `migrationJob.ttlSecondsAfterFinished` | 已完成遷移作業的存活時間 (TTL)                                                                                     | `120`   |
| `migrationJob.annotations`             | 遷移作業 pod 的額外註解 (annotations)                                                                     | `{}`    |
| `migrationJob.extraContainers`         | 與遷移作業一起執行的額外容器                                                             | `[]`    |
| `migrationJob.hooks.argocd.enabled`    | 啟用遷移作業的 ArgoCD hooks（使用 PreSync hook 及 BeforeHookCreation 刪除策略）                  | `true`  |
| `migrationJob.hooks.helm.enabled`      | 啟用遷移作業的 Helm hooks（使用 pre-install, pre-upgrade hooks 及 before-hook-creation 刪除策略） | `false` |
| `migrationJob.hooks.helm.weight`       | Helm hook 執行順序（權重越低越先執行）。選填 - 若未指定，預設為 "1"。               | N/A     |

## 存取 Admin UI

當瀏覽至根據 `ingress.*` 設定發佈的 URL 時，系統會提示您進行 **Admin Configuration**。**Proxy Endpoint** 是從 `litellm` pod 視角出發的內部 URL，由 `<RELEASE>-litellm` Kubernetes Service 發佈。若部署使用此服務的預設設定，則 **Proxy Endpoint** 應設定為 `http://<RELEASE>-litellm:4000`。

**Proxy Key** 是為 `masterkey` 指定的數值。若在 helm 命令行中未提供 `masterkey`，則 `masterkey` 將是一個隨機產生的 `sk-...` 格式字串，儲存在 `<RELEASE>-litellm-masterkey` Kubernetes Secret 中。

```bash
kubectl -n litellm get secret <RELEASE>-litellm-masterkey -o jsonpath="{.data.masterkey}"
```

## Admin UI 限制

在撰寫本文時，Admin UI 無法新增模型。這是因為它需要更新作為唯讀 ConfigMap 公開的 `config.yaml` 檔案。這是此 helm chart 的限制，而非 Admin UI 本身的限制。
