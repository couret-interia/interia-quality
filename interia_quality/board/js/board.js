// Helper : Need in add on load json's (here loadJSON & some html in local script)
const BASE_URL = base_path();

// Init with `page_name.html…` (to prepare to inject cosmos_map.json message helper)
document.querySelector('h1').insertAdjacentHTML('beforeend', '<i id="repo">' + basename('' + window.location.href) + '…</i>');
// Add link style (default)
addCssLinkInHead(base_href + 'themes/board.css', '', false, function() {
  // Show body (remove plank loader)
  document.body.removeAttribute('style');
});
// Load Favicon href link to svg
document.getElementById('favicon').href = 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><circle cx=%2250%22 cy=%2250%22 r=%2246%22 fill=%22%230d47a1%22/><text x=%2250%25%22 y=%2258%25%22 text-anchor=%22middle%22 font-size=%2254%22 fill=%22white%22 font-family=%22sans-serif%22>λ</text></svg>';
// Load title repo (if cosmos_map)
window.addEventListener('load', boardtitle);
async function boardtitle() {
  // Load cosmos_map.json attempt (to get repo title & replace it in `<i id="repo">`)
  let data;
  try {
    data = await loadJSON("cosmos_map.json");
  } catch {
    document.getElementById("repo").textContent = "No `cosmos_map.json` in this repo.";
    return;
  }
  const root = basename(data.root),
    p = basename(location.pathname);
    t = document.querySelector('title');
  document.querySelector('#repo').textContent = '' + root;
  t.textContent = root + ' · ' + t.textContent + ' · ' + p;
}

// Helpers
// Inject link in head Dom helper (todo: add `, opts`?)
function addCssLinkInHead(href, pos, id, cb){
  const p = (' beforebegin afterbegin beforeend afterend'.search(pos) > 0) ? pos : 'beforeend',
  z = document.createElement('link');
  z.href = href;
  z.rel = 'stylesheet';
  if (id) z.id = id;
  if (typeof cb == 'function') z.onload = function(e) {cb();e.target.removeAttribute('onload');}
  document.querySelector('head').insertAdjacentElement(p, z);
}

/*
// window.document.addEventListener Wrapper Function (uncomment me for debug)
const globalAddListener = window.document.addEventListener; // Save the original method
window.document.addEventListener = function(type, listener, options) {
  console.trace(`Adding event listener for: ${type}`);
  globalAddListener.call(this, type, listener, options);
};
*/

async function loadJSON(url) {
  const res = await fetch(BASE_URL + url, {cache: "no-store"});
  if (!res.ok) throw new Error("Cannot load " + BASE_URL + url);
  return await res.json();
}

// Inject Js in Dom helper (todo: add `, opts`?)
function addJsInDom(src, pos, defer, head, type, cb){
  const p = (!!pos && ' beforebegin afterbegin beforeend afterend'.search(pos) > 0) ? pos : 'beforeend',
  w = document.querySelector(head ? 'head' : 'body'),
  z = document.createElement('script');
  z.src = src;
  if (defer) z.defer = defer;
  if (type)  z.type = type;
  if (typeof cb == 'function') z.onload = function(e) {cb();e.target.removeAttribute('onload');}
  w.insertAdjacentElement(p, z);
}

// Helpers (for url, path, file, page comparison, title...)
function basename(path) {
  return path.split('/').reverse()[0];
}
function dirname(filePath) {
  return filePath.substring(0, filePath.lastIndexOf('/'));
}
function base_path() {
  return basename(dirname('' + location.pathname)) == 'board' ? '../../' : ( basename(location.pathname) == 'index.html' ? '../../../../' : ''); // Relative, to get *.json (on root repo)
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function scrollToMe(id) {
  const c = document.querySelector('#' + id);
    yPosition = c.getBoundingClientRect().top + window.scrollY;
  window.scrollTo({
    top: yPosition,
    behavior: 'smooth' // Smooth scrolling
  });
}

function str2onlyChars(s) {
  return s.replace(/[\W]/gi, '');
}
const nodigit = 'a b c d e f g h i j'.split(' ');
function str2className(s) {
  if (nodigit[parseInt(s[0])]) { // number2letter
    s = nodigit[parseInt(s[0])] + s.substring(1); // never begin with number
  }
  return str2onlyChars(s).replace(/^[\d]+/, '_').toLowerCase(); // + fallback
}

/* --- Automatic main() function & init some tools --- */

// Add init tools js + style (option by meta.id == init)
const metaInit = document.getElementById('init');
if (metaInit) {
  const inits    = metaInit.getAttribute('content'); // tools.module
  const iia_init = inits ? inits.split('.')[0] : iia_page.replace(/\.html$/, ''); // name
  const typeJs   = inits ? inits.split('.')[1] : false; // module
  addJsInDom(base_href + 'js/' + iia_init + '.js', '', true, true, typeJs);
  addCssLinkInHead(base_href + 'themes/' + iia_init + '.css');
  console.log('💠 Init tools by meta in ' + iia_page); // metaInit
}

// Automatic launch + tool (if init exist)
const bootstrap = function (evt) {
  if (evt.target.readyState === "complete") {
    console.log('🌱 --- DOM readyState: ' + evt.target.readyState);
    if (typeof main === "function") {
      console.log('🌟 Automatic launch main ' + typeof main);
      window.mainloader = main(); // Automatic init (Load data + DOM)
      if (typeof init === "function") {
        console.log('🌟 Automatic launch init ' + typeof init);
        window.mainloader.finally(init); // Add tools if exist
      }
    }
  }
};
window.document.addEventListener("readystatechange", bootstrap);

// Launch CLI commands on board pages (Only served by interia-quality portal)
async function runCli(btn, com) {
  if (! confirm('Launch `interia-quality ' + com + '`?')) {
    return false;
  }
  const u = `${location.pathname}?run=${com}`;
  let btnstr = com,
    str = '💻 Runs in CLI: ' + com,
    time = 5000;
  btn.classList.toggle('run');
  try {
    const res = await fetch(u, {cache: "no-store"});
    const run = await res.text();
    console.log(str + '\n' + run + '\n👉 Note: Reload page to see Changes.');
    str += '<br>' + run.split('\n').join('<br>');
    str += '<br><br><i>See in your terminal or console (F12)</i> 👀';
  } catch (e) {
    console.trace('runCli Error:', e);
  }
  btn.classList.toggle('run');
  showNotification(btn, btnstr, str, time)
}

window.webcli = false;
async function onCli() {
  const reswebcli = await fetch('/webcli.html', {cache: "no-store"});
  if(reswebcli.ok && reswebcli.status == 200) {
    console.log('🟢 Run Commands in all web page is ON');
    window.webcli = true;
    const _CLI_COMMANDS = [
      'check',
      'refactor-plan',
      'refactor-apply',
      'ai-request',
      'ai-prompt',
      'ai-summary',
      'ai-apply',
      'cosmos-map',
      'cosmos-timelapse',
      'latex-galaxy',
      'latex-explorer',
      'bib-galaxy'
    ];
    let cli_links = '';
    _CLI_COMMANDS.forEach(s => {
      cli_links += `<button onclick="runCli(this, '${s}');" class="btn-tiny btn-cli" title="Click to Run ${s} like in CLI">${s}</button>`;
    })
    document.body.insertAdjacentHTML('afterbegin', `<details class="top-bar cli-commands">
  <summary title="Toggle One Click Commands Launcher">🖰</summary>
  <div class="card">${cli_links}</div>
</details>`);
  }
}
onCli();


/* --- notification (copy by default) --- */

// Add HTML in DOM
document.body.insertAdjacentHTML('beforeend', '<div id="notification" class="notification"></div>');

IDTONOTIF = false; // id timeout
function showNotification(btn, btnstr, str, time) {
    clearTimeout(IDTONOTIF);
    const notification = document.getElementById('notification');
    if (! btn.getAttribute('data-txt')) btn.setAttribute('data-txt', btn.textContent);
    const t = time || 2000;
    btn.textContent = btnstr || '✅ Copied!'
    notification.innerHTML = str || '✅ Copied code!';
    notification.style.display = 'block';
    IDTONOTIF = setTimeout(() => {
        notification.style.display = 'none';
    }, t);
    setTimeout(() => {
        btn.textContent = btn.getAttribute('data-txt');
    }, t);
}

/* --- Check Storage Helper --- */
const _LS = typeof localStorage !== 'undefined';

/* --- Toggle Commands link (portal only) --- */
const TOP_BAR_BOARD = `
  ·&nbsp;<a id="board-commands" class="active" href="javascript:void(0);" title="Toggle Commands">Hide&nbsp;⌨</a>&nbsp;·
`;

// Top bar shared menu links
const TOP_BAR_MENU = `
  <a href="interia_portal.html" title="📡 InterIA Portal">📡</a>
  <a href="quality_report.html" title="🧪 Quality Report">🧪</a>
  <a href="ai_preview.html" title="🤖 Refactor Assist (AI Bridge)">🤖</a>
  <a href="galaxy_latex_explorer.html" title="🔭 LaTeX Galaxy Explorer">🔭</a>
  <a href="doctor_latex_galaxy.html" title="🌌 LaTeX Galaxy">🌌</a>
  <a href="bib_galaxy.html" title="💫 BibTeX Galaxy">💫</a>
  <a href="cosmos_explorer.html" title="🌐 Cosmos Map">🌐</a>
  <a href="cosmos_timeline.html" title="⏳ Cosmos Timeline">⏳</a>
  <a href="multiverse_3d.html" title="🌠 Multiverse 3D">🌠</a>
  <a href="docs/quality/index.html" title="❓ Quality Docs &amp; Help">❓</a>
`;

// Top bar right shared light / dark switches
const LIGHT_SWITCH = `
<div class="light-switch top-bar top-bar-right" title="💡 Dark/Light">
  <input id="rls" name="color-scheme" type="radio" value="light dark" checked><label for="rls" title="System">🌓</label>
  <input id="rll" name="color-scheme" type="radio" value="light"><label for="rll" title="Light">🌞</label>
  <input id="rld" name="color-scheme" type="radio" value="dark"><label for="rld" title="Dark">🌙</label>
</div>
`;// top bars + injection
var top_bar = '<div class="top-bar">' + TOP_BAR_MENU + (basename('' + window.location.href) != 'interia_portal.html' ? '' : TOP_BAR_BOARD) + '</div>' + LIGHT_SWITCH;
document.querySelector('body').insertAdjacentHTML('beforeend', top_bar);

// Load color-scheme from localStorage
function loadColorSheme() {
  if (_LS) {
    try {
      const radios = document.querySelectorAll('input[name="color-scheme"]');

      // Vérifie la mémoire locale lors du chargement
      const storedValue = localStorage.getItem('selectedColorScheme');

      if (storedValue && storedValue !== 'light dark') {
        document.querySelector(`input[name="color-scheme"][value="${storedValue}"]`).checked = true;
      }

      // Ajoute un écouteur d'événements pour chaque radio
      radios.forEach((radio) => {
        radio.addEventListener('change', function () {
          if (this.value !== 'light dark') {
            localStorage.setItem('selectedColorScheme', this.value);
          } else {
            localStorage.removeItem('selectedColorScheme');
          }
        });
      });
    } catch (e) {
        console.log('localStorage is deactivated/not supported/not working as expected.', e);
    }
  }
}
loadColorSheme();

// Bascule des commande + localStorage (interia_portal)
const board_commands = document.querySelector('#board-commands');
const cs = document.querySelectorAll('.card .small');
// Bascule l'affichage des commandes (CLI make)
function toggle_commands() {
  // Ajoute/supprime .hide pour chaque .card .small
  cs.forEach((cs) => {
    cs.classList.toggle('hide');
  });
  board_commands.classList.toggle('active');
  let m = board_commands.classList.contains('active');
  board_commands.textContent = (m ? 'Hide' : 'Show') + ' ⌨';// Fix &nbsp; https://stackoverflow.com/a/74377675
}
// On recharge & vérifie si les commandes doivent-être affiché ou non
if(board_commands && cs.length > 0) {
  // board_commands.classList.toggle('muted');
  if (_LS) {
    try {
      // Vérifie la mémoire locale lors du chargement & au besoin, cache les commandes
      if (localStorage.getItem('board_commands') && board_commands.classList.contains('active')) {
        toggle_commands();
      }
    } catch (e) {
        console.log('localStorage is deactivated/not supported/not working as expected.', e);
    }
  }
  // board_commands.onclick = 'toggle_commands();';
  board_commands.addEventListener('click', function () {
    toggle_commands();
    if (_LS) {
      if (this.classList.contains('active')) {
        localStorage.removeItem('board_commands');
      } else {
        localStorage.setItem('board_commands', 'hide');
      }
    }
  });
}


/* --- Adjust some top-bar menu href & add active class --- */

// All top bar links (only left normaly)
const top_bar_menu_links = document.querySelectorAll('.top-bar a');
if(top_bar_menu_links) {
  // Some tweaks (menu)
  top_bar_menu_links.forEach((link) => {
    // page_file_name.html (not path)
    let page_html = '' + basename(link.href);

    // Only docs/quality have index.html
    let index_doc = !1;
    if(window.iia_page == 'index.html' && page_html == 'index.html'){
      index_doc = !0;
    }

    // IDEA: .prepend(window.base_href); // BUT // link.href.prepend is not a function & maybe bad idea (begin with http...)
    // IDEA: If no json file (and if hide) show commands (maybe other, local served repo, _LS (memory) or json cleaned or ...
    // Shift some href to ../../ if in doc page
    if(window.base_href && link.href.search('script:') < 0) {
      // Change for relative (good) path in link.href
      link.href = (index_doc ? '' : window.base_href) + page_html;
    }

    // Add active class on same url (basic)
    if(page_html == iia_page){
      console.log('🌟 --- page active: ' + page_html);
      link.classList.add('active');
      // break; // Illegal break statement (in forEach)
    }
  });
}
