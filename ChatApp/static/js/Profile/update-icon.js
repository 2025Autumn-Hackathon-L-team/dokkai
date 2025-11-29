/*　アイコンを更新するモーダルの制御　*/

const updateIconButton = document.getElementById("update-icon-button");
const updateIconModal = document.getElementById("update-icon-modal");
const updateIconButtonClose = document.getElementById("update-icon-close-button");
const iconArea = document.getElementById("icon-area");
const paginationContainer = document.getElementById("pagination_icon");

// モーダルが存在するページのみ
if (updateIconModal) {
  // モーダル表示ボタンが押された時にモーダルを表示する
  updateIconButton.addEventListener("click", () => {
    updateIconModal.style.display = "flex";
  });

  // モーダル内のXボタンが押された時にモーダルを非表示にする
  updateIconButtonClose.addEventListener("click", () => {
    updateIconModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == updateIconModal) {
      updateIconModal.style.display = "none";
    }
  });
}

// app.pyのprofile_icons_js関数を実行して、json形式のデータをもらう
async function loadIcons(page = 1) {
  const iconresponse = await fetch(`/profile/icons?page=${page}`, { cache: "no-store" });
  const data = await iconresponse.json();
  
  // モーダル内に表示を取得した要素に置き換える
  renderIcons(data.icons);
  renderPagination(data.page, data.total_pages);
}

// アイコン一覧を取得し、innerHTMLに入れて新しいHTMLの配列を作成しHTML上に返す（モーダル内の表示を差し替える）
function renderIcons(icons) {
  iconArea.innerHTML = icons.map(icon => `
    <button class="icon_styled" type="submit" name="icon_name" value="${icon.id}">
      <img class="icon-image" src="${icon.icon_image}" alt="${icon.icon_name}">
    </button>
  `).join("");
}

// モーダル内にページ番号を表示
function renderPagination(current, total) {
  paginationContainer.innerHTML = ""; // ページ番号を描画するところを一旦リセットする。
  if (total <= 1) return; // 総ページが１ページ以下ならページネーション不要。そのまま返す。

  // ページネーションのボタン
  for (let pagenumber = 1; pagenumber <= total; pagenumber++) {
    const btn = document.createElement("button"); // ボタンを作成
    btn.className = "page-btn";
    btn.textContent = pagenumber;
    if (pagenumber === current) btn.classList.add("active"); // 現在のページをアクティブにする
    btn.addEventListener("click", () => loadIcons(pagenumber)); // ボタンをクリックするとそのページのアイコンだけ読み込む
    paginationContainer.appendChild(btn); // 作ったボタンをHTMLに追加
  }
}

// モーダルが開いたら 1ページ目表示
updateIconButton.addEventListener("click", () => {
  updateIconModal.style.display = "flex";
  loadIcons(1);
});
