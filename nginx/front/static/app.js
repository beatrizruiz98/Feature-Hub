(function () {
  // ==== CONFIG ====
  const API_BASE = ""; // ajusta si usas /api

  // ==== I18N ====
  const translations = {
    en: {
      brand_sub: "Lightweight UI for your FastAPI backend",
      status_signed_out: "Not signed in",
      status_signed_in: "Signed in as {name}",
      logout_btn: "Log out",
      info_bar_text:
        "This UI is wired to your API (/auth/*, /features, /likes, /comments). If the API is down, data will not be available.",
      demo_toggle: "Demo data",
      tab_feed: "Feed",
      tab_myspace: "My space",

      features_title: "Features",
      features_subtitle: "Home feed from GET /features",
      refresh_btn: "Refresh",
      search_label: "Search (title & description)",
      search_placeholder: "Search features",
      owner_label: "Owner",
      owner_all: "All",
      owner_me: "Mine",

      myspace_title: "My space",
      myspace_subtitle: "Your features and comments",
      myspace_login_hint: "Log in to see your profile and content.",

      account_title: "Account",
      account_subtitle: "Sign up, log in and manage your content",
      login_tab: "Login",
      signup_tab: "Sign up",
      login_username_label: "Email",
      login_username_placeholder: "you@example.com",
      login_password_label: "Password",
      login_password_placeholder: "Your password",
      login_btn: "Log in",
      login_helper: "Calls POST /auth/login (OAuth2 password form).",
      signup_email_label: "Email",
      signup_email_placeholder: "you@example.com",
      signup_username_label: "Name (optional)",
      signup_username_placeholder: "username",
      signup_password_label: "Password",
      signup_password_placeholder: "Choose a password",
      signup_repeat_label: "Repeat password",
      signup_repeat_placeholder: "Repeat password",
      signup_btn: "Create account",
      signup_helper: "Calls POST /auth/register.",
      new_feature_title: "New feature",
      new_feature_subtitle: "Create features via POST /features",
      feature_title_label: "Title",
      feature_title_placeholder: "Short, clear title",
      feature_desc_label: "Description",
      feature_desc_placeholder: "Explain what you want to add or change",
      feature_submit_btn: "Submit feature",
      feature_helper:
        "Requires authentication with Authorization: Bearer <token>.",

      feed_empty: "No features found. Be the first to create one.",
      feed_loading: "Loading features…",
      comments_loading: "Loading comments…",
      comments_empty: "No comments yet.",
      comments_error_generic: "Error loading comments",
      features_error_generic: "Error loading features",
      feature_meta_created: " ",
      comment_meta_user: "User comment",

      btn_like: "Like",
      btn_view_comments: "View comments",
      btn_hide_comments: "Hide comments",
      modal_comment_label: "Comment",
      modal_comment_placeholder: "Write your thoughts",
      modal_comment_submit: "Post comment",

      toast_like: "Like registered",
      toast_demo_on: "Demo mode enabled",
      toast_demo_off: "Demo mode disabled – using real API",
      toast_logged_out: "Logged out",
      toast_comment_posted: "Comment posted",
      toast_title_required: "Title and description are required",
      toast_login_required_feature:
        "You need to log in to create or edit a feature",
      toast_login_required_like: "Log in to like features",
      toast_login_required_comment: "Log in to comment",
      toast_signup_demo:
        "Signup simulated in demo mode. Use login to continue.",
      toast_login_demo: "Logged in (demo mode)",
      toast_login_success: "Logged in successfully",
      toast_session_expired: "Session expired, please log in again",
      toast_passwords_mismatch: "Passwords do not match",
      toast_credentials_required: "Username and password are required",
      toast_email_password_required: "Email and password are required",
      toast_comment_empty: "Comment cannot be empty",
      toast_feature_created: "Feature created",
    },
    es: {
      brand_sub: "Interfaz ligera para tu backend FastAPI",
      status_signed_out: "Sin sesión",
      status_signed_in: "Sesión iniciada como {name}",
      logout_btn: "Cerrar sesión",
      info_bar_text:
        "Esta UI se conecta a tu API (/auth/*, /features, /likes, /comments). Si la API no responde, no habrá datos disponibles.",
      demo_toggle: "Datos demo",
      tab_feed: "Feed",
      tab_myspace: "Mi espacio",

      features_title: "Features",
      features_subtitle: "Feed principal desde GET /features",
      refresh_btn: "Refrescar",
      search_label: "Buscar (título y descripción)",
      search_placeholder: "Buscar features",
      owner_label: "Propietario",
      owner_all: "Todos",
      owner_me: "Míos",

      myspace_title: "Mi espacio",
      myspace_subtitle: "Tus features y comentarios",
      myspace_login_hint: "Inicia sesión para ver tu perfil y contenido.",

      account_title: "Cuenta",
      account_subtitle:
        "Regístrate, inicia sesión y gestiona tu contenido",
      login_tab: "Iniciar sesión",
      signup_tab: "Registro",
      login_username_label: "Email",
      login_username_placeholder: "tu@ejemplo.com",
      login_password_label: "Contraseña",
      login_password_placeholder: "Tu contraseña",
      login_btn: "Entrar",
      login_helper: "Llama a POST /auth/login (OAuth2 password form).",
      signup_email_label: "Email",
      signup_email_placeholder: "tu@ejemplo.com",
      signup_username_label: "Nombre",
      signup_username_placeholder: "usuario",
      signup_password_label: "Contraseña",
      signup_password_placeholder: "Elige una contraseña",
      signup_repeat_label: "Repite contraseña",
      signup_repeat_placeholder: "Repite la contraseña",
      signup_btn: "Crear cuenta",
      signup_helper: "Llama a POST /auth/register.",
      new_feature_title: "Nueva feature",
      new_feature_subtitle: "Crea features con POST /features",
      feature_title_label: "Título",
      feature_title_placeholder: "Título breve y claro",
      feature_desc_label: "Descripción",
      feature_desc_placeholder: "Explica qué quieres añadir o cambiar",
      feature_submit_btn: "Crear feature",
      feature_helper:
        "Requiere autenticación con Authorization: Bearer <token>.",

      feed_empty: "No hay features. Sé la primera en crear una.",
      feed_loading: "Cargando features…",
      comments_loading: "Cargando comentarios…",
      comments_empty: "Todavía no hay comentarios.",
      comments_error_generic: "Error al cargar los comentarios",
      features_error_generic: "Error al cargar las features",
      feature_meta_created: " ",
      comment_meta_user: "Comentario de usuario",

      btn_like: "Like",
      btn_view_comments: "Ver comentarios",
      btn_hide_comments: "Ocultar comentarios",
      modal_comment_label: "Comentario",
      modal_comment_placeholder: "Escribe lo que piensas",
      modal_comment_submit: "Publicar comentario",

      toast_like: "Like registrado",
      toast_demo_on: "Modo demo activado",
      toast_demo_off: "Modo demo desactivado – usando API real",
      toast_logged_out: "Sesión cerrada",
      toast_comment_posted: "Comentario publicado",
      toast_title_required: "Título y descripción son obligatorios",
      toast_login_required_feature:
        "Necesitas iniciar sesión para crear o editar una feature",
      toast_login_required_like: "Inicia sesión para dar like",
      toast_login_required_comment: "Inicia sesión para comentar",
      toast_signup_demo:
        "Registro simulado en modo demo. Usa login para continuar.",
      toast_login_demo: "Sesión iniciada (modo demo)",
      toast_login_success: "Sesión iniciada correctamente",
      toast_session_expired:
        "La sesión ha caducado, vuelve a iniciar sesión",
      toast_passwords_mismatch: "Las contraseñas no coinciden",
      toast_credentials_required:
        "Usuario y contraseña son obligatorios",
      toast_email_password_required:
        "Email y contraseña son obligatorios",
      toast_comment_empty: "El comentario no puede estar vacío",
      toast_feature_created: "Feature creada",
    },
  };

  let currentLang = "en";
  // let accessToken = localStorage.getItem("featurehub_token") || null;
  let currentUser = null;

  // ==== HELPERS ====
  function t(key) {
    const pack = translations[currentLang] || translations.en;
    return pack[key] || translations.en[key] || key;
  }

  function applyTranslations() {
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      if (!key) return;
      el.textContent = t(key);
    });
    document
      .querySelectorAll("[data-i18n-placeholder]")
      .forEach((el) => {
        const key = el.getAttribute("data-i18n-placeholder");
        if (!key) return;
        el.placeholder = t(key);
      });
    updateAuthStatusText();
  }

  function showToast(keyOrText, isError = false, isKey = true) {
    const toast = document.getElementById("toast");
    if (!toast) return;
    const text = isKey ? t(keyOrText) : keyOrText;
    toast.textContent = text;
    toast.classList.toggle("error", isError);
    toast.style.display = "block";
    setTimeout(() => {
      toast.style.display = "none";
    }, 2500);
  }

  function updateAuthStatusText() {
    const statusEl = document.getElementById("auth-status");
    if (!statusEl) return;
    if (accessToken && currentUser) {
      const name =
        currentUser.email || currentUser.username || currentUser.id || "me";
      statusEl.textContent = t("status_signed_in").replace("{name}", name);
    } else {
      statusEl.textContent = t("status_signed_out");
    }
  }

  function setToken(token) {
    accessToken = token;
    if (token) localStorage.setItem("featurehub_token", token);
    else localStorage.removeItem("featurehub_token");
    updateAuthUI();
  }

  function authHeaders() {
    if (!accessToken) return {};
    return { Authorization: `Bearer ${accessToken}` };
  }

  async function apiFetch(path, options = {}) {
    const url = `${API_BASE}${path}`;
    const headers = {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    };
    const resp = await fetch(url, { ...options, headers });
    let data = null;
    try {
      data = await resp.json();
    } catch {
      data = null;
    }
    if (!resp.ok) {
      const detail = data && data.detail ? data.detail : resp.statusText;
      throw new Error(detail || "Request failed");
    }
    return data;
  }

  function updateAuthUI() {
    const logoutBtn = document.getElementById("logout-btn");
    const newFeatureForm = document.getElementById("new-feature-form");
    const controls = newFeatureForm
      ? newFeatureForm.querySelectorAll("input, textarea, button")
      : [];

    if (accessToken && currentUser) {
      if (logoutBtn) logoutBtn.style.display = "inline-flex";
      controls.forEach((el) => {
        el.disabled = false;
      });
    } else {
      if (logoutBtn) logoutBtn.style.display = "none";
      controls.forEach((el) => {
        el.disabled = true;
      });
    }
    updateAuthStatusText();
  }

  // ==== FEED ====
  function renderFeatures(features) {
    const list = document.getElementById("feature-list");
    if (!list) return;
    list.innerHTML = "";
    if (!features || !features.length) {
      list.innerHTML = `<div class="feature-empty">${t("feed_empty")}</div>`;
      return;
    }

    features.forEach((feature) => {
      const card = document.createElement("article");
      card.className = "feature-card";

      const header = document.createElement("div");
      header.className = "feature-header";

      const titleBlock = document.createElement("div");
      const title = document.createElement("div");
      title.className = "feature-title feature-title-link";
      title.textContent = feature.title;
      title.addEventListener("click", () => openFeatureModal(feature.id));

      const meta = document.createElement("div");
      meta.className = "feature-meta";
      meta.textContent = t("feature_meta_created");

      titleBlock.appendChild(title);
      titleBlock.appendChild(meta);

      const stats = document.createElement("div");
      stats.className = "feature-stats";

      const likesSpan = document.createElement("span");
      likesSpan.textContent = `❤ ${feature.likes ?? 0}`;

      const commentsSpan = document.createElement("span");
      const cc = feature.comments_count ?? 0;
      commentsSpan.textContent = `💬 ${cc}`;
      commentsSpan.dataset.role = "comments-count";
      commentsSpan.dataset.featureId = String(feature.id);

      stats.appendChild(likesSpan);
      stats.appendChild(commentsSpan);

      header.appendChild(titleBlock);
      header.appendChild(stats);

      const desc = document.createElement("div");
      desc.className = "feature-description";
      desc.textContent = feature.description || "";

      const actions = document.createElement("div");
      actions.className = "feature-actions";

      const likeBtn = document.createElement("button");
      likeBtn.className = "btn-icon";
      likeBtn.innerHTML = `<span>❤</span><span>${t("btn_like")}</span>`;
      likeBtn.addEventListener("click", () => toggleLike(feature.id));

      const commentsToggle = document.createElement("div");
      commentsToggle.className = "comments-toggle";
      commentsToggle.textContent = t("btn_view_comments");

      const commentsSection = document.createElement("div");
      commentsSection.className = "comments-section";

      commentsToggle.addEventListener("click", async () => {
        if (commentsSection.style.display === "flex") {
          commentsSection.style.display = "none";
          commentsToggle.textContent = t("btn_view_comments");
          return;
        }
        commentsSection.style.display = "flex";
        commentsToggle.textContent = t("btn_hide_comments");
        await loadCommentsForFeature(feature.id, commentsSection);
      });

      actions.appendChild(likeBtn);
      actions.appendChild(commentsToggle);

      card.appendChild(header);
      card.appendChild(desc);
      card.appendChild(actions);
      card.appendChild(commentsSection);

      list.appendChild(card);
    });
  }

  async function loadFeatures() {
    const list = document.getElementById("feature-list");
    if (!list) return;

    // No token => no feed
    if (!accessToken) {
      showToast("toast_login_required_feature", true);
      list.innerHTML = `<div class="feature-empty">${t(
        "myspace_login_hint"
      )}</div>`;
      return;
    }

    list.innerHTML = `<div class="feature-empty">${t(
      "feed_loading"
    )}</div>`;

    const search = (
      document.getElementById("search-input")?.value || ""
    )
      .trim()
      .toLowerCase();
    const ownerFilter =
      document.getElementById("owner-filter")?.value || "all";

    // Owner "me" requiere auth (y ya lo hemos comprobado arriba)
    try {
      const params = new URLSearchParams();
      if (search) params.append("search", search);
      if (ownerFilter === "me") params.append("owner", "me");
      const data = await apiFetch(
        `/features?${params.toString()}`,
        { headers: authHeaders() }
      );
      const items = data.data || data.items || [];
      renderFeatures(items);
    } catch (e) {
      list.innerHTML = `<div class="feature-empty">${t(
        "features_error_generic"
      )}: ${e.message}</div>`;
    }
  }

  // ==== COMMENTS ====

  function extractCommentText(c) {
    if (c.body) return c.body;
    if (c.content) return c.content;
    if (c.comment) return c.comment;
    if (c.text) return c.text;
    return JSON.stringify(c);
  }

  function renderCommentsList(comments, container, featureId) {
    console.log("Rendering comments for feature", featureId, comments);
    container.innerHTML = "";

    if (!comments || !comments.length) {
      container.innerHTML = `<div class="helper-text">${t(
        "comments_empty"
      )}</div>`;
      const badgeEmpty = document.querySelector(
        `[data-role="comments-count"][data-feature-id="${String(featureId)}"]`
      );
      if (badgeEmpty) badgeEmpty.textContent = "💬 0";
      return;
    }

    const stack = document.createElement("div");
    stack.className = "stack";

    comments.forEach((c) => {
      const item = document.createElement("div");
      item.className = "comment-item";

      const body = document.createElement("div");
      body.className = "comment-body";
      body.textContent = extractCommentText(c);
      body.title = JSON.stringify(c); // debug

      item.appendChild(body);
      stack.appendChild(item);
    });

    container.appendChild(stack);

    const badge = document.querySelector(
      `[data-role="comments-count"][data-feature-id="${String(featureId)}"]`
    );
    if (badge) {
      badge.textContent = `💬 ${comments.length}`;
    }
  }

  async function loadCommentsForFeature(featureId, container) {
    container.innerHTML = `<div class="helper-text">${t(
      "comments_loading"
    )}</div>`;
    try {
      const data = await apiFetch(
        `/features/${featureId}/comments`,
        { headers: authHeaders() }
      );
      const comments = Array.isArray(data) ? data : data.data || [];
      renderCommentsList(comments, container, featureId);
    } catch (e) {
      container.innerHTML = `<div class="helper-text">${t(
        "comments_error_generic"
      )}: ${e.message}</div>`;
    }
  }

  // ==== LIKES ====
  async function toggleLike(featureId) {
    if (!accessToken) {
      showToast("toast_login_required_like", true);
      return;
    }
    try {
      await apiFetch("/likes", {
        method: "POST",
        headers: { ...authHeaders() },
        body: JSON.stringify({ feature_id: featureId, dir: 1 }),
      });
      showToast("toast_like", false);
      loadFeatures();
    } catch (e) {
      showToast(e.message, true, false);
    }
  }

  // ==== MODAL DETALLE ====
  function openFeatureModal(featureId) {
    const backdrop = document.getElementById("modal-backdrop");
    if (!backdrop) return;
    loadFeatureDetail(featureId);
    backdrop.style.display = "flex";
  }

  function closeFeatureModal() {
    const backdrop = document.getElementById("modal-backdrop");
    if (!backdrop) return;
    backdrop.style.display = "none";
  }

  async function loadFeatureDetail(featureId) {
    const modalTitle = document.getElementById("modal-title");
    const modalContent = document.getElementById("modal-content");
    const modalComments = document.getElementById("modal-comments");
    const modalNewComment = document.getElementById("modal-new-comment");

    if (!modalTitle || !modalContent || !modalComments || !modalNewComment)
      return;

    modalTitle.textContent = "Feature";
    modalContent.innerHTML = t("feed_loading");
    modalComments.innerHTML = "";
    modalNewComment.innerHTML = "";

    try {
      const data = await apiFetch(`/features/${featureId}`, {
        headers: authHeaders(),
      });
      const feature = data.data || data;

      if (!feature) {
        modalContent.textContent = t("features_error_generic");
        return;
      }

      modalTitle.textContent = feature.title;
      modalContent.innerHTML = `
        <div class="tag-pill">${t("feature_meta_created")}</div>
        <p style="margin-top:6px;">${feature.description || ""}</p>
      `;

      modalComments.innerHTML = `<div class="helper-text">${t(
        "comments_loading"
      )}</div>`;

      const dataComments = await apiFetch(
        `/features/${featureId}/comments`,
        { headers: authHeaders() }
      );
      const comments = Array.isArray(dataComments)
        ? dataComments
        : dataComments.data || [];
      renderCommentsList(comments, modalComments, featureId);

      const canComment = !!accessToken;
      if (canComment) {
        modalNewComment.innerHTML = `
          <label for="modal-comment-input">${t(
            "modal_comment_label"
          )}</label>
          <textarea id="modal-comment-input" placeholder="${t(
            "modal_comment_placeholder"
          )}"></textarea>
          <button id="modal-comment-submit" class="btn-icon">
            <span>💬</span><span>${t(
              "modal_comment_submit"
            )}</span>
          </button>
        `;
        const btn = document.getElementById("modal-comment-submit");
        if (btn) {
          btn.addEventListener("click", async () => {
            const textarea =
              document.getElementById("modal-comment-input");
            const content =
              (textarea && textarea.value.trim()) || "";
            if (!content) {
              showToast("toast_comment_empty", true);
              return;
            }
            try {
              if (!accessToken) {
                showToast(
                  "toast_login_required_comment",
                  true
                );
                return;
              }
              await apiFetch("/comments", {
                method: "POST",
                headers: { ...authHeaders() },
                body: JSON.stringify({
                  feature_id: featureId,
                  body: content,
                }),
              });

              showToast("toast_comment_posted", false);
              if (textarea) textarea.value = "";
              await loadFeatureDetail(featureId);
            } catch (e) {
              showToast(e.message, true, false);
            }
          });
        }
      } else {
        modalNewComment.innerHTML = `<div class="helper-text">${t(
          "toast_login_required_comment"
        )}</div>`;
      }
    } catch (e) {
      modalContent.textContent = `${t(
        "features_error_generic"
      )}: ${e.message}`;
    }
  }

  // ==== AUTH (login/signup + new feature) ====
  function wireAuthForms() {
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");
    const authTabs = document.querySelectorAll(".tab-auth");

    authTabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        authTabs.forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");
        const target = tab.getAttribute("data-tab");
        if (target === "signup") {
          if (loginForm) loginForm.style.display = "none";
          if (signupForm) signupForm.style.display = "flex";
        } else {
          if (loginForm) loginForm.style.display = "flex";
          if (signupForm) signupForm.style.display = "none";
        }
      });
    });

    // Login
    if (loginForm) {
      loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const userInput = document.getElementById("login-username");
        const passInput = document.getElementById("login-password");
        const username = userInput ? userInput.value.trim() : "";
        const password = passInput ? passInput.value : "";

        if (!username || !password) {
          showToast("toast_credentials_required", true);
          return;
        }

        try {
          const body = new URLSearchParams();
          body.append("username", username);
          body.append("password", password);
          const resp = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
            body,
          });
          const data = await resp.json().catch(() => null);
          if (!resp.ok || !data || !data.access_token) {
            throw new Error((data && data.detail) || "Login failed");
          }
          setToken(data.access_token);
          showToast("toast_login_success", false);

          try {
            const me = await apiFetch("/auth/me", {
              headers: authHeaders(),
            });
            currentUser = me;
          } catch {
            currentUser = { id: "me", email: username };
          }
          updateAuthUI();
          loadFeatures();
        } catch (e2) {
          showToast(e2.message, true, false);
        }
      });
    }

    // Signup
    if (signupForm) {
      signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const emailInput = document.getElementById("signup-email");
        const userInput = document.getElementById("signup-username");
        const pass1 = document.getElementById("signup-password");
        const pass2 = document.getElementById("signup-password2");

        const email = emailInput ? emailInput.value.trim() : "";
        const name = userInput ? userInput.value.trim() : "";
        const p1 = pass1 ? pass1.value : "";
        const p2 = pass2 ? pass2.value : "";

        if (!email || !p1) {
          showToast("toast_email_password_required", true);
          return;
        }
        if (p1 !== p2) {
          showToast("toast_passwords_mismatch", true);
          return;
        }

        try {
          const payload = { email, password: p1 };
          if (name) payload.name = name;
          await apiFetch("/auth/register", {
            method: "POST",
            body: JSON.stringify(payload),
          });
          showToast("signup_btn", false);
          const loginTab = document.querySelector(
            '.tab-auth[data-tab="login"]'
          );
          if (loginTab) loginTab.click();
        } catch (e2) {
          showToast(e2.message, true, false);
        }
      });
    }

    // New feature
    const newFeatureForm = document.getElementById("new-feature-form");
    if (newFeatureForm) {
      newFeatureForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const titleInput = document.getElementById("feature-title");
        const descInput =
          document.getElementById("feature-description");
        const title = titleInput ? titleInput.value.trim() : "";
        const description = descInput
          ? descInput.value.trim()
          : "";

        if (!title || !description) {
          showToast("toast_title_required", true);
          return;
        }

        try {
          if (!accessToken) {
            showToast("toast_login_required_feature", true);
            return;
          }
          await apiFetch("/features", {
            method: "POST",
            headers: { ...authHeaders() },
            body: JSON.stringify({ title, description }),
          });

          showToast("toast_feature_created", false);
          if (titleInput) titleInput.value = "";
          if (descInput) descInput.value = "";
          loadFeatures();
        } catch (e2) {
          showToast(e2.message, true, false);
        }
      });
    }

    // Logout
    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", () => {
        setToken(null);
        currentUser = null;
        showToast("toast_logged_out", false);
        const list = document.getElementById("feature-list");
        if (list) {
          list.innerHTML = `<div class="feature-empty">${t(
            "myspace_login_hint"
          )}</div>`;
        }
      });
    }
  }

  // ==== INIT ====
  document.addEventListener("DOMContentLoaded", () => {
    // Tabs Feed / My space
    const tabsMain = document.querySelectorAll(".tab-main");
    const feedPanel = document.getElementById("feed-panel");
    const myspacePanel = document.getElementById("myspace-panel");
    tabsMain.forEach((tab) => {
      tab.addEventListener("click", () => {
        tabsMain.forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");
        const target = tab.getAttribute("data-main-tab");
        if (target === "myspace") {
          if (feedPanel) feedPanel.style.display = "none";
          if (myspacePanel) myspacePanel.style.display = "block";
        } else {
          if (feedPanel) feedPanel.style.display = "block";
          if (myspacePanel) myspacePanel.style.display = "none";
        }
      });
    });

    // Lang switch
    const langSwitch = document.getElementById("lang-switch");
    if (langSwitch) {
      langSwitch.value = currentLang;
      langSwitch.addEventListener("change", () => {
        currentLang = langSwitch.value || "en";
        applyTranslations();
      });
    }

    // Refresh
    const refreshBtn = document.getElementById("refresh-features-btn");
    if (refreshBtn) {
      refreshBtn.addEventListener("click", () => {
        loadFeatures();
      });
    }

    // Search
    const searchInput = document.getElementById("search-input");
    if (searchInput) {
      searchInput.addEventListener("input", () => {
        clearTimeout(window.__fhSearchTimer);
        window.__fhSearchTimer = setTimeout(
          () => loadFeatures(),
          220
        );
      });
    }

    // Owner filter
    const ownerFilter = document.getElementById("owner-filter");
    if (ownerFilter) {
      ownerFilter.addEventListener("change", () => loadFeatures());
    }

    // Modal close
    const modalClose = document.getElementById("modal-close");
    const modalBackdrop = document.getElementById("modal-backdrop");
    if (modalClose) {
      modalClose.addEventListener("click", closeFeatureModal);
    }
    if (modalBackdrop) {
      modalBackdrop.addEventListener("click", (e) => {
        if (e.target === modalBackdrop) closeFeatureModal();
      });
    }

    // Auth
    wireAuthForms();

    // i18n + estado
    applyTranslations();
    updateAuthUI();
    // No cargamos feed hasta que haya login
    const list = document.getElementById("feature-list");
    if (list && !accessToken) {
      list.innerHTML = `<div class="feature-empty">${t(
        "myspace_login_hint"
      )}</div>`;
    } else if (accessToken) {
      loadFeatures();
    }
  });
})();
