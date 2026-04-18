const DATA_VERSION = "20260418-text4";

const DATA_PATHS = Array.from({ length: 10 }, (_, index) =>
  `../data/asakusa_omikuji_part${String(index + 1).padStart(2, "0")}.json?v=${DATA_VERSION}`,
);

const FORTUNE_BUCKETS = {
  大吉: "upper",
  吉: "upper",
  小吉: "middle",
  半吉: "middle",
  末吉: "middle",
  末小吉: "middle",
  凶: "lower",
};

const DRAW_SUMMARIES = {
  upper: "此签气象偏明，路数可开，但越在顺意处，越要守住分寸。",
  middle: "此签不是骤然开门，而是缓缓见光，宜稳住心气，不可躁进。",
  lower: "此签气象偏峭，不利强推，更像提醒你先止躁、避失、收束脚步。",
};

const REDRAW_ELIGIBLE = new Set(["凶", "半吉", "末吉", "末小吉"]);

const REDRAW_INVITATIONS = {
  凶: "这一签若你不愿强留，可把它视作替你拦下一段逆气。若愿意，便行一回纳签重请，再请新签。",
  default:
    "这一签若仍叫你心中发紧，也不必强留。可将旧签纳去，再请一签，换一重心气与路数。",
};

const REDRAW_RITUAL_TEXT =
  "销签不是抹去已经发生的事，而是把旧签所示的滞、急、逆，留在纸上，从此不再携它同行。";

const REDRAW_SHIFT_TEXTS = {
  upper:
    "新签偏明，表示此后这一路更宜守正而行。改写的不是过去，而是你从此刻起的步法与气象。",
  middle:
    "新签转平，表示局面虽未大开，却已从逼仄转为可缓、可调、可扶正。改的是此后的行路之势。",
  lower:
    "新签仍峭，也不必再逼着翻转。它提醒你今日之意在止，不在争；真正的转势，是肯把脚步收稳。",
};

const OPENING_TEMPLATES = [
  "先把杂念放低一些，如晨烟拂过浅草的木檐，把一路行来的喧声都压得远了一层。签筒已静，木签未启，此刻不必急着向前，只需把心慢慢收拢。然后，我们来请这一签。",
  "不必多言，也不必先分辨吉凶。世间许多未定之事，此刻都可以先放在阶前，让香意替你压一压心上的浮动。你只管定住片刻，让木签先替你说话。",
  "世事先放在阶前，香意未散，签意未明，檐下的风也像比别处更轻一些。此刻不问来处，不问归处，只做一件事，轻轻启这一签。",
  "风从雷门外过，尘声渐歇，像有人把一整日的杂念都缓缓拂落。你不必急着把心事说破，只需把目光放低，把呼吸放稳。余下的，交给这一支签来开口。",
];

const REVEAL_TEMPLATES = [
  "签筒既启，你得的是：第{signNo}签 · {fortuneName}",
  "木签已出，眼前这一签是：第{signNo}签 · {fortuneName}",
  "檐下启签，所得如下：第{signNo}签 · {fortuneName}",
  "这一回落在你手中的，是：第{signNo}签 · {fortuneName}",
];

const DRAW_CLOSING_TEMPLATES = [
  "签意已明，路仍在你脚下。今日记得把心放稳一些。",
  "这一签照见的，不只是吉凶，也是在提醒你行路的姿势。",
  "若你信它，不妨信它替你拂去了一点浮躁，余下的路，再慢慢走。",
  "签纸至此可以轻轻收起，真正要走的路，仍要你自己一步一步踏稳。",
];

const REDRAW_OPENING_TEMPLATES = [
  "旧签至此纳去，不再贴身。我们不问前尘，只问从这一刻起，路怎样改向。",
  "前一签已留在纸上，随香火一并安放。此刻重请，不为否认过去，只为另开一路。",
  "旧签已纳，旧气不再随身。如今再启一回，只看此后该如何行路。",
];

const REDRAW_REVEAL_TEMPLATES = [
  "再启木签，新意已至：第{signNo}签 · {fortuneName}",
  "销签之后，重新落下的是：第{signNo}签 · {fortuneName}",
  "旧纸已留，新签已明：第{signNo}签 · {fortuneName}",
];

const REDRAW_CLOSING_TEMPLATES = [
  "旧签已留于旧纸，新意便从此刻起算。往后这一程，记得照着新签的气象去走。",
  "命不在一纸之间骤然改写，真正转过去的，是你从此刻起携带的心与步。",
  "销去的，是不必再背的旧滞；留下的，是此后可慢慢扶正的新路数。",
];

const DEFAULT_STATUS =
  "风从雷门外过，尘声渐歇。若你愿意，请先步入签前，再启一支签。";

const INSTALL_COPY = {
  ios:
    "在苹果手机或平板上，可以把它安放到主屏幕。这样以后再打开，就会更像一枚安静独立的主屏应用。",
  prompt:
    "现在可以直接把它安装到手机主屏。装好以后，从主屏幕打开时会更像一枚独立的主屏应用。",
  fallback:
    "如果你的浏览器支持安装网页应用，可以把它添加到主屏幕，之后就能像主屏应用一样打开。",
};

const deferredState = {
  installPrompt: null,
};

function isNativeShell() {
  return (
    window.location.protocol === "asakusa:" ||
    /AsakusaOmikujiApp/i.test(window.navigator.userAgent)
  );
}

function postNativeMessage(name, payload) {
  const handler = window.webkit?.messageHandlers?.[name];
  if (!handler) {
    return false;
  }

  try {
    handler.postMessage(payload);
    return true;
  } catch (error) {
    console.error(`native bridge failed for ${name}`, error);
    return false;
  }
}

const initialState = {
  fortunes: [],
  currentPayload: null,
  previousFortune: null,
  hasRedrawn: false,
  loading: false,
  ritualCount: 0,
};

const state = { ...initialState };

const elements = {
  startRitual: document.querySelector("#start-ritual"),
  scrollOverview: document.querySelector("#scroll-overview"),
  installApp: document.querySelector("#install-app"),
  installHint: document.querySelector("#install-hint"),
  resetSession: document.querySelector("#reset-session"),
  ritualPanel: document.querySelector("#ritual-panel"),
  ritualTitle: document.querySelector("#ritual-title"),
  ritualStatus: document.querySelector("#ritual-status"),
  ritualMachine: document.querySelector("#ritual-machine"),
  drawButton: document.querySelector("#draw-button"),
  resultCard: document.querySelector("#result-card"),
  resultTopline: document.querySelector("#result-topline"),
  resultReveal: document.querySelector("#result-reveal"),
  fortuneChip: document.querySelector("#fortune-chip"),
  fortunePoem: document.querySelector("#fortune-poem"),
  fortuneSummary: document.querySelector("#fortune-summary"),
  fortuneExplain: document.querySelector("#fortune-explain"),
  fortuneGuidance: document.querySelector("#fortune-guidance"),
  redrawNote: document.querySelector("#redraw-note"),
  redrawInvitation: document.querySelector("#redraw-invitation"),
  redrawRitual: document.querySelector("#redraw-ritual"),
  redrawShift: document.querySelector("#redraw-shift"),
  fateShiftNote: document.querySelector("#fate-shift-note"),
  fateShiftBefore: document.querySelector("#fate-shift-before"),
  fateShiftAfter: document.querySelector("#fate-shift-after"),
  stopNote: document.querySelector("#stop-note"),
  resultClosing: document.querySelector("#result-closing"),
  resultActions: document.querySelector("#result-actions"),
  redrawDialog: document.querySelector("#redraw-dialog"),
  confirmRedraw: document.querySelector("#confirm-redraw"),
  installDialog: document.querySelector("#install-dialog"),
  installDialogCopy: document.querySelector("#install-dialog-copy"),
  installDialogSteps: document.querySelector("#install-dialog-steps"),
  closeInstallDialog: document.querySelector("#close-install-dialog"),
  actionButtonTemplate: document.querySelector("#action-button-template"),
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function resolveBucket(fortuneName) {
  return FORTUNE_BUCKETS[fortuneName] ?? "middle";
}

function pickTemplate(options, ...keys) {
  const marker = keys.join("");
  const index =
    [...marker].reduce((sum, char) => sum + char.charCodeAt(0), 0) %
    options.length;
  return options[index];
}

function fillTemplate(template, values) {
  return template.replaceAll(/\{(\w+)\}/g, (_, key) => values[key] ?? "");
}

function chooseFortune({ excludeSignNo = null } = {}) {
  const pool = state.fortunes.filter(
    (fortune) => excludeSignNo === null || fortune["签号"] !== excludeSignNo,
  );
  const index = Math.floor(Math.random() * pool.length);
  return pool[index];
}

function parseGuidance(text) {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      if (line.includes("：")) {
        const [label, ...rest] = line.split("：");
        return { label, value: rest.join("：") };
      }
      return { label: "补充", value: line };
    });
}

function buildPayload(record, previousRecord = null) {
  const bucket = resolveBucket(record["吉凶"]);
  const payload = {
    mode: previousRecord ? "redraw" : "draw",
    fortuneBucket: bucket,
    summary: DRAW_SUMMARIES[bucket],
    guidance: parseGuidance(record["解曰"]),
    fortune: { ...record },
  };

  if (!previousRecord) {
    const fortuneName = record["吉凶"];
    const isWeak = REDRAW_ELIGIBLE.has(fortuneName);
    payload.redraw = isWeak
      ? {
          offered: true,
          invitation:
            REDRAW_INVITATIONS[fortuneName] ?? REDRAW_INVITATIONS.default,
          ritual: REDRAW_RITUAL_TEXT,
          fateShiftHint:
            "重请之后，变的不是已经发生的过去，而是你从此刻起所携带的心气与行路之势。",
        }
      : { offered: false };
    payload.ceremony = {
      opening: pickTemplate(
        OPENING_TEMPLATES,
        "draw",
        record["签号"],
        record["吉凶"],
      ),
      reveal: fillTemplate(
        pickTemplate(
          REVEAL_TEMPLATES,
          "draw-reveal",
          record["签号"],
          record["吉凶"],
        ),
        {
          signNo: record["签号"],
          fortuneName: record["吉凶"],
        },
      ),
      closing: pickTemplate(
        DRAW_CLOSING_TEMPLATES,
        "draw-closing",
        record["签号"],
        record["吉凶"],
      ),
    };
    return payload;
  }

  payload.previousFortune = { ...previousRecord };
  payload.fateShift = {
    destroyedSignMeaning: `前一签第${previousRecord["签号"]}签所示的滞气与提醒，至此留在旧纸上，不再贴身同行。`,
    newPathMeaning: REDRAW_SHIFT_TEXTS[bucket],
  };
  payload.ceremony = {
    opening: pickTemplate(
      REDRAW_OPENING_TEMPLATES,
      "redraw-opening",
      previousRecord["签号"],
      record["签号"],
    ),
    reveal: fillTemplate(
      pickTemplate(
        REDRAW_REVEAL_TEMPLATES,
        "redraw-reveal",
        previousRecord["签号"],
        record["签号"],
        record["吉凶"],
      ),
      {
        signNo: record["签号"],
        fortuneName: record["吉凶"],
      },
    ),
    closing: pickTemplate(
      REDRAW_CLOSING_TEMPLATES,
      "redraw-closing",
      previousRecord["签号"],
      record["签号"],
      record["吉凶"],
    ),
  };
  return payload;
}

async function loadFortunes() {
  const responses = await Promise.all(
    DATA_PATHS.map(async (path) => {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`无法读取签文分片：${path}`);
      }
      return response.json();
    }),
  );
  state.fortunes = responses.flat();
}

function setStatus(text) {
  elements.ritualStatus.textContent = text;
}

function isStandaloneMode() {
  return (
    window.matchMedia("(display-mode: standalone)").matches ||
    window.navigator.standalone === true
  );
}

function isIosSafari() {
  const userAgent = window.navigator.userAgent;
  const isAppleDevice = /iphone|ipad|ipod/i.test(userAgent);
  const isSafari = /safari/i.test(userAgent) && !/crios|fxios|edgios/i.test(userAgent);
  return isAppleDevice && isSafari;
}

function renderInstallSteps(steps) {
  elements.installDialogSteps.replaceChildren();
  steps.forEach((step) => {
    const li = document.createElement("li");
    li.textContent = step;
    elements.installDialogSteps.appendChild(li);
  });
}

function openInstallDialog() {
  if (deferredState.installPrompt) {
    return;
  }

  if (isIosSafari() && !isStandaloneMode()) {
    elements.installDialogCopy.textContent = INSTALL_COPY.ios;
    renderInstallSteps([
      "点开浏览器底部或顶部的“分享”按钮。",
      "在菜单里找到“添加到主屏幕”。",
      "确认名称后点“添加”，以后就能像主屏应用一样打开。",
    ]);
  } else {
    elements.installDialogCopy.textContent = INSTALL_COPY.fallback;
    renderInstallSteps([
      "如果浏览器地址栏或菜单里出现“安装应用”或“添加到主屏幕”，直接点它。",
      "若暂时没有看到安装入口，可以先把这个页面收藏，之后再从支持安装的浏览器打开。",
    ]);
  }

  elements.installDialog.showModal();
}

function updateInstallUI() {
  if (isNativeShell()) {
    elements.installApp.hidden = true;
    elements.installHint.hidden = true;
    return;
  }

  const standalone = isStandaloneMode();

  if (standalone) {
    elements.installApp.hidden = true;
    elements.installHint.hidden = false;
    elements.installHint.textContent = "当前已在主屏模式中打开，可以像主屏应用一样使用。";
    return;
  }

  if (deferredState.installPrompt) {
    elements.installApp.hidden = false;
    elements.installApp.textContent = "安装到手机";
    elements.installHint.hidden = false;
    elements.installHint.textContent = "可以添加到手机主屏，以更贴近主屏应用的方式打开。";
    return;
  }

  if (isIosSafari()) {
    elements.installApp.hidden = false;
    elements.installApp.textContent = "添加到主屏幕";
    elements.installHint.hidden = false;
    elements.installHint.textContent = "在 Safari 中可通过分享菜单添加到主屏幕。";
    return;
  }

  elements.installApp.hidden = false;
  elements.installApp.textContent = "如何安装";
  elements.installHint.hidden = false;
  elements.installHint.textContent = "在支持安装网页应用的浏览器里，可以把它作为主屏应用添加到手机。";
}

async function handleInstallAction() {
  if (deferredState.installPrompt) {
    deferredState.installPrompt.prompt();
    const { outcome } = await deferredState.installPrompt.userChoice;
    deferredState.installPrompt = null;
    updateInstallUI();
    if (outcome === "accepted") {
      setStatus("这枚签已可安放到手机主屏。下次再见，会更像一枚静静候着你的主屏应用。");
    }
    return;
  }

  openInstallDialog();
}

function triggerHaptic(type) {
  postNativeMessage("haptics", { type });
}

async function registerServiceWorker() {
  if (
    isNativeShell() ||
    !("serviceWorker" in window.navigator) ||
    !/^https?:$/.test(window.location.protocol)
  ) {
    return;
  }

  try {
    await window.navigator.serviceWorker.register("../sw.js", {
      scope: "../",
    });
  } catch (error) {
    console.error("service worker registration failed", error);
  }
}

function syncControls() {
  const hasSession = Boolean(state.currentPayload);
  elements.drawButton.textContent = state.loading
    ? "启签中..."
    : hasSession
      ? "另起新签"
      : "现在启签";
  elements.resetSession.hidden = !hasSession;
}

function setLoading(loading) {
  state.loading = loading;
  elements.startRitual.disabled = loading;
  elements.drawButton.disabled = loading;
  elements.resetSession.disabled = loading;
  elements.confirmRedraw.disabled = loading;
  syncControls();
}

function buildAction(label, kind, onClick) {
  const button = elements.actionButtonTemplate.content.firstElementChild.cloneNode(
    true,
  );
  button.type = "button";
  button.textContent = label;
  button.classList.add(kind);
  button.addEventListener("click", onClick);
  return button;
}

function clearResultActions() {
  elements.resultActions.replaceChildren();
}

function renderGuidance(guidance) {
  elements.fortuneGuidance.replaceChildren();
  guidance.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.label}：${item.value}`;
    elements.fortuneGuidance.appendChild(li);
  });
}

function renderResult(payload) {
  state.currentPayload = payload;
  elements.resultCard.classList.remove("hidden");
  elements.resultCard.classList.remove("is-visible");
  elements.ritualTitle.textContent =
    payload.mode === "redraw" ? "纳签重请" : "签已揭晓";
  elements.resultTopline.textContent = payload.ceremony.opening;
  elements.resultReveal.textContent = payload.ceremony.reveal;
  elements.fortuneChip.textContent = `第${payload.fortune["签号"]}签 · ${payload.fortune["吉凶"]}`;
  elements.fortuneChip.dataset.bucket = payload.fortuneBucket;
  elements.fortunePoem.textContent = payload.fortune["诗曰"];
  elements.fortuneSummary.textContent = payload.summary;
  elements.fortuneExplain.textContent = payload.fortune["四句解说"];
  renderGuidance(payload.guidance);
  syncControls();

  elements.redrawNote.classList.add("hidden");
  elements.fateShiftNote.classList.add("hidden");
  elements.stopNote.classList.add("hidden");

  if (payload.mode === "draw" && payload.redraw.offered && !state.hasRedrawn) {
    elements.redrawNote.classList.remove("hidden");
    elements.redrawInvitation.textContent = payload.redraw.invitation;
    elements.redrawRitual.textContent = payload.redraw.ritual;
    elements.redrawShift.textContent = payload.redraw.fateShiftHint;
  }

  if (payload.mode === "redraw") {
    elements.fateShiftNote.classList.remove("hidden");
    elements.fateShiftBefore.textContent =
      payload.fateShift.destroyedSignMeaning;
    elements.fateShiftAfter.textContent = payload.fateShift.newPathMeaning;
    if (payload.fortuneBucket === "lower") {
      elements.stopNote.classList.remove("hidden");
    }
  }

  if (payload.fortuneBucket === "upper") {
    triggerHaptic("success");
  } else if (payload.fortuneBucket === "middle") {
    triggerHaptic("selection");
  } else {
    triggerHaptic("warning");
  }

  elements.resultClosing.textContent = payload.ceremony.closing;
  clearResultActions();

  if (payload.mode === "draw") {
    if (payload.redraw.offered) {
      elements.resultActions.appendChild(
        buildAction("纳签重请", "button-primary", () => {
          elements.redrawDialog.showModal();
        }),
      );
    } else {
      elements.resultActions.appendChild(
        buildAction("另起新签", "button-primary", () => {
          void performDraw("draw");
        }),
      );
    }
    elements.resultActions.appendChild(
      buildAction("收起签纸", "button-secondary", () => {
        resetSession({
          status:
            "签纸已轻轻收起。若还想再请一回新的愿，可按下“另起新签”。",
        });
      }),
    );
  }

  if (payload.mode === "redraw") {
    if (payload.fortuneBucket === "lower") {
      elements.resultActions.appendChild(
        buildAction("今日收束", "button-primary", () => {
          resetSession({
            status: "今日的签意已经说尽。把步子放稳，改日再来。",
          });
        }),
      );
      elements.resultActions.appendChild(
        buildAction("收起签纸", "button-secondary", () => {
          resetSession({
            status: "签纸已收。今日宜止，改日再来，也是一种分寸。",
          });
        }),
      );
    } else {
      elements.resultActions.appendChild(
        buildAction("另起新签", "button-primary", () => {
          void performDraw("draw");
        }),
      );
      elements.resultActions.appendChild(
        buildAction("收起签纸", "button-secondary", () => {
          resetSession({
            status:
              "新签已明，签纸也已收起。若还想再请一回新的愿，可按下“另起新签”。",
          });
        }),
      );
    }
  }

  requestAnimationFrame(() => {
    elements.resultCard.classList.add("is-visible");
  });
}

async function ritualSequence(lines) {
  for (const line of lines) {
    setStatus(line);
    await sleep(720);
  }
}

function clearSessionState() {
  state.currentPayload = null;
  state.previousFortune = null;
  state.hasRedrawn = false;
  state.loading = false;
  elements.ritualTitle.textContent = "请一签";
  elements.resultCard.classList.add("hidden");
  elements.resultCard.classList.remove("is-visible");
  clearResultActions();
  syncControls();
}

function resetSession({ status = DEFAULT_STATUS, scroll = true } = {}) {
  clearSessionState();
  if (elements.redrawDialog.open) {
    elements.redrawDialog.close();
  }
  setStatus(status);
  if (scroll) {
    elements.ritualPanel.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

async function performDraw(mode = "draw") {
  if (state.loading) {
    return;
  }

  if (mode === "redraw" && !state.previousFortune) {
    return;
  }

  if (mode === "draw" && state.currentPayload) {
    clearSessionState();
  }

  state.ritualCount += 1;
  setLoading(true);
  elements.resultCard.classList.add("hidden");
  elements.ritualMachine.classList.add("is-drawing");
  triggerHaptic(mode === "redraw" ? "impactMedium" : "impactLight");

  if (mode === "draw") {
    await ritualSequence([
      "把心慢慢收拢，不必急着问它会落向哪里。",
      "签筒已静，木签轻响，檐下只剩一线缓慢的呼吸。",
      "这一纸吉凶，就要从静里开口。",
    ]);
    const record = chooseFortune();
    state.previousFortune = record;
    renderResult(buildPayload(record));
  } else {
    await ritualSequence([
      "旧签纳去，旧气止于纸上，不再贴身同行。",
      "香意未散，再启一回，只看此后该如何行路。",
      "新签将落，余下的，让它自己说话。",
    ]);
    const record = chooseFortune({
      excludeSignNo: state.previousFortune["签号"],
    });
    state.hasRedrawn = true;
    renderResult(buildPayload(record, state.previousFortune));
  }

  elements.ritualMachine.classList.remove("is-drawing");
  setLoading(false);
  elements.resultCard.scrollIntoView({ behavior: "smooth", block: "start" });
}

function bindEvents() {
  window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    deferredState.installPrompt = event;
    updateInstallUI();
  });

  window.addEventListener("appinstalled", () => {
    deferredState.installPrompt = null;
    updateInstallUI();
    setStatus("浅草·启签已安放到主屏。往后再开时，会像一枚独立的主屏应用静静候在那里。");
  });

  elements.scrollOverview.addEventListener("click", () => {
    document.querySelector("#overview").scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  });

  elements.startRitual.addEventListener("click", () => {
    elements.ritualPanel.scrollIntoView({ behavior: "smooth", block: "start" });
    setStatus(
      state.currentPayload
        ? "你已回到签前。若想重新启一支新签，可按下“另起新签”。"
        : "你已来到签前。若心绪已定，按下“现在启签”，让木签先开口。",
    );
    setTimeout(() => {
      elements.drawButton.focus({ preventScroll: true });
    }, 260);
  });

  elements.installApp.addEventListener("click", () => {
    void handleInstallAction();
  });

  elements.drawButton.addEventListener("click", () => performDraw("draw"));
  elements.resetSession.addEventListener("click", () => {
    resetSession({
      status: "签纸已收起。若还想再请一回新的愿，可按下“现在启签”。",
    });
  });
  elements.confirmRedraw.addEventListener("click", async (event) => {
    event.preventDefault();
    elements.redrawDialog.close();
    await performDraw("redraw");
  });

  elements.closeInstallDialog.addEventListener("click", () => {
    elements.installDialog.close();
  });
}

async function bootstrap() {
  try {
    await loadFortunes();
    await registerServiceWorker();
    bindEvents();
    syncControls();
    updateInstallUI();
    setStatus(DEFAULT_STATUS);
  } catch (error) {
    console.error(error);
    setStatus("签文没有顺利载入。请确认你正在通过本地服务器打开这个页面。");
    elements.drawButton.disabled = true;
    elements.startRitual.disabled = true;
  }
}

bootstrap();
