#!/bin/bash

# スクリプトがエラーで停止するように設定
set -e

# --- 色定義 (ターミナル出力を見やすくするため) ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# --- スクリプト本体 ---

echo -e "${GREEN}### Docker DNS設定修正スクリプトを開始します ###${NC}"

# 1. ルート権限で実行されているかチェック
if [ "$(id -u)" -ne 0 ]; then
  echo -e "${RED}エラー: このスクリプトは管理者権限で実行する必要があります。${NC}"
  echo -e "${YELLOW}コマンドの前に 'sudo' をつけて実行してください: sudo ./fix_docker_dns.sh${NC}"
  exit 1
fi

# 2. jqがインストールされているかチェック
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}JSON編集ツール 'jq' が見つかりません。インストールします...${NC}"
    apt-get update
    apt-get install -y jq
    echo -e "${GREEN}'jq' のインストールが完了しました。${NC}"
fi

# 3. Dockerの設定ファイルを定義
DAEMON_JSON_FILE="/etc/docker/daemon.json"
TEMP_FILE="/etc/docker/daemon.json.tmp"
DNS_SERVERS='["8.8.8.8", "8.8.4.4"]'

echo "Docker設定ファイル: ${DAEMON_JSON_FILE} を確認・更新します..."

# 4. daemon.jsonファイルの状態に応じて処理を分岐
if [ ! -f "$DAEMON_JSON_FILE" ] || [ ! -s "$DAEMON_JSON_FILE" ]; then
  # ファイルが存在しない、または空の場合
  echo "ファイルが存在しないか空のため、新しい設定ファイルを作成します。"
  echo "{}" | jq --argjson dns "$DNS_SERVERS" '. + {dns: $dns}' > "$DAEMON_JSON_FILE"
  echo "作成された内容:"
  cat "$DAEMON_JSON_FILE"
else
  # ファイルが存在し、中身がある場合
  echo "既存の設定ファイルにDNS設定をマージします。"
  # 既存のDNS設定があるか確認
  if cat "$DAEMON_JSON_FILE" | jq -e '.dns' > /dev/null; then
    echo "既にDNS設定が存在するため、上書きします。"
  else
    echo "新しいDNS設定を追加します。"
  fi
  # jqを使って既存の設定とDNS設定をマージし、一時ファイルに書き出す
  jq --argjson dns "$DNS_SERVERS" '. + {dns: $dns}' "$DAEMON_JSON_FILE" > "$TEMP_FILE"
  
  # 一時ファイルで元のファイルを上書き
  mv "$TEMP_FILE" "$DAEMON_JSON_FILE"
  
  echo "更新後の内容:"
  cat "$DAEMON_JSON_FILE"
fi

# 5. Dockerサービスを再起動して設定を反映
echo -e "${YELLOW}Dockerサービスを再起動して設定を適用します...${NC}"
systemctl restart docker
echo -e "${GREEN}Dockerの再起動が完了しました。${NC}"

# 6. 完了メッセージ
echo ""
echo -e "${GREEN}✅ DockerのDNS設定が正常に完了しました！${NC}"
echo -e "${YELLOW}VS Codeに戻り、'F1'キーから 'Dev Containers: Rebuild and Reopen in Container' を実行してください。${NC}"