# Docker 開發指南

本指南提供使用 Docker 與 Docker Compose 建置與執行 LiteLLM 應用程式的說明。

## 先決條件

- Docker
- Docker Compose

## 建置與執行應用程式

若要建置並執行應用程式，您將使用位於專案根目錄的 `docker-compose.yml` 檔案。此檔案已配置為使用 `Dockerfile.non_root`，以提供安全的非 root (non-root) 容器環境。

### 1. 設定 Master Key

應用程式需要一個 `MASTER_KEY` 用於簽署與驗證 tokens。在執行應用程式之前，您必須將此金鑰設定為環境變數。

在專案根目錄建立一個 `.env` 檔案，並加入以下內容：

```
MASTER_KEY=your-secret-key
```

將 `your-secret-key` 替換為一個強大且隨機產生的密鑰。

### 2. 建置與執行容器

設定好 `MASTER_KEY` 後，您可以使用以下命令建置並執行容器：

```bash
docker compose up -d --build
```

此命令將：

-   使用 `Dockerfile.non_root` 建置 Docker 映像檔。
-   以分離模式 (`-d`, detached mode) 啟動 `litellm`、`litellm_db` 與 `prometheus` 服務。
-   `--build` 旗標確保在 Dockerfile 或應用程式程式碼有任何變更時，映像檔會重新建置。

### 3. 驗證應用程式是否正在執行

您可以使用以下命令檢查執行中容器的狀態 (status)：

```bash
docker compose ps
```

若要查看 `litellm` 容器的日誌 (logs)，請執行：

```bash
docker compose logs -f litellm
```

### 4. 停止應用程式

若要停止執行中的容器，請使用以下命令：

```bash
docker compose down
```

## 硬化 (Hardened) / 離線測試

為了確保變更對於非 root (non-root)、唯讀 root 檔案系統 (read-only rootfs) 以及受限出口 (restricted egress) 是安全的，請務必使用硬化過的 compose 檔案進行驗證：

```bash
docker compose -f docker-compose.yml -f docker-compose.hardened.yml build --no-cache
docker compose -f docker-compose.yml -f docker-compose.hardened.yml up -d
```

此設定：
- 從 `docker/Dockerfile.non_root` 建置，映像檔中已內置 Prisma engines 與 Node 工具鏈。
- 以非 root 使用者身份執行 proxy，使用唯讀 rootfs 並僅掛載可寫入的 tmpfs：
  - `/app/cache` (Prisma/NPM 快取；支援 `PRISMA_BINARY_CACHE_DIR`、`NPM_CONFIG_CACHE`、`XDG_CACHE_HOME`)
  - `/app/migrations` (Prisma 遷移工作區；支援 `LITELLM_MIGRATION_DIR`)
- 預先建置並從唯讀路徑提供 admin UI：
  - `/var/lib/litellm/ui` (預先重組且帶有 `.litellm_ui_ready` 標記的 Next.js UI)
  - `/var/lib/litellm/assets` (UI 標誌與資產)
- 將所有對外流量導向本地 Squid proxy 並拒絕出口 (egress)，因此 Prisma 遷移必須使用快取中的 CLI 與 engines。

您還應該使用以下命令驗證離線 Prisma 行為：

```bash
docker run --rm --network none --entrypoint prisma ghcr.io/berriai/litellm:main-stable --version
```

即使使用 `--network none`，此命令也應該成功（顯示引擎版本），確認 Prisma 二進制檔案在沒有網路存取的情況下仍可使用。

## 疑難排解 (Troubleshooting)

-   **`build_admin_ui.sh: not found`**: 如果 Docker 建置上下文 (context) 設定不正確，可能會發生此錯誤。請確保您是在專案根目錄下執行 `docker compose` 命令。
-   **`Master key is not initialized`**: 此錯誤表示未設定 `MASTER_KEY` 環境變數。請確保您已在專案根目錄建立了包含 `MASTER_KEY` 定義的 `.env` 檔案。
